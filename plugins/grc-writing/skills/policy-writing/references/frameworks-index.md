# Frameworks Index — The Policy Backbone

These are the public, widely-cited frameworks that define what an information
security policy set should contain and which document each requirement lives in.
They are the backbone of this skill the way NIST SP 800-53 is the backbone of
`control-writing` and NIST SP 800-34 is the backbone of `process-writing`. Use
them to decide *which policies a program needs*, *what a given policy must
address*, and *which framework references a policy earns credit against*.

This is a structural reference, not a record of what any organization has
implemented. A policy that quotes a framework but names no real owner, system,
or requirement is not a policy, it is filler. Translate every requirement into
the organization's real roles, intervals, and terms.

## The canonical ISP policy set

No framework mandates one universal list, but SANS templates, ISO/IEC 27002's
topic-specific policy areas, NIST SP 800-53's control families, and the policy
packs that GRC vendors ship for SOC 2 and ISO 27001 converge on the same core
set. That convergence is the strongest argument for the canonical set below. A
mature program publishes a **master Information Security Policy** plus a layer of
**topic-specific policies** beneath it.

| Policy | One-line scope |
| --- | --- |
| Information Security Policy (master / ISP) | Top-level governing policy: intent, scope, governance, roles, management commitment. The umbrella the topic-specific policies hang under. |
| Acceptable Use Policy | Permitted and prohibited use of systems, data, networks, and assets by personnel. |
| Access Control Policy | Provisioning, least privilege, RBAC, joiner/mover/leaver, periodic access reviews. |
| Password / Authentication Policy | Credential strength, MFA, account lifecycle, privileged accounts. |
| Asset Management Policy | Inventory of hardware, software, and information assets; ownership; lifecycle; disposal. |
| Data Classification and Handling Policy | Classification tiers, labeling, and handling rules per tier. |
| Data Protection / Privacy Policy | Protection of personal and sensitive data; retention; deletion; data-subject obligations. |
| Cryptography / Encryption Policy | Encryption at rest and in transit, key management, approved algorithms. |
| Backup Policy | Backup scope, frequency, retention, restoration testing. |
| Business Continuity and Disaster Recovery Policy | Resilience objectives, RTO/RPO governance, BCP/DR plan ownership. (The plans themselves are `process-writing`.) |
| Change Management Policy | Authorization, testing, approval, and rollback for production changes. |
| Secure Configuration Policy | Hardening baselines and secure system configuration. |
| Vendor / Third-Party Risk Policy | Due diligence, contractual security terms, ongoing vendor monitoring. |
| Risk Management Policy | Risk assessment methodology, risk register, treatment, acceptance. |
| Physical and Environmental Security Policy | Facility access, secure areas, equipment, environmental controls. |
| Network / Firewall Security Policy | Segmentation, perimeter controls, firewall rule governance. |
| Logging and Monitoring Policy | Event logging, log retention and protection, monitoring and alerting. |
| Vulnerability / Patch Management Policy | Scanning cadence, remediation SLAs, patch deployment. |
| Incident Response Policy | Detection, reporting, triage, notification obligations. (The IR *plan* is `process-writing`.) |
| Personnel Security Policy | Screening, onboarding and offboarding, disciplinary process, security responsibilities. |
| Security Awareness and Training Policy | Mandatory training cadence, phishing simulation, role-based training. |
| Secure Development / SDLC Policy | Secure coding, code review, testing, environment separation. |
| Remote Access / Teleworking Policy | Secure remote connectivity, VPN, endpoint requirements. |
| Acceptable Use of AI Policy | (Emerging) governance of AI and generative-AI tool usage. |

Two boundaries worth keeping straight:

- A policy names the **requirement and the objective**; the **executable plan**
  (BCP, DRP, IRP) and the **step-by-step procedure** are `process-writing`. A
  Backup Policy says backups must be tested quarterly; the restore runbook that
  says how is a process.
- A policy states **what must be true**; the **testable safeguard that proves it
  is true** is `control-writing`. "Data must be encrypted at rest" is the policy;
  "the platform team confirms quarterly that all RDS instances report
  `StorageEncrypted=true`" is the control.

## Which framework wants which policy

| Framework | What it expects of policy | Where the policy obligation lives |
| --- | --- | --- |
| ISO/IEC 27001:2022 | One mandatory top-level information security policy, plus risk-driven topic-specific policies. | Clause 5.2 (the policy); Annex A 5.1 (topic-specific policies). |
| ISO/IEC 27002:2022 | Guidance on the topic-specific policy areas to consider. | Control 5.1 guidance. |
| NIST CSF 2.0 | Establish, communicate, enforce, and review cybersecurity policy. | GOVERN function, GV.PO category. |
| NIST SP 800-53 Rev 5 | A policy and procedures document per control family. | The `xx-1` control in each family (AC-1, AU-1, etc.). |
| SOC 2 (AICPA TSC) | Documented policies that are communicated and implement management's directives. | Common Criteria CC1, CC2.2/CC2.3, CC5.3; topic policies evidence CC6 to CC9. |
| NIST SP 800-12 Rev 1 | Three policy altitudes: program, issue-specific, system-specific. | Chapter 5. |

## ISO/IEC 27001:2022 and 27002:2022

### What 27001 explicitly requires

ISO 27001 hard-mandates exactly **one** policy in the clauses (4 to 10): the
top-level **information security policy** at **Clause 5.2**, approved by top
management. Everything else is risk-driven (selected through the risk assessment
and Statement of Applicability) or comes from the Annex A 5.1 topic list. Other
mandatory *documented information* (scope, risk methodology, SoA, risk treatment
plan, objectives, internal audit and management review records) is not "policy"
but lives in the same governance set.

### The four 27002:2022 control themes

The 2022 edition reorganized the 114 controls of the 2013 edition into **93
controls** across four themes:

| Theme | Clause | Controls |
| --- | --- | --- |
| Organizational | 5 | 37 (A.5.1 to A.5.37) |
| People | 6 | 8 (A.6.1 to A.6.8) |
| Physical | 7 | 14 (A.7.1 to A.7.14) |
| Technological | 8 | 34 (A.8.1 to A.8.34) |

### The topic-specific policy list (A.5.1 guidance)

**A.5.1 (Policies for information security)** is the single Annex A control that
explicitly mandates policy. It requires both a master policy and a set of
**topic-specific policies**, and the 27002 guidance names the areas to consider:

- Access control
- Physical and environmental security
- Asset management
- Information transfer
- Secure configuration and handling of endpoint devices
- Networking security
- Information security incident management
- Backup
- Cryptography and key management
- Information classification and handling
- Management of technical vulnerabilities
- Secure development

This list is the most useful "policy menu" the frameworks give you. Map a
program's existing policies against it to find gaps.

## NIST CSF 2.0

CSF 2.0 (NIST CSWP 29, February 2024) organizes the Core into **six Functions**:
**Govern, Identify, Protect, Detect, Respond, Recover.** **Govern (GV) is the
addition in 2.0** and is where policy lives explicitly. Its **Policy (GV.PO)**
category expects the organization to establish, communicate, and enforce
cybersecurity policy and to review and revise it as requirements, threats,
technology, and mission change. GV.PO is the clean framework anchor for a master
ISP and its review cadence.

The other GV categories (Organizational Context, Risk Management Strategy, Roles
Responsibilities and Authorities, Oversight, Supply Chain Risk Management) frame
the governance content that a master ISP and a Risk Management Policy carry.

## NIST SP 800-53 Rev 5 — the "-1" policy controls

Every control family in 800-53 has an **`xx-1` "Policy and Procedures" control**
that requires the organization to develop, document, and disseminate a policy and
procedures for that family and to review and update them at a defined frequency.
The `xx-1` control is the **policy hook** for each family. AC-1 is
representative: a policy addressing purpose, scope, roles, responsibilities,
management commitment, coordination, and compliance, plus procedures, with a
stated review frequency. That is a ready-made outline for any topic-specific
policy.

| Family | -1 control | | Family | -1 control |
| --- | --- | --- | --- | --- |
| AC Access Control | AC-1 | | PE Physical and Environmental Protection | PE-1 |
| AT Awareness and Training | AT-1 | | PL Planning | PL-1 |
| AU Audit and Accountability | AU-1 | | PS Personnel Security | PS-1 |
| CA Assessment, Authorization, Monitoring | CA-1 | | PT PII Processing and Transparency | PT-1 |
| CM Configuration Management | CM-1 | | RA Risk Assessment | RA-1 |
| CP Contingency Planning | CP-1 | | SA System and Services Acquisition | SA-1 |
| IA Identification and Authentication | IA-1 | | SC System and Communications Protection | SC-1 |
| IR Incident Response | IR-1 | | SI System and Information Integrity | SI-1 |
| MA Maintenance | MA-1 | | SR Supply Chain Risk Management | SR-1 |
| MP Media Protection | MP-1 | | PM Program Management | *(no PM-1)* |

Note the exception: **Program Management (PM) has no PM-1.** Its controls are
program-level and apply organization-wide rather than per-system, so 19 of the 20
families carry the classic `-1` policy control. `control-writing` carries the full
800-53 catalog (statement, discussion, parameters, baselines, assessment
objectives); read the `xx-1` record there when drafting the matching policy.

## SOC 2 — Trust Services Criteria

SOC 2 has five categories. **Security (the Common Criteria) is in every SOC 2**;
Availability, Confidentiality, Processing Integrity, and Privacy are optional and
chosen by scope. The Common Criteria run CC1 to CC9 (CC1 to CC5 map to COSO; CC6
to CC9 are security-specific). The criteria that most directly require
**documented, communicated policy**:

- **CC1.x (Control Environment)** establishes the policy-setting authority and
  accountability. A master ISP and the Roles and Responsibilities table evidence
  it.
- **CC2.2 / CC2.3 (Communication and Information)** require that internal and
  external parties are informed of security policies and their responsibilities.
  This is the explicit "policies must be documented and communicated" hook.
- **CC5.3 (Control Activities)** expects policies and procedures that put
  management's directives into action. This is the criterion auditors map most
  policy documents to.
- **CC6 to CC9** are evidenced by the topic-specific policies: CC6 (access
  control, encryption, physical security), CC7 (logging and monitoring,
  vulnerability and incident management), CC8 (change management), CC9 (vendor and
  third-party risk).

When justifying why a policy exists, cite CC1, CC2.2/CC2.3, and CC5.3 for the
obligation and the relevant CC6 to CC9 criterion for the topic.

## How to use this index

1. **Find the gaps.** Map the program's existing policies against the canonical
   set and the ISO 27002 5.1 list. A missing topic-specific policy in a risk area
   the program faces is the first finding.
2. **Outline from the framework, write for the org.** Use the 800-53 `xx-1`
   structure (purpose, scope, roles, responsibilities, management commitment,
   coordination, compliance) as the skeleton, then fill it with the
   organization's real roles, systems, intervals, and defined terms.
3. **Earn credit once.** One well-written policy maps to ISO 27001 Annex A, a
   CSF GV.PO subcategory, an 800-53 `xx-1` control, and one or more SOC 2 Common
   Criteria at the same time. Record the mappings so the policy is not an orphan.
4. **Keep altitude.** The framework tells you a policy must address a topic; it
   does not tell you to bury step-by-step detail in it. Push specifics down to a
   standard and steps down to a procedure. See `policy-design.md`.

## Sources

- ISO/IEC 27001:2022 (ISMS requirements), Clause 5.2 and Annex A 5.1.
- ISO/IEC 27002:2022 (information security controls), control 5.1 guidance:
  https://www.iso.org/standard/75652.html
- NIST Cybersecurity Framework (CSF) 2.0, NIST CSWP 29:
  https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
- NIST SP 800-53 Rev 5 (control families and the `xx-1` controls):
  https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-12 Rev 1 (policy types, Chapter 5):
  https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-12r1.pdf
- AICPA Trust Services Criteria (SOC 2 Common Criteria CC1 to CC9).
- SANS / CIS security policy templates:
  https://www.sans.org/information-security-policy and
  https://www.cisecurity.org/wp-content/uploads/2019/08/NCSR-SANS-Policy-Templates.pdf
