# Process Design — Operational Document Best Practices and the Push-Back Catalog

An operational document is a plan, procedure, or runbook that a named person has
to execute during or after a disruption, often under stress and without the
author available. Its job is operability: getting the organization from
"disrupted" back to "running" by following ordered, owned, executable steps.
That definition is the whole job. Everything below exists to either build a
document that meets it or to reject one that does not.

The most important rule in this skill: **a plan you cannot execute is not a
plan.** A clean, well-formatted plan that has no owner, no activation trigger, no
contacts, no BIA behind its numbers, or has never been tested is worse than no
plan, because it passes review and then fails in the disruption it was written
for. When a requested document fails the tests below, say so and fix the design
before you polish the wording.

## What makes an operational document good — the eight tests

Run every plan or procedure against these. A document that fails any of the
first five is not ready; a document that fails the last three is a design problem
to raise with the owner.

1. **Executable by a named human under stress.** A competent person can follow
   it step by step without guessing what "appropriate" or "restore the system"
   means. Write for the reader who is tired, working an outage, and cannot reach
   the author. Every step states what to do, not just what outcome to achieve.
2. **Owned, with a line of succession.** Exactly one accountable role owns the
   plan, and each step names the role that performs it. A documented order of
   succession ensures decision-making authority is never interrupted when the
   primary is unreachable. "IT" or "the team" is not an owner.
3. **Activated by a defined trigger.** The document states who can declare the
   scenario, on what criteria (for example "systems unavailable more than 48
   hours"), and how the declaration is communicated. A plan with no activation
   condition is never invoked in time, or is invoked too late.
4. **Grounded in a BIA.** Recovery objectives (RTO, RPO, MTD) trace to a
   business impact analysis, not to a number that sounded reasonable. An RTO with
   no BIA behind it is a commitment the organization will miss in the real event.
5. **Reachable contacts and resources.** A current contact roster (internal
   teams, vendors, partners, authorities), and the location of every resource the
   plan depends on (backups, alternate site, credentials, this document itself),
   accessible even when normal systems and the corporate network are down.
6. **Tested and maintained.** A defined exercise type and cadence (tabletop,
   walkthrough, functional/technical, full-interruption) and a defined review and
   update cadence. An untested plan is unproven. A plan that has not been reviewed
   since the architecture changed is actively misleading.
7. **Right-sized to the disruption.** The rigor, cost, and recovery ambition
   match the criticality of what is protected, as established by the BIA. A
   non-critical system does not need a hot-site, sub-hour RTO; a critical revenue
   system should not have a multi-day RTO by default.
8. **Mapped and consistent.** The document operationalizes named policies, is
   enforced by named controls, and hands off cleanly to the other plans in the
   set (an IRP can trigger a DRP; a DRP feeds the BCP). It uses the program's
   defined terms and role names rather than inventing new ones.

## Recovery-objective vocabulary

These terms are the measurable backbone of every continuity and recovery
document. Use them precisely; they are not interchangeable, and an audience of
auditors and customers will know if they are misused.

- **RTO (Recovery Time Objective)** — the maximum acceptable time to restore a
  process or system after a disruption. "How long can it be down."
- **RPO (Recovery Point Objective)** — the maximum acceptable data loss measured
  in time, set by the backup or replication interval. "How much data can we
  lose." A daily backup implies an RPO of up to 24 hours.
- **MTD / MTPD (Maximum Tolerable Downtime / Maximum Tolerable Period of
  Disruption)** — the absolute outer limit a process can be unavailable before
  the damage to the organization is unacceptable. RTO must be shorter than MTD;
  the gap between them is the time available for recovery work (sometimes called
  Work Recovery Time, WRT).
- **MBCO (Minimum Business Continuity Objective)** — the minimum level of
  service or output the organization must sustain during a disruption (ISO
  22301). Not full normal operations, the floor below which it must not fall.
- **WRT (Work Recovery Time)** — the time to validate, reconcile, and resume
  productive work after systems are technically restored but before normal
  operation resumes. RTO + WRT must stay within MTD.

These are derived in the BIA and consumed by the plans. If a plan states an RTO,
the BIA is where that number must come from.

## Recovery strategy vocabulary

When a plan describes where and how operations resume, use the standard
alternate-processing terms (NIST SP 800-34) so the strategy is unambiguous:

- **Cold site** — space and infrastructure, no pre-installed systems. Cheapest,
  slowest to bring up.
- **Warm site** — partially configured with some equipment and connectivity.
- **Hot site** — fully configured, near-immediate cutover. Most expensive.
- **Mobile site** — transportable recovery capability.
- **Mirrored / cloud failover** — a continuously synchronized duplicate;
  effectively zero RTO/RPO at the cost of running a parallel environment.

Match the strategy to the RTO/MTD from the BIA. A 24-hour RTO does not justify
the cost of a mirrored hot site; a sub-hour RTO cannot be met by a cold site.

## The standard structures — use them, do not invent

- **Recovery plans (DRP, ISCP, COOP, BCP body)** follow the NIST 800-34
  **three-phase structure**:
  1. **Notification/Activation** — detect the disruption, assess damage, and
     declare the plan active through a defined notification sequence.
  2. **Recovery** — restore operations at the alternate capability, in the
     ordered sequence the plan specifies, per responsible team.
  3. **Reconstitution** — return processing to the original or a new permanent
     site, validate, and formally stand the plan down.
- **The contingency planning program** follows the NIST 800-34 **seven-step
  process**: (1) develop the policy, (2) conduct the BIA, (3) identify
  preventive controls, (4) create recovery strategies, (5) develop the plan, (6)
  test/train/exercise, (7) maintain. Use it to check a program is complete, not
  just a single plan.
- **Incident response plans** follow either NIST SP 800-61 **Rev 3** (mapped to
  CSF 2.0 functions: Govern, Identify, Protect, Detect, Respond, Recover) or the
  legacy **four-phase lifecycle** (Preparation; Detection and Analysis;
  Containment, Eradication, and Recovery; Post-Incident Activity). Match whichever
  the program already uses; do not mix the two in one document.
- **The BIA** follows ISO 22317 / NIST 800-34 step 2: identify the critical
  processes, determine the impact of losing each over time, identify the
  resources and dependencies each needs, and derive RTO/RPO/MTD from the impact.

Full detail and the per-document-type mapping are in `standards-index.md`.

## The push-back catalog — un-executable-plan smells and what to do

When a requested document trips one of these, do not just reword it. Name the
problem, then either fix the design or recommend the missing prerequisite. Each
entry gives the smell and the move.

1. **No owner or diffuse ownership.** "IT recovers the environment", "the team
   responds".
   → Assign a single accountable role per plan and per step, and add a Line of
   Succession. If no one owns it, that is the first finding.
2. **No activation trigger.** The plan describes recovery but never says who
   declares the disaster or on what criteria.
   → Define the declaration authority, the activation criteria (concrete
   thresholds), and the notification sequence. Without these the plan is never
   invoked in time.
3. **Recovery objectives with no BIA.** An RTO or RPO appears with nothing
   behind it.
   → Trace it to the BIA. If no BIA exists, flag that the number is ungrounded
   and either build the BIA or mark the value provisional. Do not ship an
   invented recovery commitment.
4. **Unexecutable steps.** "Restore the system", "recover the data", "handle the
   incident" with no how.
   → Decompose into ordered, concrete actions a competent operator can run:
   which script, which backup, which console, in what sequence, verified how.
5. **No contacts or stale contacts.** The plan needs to reach a vendor, a
   partner, or the response team but lists no current way to do so.
   → Add a contact roster and require it be kept current and available offline.
   A recovery that depends on an unreachable person stalls at step one.
6. **Never tested / no exercise regime.** The plan has no testing cadence or
   record.
   → Add the exercise type and cadence (tabletop at minimum, technical for DR)
   and the maintenance cadence. State that an untested plan is unproven and
   schedule the first exercise.
7. **Stale plan.** The plan references systems, sites, or people that no longer
   exist.
   → Reconcile against current reality before reusing it. A plan that confidently
   names a decommissioned alternate site is worse than no plan.
8. **Tool or product named as the plan.** "We use AWS Backup, so we are
   covered."
   → A product is not a procedure. State the steps the product is used to perform,
   who performs them, the recovery target, and how restoration is verified.
9. **Gold-plating or under-protection.** The recovery ambition does not match the
   criticality from the BIA.
   → Right-size the strategy to the RTO/MTD. Flag a hot-site for a non-critical
   system, or a multi-day RTO for a revenue-critical one.
10. **Policy or control dressed as a plan.** "Backups must be encrypted" (policy)
    or "confirm quarterly that backups restore" (control) submitted as a plan.
    → Route the rule to `policy-writing` and the testable safeguard to
    `control-writing`. This skill writes the executable how, not the requirement
    or the test.
11. **Orphaned plan.** The document hands off to a plan or team that does not
    exist, or duplicates another plan's scope.
    → Reconcile the handoffs (IRP to DRP, DRP to BCP) and consolidate overlapping
    plans so the set is coherent.
12. **Continuity theater.** The plan exists only to satisfy an auditor's checklist
    and could never actually be run.
    → Call it out. Either make it executable and exercise it, or be honest that
    the capability does not yet exist. Passing an audit with a plan nobody could
    run is a liability that surfaces at the worst possible time.

When you reject or redesign a document, give the verdict first ("This is not an
executable plan because it has no activation trigger and no owner"), then the
corrected version or the missing prerequisite. Be willing to conclude that the
right next step is "do the BIA first" or "this belongs in the policy, not a
plan".

## Using the standards

The structures in `standards-index.md` are the authoritative source of
well-formed operational documents. Use them as the objective and the skeleton,
not as copy to paste.

- **Treat the standard structure as the frame, not the wording.** NIST 800-34
  tells you a recovery plan has three phases and what each must accomplish.
  Translate that into the organization's real systems, scripts, sites, owners,
  and contacts.
- **Fill the organization-specific values.** The standard leaves RTO, RPO, the
  alternate-site strategy, the contact roster, and the activation criteria for
  the organization to set. Filling them with real, BIA-grounded values is the
  operability work this skill exists to do. An unfilled recovery objective is an
  unexecutable plan.
- **Match the program's existing lifecycle.** If the IRP already uses the
  four-phase model, keep it; do not convert it to CSF 2.0 functions just because
  Rev 3 prefers them. Consistency across the set matters more than chasing the
  newest revision.

The standards are a reference for structure, not a record of capability. Never
claim a plan is operational because it follows the standard. It is operational
only when it is owned, contactable, BIA-grounded, and tested.
