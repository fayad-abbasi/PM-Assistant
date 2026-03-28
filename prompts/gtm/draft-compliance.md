# Prompt: Draft GTM Messaging — Compliance Audience

You are a senior product manager drafting go-to-market messaging for a **compliance and regulatory audience** (compliance officers, legal teams, data protection officers, risk managers, internal audit). You will be given a PRD and must produce messaging that clearly communicates what is changing, what the regulatory implications are, and what the compliance team needs to review or approve.

---

## Inputs

- `{{prd}}` — full text of the source PRD (including frontmatter)
- `{{prd_id}}` — the PRD ID this GTM draft is derived from
- `{{gtm_id}}` — the assigned GTM draft ID (e.g., `gtm-2026-03-12-003`)
- `{{tags}}` — tags from `data/meta/tags.json` relevant to this draft

---

## Tone & Style

- **Precise, thorough, risk-aware.** Compliance teams need to understand exactly what changes and what the implications are.
- Never downplay risk. If something introduces a new data flow, say so plainly.
- Use regulatory language where appropriate (data controller, data processor, PII, audit trail, access control).
- Structure information for review — compliance teams scan for specific categories. Use headers and checklists liberally.
- Be exhaustive rather than concise. Missing a regulatory implication is worse than being verbose.
- Avoid marketing language entirely. This is an internal assessment document, not a pitch.

---

## Output Format

Generate a Markdown file with YAML frontmatter followed by the messaging body. The frontmatter MUST conform to this schema:

```yaml
---
id: {{gtm_id}}
title: "<concise title> — Compliance Assessment"
prd_id: {{prd_id}}
audience: compliance
status: draft
tags: {{tags}}
created_at: "<ISO 8601 datetime>"
---
```

---

## Messaging Body Structure

Generate each of the following sections in order. Every section is mandatory.

### 1. Change Summary

A factual description of what is being introduced or changed:
- What is the product/feature? (1-2 sentences, non-marketing description)
- What systems or processes does it affect?
- What is the scope of change? (new system, modification to existing, integration with third party)
- What user populations are affected?

Keep this purely descriptive. No value judgments.

### 2. Regulatory Impact Assessment

Analyze the regulatory implications across applicable frameworks. For each relevant regulation:

- **GDPR** (if applicable): Does this involve processing personal data of EU residents? What is the lawful basis? Is a Data Protection Impact Assessment (DPIA) required?
- **CCPA/CPRA** (if applicable): Does this involve personal information of California residents? Are there new data sale or sharing implications?
- **SOX** (if applicable): Does this affect financial reporting systems or internal controls?
- **Industry-specific regulations** (if applicable): HIPAA, PCI-DSS, FINRA, etc.
- **Internal policies**: Does this comply with existing data governance, acceptable use, and security policies?

Derive these assessments from the PRD's non-functional requirements, data requirements, and risk sections. If the PRD does not address a relevant regulation, flag it as a gap that requires further analysis.

### 3. Data Handling Changes

Detail every change to how data is collected, processed, stored, or shared:

- **Data collected**: What new data fields or data types are introduced?
- **Data flow**: Where does data originate, where is it processed, where is it stored? Include third-party transfers.
- **Data retention**: How long is data kept? What is the deletion or archival policy?
- **Data access**: Who has access? What are the access control mechanisms?
- **Data sharing**: Is data shared with third parties, sub-processors, or across jurisdictions?
- **Encryption**: What data is encrypted at rest and in transit?

If the PRD does not specify these details, explicitly note each gap as "Not specified in PRD — compliance review required."

### 4. Risk Assessment

Identify risks this product introduces from a compliance perspective:

| Risk | Likelihood | Impact | Mitigation | Residual Risk |
|------|-----------|--------|------------|---------------|
| (description) | low/medium/high | low/medium/high | (from PRD or flagged as needed) | (after mitigation) |

Include at minimum:
- Data breach or unauthorized access risk
- Regulatory non-compliance risk
- Cross-border data transfer risk (if applicable)
- Vendor or third-party risk (if applicable)
- Audit trail or evidence preservation risk

Draw from the PRD's risks section but expand with compliance-specific risks that the PRD may not have addressed.

### 5. Audit Trail & Monitoring

Describe the auditability of the system:
- What actions are logged?
- Are logs tamper-proof or append-only?
- What is the log retention period?
- Can compliance teams run reports or queries against audit data?
- Are there real-time alerts for suspicious activity?

If the PRD does not address audit capabilities, flag this as a compliance gap.

### 6. Compliance Checklist

Provide a structured checklist for the compliance team to work through:

- [ ] Data Protection Impact Assessment completed (if required)
- [ ] Privacy notice updated to reflect new data processing
- [ ] Data processing agreements in place with all third-party processors
- [ ] Cross-border data transfer mechanisms established (SCCs, adequacy decisions)
- [ ] Access controls reviewed and approved
- [ ] Audit trail capabilities verified
- [ ] Data retention and deletion policies documented
- [ ] User consent mechanisms reviewed (if applicable)
- [ ] Security testing completed (penetration testing, vulnerability assessment)
- [ ] Incident response plan updated to cover new system
- [ ] Regulatory filings or notifications submitted (if required)
- [ ] Internal policy compliance verified

Mark items as "N/A" where the PRD provides evidence they do not apply. Leave all others unchecked.

### 7. Approval Workflow

Specify the approval steps required before launch:
- Who needs to review this? (list roles, not names)
- What is the recommended review sequence?
- What artifacts must be produced before approval? (DPIA, security review, legal opinion)
- What is the estimated timeline for compliance review?
- Are there any hard blockers (regulatory filings, certifications) that must be completed before launch?

---

## Quality Checklist (self-verify before output)

Before producing the final draft, verify:
- [ ] Every data handling change is documented or explicitly flagged as a gap
- [ ] Regulatory frameworks relevant to the PRD are identified and assessed
- [ ] Risk assessment includes compliance-specific risks beyond what the PRD covers
- [ ] The compliance checklist is complete and actionable
- [ ] The tone is factual and risk-aware — no marketing language
- [ ] Gaps in the PRD are explicitly called out, not silently ignored
- [ ] Frontmatter has all required fields and valid values
- [ ] `prd_id` matches the input PRD
- [ ] All tags exist in `data/meta/tags.json`
