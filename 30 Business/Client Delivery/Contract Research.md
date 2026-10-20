---
title: "Contract Research"
type: research
status: draft
updated: 2026-10-20
tags: ["business", "contracts"]
verification: unverified
origin: "Untitled.md"
---

# Contract Research

Imported research of unknown provenance. The numbered citations below do not have corresponding source URLs or a bibliography.

> [!warning] Unverified research
> The legal claims and sample periods are retained from the original note. They have not been checked and are not approved contract terms.

**To ensure a balanced and mutually beneficial relationship with your clients, you must establish a clear legal and operational framework from day one.** In Malaysia, software development contracts are governed primarily by the **Contracts Act 1950**. Protecting your interest while keeping the client happy requires clear workflows for change requests, conflict resolution, and early termination.

## Contract structure

Before diving into operations, structure your client agreements using a **two-tier document system**. This keeps your legal terms separate from changing project details: [1]

- **Master Services Agreement (MSA):** Contains the overarching legal rules that rarely change (e.g., intellectual property rights, limits of liability, governing law, and dispute resolution). [1]

- **Statement of Work (SOW):** Contains project-specific elements like technical specifications, explicit pricing structures, project timelines, milestones, and precise **User Acceptance Testing (UAT)** parameters. [1, 2]

## Change control

Vague scopes and uncontrolled "scope creep" are the most common reasons software projects collapse. To mitigate this, embed a formal **Change Control Procedure (CCP)** directly into your contract. [1]

**The Ideal Change Request Flow:**

```text
[Client Requests Change] ➔ [Vendor Evaluates Impact] ➔ [Vendor Issues Change Order Form] ➔ [Mutual Sign-Off] ➔ [Work Begins]
```

1. **Submission:** The client must submit any request for features outside the original SOW in writing.

2. **Impact Assessment:** You calculate the impact of the change on the project's **cost, resource allocation, and final timeline**.

3. **The Change Order Form (COF):** You present a formal document outlining these shifts.

4. **Authorization:** No development work on the new feature begins until both parties sign the COF. If rejected, the project continues under the original SOW terms. [1, 2]

---

## Disputes

Disagreements regarding project delays, feature performance, or contract interpretations require a structured roadmap rather than immediate escalation to lawsuits. [1, 2, 3]

**Step-by-Step Escalation Protocol:**

- **Tier 1: Operational Negotiation.** The Project Managers from both sides meet within **7 business days** of a written dispute notice to attempt an amicable resolution. [1, 2]

- **Tier 2: Executive Escalation.** If unresolved, the conflict scales to the executive leadership (e.g., directors or owners) of both companies.

- **Tier 3: Mediation / Arbitration.** If executive talks fail, the contract should dictate third-party intervention. In Malaysia, it is common to stipulate **arbitration** through the **Asian International Arbitration Centre (AIAC)** based in Kuala Lumpur. [1, 2]

- **Tier 4: Courts.** For urgent interim relief or final litigation, your contract can leverage Malaysian courts, which include a specialized **Commercial and Admiralty Division (ICAD)**. [1]

_Note: Multi-tier dispute clauses are strictly recognized and treated as mandatory conditions by Malaysian courts (e.g., Juara Serata Sdn Bhd v Alpharich Sdn Bhd)_. [1, 2]

---

## Termination

Projects may end prematurely due to budget constraints, strategic pivots, or severe breakdowns in collaboration. Your contract must explicitly differentiate between two types of termination: [1]

**Termination for Convenience**

Either party can walk away without a specific fault, provided they give a required notice period (usually **30 to 60 days**).

- **Vendor Protection:** Ensure a clause states that if the client terminates for convenience, they must pay for all work completed up to the termination date, alongside any non-refundable costs or wind-down expenses you incur.

**Termination for Cause**

Occurs when one party breaches a critical term of the contract (e.g., non-payment by the client or failure to deliver functional milestones by the vendor). [1]

- **Cure Period:** Always include a **14-to-30-day "cure period"** allowing the breaching party a window to fix the issue before the contract is officially killed.

- **Ipso Facto Clause:** Include provisions for immediate termination if either party enters liquidation, bankruptcy, or insolvency.

**Off-boarding and Handover Framework**

Specify what happens to the code and data on the day of termination: [1]

- **IP Release:** Explicitly state that intellectual property or source code transfers to the client **only upon full payment** of all outstanding invoices. [1, 2]

- **Data Return:** Outline a timeline (e.g., 14 days) within which you will return the client's data securely, satisfying Malaysia's **Personal Data Protection Act (PDPA) 2010** requirements. [1, 2, 3]

---

## Contract provision checklist

| Strategy Area | Crucial Contractual Provision | Why It Matters for Vendors |
| --- | --- | --- |
| **Intellectual Property (IP)** | Explicit retention of "Background IP" (pre-existing frameworks, libraries, tools). | Prevents the client from owning your core, reusable codebase. |
| **Acceptance Criteria** | "Deemed Acceptance" clause (e.g., software is accepted if client doesn't log bugs within 10 days of delivery). | Prevents clients from withholding milestone payments indefinitely via silent delays. |
| Limitation of Liability | Cap your total financial liability to the amount paid by the client under the SOW (or a fixed 12-month trailing total). | Safeguards your business from catastrophic financial ruin if a software bug causes indirect business losses. |

## Sources

Unresolved citation markers from the original note: [1], [2], and [3]. Recover the original sources before using these claims in client documents.

## Related

- [[Client Engagement Workflow]]
- [[Business Index]]
- [[Source Review Queue]]
