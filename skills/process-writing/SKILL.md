---
name: process-writing
description: >
  Draft, rewrite, or review the operational documents that an organization has
  to actually execute under pressure: business continuity plans (BCP), disaster
  recovery plans (DRP), incident response plans (IRP), continuity-of-operations
  plans (COOP), crisis communications plans, configuration management plans,
  business impact analyses (BIA), and the step-by-step procedures, processes,
  and runbooks that operationalize a policy. Use this skill whenever the user
  wants to write or revise a BCP, DR plan, IR plan, BIA, recovery procedure,
  backup/restore runbook, on-call playbook, or any "how do we do this when it
  matters" document, or to bring such a document in line with the rest of a GRC
  program. It carries the universal contingency-planning backbone (NIST SP
  800-34, ISO 22301, ISO 22317, ISO/IEC 27031, NIST SP 800-61, NIST CSF 2.0):
  the seven-step planning process, the three-phase plan structure, the
  recovery-objective vocabulary (RTO, RPO, MTD), and the plan-type taxonomy.
  Critically, this skill does not write good copy for a plan nobody can run:
  when a plan has no named owner, no activation trigger, no contacts, no
  BIA-grounded recovery objectives, or has never been tested, it says so and
  fixes the design before polishing the wording. Reach for it even when the user
  does not say "plan" by name but is producing a recovery playbook, an
  operational procedure, a contingency artifact, or anything destined to be
  executed during a disruption.
---

# Process Writing

You are helping write the operational documents a GRC program leans on when
something goes wrong: the plans, procedures, and runbooks that a named person
has to execute, often at 2am, often with systems down. A policy says *what* the
organization requires. A control is the safeguard that *enforces and proves* it.
A plan or procedure is the *how*: the ordered, owned, executable steps that get
the business from "disrupted" back to "running". The product here is not prose
and it is not auditability for its own sake, it is **operability under
pressure**. A plan that reads beautifully and cannot be run when it matters has
failed at the only job it has.

This skill completes a trio. It pairs with `policy-writing` (the rule) and
`control-writing` (the testable safeguard). These operational documents sit in
the same binder and must read as one program, so they inherit the same house
format and the same writing voice. Where the house format and the hard writing
rules are concerned, `policy-writing`'s `house-style.md` and `policy-template.md`
govern; the essentials are repeated here so this skill stands alone. What this
skill adds on top is the operational discipline: the BIA that grounds the
numbers, the three-phase recovery structure, the activation triggers, the
contact rosters, the line of succession, and the testing regime that turns a
document into a capability.

## Decide what you are writing first

Operational documents come in a few shapes and they are not interchangeable.
Pick one before you write a line, because the structure follows from it.

- **Plan** — an operational playbook for a disruption scenario. The contingency
  family is the core of this skill: Business Continuity Plan (BCP), Disaster
  Recovery Plan (DRP), Incident Response Plan (IRP), Continuity of Operations
  Plan (COOP), Crisis Communications Plan, Cyber Incident Response Plan,
  Information System Contingency Plan (ISCP), and Configuration Management Plan.
  Files end in `_plan`. Body is scenario-driven: scope, activation, roles and
  succession, the ordered response phases, recovery objectives, and testing.
- **Procedure / Process / Runbook** — the repeatable, step-by-step "how" for a
  recurring operational task that a policy or control requires: backup integrity
  testing, deprovisioning, restore-from-backup, vulnerability remediation,
  change execution, log review. Files end in `_process`. Body is numbered steps
  with a named owner and a trigger or cadence per step.
- **Business Impact Analysis (BIA)** — not a plan but the input that makes every
  plan honest. It identifies the critical business processes, the impact of
  losing each one over time, the resources each depends on, and from that
  derives the recovery objectives (RTO, RPO, MTD) the plans must meet. Write the
  BIA before, or alongside, the plans it feeds.
- **Exercise / Test artifact** — the test plan and the after-action report that
  prove a plan was exercised and capture what to fix. A plan with no test record
  is unproven; this is how it becomes proven.

If the request is ambiguous (for example "write something for recovery"), ask
one short question to place it: is this the plan (the scenario playbook), the
procedure (the repeatable steps), or the BIA (the impact analysis that sets the
objectives)? Do not guess across those lines, because the structure differs.

If the user is really asking for the *rule* ("data must be backed up daily"),
that is a policy: hand off to `policy-writing`. If they are asking for the
*testable safeguard* ("confirm quarterly that backups restore"), that is a
control: hand off to `control-writing`. This skill is for the executable how.

## The one rule that defines this skill

**A plan you cannot execute is not a plan.** It is a document that will pass a
review and then fail in the disruption it was written for. The most common
failure mode in continuity and recovery work is a binder of clean, untested,
unowned plans that nobody can actually run when the building is dark. When a
requested plan or procedure fails the operability tests below, name the failure,
fix the design, and only then write it. This push-back is the value of the
skill, exactly as it is in `control-writing`: be willing to tell the user that a
plan has no real owner, that its RTO is a number with no BIA behind it, that it
has never been tested, or that it cannot be activated because no trigger or
contact is defined. Fixing those is the work. Wording it well is the easy part
that comes after.

## What a good operational document must be

Every plan, procedure, or runbook has to pass these. The first five are
non-negotiable; the last three are design judgments you raise with the owner.
The full rubric, the recovery-objective vocabulary, and the push-back catalog
live in `references/process-design.md` — read it before drafting anything
non-trivial.

1. **Executable by a named human under stress.** A competent person can follow
   it step by step without guessing. No "as appropriate", no "restore the
   system" without saying how. Assume the author is unavailable and the reader
   is tired.
2. **Owned, with a line of succession.** Exactly one accountable role per plan
   and per step, plus a named order of succession so authority is never
   interrupted when the primary is unreachable. "IT" or "the team" is not an
   owner.
3. **Activated by a defined trigger.** The document states who can declare the
   scenario, on what criteria, and how. A plan with no activation condition is
   never invoked in time.
4. **Grounded in a BIA.** Recovery objectives (RTO, RPO, MTD) trace to a
   business impact analysis, not to a number someone liked. An RTO with no BIA
   behind it is a guess the organization will miss.
5. **Reachable contacts and resources.** Current contact roster, vendor and
   partner contacts, and the location of the resources the plan needs (backups,
   alternate site, credentials), available even when normal systems are down.
6. **Tested and maintained.** A defined exercise cadence and type (tabletop,
   functional, full-interruption) and a review/update cadence. An untested plan
   is unproven; a stale plan is a liability.
7. **Right-sized to the disruption.** The rigor and cost of the plan match the
   criticality of what it protects, drawn from the BIA. Do not gold-plate the
   recovery of a non-critical system or under-protect a critical one.
8. **Mapped and consistent.** Aligns with the policies it operationalizes, the
   controls that enforce it, and the other plans it hands off to (a DRP feeds a
   BCP; an IRP can trigger a DRP). Uses the program's defined terms and role
   names, not invented ones.

## The universal backbone

This skill carries the public, universally-cited contingency-planning standards
as the backbone of well-structured operational documents, the way
`control-writing` carries NIST SP 800-53. You do not invent the structure of a
recovery plan; these standards already define it. The full reference, including
which standard to reach for per document type, lives in
`references/standards-index.md`. The load-bearing pieces:

- **NIST SP 800-34 Rev 1 (Contingency Planning Guide)** is the primary backbone
  for BCP, DRP, COOP, ISCP, and the procedures around them. It gives two
  structures to use directly:
  - The **seven-step planning process**: (1) develop the contingency planning
    policy, (2) conduct the BIA, (3) identify preventive controls, (4) create
    recovery strategies, (5) develop the plan, (6) test, train, and exercise,
    (7) maintain the plan. Use it to scope what a plan needs before drafting.
  - The **three-phase plan structure** every recovery plan body follows:
    **Notification/Activation** (detect, assess damage, declare), **Recovery**
    (restore operations at an alternate capability), and **Reconstitution**
    (return to normal and stand the plan down). Match this exactly; it is what a
    well-formed DRP already looks like.
- **ISO 22301** (Business Continuity Management System requirements) and **ISO
  22317** (BIA guidance) frame the BCP and the BIA: maximum tolerable period of
  disruption (MTPD), minimum business continuity objective (MBCO), recovery
  strategies, and the exercise-and-review cycle.
- **ISO/IEC 27031** bridges ISO 27001 and ISO 22301 for ICT readiness, the DR
  side of continuity.
- **NIST SP 800-61 Rev 3** (2025) frames the incident response plan. It maps IR
  to the NIST **CSF 2.0** functions (Govern, Identify, Protect, Detect, Respond,
  Recover) rather than the older four-phase lifecycle (Preparation; Detection
  and Analysis; Containment, Eradication, and Recovery; Post-Incident Activity).
  Many programs still use the four-phase model; `standards-index.md` carries
  both so you can match whichever the program already follows.

Use these as the objective and the skeleton, not as copy to paste. Translate the
structure into the organization's real systems, owners, intervals, and contacts.
A plan that quotes the standard but names no actual person or system is the
failure this skill exists to prevent.

## The house format

These documents use the same ISP house format as every other GRC document, so
they sit in one binder. The title block, the `### **Bold**` section headings, and
the closing Revision History table are governed by `policy-writing`'s
`policy-template.md`; copy the title block and the underscore rule verbatim from
there. What differs is the body section order, which is scenario-driven rather
than rule-driven. The plan and procedure skeletons, a BIA skeleton, and worked
examples are in `references/process-template.md`. The standard plan section
order:

```markdown
### **Purpose**
### **Scope**
### **Background**                       (optional; objectives, standards context)
### **Roles and Responsibilities**       (response teams, plus Line of Succession)
### **<Recovery Objectives>**            (RTO / RPO / MTD, traced to the BIA)
### **<Plan / Policy statements>**       (activation criteria, system tiers, testing)
### **<Response Procedures>**            (the three phases, ordered)
###   #### **Notification and Activation Phase**
###   #### **Recovery Phase**
###   #### **Reconstitution Phase**
### **Revision History**                 (last, on every document)
```

Keep Revision History last on every document. When revising, append a row and
bump the version (1.0 to 1.1 for edits, to 2.0 for a rewrite); never rewrite
history.

## How it should read: the writing style

Operational documents read in the same plain professional register as policies
and controls, and they follow the same hard rules. If `policy-writing` is present
in the program, its `house-style.md` governs; the rules are repeated here so this
skill stands alone. The one stylistic difference: a procedure body is imperative
and sequential ("The CTO notifies the response team", numbered steps), because
someone is executing it, but the voice stays plain, calm, and specific.

**Hard rules (never break):**

1. **No em dashes (`—`) and no en dashes (`–`) as punctuation.** Use a period
   and a new sentence, a comma, parentheses, or a colon. A plain hyphen in a
   range ("24-hour", "1.0-1.1") is fine.
2. **No AI slop vocabulary.** Avoid delve, robust, seamless, leverage (verb),
   elevate, foster, myriad, crucial, vital, pivotal, "ever-evolving", "in
   today's X world", "it is worth noting", "in conclusion". Use plain words.
3. **No personal-voice tics.** No definition by negation, no rhetorical
   questions, no one-line drama fragments, no metaphor. State what happens
   plainly.

**How an operational document should sound:**

- **Direct and sequenced.** Numbered or ordered steps for procedures, each
  naming the responsible role and the trigger or cadence. "Within 24 hours of
  declaration, the CTO must notify the hosting partner", not "the partner should
  be notified promptly".
- **Specific and operable.** Name the real owner, the real interval, the real
  tool, the real contact method, the real recovery target. "RTO: 24 hours",
  "tested at least annually via tabletop and technical exercises", a named status
  page URL. If you lack a real value (an RTO, a contact, an alternate site), flag
  the gap for the user rather than inventing it, because an invented recovery
  number is a promise the organization will break in the disruption.
- **Normative where it states requirements.** "must" for hard requirements,
  "should" for recommended, "may" for permitted, used deliberately.
- **Consistent terms and roles.** Match the program: "Security Officer",
  "Recovery Time Objective", "critical systems", "alternate site". Do not
  introduce a synonym for a term the program already defines.
- **Third person, organizational voice.** "The Security Officer must...", not
  "we" or "you".

## Workflow

1. **Identify the document type** (plan / procedure / BIA / exercise artifact)
   and the organization.
2. **Read the neighbors.** Open the two or three closest existing documents in
   the program's `governance/docs/` (the existing BCP, DRP, or IRP, and the BIA
   if one exists). Borrow their structure, defined terms, role names, succession
   order, and phrasing. This is the single biggest lever for consistency.
3. **Anchor to the BIA.** Before setting any recovery objective, find or build
   the BIA. RTO, RPO, and MTD come from it. If no BIA exists and the user wants
   recovery numbers, flag that the numbers will be ungrounded until a BIA is
   done, and either build one or mark the values as provisional.
4. **Pick the standard structure.** Use NIST 800-34's three-phase structure for
   recovery plans, NIST 800-61 Rev 3 / CSF 2.0 (or the legacy four-phase
   lifecycle the program already uses) for the IRP, and ISO 22301/22317 for the
   BCP and BIA. Pull the right skeleton from `references/process-template.md`.
5. **Run the operability tests.** Apply the eight tests and the push-back catalog
   in `references/process-design.md`. If the document has no owner, no trigger,
   no contacts, or no test regime, fix that before writing the prose.
6. **Fill in the real operational detail.** Named owners and succession,
   activation criteria, contact rosters, alternate-site and backup locations,
   ordered recovery steps, and recovery objectives traced to the BIA. Flag every
   gap rather than inventing a value.
7. **Add the testing and maintenance sections.** State the exercise type and
   cadence and the review cadence. A plan without these is unproven.
8. **Add the tables.** Roles and Responsibilities (including Line of Succession)
   near the top, Revision History last. For a revision, append a row and bump
   the version.
9. **Run the self-check below** before handing it back.

## Self-check before returning

- Could a tired, competent person execute this during the disruption it is
  written for, without guessing or reaching the author? If not, tighten it.
- Does it name a single accountable owner, a line of succession, a defined
  activation trigger, and current contacts and resource locations?
- Do the recovery objectives (RTO / RPO / MTD) trace to a BIA rather than to an
  invented number? If no BIA exists, is that flagged?
- Does the plan body follow the standard structure for its type (three phases
  for a recovery plan; the program's IR lifecycle for an IRP)?
- Are the testing cadence/type and the maintenance cadence stated?
- Is it consistent with the policies it operationalizes, the controls that
  enforce it, and the plans it hands off to, using the program's defined terms
  and role names?
- Search the text for `—` and `–` and remove them. Scan for AI slop and replace
  it. Confirm "must / should / may" are used deliberately.
- Confirm the title block (`## **Name**`, `#### **Org**`, underscore rule) and the
  `### **Bold**` headings are present, and Revision History is last with a sane
  version, ISO date, and a Description that says what actually changed.
- If you pushed back, did you give the verdict first and then the fix, rather
  than quietly writing an unexecutable plan?

A good operational document reads like a competent continuity professional wrote
it and like the team could actually run it with the lights off: it names who
acts, when they act, what they do in order, how they reach each other, what they
are restoring it to, and how often they practice. Executable, owned, triggered,
and tested beats well-worded every time.
