# Control Design — GRC Best Practices and the Push-Back Catalog

A control is a safeguard that reduces a specific risk to within the
organization's risk appetite, at a cost justified by the loss it prevents, in a
way you can prove operated. That definition is the whole job. Everything below
exists to either build a control that meets it or to reject one that does not.

The most important rule in this skill: **do not write good copy for a bad
control.** A clean sentence wrapped around an untestable, unowned, or
unjustified requirement is worse than no control, because it passes review and
then fails in an audit or an incident. When a requested control fails the tests
below, say so and fix the design before you polish the wording.

## What makes a control good — the seven tests

Run every control against these. A control that fails any of the first four is
not ready; a control that fails the last three is a design problem to raise with
the owner.

1. **Risk-anchored.** The control treats a named risk or threat and enforces a
   named policy requirement. A control that maps to no risk is overhead. If you
   cannot name the risk, the control probably should not exist.
2. **Specific and actionable.** It names the actor, the action, the object, and
   the trigger or cadence. A competent operator can execute it without guessing
   what "appropriate" or "regularly" means.
3. **Measurable and testable.** There is a defined artifact that proves the
   control operated and a pass/fail criterion an auditor can apply. If you
   cannot describe the evidence and the test, it is not a control yet.
4. **Owned.** Exactly one accountable role owns the control. "IT" or "the team"
   is not an owner. Unowned controls rot.
5. **Right-sized to appetite and cost.** The cost of operating the control is
   justified by the risk it reduces. It does not gold-plate a low risk or
   under-protect a high one. The NIST baseline tier (Low / Moderate / High) is a
   fast sanity check on whether the control belongs at this impact level.
6. **Operable and sustainable.** It runs at a cadence the organization can
   actually sustain with the tooling and data it has. A control nobody can
   perform is a finding waiting to happen.
7. **Mapped.** It links to the framework references it satisfies (NIST 800-53,
   SOC 2, ISO 27001) and to the policy it enforces, so it is not an orphan and
   so one control can be credited against many requirements.

## Control taxonomy — design vocabulary

Classify a control along three axes. The classification drives design choices
(a preventive automated control usually beats a detective manual one for the
same risk).

- **By function:** Preventive (stops the event), Detective (finds it after the
  fact), Corrective (fixes it), Deterrent, Recovery, and Compensating (stands in
  for a missing primary control). Prefer preventive where it is cost-effective;
  do not settle for detective-only when a cheap preventive exists.
- **By nature:** Administrative (policy, process, training), Technical
  (enforced by a system), Physical.
- **By automation:** Manual, Automated, Hybrid. Automated controls are cheaper
  to operate and easier to prove at scale. Favor them for high-frequency checks.

Also distinguish **key controls** (a failure directly exposes the risk; these
get the most rigor and the tightest evidence) from **supporting controls**, and
note when a control is **compensating** so the missing primary is visible.

## Cost efficiency and risk appetite

Controls cost money and friction. Treat the control set as a portfolio, not a
pile.

- **Spend in proportion to risk.** The expected cost of operating a control
  should be less than the expected reduction in loss (a rough annualized-loss
  comparison is enough). Do not spend more defending an asset than it is worth.
- **Right-size to the impact level.** Use the baseline tier as a proxy for
  appetite. If the system is a Moderate-impact system, controls drawn from above
  the High baseline for that risk are likely gold-plating; controls in the
  Moderate baseline that are missing are gaps. State the tier you are designing
  to.
- **Rationalize duplicates.** One well-placed control can satisfy several
  framework requirements. Before adding a control, check whether an existing one
  already treats the risk. Merge overlapping controls rather than stacking them.
- **A control is not always the answer.** Mitigation is one of four treatments;
  accept, transfer, and avoid are the others. If residual risk is already within
  appetite, adding a control is waste. Recommend acceptance (with sign-off)
  instead of inventing a safeguard nobody needs.
- **Move left when it is cheap.** A preventive control that makes the bad state
  impossible is usually cheaper over time than a detective control that finds it
  plus a corrective control that cleans it up.

## The push-back catalog — bad-control smells and what to do

When a requested control trips one of these, do not just reword it. Name the
problem, then either redesign it into a testable control or recommend dropping,
merging, or accepting. Each entry below gives the smell and the move.

1. **Unmeasurable language.** "Ensure", "appropriate", "regularly", "as
   needed", "where possible", "best effort", "adequate", "periodically".
   → Replace with a metric, threshold, and cadence, or flag the gap for the
   owner to supply. "Reviewed regularly" becomes "reviewed at least quarterly".
2. **No owner or diffuse ownership.** "IT ensures...", "the team monitors...".
   → Assign a single accountable role. If none exists, that is the first finding.
3. **No evidence / untestable.** There is no artifact that proves it ran.
   → Define the evidence (ticket, log, report, signed approval) and where it
   lives. If no evidence can exist, the control cannot be operated as written.
4. **Control with no risk.** It treats nothing identifiable.
   → Ask what risk it addresses. If there is none, recommend removing it rather
   than carrying dead weight.
5. **Gold-plating.** Cost is disproportionate to the risk, or the rigor exceeds
   the impact level.
   → Flag the mismatch and propose a right-sized version, or recommend accepting
   the residual risk.
6. **Tool named as control.** "We use CrowdStrike", "Okta handles this".
   → A product is not a control. State the behavior the product must enforce and
   the evidence it produces. The tool is the implementation, not the control.
7. **Policy objective dressed as a control.** "Data must be secure", "Access
   must be appropriate".
   → That is a policy statement, not a testable safeguard. Either it belongs in
   the policy (use the policy-writing skill) or it must be decomposed into
   specific, testable controls.
8. **Overlap and duplication.** Two or more controls treat the same risk the
   same way.
   → Consolidate into one and map it to all the requirements it satisfies.
9. **Infeasible operation.** The cadence is impossible, the data does not
   exist, or no tool can perform it.
   → Redesign to what is actually operable, or escalate that the requirement
   cannot be met as stated.
10. **Compensating control with no rationale.** A stand-in is offered without
    comparing it to the primary it replaces.
    → Require the comparison: what primary control is missing, why, and how the
    compensating control achieves equivalent risk reduction.
11. **Detective-only where prevention is cheap.** The design catches the bad
    state instead of preventing it, though prevention is available and affordable.
    → Recommend the preventive control and keep detection as backstop only if it
    adds value.
12. **Compliance theater.** The control exists only to check a framework box and
    reduces no real risk.
    → Call it out. Either tie it to a real risk and make it operate, or recommend
    dropping it. Passing an audit with a control nobody runs is a liability.

When you reject or redesign a control, give the verdict first ("This is not a
testable control because..."), then the corrected version or the
recommendation. Be willing to conclude that the right answer is "this control
should not exist" or "this is the policy's job, not a control's".

## Using the NIST SP 800-53 reference

The catalog in `references/nist-800-53.json` is the authoritative source of
well-designed control objectives. Use it as the backbone, not as copy to paste.

- **Find the control.** Scan `nist-800-53-index.md` for the family and control
  id, then read the full record in `nist-800-53.json` (keyed by lowercase id,
  e.g. `ac-2`, `ac-2.1`). Each record carries the statement, discussion,
  organization-defined parameters, baselines, related controls, and enhancement
  ids.
- **Treat the statement as the objective, not the wording.** NIST states what
  the safeguard must achieve. Translate it into the organization's voice and its
  real tools, owners, and intervals.
- **Fill the ODPs.** NIST leaves `[Assignment: ...]` and `[Selection: ...]`
  placeholders for the organization to set. Filling them with real values (the
  frequency, the roles, the thresholds) is exactly the measurability work this
  skill exists to do. An unfilled ODP is an unmeasurable control.
- **Use assessment objectives as the test plan.** `nist-800-53-assessment.json`
  holds the 800-53A assessment objectives per control, already decomposed into
  testable determination statements. These are the ready-made measurability and
  evidence checklist. Pull them when defining how a control is verified.
- **Use baselines to right-size.** The `baselines` field (Low / Moderate / High
  / Privacy) tells you at which impact level NIST expects the control. Match it
  to the system's categorization to avoid gold-plating or gaps.
- **Use related controls to avoid orphans.** The `related` and `requires` fields
  surface dependencies. A control often needs its neighbors to be real.

The catalog is generated from the official NIST OSCAL release by
`scripts/build_nist_catalog.py`. It is a reference, not a mapping of what the
organization has implemented. Never claim a control is in place because it is in
the catalog.
