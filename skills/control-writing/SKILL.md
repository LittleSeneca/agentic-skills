---
name: control-writing
description: >
  Design, write, review, or rationalize security and compliance controls so they
  are measurable, actionable, cost-efficient, and aligned with the
  organization's risk appetite. Use this skill whenever the user wants to author
  a new control, turn a policy requirement into the controls that enforce it,
  build or clean up a control register, map controls to a framework (NIST
  800-53, SOC 2, ISO 27001), define how a control is tested and evidenced, or
  review an existing control for quality. It carries the full NIST SP 800-53 Rev
  5 catalog as a machine-readable reference (control statements, discussion,
  organization-defined parameters, baselines, and assessment objectives) and a
  push-back rubric. Critically, this skill does not write good copy for a bad
  control: when a requested control is unmeasurable, unowned, untestable,
  gold-plated, or treats no real risk, it says so and fixes the design before
  polishing the wording. Reach for it even when the user does not say "control"
  by name but is producing a safeguard, a control test, an audit artifact, a
  compliance mapping, or anything that has to prove a policy is actually enforced.
---

# Control Writing

You are helping design and write security and compliance controls. A policy says
*what* the organization requires; a control is the safeguard that *enforces* it
and *proves* it is enforced. The product here is not prose, it is auditability:
a control that cannot be measured, owned, tested, and justified against a real
risk is not a control, no matter how cleanly it reads.

This skill pairs with `policy-writing`. Policies state requirements; controls
implement and verify them. If the user is really asking for a policy (the rule)
rather than a control (the testable safeguard), hand off to the policy-writing
skill. The line matters: "Data must be encrypted at rest" is a policy
statement; "The platform team must confirm quarterly that all RDS instances
report `StorageEncrypted=true`, evidenced by the AWS Config report" is a control.

## The one rule that defines this skill

**Do not write good copy for a bad control.** A clean sentence wrapped around an
untestable, unowned, or unjustified requirement is worse than nothing, because
it passes review and then fails in an audit or an incident. When a requested
control fails the design tests below, name the failure, fix the design, and only
then write it. Be willing to conclude that a control should not exist, should be
merged with another, or that the right answer is to accept the risk rather than
add a safeguard. This push-back is the value of the skill, not an aside.

## What a good control must be

Every control has to pass these. The first four are non-negotiable; the last
three are design judgments you raise with the owner. The full rubric, the
control taxonomy, and the cost/appetite reasoning are in
`references/control-design.md` — read it before designing anything non-trivial.

1. **Risk-anchored** — treats a named risk or threat and enforces a named
   policy. No risk means question whether it should exist.
2. **Specific and actionable** — names actor, action, object, and
   trigger/cadence. A competent operator can run it without guessing.
3. **Measurable and testable** — has defined evidence and a pass/fail criterion
   an assessor can apply. If you cannot describe the evidence and the test, it
   is not a control yet.
4. **Owned** — exactly one accountable role. "IT" or "the team" is not an owner.
5. **Right-sized to appetite and cost** — operating cost is justified by the
   risk reduced; not gold-plating a low risk, not under-protecting a high one.
6. **Operable and sustainable** — runs at a cadence the organization can sustain
   with the tooling and data it has.
7. **Mapped** — links to the framework references it satisfies and the policy it
   enforces, so one control earns credit against many requirements.

## The control grammar

Write every control statement as **actor + action + object + trigger/cadence +
measurable condition**. "The account manager (actor) must disable (action)
terminated-user accounts (object) within 24 hours of the HR termination event
(trigger/cadence), evidenced by the deprovisioning ticket (measurable
condition/evidence)." If a control statement is missing one of these slots, that
is usually the thing to fix.

`references/control-template.md` has the full field set (ID, statement, risk,
policy, function, nature, automation, owner, frequency, evidence, test
procedure, framework mapping), the control-register row format, the full
control-specification format, and worked examples of fixing a bad control and of
recommending no control at all. Copy from it.

## The NIST SP 800-53 reference

This skill carries the complete NIST SP 800-53 Rev 5 catalog as the backbone of
well-designed control objectives. It is generated from the official NIST OSCAL
release and lives in `references/`:

- **`nist-800-53-index.md`** — every family and control with its baseline tier
  (Low / Moderate / High / Privacy). Start here to find a control id.
- **`nist-800-53.json`** — the full catalog, keyed by lowercase id (`ac-2`,
  `ac-2.1`). Each record has the control statement (with parameters resolved to
  `[Assignment: ...]` / `[Selection: ...]`), the discussion, the
  organization-defined parameters, the baselines it belongs to, related
  controls, and enhancement ids. Read a record with a quick lookup, for example:
  `python3 -c "import json;print(json.load(open('references/nist-800-53.json'))['controls']['ac-2']['statement'])"`.
- **`nist-800-53-assessment.json`** — the 800-53A assessment objectives per
  control, already decomposed into testable determination statements. This is
  the ready-made measurability and test-plan checklist; pull from it when
  defining how a control is verified.

How to use it well (full guidance in `references/control-design.md`):

- Treat the NIST **statement as the objective, not the wording.** Translate it
  into the organization's voice, tools, owners, and intervals.
- **Fill the ODPs.** NIST leaves `[Assignment]` / `[Selection]` for the
  organization to set. Filling them with real values is the measurability work.
  An unfilled ODP is an unmeasurable control.
- **Use baselines to right-size** to the system's impact level, so you neither
  gold-plate nor leave gaps.
- **Use assessment objectives as the test plan** and `related` controls to avoid
  designing an orphan.

The catalog is a reference, not an inventory. Never claim a control is
implemented because it appears in the catalog.

### Keeping the catalog current

`scripts/build_nist_catalog.py` regenerates all three reference files from the
official `usnistgov/oscal-content` release, pinned to a ref in the script.
When NIST ships a new revision, bump `REF` in the script, rerun
`python3 scripts/build_nist_catalog.py`, and commit the regenerated files. A git
submodule was deliberately not used: the OSCAL repo is large and multi-framework,
so a pinned fetch-and-transform gives a smaller, reproducible, network-free
artifact.

## How it should read: the writing style

Controls read in the same plain professional register as policies and sit in the
same binder, so they follow the same hard rules. If the `policy-writing` skill is
present in the program, its `house-style.md` governs; the rules are repeated here
so this skill stands alone.

**Hard rules (never break):**

1. **No em dashes (`—`) and no en dashes (`–`) as punctuation.** Use a period
   and a new sentence, a comma, parentheses, or a colon. A plain hyphen in a
   range ("24-hour", "1.0-1.1") is fine.
2. **No AI slop vocabulary.** Avoid delve, robust, seamless, leverage (verb),
   elevate, foster, myriad, crucial, vital, pivotal, "ever-evolving", "in
   today's X world", "it is worth noting". Use plain words.
3. **No personal-voice tics.** No definition by negation, no rhetorical
   questions, no one-line drama fragments, no metaphor. State the requirement
   plainly.

**How a control should sound:**

- **Normative and direct.** "must" for hard requirements, "should" for
  recommended, "may" for permitted. Most control lines use "must".
- **Specific and verifiable.** Name the real interval, the real artifact, the
  real owner, the real threshold. "Reviewed at least quarterly" beats "reviewed
  regularly". If you lack a real value, flag the gap rather than inventing a
  number, because an invented number becomes a control nobody meets.
- **Third person, organizational voice.** "The Security Officer must...", not
  "we" or "you".

## Workflow

1. **Confirm it is a control, not a policy.** If the user is stating a rule
   rather than a testable safeguard, route to `policy-writing` or decompose the
   rule into the controls that enforce it.
2. **Find the risk and the policy.** Name the risk the control treats and the
   policy it enforces. If there is no risk, raise that before writing anything.
3. **Look up the NIST objective.** Find the relevant control in
   `nist-800-53-index.md`, read its record in `nist-800-53.json`, and pull its
   assessment objectives. Use it as the backbone.
4. **Run the design tests.** Apply the seven tests and the push-back catalog in
   `references/control-design.md`. If the requested control fails, fix the
   design or recommend dropping, merging, or accepting before writing.
5. **Right-size it.** Match the rigor to the impact level and the cost to the
   risk. Note the baseline tier you are designing to.
6. **Write it from the template.** Fill the field set in
   `references/control-template.md`, resolving every ODP to a real value or a
   flagged gap. Write the statement in the control grammar.
7. **Define the test and evidence.** State the artifact that proves it operated
   and how an assessor verifies it, drawing on the NIST assessment objectives.
8. **Map it.** Link the framework references it satisfies and the policy it
   enforces.
9. **Run the self-check below** before handing it back.

## Self-check before returning

- Could an assessor test compliance against this control as written? If any line
  cannot be tested, tighten it or flag the gap.
- Does it name a single accountable owner, a real cadence, a measurable
  criterion, and a concrete piece of evidence?
- Is it anchored to a named risk and a named policy? If not, should it exist?
- Is the rigor matched to the impact level, and the cost to the risk? Flag
  gold-plating and duplication.
- Are all NIST ODPs filled with real values or explicitly flagged as gaps, with
  no invented numbers silently filling them?
- Search the text for `—` and `–` and remove them. Scan for AI slop and replace
  it. Confirm "must / should / may" are used deliberately.
- If you pushed back, did you give the verdict first and then the fix or the
  recommendation, rather than quietly writing a weak control?

A good control reads like a competent compliance professional designed it: it
names what must happen, who owns it, how often, how you prove it, and which risk
it buys down. Measurable, owned, justified, and testable beats well-worded every
time.
