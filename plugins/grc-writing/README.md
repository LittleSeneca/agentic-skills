# grc-writing

One house format and one plain professional voice for governance, risk, and compliance documents.

GRC writing starts from the same ground every time: the same standards, the same section order, the same rules about what a good control or a runnable plan actually requires. This plugin carries that ground so Claude begins at the document instead of rebuilding the conventions from nothing. It does not write good copy for a bad design; when a control is unmeasurable or a plan has no owner, it fixes the design before polishing the wording.

## Skills

Three skills ship with the plugin. Each triggers on its own kind of document, and they hand off to one another at the boundaries.

| Skill | What it does |
|---|---|
| `policy-writing` | Policies and charters in the Information Security Program (ISP) house format: title block, standard section order, roles and revision-history tables. Covers policies and charters only. |
| `control-writing` | Measurable, testable, risk-aligned controls. Carries the full NIST SP 800-53 Rev 5 catalog as a machine-readable reference (control statements, discussion, parameters, baselines, assessment objectives) plus a push-back rubric for weak control design. |
| `process-writing` | The operational documents an organization executes under pressure: BCP, DR, IR plans, COOP, BIA, and the procedures and runbooks that operationalize a policy. Carries the contingency-planning backbone (NIST SP 800-34, ISO 22301/22317/27031, NIST SP 800-61, CSF 2.0). |

All three enforce the same hard style rules: no em dashes, no AI slop, auditable requirements.

## Setup

No credentials. Install the plugin and the skills trigger automatically when you write or review a policy, control, or operational plan. Each skill's `SKILL.md` documents exactly when it fires and how it behaves; the reference material lives alongside it under `references/`.
