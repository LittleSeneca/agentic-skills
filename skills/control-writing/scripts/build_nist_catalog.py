#!/usr/bin/env python3
"""Build the LLM-friendly NIST SP 800-53 reference from the official OSCAL source.

This is the "keep it current" mechanism for the control-writing skill. It pulls
the authoritative machine-readable catalog that NIST publishes (the OSCAL
content release on GitHub) and transforms ~1,200 controls into three compact
reference files the skill reads:

  references/nist-800-53.json             core catalog (statement, discussion,
                                          params, baselines, relationships)
  references/nist-800-53-assessment.json  assessment objectives, split out so
                                          the core stays lean
  references/nist-800-53-index.md         family + baseline index, human/LLM
                                          scannable

Source of truth: https://github.com/usnistgov/oscal-content
We deliberately do NOT vendor that repo as a git submodule. It is large and
carries many frameworks; a submodule would pull hundreds of MB and still need
this transform. Pinning the raw catalog URL by ref gives a reproducible,
network-free, committed artifact and a one-command refresh.

Usage:
    python3 scripts/build_nist_catalog.py            # use pinned REF
    python3 scripts/build_nist_catalog.py --ref main # track latest

When NIST ships a new revision, bump REF (to a release tag like "v1.5.0" or to
"main"), rerun, and commit the regenerated reference files.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

# Pin the OSCAL content release used to generate the committed artifacts.
# Bump this to a newer release tag (or "main") and rerun to refresh.
REF = "v1.5.0"

BASE = "https://raw.githubusercontent.com/usnistgov/oscal-content/{ref}/nist.gov/SP800-53/rev5/json"
CATALOG_FILE = "NIST_SP-800-53_rev5_catalog.json"
BASELINE_FILES = {
    "LOW": "NIST_SP-800-53_rev5_LOW-baseline_profile.json",
    "MODERATE": "NIST_SP-800-53_rev5_MODERATE-baseline_profile.json",
    "HIGH": "NIST_SP-800-53_rev5_HIGH-baseline_profile.json",
    "PRIVACY": "NIST_SP-800-53_rev5_PRIVACY-baseline_profile.json",
}

REF_DIR = Path(__file__).resolve().parents[1] / "references"

INSERT_RE = re.compile(r"\{\{\s*insert:\s*param,\s*([^}\s]+)\s*\}\}")


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_param_index(catalog: dict) -> dict:
    """Map every param id -> param object, across all controls and enhancements."""
    index: dict[str, dict] = {}

    def walk(controls: list) -> None:
        for ctrl in controls:
            for prm in ctrl.get("params", []):
                index[prm["id"]] = prm
            if ctrl.get("controls"):
                walk(ctrl["controls"])

    for group in catalog["groups"]:
        walk(group.get("controls", []))
    return index


def render_param(param_id: str, params: dict) -> str:
    """Render an ODP placeholder the way NIST does: [Assignment: ...] / [Selection: ...]."""
    prm = params.get(param_id)
    if not prm:
        return f"[Assignment: {param_id}]"
    if "select" in prm:
        sel = prm["select"]
        choices = "; ".join(sel.get("choice", []))
        how = sel.get("how-many", "one")
        return f"[Selection ({how}): {choices}]"
    label = prm.get("label")
    if label:
        return f"[Assignment: {label}]"
    # Aggregate params point at other ODPs; fall back to their guideline text.
    guidelines = prm.get("guidelines")
    if guidelines:
        return f"[Assignment: {guidelines[0].get('prose', param_id)}]"
    return f"[Assignment: {param_id}]"


def resolve(text: str, params: dict) -> str:
    if not text:
        return text
    return INSERT_RE.sub(lambda m: render_param(m.group(1), params), text)


def part_label(part: dict) -> str:
    for prop in part.get("props", []):
        if prop.get("name") == "label":
            return prop["value"]
    return ""


def render_statement(parts: list, params: dict, depth: int = 0) -> list[str]:
    """Flatten the statement parts into indented, labelled lines."""
    lines: list[str] = []
    for part in parts:
        if part.get("name") not in ("statement", "item"):
            continue
        prose = resolve(part.get("prose", ""), params).strip()
        label = part_label(part)
        indent = "  " * depth
        if prose:
            prefix = f"{label} " if label else ""
            lines.append(f"{indent}{prefix}{prose}")
        if part.get("parts"):
            child_depth = depth if (not prose and not label) else depth + 1
            lines.extend(render_statement(part["parts"], params, child_depth))
    return lines


def get_part(parts: list, name: str) -> dict | None:
    for part in parts:
        if part.get("name") == name:
            return part
    return None


def collect_objectives(part: dict, params: dict, acc: list[str]) -> None:
    """Flatten assessment-objective leaf prose into a list."""
    if part.get("name") == "assessment-objective":
        prose = resolve(part.get("prose", ""), params).strip()
        if prose:
            acc.append(prose)
    for child in part.get("parts", []):
        collect_objectives(child, params, acc)


def control_baselines(control_id: str, membership: dict) -> list[str]:
    return [name for name in ("LOW", "MODERATE", "HIGH", "PRIVACY") if control_id in membership.get(name, set())]


def family_of(control_id: str) -> str:
    return control_id.split("-")[0].upper()


def transform_control(ctrl: dict, family_id: str, family_title: str, params: dict,
                      membership: dict, parent: str | None, core: dict, assessments: dict) -> None:
    cid = ctrl["id"]
    parts = ctrl.get("parts", [])
    statement_part = get_part(parts, "statement")
    guidance_part = get_part(parts, "guidance")

    label = next((p["value"] for p in ctrl.get("props", []) if p["name"] == "label"), cid.upper())

    statement_lines = render_statement([statement_part], params) if statement_part else []
    # render_statement skips the top wrapper if it has no prose/label; handle directly:
    if statement_part:
        statement_lines = render_statement(statement_part.get("parts", []), params)
        if statement_part.get("prose"):
            statement_lines = [resolve(statement_part["prose"], params).strip()] + statement_lines

    related = [l["href"].lstrip("#") for l in ctrl.get("links", []) if l.get("rel") == "related"]
    requires = [l["href"].lstrip("#") for l in ctrl.get("links", []) if l.get("rel") == "required"]

    odps = []
    for prm in ctrl.get("params", []):
        entry = {"id": prm["id"]}
        if "select" in prm:
            entry["select"] = prm["select"].get("choice", [])
            entry["how_many"] = prm["select"].get("how-many", "one")
        if prm.get("label"):
            entry["label"] = prm["label"]
        if prm.get("guidelines"):
            entry["guideline"] = prm["guidelines"][0].get("prose", "")
        odps.append(entry)

    enhancement_ids = [c["id"] for c in ctrl.get("controls", [])]

    record = {
        "id": cid,
        "label": label,
        "title": ctrl.get("title", ""),
        "family": family_id.upper(),
        "family_title": family_title,
        "baselines": control_baselines(cid, membership),
        "statement": "\n".join(statement_lines).strip(),
        "discussion": resolve(guidance_part.get("prose", ""), params).strip() if guidance_part else "",
        "params": odps,
        "related": related,
    }
    if requires:
        record["requires"] = requires
    if parent:
        record["parent"] = parent
        record["is_enhancement"] = True
    if enhancement_ids:
        record["enhancement_ids"] = enhancement_ids
    core[cid] = record

    # Assessment objectives -> separate file.
    obj_part = get_part(parts, "assessment-objective")
    if obj_part:
        acc: list[str] = []
        collect_objectives(obj_part, params, acc)
        if acc:
            assessments[cid] = acc

    for child in ctrl.get("controls", []):
        transform_control(child, family_id, family_title, params, membership, cid, core, assessments)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ref", default=REF, help="git ref/tag of usnistgov/oscal-content (default: pinned %s)" % REF)
    args = ap.parse_args()

    base = BASE.format(ref=args.ref)
    print(f"Fetching catalog from oscal-content@{args.ref} ...", file=sys.stderr)
    catalog_doc = fetch_json(f"{base}/{CATALOG_FILE}")
    catalog = catalog_doc["catalog"]

    membership: dict[str, set] = {}
    for name, fname in BASELINE_FILES.items():
        prof = fetch_json(f"{base}/{fname}")["profile"]
        ids: set[str] = set()
        for imp in prof.get("imports", []):
            for inc in imp.get("include-controls", []):
                ids.update(inc.get("with-ids", []))
        membership[name] = ids
        print(f"  baseline {name}: {len(ids)} controls", file=sys.stderr)

    params = build_param_index(catalog)
    print(f"  indexed {len(params)} parameters", file=sys.stderr)

    core: dict[str, dict] = {}
    assessments: dict[str, list] = {}
    families = []
    for group in catalog["groups"]:
        fid = group["id"]
        ftitle = group["title"]
        base_ids = [c["id"] for c in group.get("controls", [])]
        families.append({"id": fid.upper(), "title": ftitle, "control_ids": base_ids})
        for ctrl in group.get("controls", []):
            transform_control(ctrl, fid, ftitle, params, membership, None, core, assessments)

    meta = catalog["metadata"]
    source = {
        "title": meta.get("title"),
        "catalog_version": meta.get("version"),
        "oscal_version": meta.get("oscal-version"),
        "oscal_content_ref": args.ref,
        "source_url": f"{base}/{CATALOG_FILE}",
        "generated": date.today().isoformat(),
        "generator": "scripts/build_nist_catalog.py",
        "base_controls": sum(1 for c in core.values() if not c.get("is_enhancement")),
        "enhancements": sum(1 for c in core.values() if c.get("is_enhancement")),
        "total_controls": len(core),
    }

    core_out = {"source": source, "families": families, "controls": core}
    (REF_DIR / "nist-800-53.json").write_text(json.dumps(core_out, indent=1, ensure_ascii=False))
    (REF_DIR / "nist-800-53-assessment.json").write_text(
        json.dumps({"source": source, "assessment_objectives": assessments}, indent=1, ensure_ascii=False)
    )

    # Index markdown.
    lines = [
        "# NIST SP 800-53 — Control Index",
        "",
        f"Generated by `scripts/build_nist_catalog.py` from "
        f"[usnistgov/oscal-content@{args.ref}]"
        f"(https://github.com/usnistgov/oscal-content/tree/{args.ref}).",
        "",
        f"- Catalog: {source['title']}",
        f"- Catalog version: **{source['catalog_version']}** (OSCAL {source['oscal_version']})",
        f"- Generated: {source['generated']}",
        f"- {source['base_controls']} base controls, {source['enhancements']} enhancements "
        f"({source['total_controls']} total) across {len(families)} families.",
        "",
        "Full control text lives in `nist-800-53.json` (keyed by lowercase id, e.g. `ac-2`, "
        "`ac-2.1`). Assessment objectives live in `nist-800-53-assessment.json`.",
        "",
        "Baseline legend: **L** = Low, **M** = Moderate, **H** = High, **P** = Privacy.",
        "",
    ]
    for fam in families:
        fam_ctrls = [core[cid] for cid in fam["control_ids"]]
        lines.append(f"## {fam['id']} — {fam['title']}")
        lines.append("")
        lines.append("| Control | Title | Baselines |")
        lines.append("| --- | --- | --- |")
        for c in fam_ctrls:
            badges = "".join(b[0] for b in c["baselines"]) or "—"
            lines.append(f"| {c['label']} | {c['title']} | {badges} |")
        lines.append("")
    (REF_DIR / "nist-800-53-index.md").write_text("\n".join(lines))

    print(
        f"Wrote {len(core)} controls -> references/nist-800-53.json "
        f"({len(assessments)} with assessment objectives).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
