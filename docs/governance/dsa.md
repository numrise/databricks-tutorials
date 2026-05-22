# Data Sharing & Stewardship Agreements (DSA)

A **Data Sharing Agreement (DSA)** (also called a **Data Stewardship Agreement** in some organisations) is a formal contract that governs the terms under which data is shared between two or more parties. It defines who is responsible for data, how it may be used, and what obligations each party holds.

---

## Why DSAs Matter

- **Legal protection**: establishes liability and responsibilities clearly.
- **Regulatory compliance**: required or strongly recommended under GDPR, HIPAA, CCPA, and other frameworks.
- **Trust**: data consumers know exactly what they are allowed to do with data.
- **Governance**: makes data access auditable and revocable.

---

## Types

### Data Sharing Agreement

Governs the **transfer of data from one organisation (or team) to another**.

Use when:
- Sharing data with an external partner, vendor, or regulator.
- Providing data to a subsidiary or affiliate.
- Receiving data from a third-party provider.

### Data Stewardship Agreement

Defines the **responsibilities of a data steward** within an organisation for a specific data domain or dataset.

Use when:
- Assigning ownership of a data domain (e.g. "HR is the steward of employee data").
- Formalising the obligations of a data owner in a data governance programme.

---

## Key Elements of a DSA

| Section | Description |
| ------- | ----------- |
| **Parties** | Full legal names of the data provider and data recipient |
| **Purpose** | The specific, stated purpose for which the data is shared |
| **Data description** | What data is included (fields, date ranges, volume) |
| **Data classification** | Sensitivity level (Public, Internal, Confidential, Restricted) |
| **Permitted use** | Explicit list of allowed activities |
| **Prohibited use** | Activities that are explicitly forbidden |
| **Retention period** | How long the recipient may hold the data |
| **Deletion obligations** | How and when data must be deleted at end of agreement |
| **Security requirements** | Encryption, access controls, audit logging obligations |
| **Sub-processing** | Whether the recipient may share the data with third parties |
| **Breach notification** | Timelines and procedures for reporting data breaches |
| **Governing law** | Jurisdiction |
| **Term and termination** | Duration of the agreement and conditions for early termination |
| **Signatures** | Authorised signatories from each party |

---

## Data Classification Levels

Most DSAs reference a classification scheme. A common four-tier model:

| Level | Description | Examples |
| ----- | ----------- | -------- |
| **Public** | Approved for public release | Press releases, public APIs |
| **Internal** | For employees only | Internal reports, org charts |
| **Confidential** | Restricted to authorised roles | Customer PII, financial data |
| **Restricted** | Highest sensitivity; strict need-to-know | Health records, credentials |

Classification level determines the security controls required in the agreement.

---

## DSA Lifecycle

```text
1. Request       — Data consumer submits a request with stated purpose
2. Review        — Data owner and legal review the request
3. Negotiation   — Agree terms (permitted use, retention, security)
4. Approval      — Sign-off from data owner, legal, DPO if PII involved
5. Provisioning  — Access granted (Databricks GRANT, Collibra access workflow)
6. Active use    — Consumer uses data within agreed terms
7. Review/Renew  — Periodic re-certification that use is still valid
8. Termination   — Access revoked, data deleted, audit trail retained
```

---

## DSA and Technical Controls

A signed DSA should translate directly into technical controls. Mapping:

| DSA clause | Technical implementation |
| ---------- | ------------------------ |
| Permitted use: analytics only | GRANT SELECT — no MODIFY |
| Retention: 90 days | Automated Delta table lifecycle / VACUUM policy |
| PII must be masked | Column mask via Unity Catalog dynamic view |
| Access limited to team X | Databricks account group GRANT |
| Audit logging required | Databricks audit logs → Azure Monitor |
| Sub-processing prohibited | No GRANT to other principals |

---

## DSA in Collibra

Collibra Policy Manager can store and manage DSAs as governed assets:

1. Create a **Policy Domain** for agreements.
2. Create an **Agreement** asset type with fields matching the DSA elements above.
3. Attach the agreement to the relevant data assets (tables, schemas).
4. Link the agreement to the groups or users it applies to.
5. Trigger a **workflow** for approval and periodic review.
6. Use Collibra's **data access governance** module to link agreement approval to automated access provisioning.

---

## GDPR Considerations

For data involving EU residents:

- A DSA between two independent controllers is a **Data Sharing Agreement**.
- A DSA between a controller and a processor is a **Data Processing Agreement (DPA)** — required by GDPR Article 28.
- Include lawful basis for processing, data subject rights obligations, and DPA transfer mechanisms (SCCs, adequacy decision).

---

## Template Outline

```
DATA SHARING AGREEMENT

Between: [Provider Name] ("Provider")
And:     [Recipient Name] ("Recipient")
Date:    [Date]

1. Purpose
   The Provider agrees to share [describe data] for the purpose of [specific purpose].

2. Data Description
   [List fields, date range, estimated volume]

3. Permitted and Prohibited Uses
   Permitted:  [list]
   Prohibited: [list] — including onward sharing, commercial use, re-identification

4. Data Classification: [Public | Internal | Confidential | Restricted]

5. Security Requirements
   - Encryption in transit (TLS 1.2+) and at rest (AES-256)
   - Access limited to [named roles or groups]
   - Multi-factor authentication required

6. Retention and Deletion
   Data to be deleted within [X] days of [event or end date].

7. Breach Notification
   Recipient must notify Provider within 72 hours of discovering a breach.

8. Term
   This agreement is effective from [start date] to [end date], renewable by mutual consent.

Signed:
Provider: _________________________ Date: _______
Recipient: ________________________ Date: _______
```

---

## Related

- [data_usage.md](data_usage.md) — Data usage policies
- [collibra.md](collibra.md) — Managing agreements in Collibra
- [permissions.md](../databricks/permissions.md) — Implementing access controls in Unity Catalog
