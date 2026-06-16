# Policy / Procedure / Plan Templates

Copy from these skeletons. The bold-wrapped headings and the underscore rule
are deliberate (they form the PDF title block). Keep them verbatim.

Throughout, replace `<Organization>` with the org name and fill the bracketed
placeholders. Keep Revision History last on every document.

---

## 1. Policy skeleton (the common case)

```markdown
# <Policy Name>

## **<Policy Name>**

#### **<Organization>**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### **Purpose**

This policy <one or two sentences: what the policy requires and the objective it
serves, for example "defines organizational requirements for ... in order to
protect the confidentiality, integrity, and availability of ...">.

### **Scope**

This policy applies to <systems / data / facilities in scope> within the scope
of <Organization>'s information security program. All employees, contractors,
part-time and temporary workers, service providers, and those employed by others
to perform work on behalf of the organization <who this binds> are subject to
this policy and must comply with it.

### **Background**

<Optional. Include when the reader needs the "why" or the standards context.
Explain the high-level objective and why a standard approach matters. Omit the
heading entirely if Purpose already covers it.>

### **Roles and Responsibilities**

|  |  |
| --- | --- |
| **Role** | **Responsibility** |
| Security Officer | Annual review and updates |
| Privacy Officer | Approval |

### **Policy**

<Lead statement that frames the requirements.>

#### **<Subsection>**

* <Requirement, normative: "must" / "should" / "may">
* <Requirement>

#### **<Subsection>**

<Requirements as prose or tables as appropriate.>

### **Enforcement**

<Optional. Many policies include a line on consequences of non-compliance, for
example: "Violations of this policy may result in disciplinary action, up to and
including termination of employment or contract.">

### **Revision History**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Version** | **Date** | **Editor** | **Approver** | **Description of Changes** | **Format** |
| 1.0 | <YYYY-MM-DD> | <Editor name> | <Approver name> | Initial version | Electronic |
```

---

## 2. Procedure / Process skeleton

Same title block and Revision History. The body is steps, owners, and triggers
instead of rules.

```markdown
# <Process Name>

## **<Process Name>**

#### **<Organization>**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### **Purpose**

<What this procedure operationalizes and which policy it supports.>

### **Scope**

<What and who the procedure covers.>

### **Roles and Responsibilities**

|  |  |
| --- | --- |
| **Role** | **Responsibility** |
| <Owner role> | <What they do in this process> |
| Security Officer | Annual review and updates |

### **Procedure**

#### **<Phase or step group>**

1. <Step, with the responsible role named.>
2. <Step, with trigger or cadence: "Daily", "On detection", "Within 24 hours".>

#### **<Phase or step group>**

1. <Step.>

### **Review**

<Cadence at which this procedure is tested or reviewed.>

### **Revision History**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Version** | **Date** | **Editor** | **Approver** | **Description of Changes** | **Format** |
| 1.0 | <YYYY-MM-DD> | <Editor name> | <Approver name> | Initial version | Electronic |
```

---

## 3. Plan skeleton (BCP / DR / IR / Config Management)

Same title block and Revision History. Body is scenario-driven.

```markdown
### **Purpose**
### **Scope**
### **Roles and Responsibilities**     (the response team and their duties)
### **<Activation / Detection>**       (what triggers the plan)
### **<Procedures>**                   (the ordered response steps)
### **<Recovery Objectives>**          (RTO / RPO for DR/BCP, where relevant)
### **<Testing>**                      (how and how often the plan is exercised)
### **Revision History**
```

---

## 4. Filled mini-example (shows the tone and the tables)

```markdown
# Removable Media Policy

## **Removable Media Policy**

#### **<Organization>**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### **Purpose**

This policy defines the requirements for the use of removable media in order to
protect the confidentiality and integrity of information stored on or
transferred by such media.

### **Scope**

This policy applies to all removable media used to store or transport
organizational information, and to all employees, contractors, and service
providers who use removable media on behalf of the organization.

### **Roles and Responsibilities**

|  |  |
| --- | --- |
| **Role** | **Responsibility** |
| Security Officer | Annual review and updates |
| Privacy Officer | Approval |

### **Policy**

* Removable media must be encrypted at rest using an approved algorithm when it
  stores sensitive data.
* Removable media must not be used to store the sole copy of any business record.
* Lost or stolen removable media must be reported to the Security Officer
  immediately.

### **Revision History**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Version** | **Date** | **Editor** | **Approver** | **Description of Changes** | **Format** |
| 1.0 | 2026-01-01 | <Editor name> | <pending> | Initial version | Electronic |
```

Note how every requirement is testable, uses "must", names a specific actor,
and contains no em dashes, no slop, and no rhetorical flourish.
