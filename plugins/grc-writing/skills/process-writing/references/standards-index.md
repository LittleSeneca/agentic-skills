# Standards Index — The Universal Contingency-Planning Backbone

These are the public, widely-cited standards that define the structure of
operational GRC documents. They are the backbone of this skill the way NIST SP
800-53 is the backbone of `control-writing`. Use them as the objective and the
skeleton; translate every structure into the organization's real systems,
owners, intervals, and contacts. A plan that quotes a standard but names no
actual person or system is the failure this skill exists to prevent.

This is a structural reference, not a record of what any organization has
implemented. Following a standard does not make a plan operational. Ownership,
contacts, BIA-grounded objectives, and testing do.

## Which standard for which document

| Document | Primary standard | Supplements |
| --- | --- | --- |
| Business Continuity Plan (BCP) | ISO 22301 | NIST SP 800-34, ISO 22313 |
| Disaster Recovery Plan (DRP) | NIST SP 800-34 Rev 1 | ISO/IEC 27031, ISO 22301 |
| Information System Contingency Plan (ISCP) | NIST SP 800-34 Rev 1 | — |
| Continuity of Operations Plan (COOP) | NIST SP 800-34 Rev 1 | — |
| Incident Response Plan (IRP) | NIST SP 800-61 Rev 3 (CSF 2.0) | NIST SP 800-61 Rev 2 (4-phase), NIST CSF 2.0 |
| Crisis Communications Plan | NIST SP 800-34 Rev 1 | ISO 22301 |
| Business Impact Analysis (BIA) | ISO 22317 | NIST SP 800-34 Rev 1 step 2 |
| Configuration Management Plan | NIST SP 800-128 | NIST SP 800-53 CM family |
| Recovery / backup / restore procedures | NIST SP 800-34 Rev 1 | the plan they support |

## NIST SP 800-34 Rev 1 — Contingency Planning Guide

The primary backbone for recovery plans. Free and public. Two structures to use
directly.

### The seven-step contingency planning process

Use this to scope a plan or to check a program is complete, not just a single
document.

1. **Develop the contingency planning policy statement.** Establish the authority
   and guidance for the program. (This is a policy: `policy-writing` owns it.)
2. **Conduct the business impact analysis (BIA).** Identify and prioritize the
   critical systems and processes and derive their recovery objectives.
3. **Identify preventive controls.** Measures that reduce the likelihood or
   impact of disruption (these are controls: `control-writing` owns them).
4. **Create contingency / recovery strategies.** Backup, alternate site, and
   restoration approaches sized to the recovery objectives.
5. **Develop the contingency plan.** The executable document, in the three-phase
   structure below.
6. **Ensure plan testing, training, and exercises.** Tabletop and functional
   exercises on a defined cadence.
7. **Ensure plan maintenance.** Review and update on a defined cadence and after
   significant change.

### The three-phase plan structure

Every recovery plan body (DRP, ISCP, COOP) follows these three phases in order.
This is what a well-formed DRP already looks like.

1. **Notification/Activation Phase.** Detect the disruption, notify recovery
   personnel through a defined sequence, perform damage assessment, and declare
   the plan active against defined activation criteria. Names: who is notified
   first, who declares, on what thresholds, by what channels.
2. **Recovery Phase.** Restore operations at the alternate capability. Ordered
   recovery steps per responsible team, executed in sequence (some steps may run
   in parallel where stated). Ends when the minimum service level is restored.
3. **Reconstitution Phase.** Restore full operations at the original or a new
   permanent site, validate functionality and security, transition back from the
   alternate capability, and formally deactivate the plan (including disposal of
   any temporary resources).

### Plan-type taxonomy

NIST 800-34 distinguishes these plan types. They are related but not
interchangeable; a program may have several, each with a defined scope and
handoffs to the others.

- **Business Continuity Plan (BCP)** — sustains the organization's essential
  business processes during and after a disruption. Broadest scope.
- **Continuity of Operations Plan (COOP)** — sustains an organization's essential
  functions at an alternate site for up to an extended period.
- **Crisis Communications Plan** — internal and external communications during a
  disruption (status page, customer notice, press, authorities).
- **Critical Infrastructure Protection (CIP) Plan** — protects critical
  infrastructure components.
- **Cyber Incident Response Plan** — responds to a cyber attack specifically
  (overlaps with the IRP; see 800-61).
- **Disaster Recovery Plan (DRP)** — restores IT systems and operations at an
  alternate site after a major disruption. The IT-recovery workhorse.
- **Information System Contingency Plan (ISCP)** — recovery of a single
  information system.
- **Occupant Emergency Plan (OEP)** — life-safety and facility evacuation.

### Alternate-site strategies

Cold site, warm site, hot site, mobile site, mirrored/cloud failover. Match to
the RTO/MTD from the BIA. See the recovery-strategy vocabulary in
`process-design.md`.

## ISO 22301 — Business Continuity Management Systems

The certifiable BCMS standard. Frames the BCP and the wider continuity program
on a plan-do-check-act cycle. Load-bearing concepts:

- **MTPD (Maximum Tolerable Period of Disruption)** — the outer limit before
  damage is unacceptable. Same idea as MTD.
- **MBCO (Minimum Business Continuity Objective)** — the minimum acceptable
  service level during disruption.
- **BIA and risk assessment** as the foundation, recovery strategies sized to the
  objectives, and a required **exercise and review** cycle.
- Management commitment, defined roles, and continual improvement.

**ISO 22313** is the implementation guidance companion to 22301. **ISO 22317** is
the dedicated BIA guidance.

## ISO/IEC 27031 — ICT Readiness for Business Continuity

Bridges ISO/IEC 27001 (information security) and ISO 22301 (business continuity)
for the ICT / disaster-recovery side. Frames how IT continuity and recovery
support the broader BCMS. The 2025 edition ties ICT readiness explicitly to both
27001 and 22301. Reach for it when the DRP needs to show how IT recovery fits the
business continuity program.

## NIST SP 800-61 — Incident Response

The backbone for the Incident Response Plan. Two models exist; match the one the
program already uses and do not mix them in a single document.

### Rev 3 (2025) — CSF 2.0 community profile

Rev 3 reframes incident response as part of continuous cybersecurity risk
management rather than a discrete few-day event, and maps IR activities to the
six **NIST CSF 2.0 functions**:

- **Govern** — policy, roles, risk tolerance, supply-chain and continuity ties.
- **Identify** — asset, vulnerability, and risk awareness that feeds response.
- **Protect** — safeguards that reduce incident likelihood and blast radius.
- **Detect** — monitoring and detection that surfaces incidents.
- **Respond** — containment, eradication, analysis, and communication.
- **Recover** — restoration of services and post-incident improvement.

### Rev 2 — the legacy four-phase lifecycle

Many programs still structure their IRP on the older four-phase lifecycle, and it
remains valid:

1. **Preparation** — staffing, tooling, training, and the response system.
2. **Detection and Analysis** — identify, scope, and triage the incident; assign
   severity.
3. **Containment, Eradication, and Recovery** — limit damage, remove the cause,
   and restore systems.
4. **Post-Incident Activity** — root-cause analysis, lessons learned, and
   improvement.

If the existing IRP already uses the four-phase model, keep it. Consistency
across the program matters more than adopting the newest revision for its own
sake.

## NIST CSF 2.0 — the Respond and Recover functions

The Cybersecurity Framework 2.0 functions (Govern, Identify, Protect, Detect,
Respond, Recover) underpin the response and recovery documents. The **Respond**
and **Recover** functions are the operational ones this skill produces documents
for. Use the function names when the program organizes its plans around CSF, so
the operational documents map cleanly to the framework the controls are mapped
to.

## Exercise and test types

A plan is unproven until exercised. State the type and cadence in the plan's
testing section. From least to most disruptive:

- **Tabletop / walkthrough** — a discussion-based exercise that validates that
  personnel know the notification and activation steps and their roles. The
  minimum bar for any plan, at least annually.
- **Functional / technical test** — actually perform a recovery action: restore
  from backup, fail over to the alternate site, validate the restored
  environment. The bar for a DRP.
- **Full-interruption / full-scale** — execute the plan against a real or
  simulated outage of the production capability. Highest assurance, highest risk.

Every exercise produces an **after-action report / lessons-learned record**:
what worked, what failed, the recovery metrics actually achieved versus the
objectives, and the corrective actions filed. That record is the evidence the
plan is real.

## Sources

- NIST SP 800-34 Rev 1, Contingency Planning Guide for Federal Information
  Systems: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf
- NIST SP 800-61 Rev 3, Incident Response Recommendations and Considerations for
  Cybersecurity Risk Management (CSF 2.0 Community Profile):
  https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r3.pdf
- NIST Cybersecurity Framework (CSF) 2.0.
- ISO 22301 (BCMS requirements), ISO 22313 (BCMS guidance), ISO 22317 (BIA),
  ISO/IEC 27031 (ICT readiness for business continuity).
- NIST SP 800-128 (configuration management for information systems).
