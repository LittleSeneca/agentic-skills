---
name: policy-writing
description: >
  Draft, rewrite, or review formal governance, risk, and compliance (GRC)
  policies and charters so they are consistent in format and voice: information
  security policies and the charters that establish governance bodies and
  responsibilities. Use this skill whenever the user wants to write a new policy
  or charter, revise an existing one, fix the formatting or tone of one, add a
  section to a policy or charter, or bring it in line with the rest of a policy
  set. It owns the Information Security Program (ISP) house format (title block,
  standard section order, roles and revision-history tables) and a plain
  professional writing style with hard rules (no em dashes, no AI slop, no
  personal-voice tics) that the whole GRC document set shares. This skill covers
  policies and charters only. For the operational documents that get executed
  under pressure (business continuity, disaster recovery, and incident response
  plans, COOP, the Business Impact Analysis, and the procedures and runbooks
  that operationalize a policy), hand off to the dedicated process-writing skill;
  for measurable, testable controls, hand off to control-writing. Reach for this
  skill even when the user does not say "policy" by name but is clearly producing
  a policy or charter destined for governance/docs.
---

# Policy Writing

You are helping write GRC documents that have to read as one consistent set:
every policy in the same skeleton, every sentence in the same calm
professional register. Auditors, customers, and investors read these
side by side. Drift in format or tone makes the whole program look sloppy, so
consistency is the product here, not prose flair.

This skill works for any GRC program. The source of truth for a given program
is its governance docs directory, commonly `governance/docs/` in a security
repo. Before drafting anything, read two or three existing documents in that
folder that are closest to what you are writing, so the new document inherits
real phrasing, defined terms, and named roles rather than invented ones. If no
policy set exists yet, the canonical format below is a safe starting skeleton.

## Decide what you are writing first

This skill writes two GRC document shapes, policies and charters. The third
bullet below is a related shape it does not write but should recognize and route
to the right skill. Pick the right one before you write a line, because the
structure follows from it.

- **Policy** — states *what* the organization requires and why. High level,
  durable, role-and-rule oriented. Files end in `_policy`. Most requests are
  this. Uses the full canonical skeleton below.
- **Charter** — establishes a body or responsibility (board, advisory board,
  oversight of internal control). Same title block; body covers purpose,
  authority, membership, responsibilities, meeting cadence.
- **Procedure / Process / Plan** — the operational *how*: step-by-step
  procedures and runbooks (files end in `_process`), and scenario playbooks like
  Business Continuity, Disaster Recovery, Incident Response, and Configuration
  Management (files end in `_plan`), plus the Business Impact Analysis that
  grounds their recovery objectives. **Hand these off to the `process-writing`
  skill**, the specialist for operational documents. It carries the
  contingency-planning backbone (NIST SP 800-34, ISO 22301, NIST SP 800-61) and
  the operability checks (named owner, line of succession, activation trigger,
  BIA-grounded RTO/RPO, testing) that a plan needs and a policy does not. These
  documents share this skill's house format and voice, so if `process-writing`
  is not available, reuse the title block and Revision History conventions from
  `references/policy-template.md` and follow the same plain professional voice.

This skill does not write procedures, processes, or operational plans (Business
Continuity, Disaster Recovery, Incident Response, Configuration Management).
Those state the step-by-step *how* or a scenario playbook, not the *what*. Hand
them to the `process-writing` skill rather than forcing them into the policy
format. If the request is ambiguous (for example "write something for backups"),
ask one short question: is this a policy (the rule, which this skill writes) or a
procedure or plan (the steps, which `process-writing` writes)? Do not guess
across that line.

## The canonical format (ISP house style)

This is a common, audit-friendly ISP policy format and it exports cleanly to
PDF. Match it exactly. The bold-wrapped headings and the underscore rule are
intentional: they render as a title block on the PDF cover. Do not "clean them
up" into plain markdown headings.

```markdown
# <Document Name>

## **<Document Name>**

#### **<Organization>**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### **Purpose**

### **Scope**

### **Background**          (optional; include when the "why" needs context)

### **Roles and Responsibilities**

### **Policy**

#### **<Subsection>**
#### **<Subsection>**

### **Revision History**
```

Rules that keep the set consistent:

- **Section order is fixed**: Purpose, Scope, (Background), Roles and
  Responsibilities, Policy, then any document-specific sections, then Revision
  History last. Every document ends with Revision History.
- **Section headings are `### **Bold**`**. Subsections inside the body are
  `#### **Bold**`. The H1 is the plain document name; the H2 repeats it bold.
- **Write "Roles and Responsibilities"** (the spelled-out "and", not `&`) for
  consistency across the set.
- The underscore rule is a literal run of escaped underscores (`\_`). Copy it
  verbatim from `references/policy-template.md` rather than retyping it.

The exact skeleton, the standard two tables, and a filled mini-example live in
`references/policy-template.md`. Read it before drafting and copy from it.

### The two standard tables

**Roles and Responsibilities** is a two-column table. A near-universal default
is:

| **Role** | **Responsibility** |
| --- | --- |
| Security Officer | Annual review and updates |
| Privacy Officer | Approval |

Add document-specific roles below these when the policy assigns real duties to
others (for example "System Owner", "Incident Commander"). Do not invent roles
that the body never references. If the program names these roles differently,
match its names.

**Revision History** is the closing table on every document:

| **Version** | **Date** | **Editor** | **Approver** | **Description of Changes** | **Format** |
| --- | --- | --- | --- | --- | --- |
| 1.0 | YYYY-MM-DD | <name> | <name> | Initial version | Electronic |

When revising an existing document, append a row; never rewrite history. Bump
the version (1.0 to 1.1 for edits, to 2.0 for a rewrite), use today's date in
ISO format, set Editor to the person doing the work, and write a Description
that names what changed ("Refined the For Customers section", not "Updated").
Leave the Approver to be filled at sign-off unless the user tells you who it is.

## How it should read: the writing style

Write these in a plain professional register: the calm, verifiable voice of a
competent compliance professional. A policy is the opposite of an essay. Lead
with what the requirement *is* and state it in calm, full sentences. The hard
rules below are non-negotiable because they keep every document in the set
sounding like one author.

**Hard rules (never break):**

1. **No em dashes (`—`) and no en dashes (`–`) as punctuation.** Not one. When
   you want the pause a dash gives, end the sentence with a period and start a
   new one, use a comma, use parentheses, or use a colon. A plain hyphen in a
   range ("12-month", "1.0-1.1") is fine.
2. **No AI slop vocabulary.** Avoid delve, robust, seamless, leverage (verb),
   elevate, foster, myriad, crucial, vital, pivotal, "navigating the X", "X
   landscape", "ever-evolving", "in today's X world", "it is worth noting", "in
   conclusion". These are the tells that make a document read like it was
   generated. Use plain words instead.
3. **No personal-voice tics.** A control document is not a blog post. Do not
   define a thing by what it is not, do not use anaphora or repeated sentence
   openers for rhythm, do not drop one-line thesis fragments for drama, do not
   ask rhetorical questions, and do not use profanity, politics, or metaphor.
   Say what the requirement is, plainly, and move on.

**How a policy should sound:**

- **Normative and direct.** Use "must" for hard requirements, "should" for
  recommended practice, "may" for permitted options. Be consistent. Most policy
  lines use "must".
- **Full sentences of normal length**, standard paragraphs, ordinary
  transitions (Additionally, However, When required). Bullet lists and tables
  are good and encouraged for requirements and enumerations.
- **Specific and verifiable.** Name the real tool, the real interval, the real
  algorithm ("rotate keys at least once every 12 months", a named password
  manager, "AES-256"). A control that cannot be audited is not a control. Pull
  these specifics from existing docs or ask; do not invent a number to fill a
  gap.
- **Defined terms stay consistent** with the rest of the program. If the set
  already says "secret authentication information", "sensitive data", "PII", or
  "information security program", use those exact terms rather than synonyms.
- **Third person, organizational voice.** "The organization must..." or "All
  employees must...", not "we" or "you" (except where an existing acceptable-use
  style document already addresses the reader directly).

`references/house-style.md` has the full do/don't list with before-and-after
rewrites. Read it when the tone of a draft feels off or when you are revising
someone else's prose into house style.

## Workflow

1. **Identify the document type** (policy or charter) and the organization.
2. **Read the neighbors.** Open the two or three closest existing documents in
   the program's `governance/docs/` (or the relevant repo). Borrow their
   structure, defined terms, role names, and phrasing. This is the single
   biggest lever for consistency.
3. **Draft from the template.** Start from `references/policy-template.md`,
   keep the section order, fill Purpose and Scope first (they are formulaic and
   set the frame), then the Policy body.
4. **Make every requirement specific and auditable.** Where you lack a real
   value (an interval, a tool, an owner), flag it for the user rather than
   inventing it.
5. **Add the tables.** Roles and Responsibilities near the top, Revision
   History last. For a revision, append a row and bump the version.
6. **Run the self-check below** before handing it back.
7. **PDF export.** If the program generates PDFs from these markdown sources
   with an export script, regenerate via that script rather than hand-editing
   the exported files. Mention it; run it only if asked.

## Self-check before returning

- Search the text for `—` and `–`. If you find any, remove them. This is the
  most common failure.
- Scan for AI slop words and replace each with a plain word.
- Confirm the section order: Purpose, Scope, (Background), Roles and
  Responsibilities, Policy, document-specific sections, Revision History last.
- Confirm headings use the `### **Bold**` / `#### **Bold**` convention and the
  title block (`## **Name**`, `#### **Org**`, underscore rule) is present.
- Confirm "must / should / may" are used deliberately and consistently.
- Confirm requirements are specific and auditable, with no invented numbers
  silently filling gaps (flag gaps instead).
- Confirm Revision History exists, with a sane version, ISO date, and a
  Description that says what actually changed.
- Read it once as an auditor would: could someone test compliance against each
  statement? If a line cannot be tested, tighten it.

A good GRC document reads like a competent, level-headed compliance
professional wrote it, and like it belongs in the same binder as every other
policy in the program. Plain, consistent, and verifiable beats clever every
time.
