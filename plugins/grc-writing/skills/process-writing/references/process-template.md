# Operational Document Templates and Worked Examples

Copy from these skeletons. They share the ISP house title block and Revision
History with `policy-writing`'s `policy-template.md` (keep the bold-wrapped
headings and the underscore rule verbatim, they form the PDF title block). What
differs is the scenario-driven body. Every recovery plan body uses the NIST
800-34 three-phase structure; see `standards-index.md`.

Throughout, replace `<Organization>` with the org name and fill the bracketed
placeholders. Where you lack a real value (an RTO, a contact, an alternate site),
flag the gap for the user rather than inventing it. Keep Revision History last on
every document.

---

## 1. Recovery plan skeleton (DRP / ISCP / COOP)

The three-phase structure is the core. This is what a well-formed Disaster
Recovery Plan looks like.

```markdown
# <Plan Name>

## **<Plan Name>**

#### **<Organization>**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### **Purpose**

This plan establishes the procedures to recover <Organization> following a
disruption resulting from <scenario>. It is maintained by the <owner role>.

### **Background**

The following objectives have been established for this plan:

* Maximize the effectiveness of contingency operations through an established
  plan that consists of the following phases:
  + **Notification/Activation phase** to detect and assess damage and to
    activate the plan.
  + **Recovery phase** to restore temporary operations and recover damage done
    to the original system.
  + **Reconstitution phase** to restore system processing capabilities to
    normal operations.
* Identify the activities, resources, and procedures needed during prolonged
  interruptions to normal operations.
* Assign responsibilities to designated personnel and provide guidance for
  recovering during prolonged interruptions.

### **Roles and Responsibilities**

This plan is maintained by the <owner role>. <Statement of who is informed of a
contingency event.>

#### **Line of Succession**

<The order of succession that keeps decision-making authority uninterrupted.
Name the primary authority, what they are responsible for, and the named
successor if the primary is unable to act.>

#### **Response Teams and Responsibilities**

<Each response team, what it is responsible for, and the named team lead. For
example: DevOps is responsible for the cloud applications and supporting
infrastructure; the team lead is the Head of Engineering.>

<Team members must maintain local/offline copies of the contact roster and this
plan in case normal systems or Internet access are unavailable during a
disaster.>

### **Recovery Objectives**

<Organization> maintains the following recovery targets for critical systems,
derived from the Business Impact Analysis:

* **Recovery Time Objective (RTO): <value>.** The maximum acceptable time to
  restore operations after a disruption.
* **Recovery Point Objective (RPO): <value>.** The maximum acceptable data loss
  measured in time (aligned with the backup interval).

### **System Categorization**

<Organization> defines two categories of systems for recovery:

* **Critical Systems.** <Definition; these must be restored, or restoration
  begun, immediately upon becoming unavailable.>
* **Non-critical Systems.** <Definition; restored at a lower priority.>

### **Testing and Maintenance**

The <owner role> shall establish criteria for testing this plan, an annual test
schedule, and ensure the test is performed. At a minimum the plan shall be tested
annually. Test types include tabletop and technical exercises. <State the
maintenance/review cadence.>

### **Disaster Recovery Procedures**

#### **Notification and Activation Phase**

<The initial actions to detect and assess damage. The notification sequence: who
is notified first, who declares, and the activation criteria, for example
"systems will be unavailable for more than 48 hours".>

#### **Recovery Phase**

<The ordered procedures for recovering at the alternate capability, per team.
Number the steps; note where steps can run in parallel.>

#### **Reconstitution Phase**

<The activities to restore operations at the original or new permanent site,
validate, transition back, and deactivate the plan.>

### **Revision History**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Version** | **Date** | **Editor** | **Approver** | **Description of Changes** | **Format** |
| 1.0 | <YYYY-MM-DD> | <Editor name> | <Approver name> | Initial version | Electronic |
```

---

## 2. Business Continuity Plan skeleton (BCP)

Broader than the DRP. The BCP sustains essential business processes; it
references and hands off to the DRP for IT recovery.

```markdown
### **Purpose**          (recover the organization following a disruption, in
                          conjunction with the Disaster Recovery Plan)
### **Policy**           (the high-level continuity requirements: a documented
                          plan exists, it is tested at least annually, security
                          controls are maintained at primary and alternate sites)
### **Roles and Responsibilities**
###   #### **Line of Succession**
###   #### **Response Teams and Responsibilities**
### **Work Site Recovery**        (where people work when a facility is down)
### **Application Service Event Recovery**   (status page, customer comms)
### **Revision History**
```

---

## 3. Incident Response Plan skeleton (IRP)

Match the lifecycle the program already uses. Below is the legacy four-phase
model (NIST 800-61 Rev 2); for a CSF 2.0 program, organize the procedures under
Govern / Identify / Protect / Detect / Respond / Recover instead (see
`standards-index.md`).

```markdown
### **Purpose**
### **Scope**
### **Background**       (definitions: information security incident, event,
                          vulnerability)
### **Roles and Responsibilities**
### **Policy**           (reporting obligations, evidence preservation,
                          timelines)
### **Procedure For Establishing Incident Response System**   (Preparation:
                          on-call, notification channel, sponsors, training)
### **Procedure For Executing Incident Response**             (Detection and
                          Analysis; Containment, Eradication, and Recovery:
                          notify, assess severity, contain, preserve evidence,
                          communicate, resolve)
###   <Severity levels: High / Medium / Low, each defined.>
### **Post-Incident Activity**   (post-mortem, root-cause analysis, lessons
                          learned)
### **Revision History**
```

---

## 4. Business Impact Analysis skeleton (BIA)

The BIA is the input that grounds every plan's recovery objectives. It is an
analysis, not a playbook.

```markdown
### **Purpose**         (identify critical processes and derive recovery
                         objectives that the continuity and recovery plans must
                         meet)
### **Scope**
### **Methodology**     (how processes were identified, how impact was scored
                         over time, who was consulted)
### **Critical Process Inventory**

| **Process** | **Owner** | **Impact of disruption (over time)** | **Dependencies** | **MTD** | **RTO** | **RPO** |
| --- | --- | --- | --- | --- | --- | --- |
| <process> | <role> | <financial / operational / reputational / regulatory impact, escalating over hours/days> | <systems, vendors, people> | <value> | <value> | <value> |

### **Recovery Prioritization**   (the order in which processes are recovered,
                         derived from the impacts and MTDs above)
### **Resource Requirements**     (the people, systems, sites, and vendors each
                         critical process needs to recover)
### **Revision History**
```

The recovery objectives in this table are exactly the numbers the DRP and BCP
must honor. If a plan states an RTO, this is where it comes from.

---

## 5. Procedure / runbook skeleton

The repeatable "how" for a recurring operational task. Same title block and
Revision History; body is numbered steps with an owner and trigger per step.

```markdown
### **Purpose**         (what this procedure operationalizes and which policy or
                         plan it supports)
### **Scope**
### **Roles and Responsibilities**
### **Procedure**

#### **<Phase or step group>**

1. <Step, naming the responsible role and the trigger or cadence: "Daily", "On
   detection", "Within 24 hours of declaration".>
2. <Step, with the verification: how the operator confirms the step succeeded.>

### **Review**          (the cadence at which this procedure is tested/reviewed)
### **Revision History**
```

---

## 6. Filled mini-example (shows the tone and the structure)

This is a Notification and Activation phase written the way it should read:
ordered, owned, specific, with concrete activation criteria.

```markdown
#### **Notification and Activation Phase**

This phase addresses the initial actions taken to detect and assess damage
inflicted by a disruption. Based on the assessment of the event, sometimes
according to the Incident Response Plan, this plan may be activated by the
Security Officer and/or CTO.

***Notification Sequence***

1. The first responder must notify the CTO. All known information must be
   relayed to the CTO.
2. The CTO must contact the response team, inform them of the event, and begin
   assessment procedures.
3. The CTO must direct team members to complete the damage assessment to
   determine the extent of damage and the estimated recovery time.

***Activation Criteria***

This plan must be activated if one or more of the following criteria are met:

* Critical systems will be unavailable for more than 48 hours.
* The hosting facility is damaged and will be unavailable for more than 24 hours.

Upon activation, the CTO must notify team leads, who must notify their teams, and
must notify executive leadership of the general status of the event. Notification
may be delivered by message, email, or phone.
```

Note how every step names the actor, the action, and the trigger; the activation
criteria are concrete thresholds, not "a major outage"; and there are no em
dashes, no slop, and no rhetorical flourish. The recovery numbers it depends on
(RTO, RPO) would trace to the BIA, not to this document.
