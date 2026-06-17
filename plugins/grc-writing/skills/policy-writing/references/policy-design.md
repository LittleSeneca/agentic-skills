# Policy Design — GRC Best Practices and the Push-Back Catalog

A policy is a mandatory, durable statement of *what* the organization requires
and *why*, approved by an authority with the standing to mandate it, written so
that compliance can be measured. That definition is the whole job. Everything
below exists to either build a policy that meets it or to reject one that does
not.

The rule that pairs this skill with its two siblings: **do not write good copy
for an unenforceable policy.** A clean, well-formatted policy that has no owner,
no defined scope, no enforceable requirement, or that nobody has read since the
architecture changed, is worse than no policy. It passes review, anchors an
audit it cannot survive, and erodes trust in the whole program. When a requested
policy fails the tests below, name the failure, fix the design, and only then
polish the wording. This push-back is the value of the skill, exactly as it is in
`control-writing` and `process-writing`.

## The governance document hierarchy — get the altitude right

The most common policy defect is altitude: a "policy" that is really a procedure,
or a policy stuffed with volatile detail that forces constant re-approval. Keep
the five document types straight, because the structure and durability follow
from which one you are writing.

| Type | What it is | Mandatory? | Altitude | Durability | Answers |
| --- | --- | --- | --- | --- | --- |
| **Policy** | A formal, mandatory statement of objective and intent that governs behavior. | Yes | Strategic | High; reviewed roughly annually | *What* and *why* |
| **Standard** | The specific, measurable, mandatory requirements that satisfy a policy. | Yes | Tactical | Medium; changes as technology changes | *What, specifically* |
| **Procedure** | The step-by-step "how" for carrying out a control or policy. | The steps are | Operational | Low; changes often | *How* |
| **Guideline** | A recommended, non-mandatory course of action. | No | Advisory | Medium | *How, suggested* |
| **Baseline** | The minimum mandatory configuration for a platform or system. | Yes (the minimum) | Tactical | Low to medium | *Minimum required* |

Worked example, same topic (authentication):

- **Policy:** "All accounts must be authenticated, and all internet-exposed
  accounts must use multi-factor authentication."
- **Standard:** "Passwords must be at least 12 characters with three character
  classes; MFA must use an authenticator app or hardware key, not SMS."
- **Baseline:** "MFA is enforced on every production host per the platform
  hardening baseline."
- **Procedure:** "To reset a password: verify identity through the help desk,
  then follow the self-service portal steps 1 to 4."
- **Guideline:** "Prefer a passphrase of four or more unrelated words."

The lever for durability: a policy says *internet-exposed accounts must use MFA*;
it does not name the exact authenticator product or the precise character count.
Push volatile specifics down to a standard so the policy survives a tool change
without re-approval. `process-writing` owns the procedure; `control-writing` owns
the testable safeguard. This skill writes the policy (and, when asked, the
standard and guideline, which sit in the same rule-stating family). The line that
matters: if the request is the executable *how* under pressure, it is a process;
if it is the *testable safeguard that proves enforcement*, it is a control.

NIST SP 800-12 cuts a complementary axis by policy altitude: **program policy**
(establishes the security program), **issue-specific policy** (one area of
concern, which is what most named ISP policies are), and **system-specific
policy** (one system). The master ISP is the program policy; the topic-specific
policies are issue-specific.

## What makes a policy good — the seven tests

Run every policy against these. A policy that fails any of the first four is not
ready; a policy that fails the last three is a design problem to raise with the
owner.

1. **Purposeful and scoped.** It states a clear objective and names exactly what
   and who it covers, including explicit exclusions. Without a defined scope,
   enforcement is guesswork.
2. **Enforceable and auditable.** Every requirement is backed by a control that
   makes compliance measurable, and is written so an assessor can tell pass from
   fail. Aspirational language an auditor cannot test is not a policy
   requirement.
3. **Owned and approved.** A named role owns the policy, and an authority with
   the standing to mandate it has approved it. ISO 27001 Clause 5.2 requires
   top-management approval of the information security policy. "IT" is not an
   owner.
4. **Right altitude.** It states *what* and *why* and pushes the *how* to
   procedures and the volatile specifics to standards, so it stays durable. A
   policy that needs editing every quarter is at the wrong altitude.
5. **Risk- and framework-aligned.** It is driven by the organization's real risk
   profile, not a generic template, and it maps to the frameworks it earns credit
   against (see `frameworks-index.md`).
6. **Maintained.** It has a defined review cadence (at least annually, or on
   significant change) and a revision history that proves the cadence is honored.
7. **Consistent and non-contradictory.** It uses the program's defined terms and
   role names, references its sibling documents, and does not contradict another
   policy in the set.

## The policy lifecycle

A policy is a living document, not a one-time artifact. The cycle: **draft,
review, approve, publish and communicate, acknowledge, enforce, periodically
review, then update or retire.**

- **Approval authority.** Top management must approve and visibly back the
  policy; approval authority scales with the risk the policy governs. ISO 27001
  Clause 5.2 makes management approval of the information security policy
  explicit.
- **Review cadence.** Review at planned intervals, **at least annually or when
  significant change occurs.** State the cadence in the document and record each
  review in the revision history.
- **Version control.** Maintain a revision history (version, date, editor,
  approver, description of what changed) so the current authoritative version is
  unambiguous. Append rows; never rewrite history.
- **Exception and waiver process.** A real policy has a documented route to
  request, approve, time-box, and review deviations. Hallmarks: the exception is
  approved by an authority matched to the risk; it is time-bounded (a maximum of
  one year is the common default) and renewed only on review; the residual risk
  is accepted explicitly by the owner; compensating controls and a remediation
  date are recorded. Without an exception path, users quietly ignore impractical
  requirements and the policy becomes fiction.
- **Enforcement and consequences.** Define what a violation is and the
  proportionate sanctions, and apply them consistently. The standard line is
  "Violations may result in disciplinary action, up to and including termination
  of employment or contract."
- **Communication and acknowledgment.** Distribute the policy to the population
  it binds and capture acknowledgment. An unread policy is unenforceable.
- **Retirement.** Superseded policies are archived with a dated record, not
  silently deleted, and removed from force.

## Normative language conventions

Policies are tested against their normative verbs, so use them deliberately.

- **must / shall / required** = an absolute requirement. The default for policy
  lines and the verb auditors test against.
- **must not / shall not** = an absolute prohibition.
- **should / recommended** = a strong default; deviation is allowed with
  understood, documented justification.
- **may / optional** = a permitted, discretionary option.

RFC 2119 (with RFC 8174) is the canonical reference. Two conventions worth
applying:

- **Use the requirement verbs sparingly.** Reserve "must" for genuine
  requirements. Over-using it dilutes the word and creates requirements nobody can
  meet.
- **Prefer "must" over "shall."** They are normatively identical, but
  plain-language and legal-drafting guidance treats "shall" as ambiguous (it gets
  used to mean must, should, will, and may) while "must" is unambiguously
  obligatory. Pick one obligation verb, state the convention once, and apply it
  consistently. Some ISO-aligned programs use "shall"; match the program rather
  than fighting it.

## Standard policy structure and why each section earns its place

| Section | Why it matters |
| --- | --- |
| Title block (name, organization, version) | Identifies the authoritative current version; supports version control and PDF export. |
| Purpose | States the objective and rationale; frames everything below. |
| Scope | Defines covered systems, data, and people, and the exclusions; without it, enforcement is guesswork. |
| Roles and Responsibilities | Assigns accountability; no named role means no execution. |
| Policy (statements) | The binding requirements, where the must/should language lives. |
| Enforcement (optional) | Defines violations and proportionate sanctions; makes the policy enforceable. |
| Exceptions (optional) | A controlled alternative to silent non-compliance. |
| References (optional) | Links to laws, frameworks, and sibling documents; prevents contradiction and shows alignment. |
| Revision History | Proves the review cadence and keeps changes traceable. |

The fixed section order and the two standard tables live in
`policy-template.md`. This list is the rationale behind that template.

## The push-back catalog — bad-policy smells and what to do

When a requested policy trips one of these, do not just reword it. Name the
problem, then fix the design or recommend the missing prerequisite. Each entry
gives the smell and the move.

1. **Unenforceable, aspirational language.** "Employees will always act
   securely", "data will be protected at all times".
   → Rewrite each requirement so a control can prove it and a sanction can attach
   to it. If no control can exist, it is not a policy requirement.
2. **Procedure dressed as a policy.** Step-by-step instructions, tool click-paths,
   or runbook detail in the policy body.
   → Lift the steps into a procedure (`process-writing`) and keep the policy at the
   *what and why* altitude. The policy says backups are tested quarterly; the
   procedure says how.
3. **Too detailed, brittle.** Hardcoded product names, exact config values, and
   thresholds that change every quarter.
   → Push the volatile specifics down to a standard or baseline so the policy
   stays durable and does not need constant re-approval.
4. **No owner.** No named role accountable for the policy or its enforcement.
   → Assign a single accountable owner and a named approver. An unowned policy is
   the first finding.
5. **Stale, never reviewed.** The policy references systems, roles, or tools that
   no longer exist.
   → Reconcile against current reality, set a review cadence (at least annually),
   and record the review. A policy that confidently names a decommissioned system
   is worse than none.
6. **Vague, unauditable requirement.** "Strong passwords", "access is
   appropriate", "reviewed regularly".
   → Replace with a measurable criterion, threshold, or cadence, or flag the gap
   for the owner. "Reviewed regularly" becomes "reviewed at least quarterly".
7. **Contradicts another policy.** Two documents impose conflicting requirements
   on the same subject.
   → Reconcile during review and cross-reference the sibling documents so the set
   is coherent.
8. **Shelfware written only to pass an audit.** A policy that exists on paper but
   is not practiced, communicated, or acknowledged.
   → Tie it to operating controls and acknowledgment, or be honest that the
   capability does not yet exist. Passing an audit with a policy nobody follows is
   a liability that surfaces at the worst time.
9. **Copy-pasted template, not tailored.** A generic policy that ignores the
   organization's real environment and risk.
   → Tailor it to the actual systems, roles, and risk profile. As soon as a
   generic policy is adopted, the program discovers how much of its reality
   already violates it; reconcile the gaps before publishing.
10. **No scope or scope creep.** The policy tries to cover everything, or never
    says what it covers.
    → Define the covered systems, data, and people and the explicit exclusions.
11. **Control or test dressed as a policy.** "Confirm quarterly that backups
    restore" (a control) submitted as a policy.
    → Route the testable safeguard to `control-writing`. The policy states the
    requirement; the control proves it; this skill does not write the test.
12. **No exception path.** A rigid requirement with no documented way to request a
    time-boxed deviation.
    → Add an exception process (authority matched to risk, time-bounded, risk
    accepted, compensating control recorded), so non-compliance is controlled
    rather than silent.

When you reject or redesign a policy, give the verdict first ("This is not an
enforceable policy because its central requirement cannot be tested and it has no
owner"), then the corrected version or the missing prerequisite. Be willing to
conclude that the right next step is "this belongs in a standard, not the policy"
or "this is the control's job, not the policy's".

## Using the frameworks

`frameworks-index.md` is the authoritative source of which policies a program
needs and what each must address. Use it as the objective and the skeleton, not
as copy to paste.

- **Treat the framework requirement as the objective, not the wording.** ISO
  27001 5.1 tells you a topic-specific policy should exist for access control;
  800-53 AC-1 tells you what that policy must address. Translate both into the
  organization's voice, roles, and intervals.
- **Find the gaps, then write to them.** Map the program's policies against the
  canonical set and the ISO 27002 5.1 list before drafting. The missing policy in
  a real risk area is more valuable than a cleaner version of an existing one.
- **Earn credit once.** One well-written policy maps to ISO 27001 Annex A, a CSF
  GV.PO subcategory, an 800-53 `xx-1` control, and one or more SOC 2 Common
  Criteria. Record the mappings so it is not an orphan.

The frameworks are a reference for what a complete, well-formed policy set looks
like, not a record of capability. A policy is real only when it is owned,
approved, communicated, enforceable, and maintained.
