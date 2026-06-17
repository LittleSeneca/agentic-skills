# Control Templates and Worked Examples

A control is recorded in one of two shapes depending on the audience. Both use
the same fields; the register row is the summary, the control specification is
the full record. Keep the field set consistent so a control set reads as one
program.

Every control statement follows the same grammar: **actor + action + object +
trigger/cadence + measurable condition.** "The account manager (actor) disables
(action) terminated-user accounts (object) within 24 hours of the HR
termination event (trigger), evidenced by the deprovisioning ticket (evidence)."

## The control field set

| Field | What it holds | Why it matters |
| --- | --- | --- |
| Control ID | Organization's identifier (e.g. `AC-02-01`) | Stable reference for mapping and testing |
| Title | Short noun phrase | Scannability |
| Control statement | The normative requirement, in actor-action-object-cadence grammar | The control itself; must be testable |
| Risk addressed | Risk register id or named threat | Anchors the control; no risk means question it |
| Policy enforced | The policy/section this implements | Keeps it from being an orphan |
| Function | Preventive / Detective / Corrective / Compensating / Recovery | Design intent |
| Nature | Administrative / Technical / Physical | Where it lives |
| Automation | Manual / Automated / Hybrid | Cost and provability |
| Owner | Single accountable role | Accountability |
| Frequency | Cadence or "continuous" / "event-driven" | Operability and test scope |
| Evidence | The artifact that proves it operated, and where it lives | Measurability |
| Test procedure | How an assessor verifies it, including sampling | Auditability |
| Framework mapping | NIST 800-53 id(s), SOC 2 CC, ISO 27001 Annex A | Credit one control against many requirements |
| Status | Implemented / Partial / Planned (optional) | Honest posture |

## 1. Control register row (the summary view)

A register is a table of controls. Keep one row per control, key controls
flagged.

```markdown
| ID | Title | Statement (summary) | Function | Owner | Frequency | Evidence | NIST 800-53 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-02-01 | Joiner provisioning | Access is granted only after documented approval by the resource owner before the account is enabled | Preventive | IT Operations Manager | Per request (event-driven) | Approved access request ticket | AC-2, AC-6 |
| AC-02-02 | Leaver deprovisioning | Accounts are disabled within 24 hours of the HR termination event | Preventive | IT Operations Manager | Event-driven | Deprovisioning ticket with timestamps | AC-2 |
| AC-02-03 | Access recertification | Resource owners review and reattest all privileged access | Detective | Security Officer | Quarterly | Signed recertification report | AC-2, AC-6(7) |
```

## 2. Control specification (the full record)

Use this for key controls and anywhere an auditor needs the complete picture.

```markdown
### AC-02-03 — Privileged Access Recertification

**Control statement.** At least quarterly, each resource owner must review every
account with privileged access to systems they own, confirm that continued
access is required, and revoke access that is no longer justified. The review
must be completed and signed within ten business days of being initiated.

| Field | Value |
| --- | --- |
| Risk addressed | RR-014 Excessive standing privilege / insider misuse |
| Policy enforced | Access Control Policy, Least Privilege section |
| Function | Detective |
| Nature | Administrative |
| Automation | Hybrid (access list generated automatically; review is manual) |
| Owner | Security Officer (accountable); resource owners (perform) |
| Frequency | Quarterly |
| Evidence | Signed recertification report per system, stored in the GRC tool |
| Test procedure | For a sample of systems, confirm a signed report exists for each quarter, that revocations identified were completed within the SLA, and that the reviewer was the current resource owner |
| Framework mapping | NIST 800-53 AC-2, AC-6(7); SOC 2 CC6.1, CC6.3; ISO 27001 A.5.18 |
| Status | Implemented |
```

## 3. Worked example — fixing a bad control

This shows the push-back the skill is for. The requested control is reworded
only after its design is fixed.

**Requested (bad):**
> "IT will ensure that user access is reviewed regularly and that access is
> appropriate. We use Okta for this."

**Verdict.** This is not a testable control. It fails four tests:
no measurable cadence ("regularly"), no measurable criterion ("appropriate"),
no single owner ("IT"), and it names a tool instead of a behavior. As written it
would pass a casual read and fail an audit.

**Redesigned:**
> "At least quarterly, the Security Officer must initiate a review in which each
> resource owner reattests that every active account on their systems still
> requires its current access level. Access not reattested within ten business
> days must be disabled. Okta access reports provide the account list; the
> signed reattestation in the GRC tool is the evidence."

What changed: a real cadence (quarterly), a real owner (Security Officer
accountable, resource owners performing), a measurable criterion (reattested or
disabled), a deadline (ten business days), and the tool demoted to its real
role (it produces the input, it is not the control).

## 4. Worked example — recommending no control

Not every requested control should exist.

**Requested:**
> "Add a control requiring weekly manual review of firewall rule-base diffs by
> two engineers."

**Verdict and recommendation.** For a Moderate-impact system whose firewall
changes already go through approved change management with automated
configuration drift detection, a second weekly manual two-person review is
gold-plating. It duplicates the change-management control and the drift-detection
control and costs engineer time disproportionate to the residual risk.
Recommendation: do not add it. Rely on the existing change-management approval
(preventive) and drift detection (detective), and if assurance is still wanted,
add the firewall to the quarterly configuration audit rather than a weekly
manual review. If leadership still wants the review, document it as an accepted
cost, not a risk-driven control.

## House style for control statements

Controls inherit the same hard writing rules as policies (see
`house-style.md` if the policy-writing skill is present in the same program):

- **Normative verbs used deliberately.** "must" for hard requirements, "should"
  for recommended, "may" for permitted. Most control lines use "must".
- **No em dashes or en dashes as punctuation. No AI slop.** A plain hyphen in a
  range ("24-hour") is fine.
- **Specific and auditable.** Name the real interval, the real artifact, the
  real role. An invented number becomes a control nobody meets; flag the gap
  instead of filling it silently.
- **Third person, organizational voice.** "The Security Officer must...", not
  "we" or "you".
