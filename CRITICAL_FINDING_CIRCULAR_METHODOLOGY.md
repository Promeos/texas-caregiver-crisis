# Critical Finding: The Circular Wage Methodology

**Priority:** Integrate immediately into `METHODOLOGY.md`, `references/rate_methodology.md`, and the README's "What We Found" section.

**Date discovered:** March 15, 2026
**Source:** Texas Register, Volume 50, Number 36, September 5, 2025 — Adopted Rules for 1 TAC Chapter 355

---

## The Finding

On September 5, 2025, HHSC adopted a sweeping package of rule changes implementing Rider 23 of the 89th Legislature's General Appropriations Act (SB 1) and Senate Bill 457. During the 21-day public comment period (ending August 1, 2025), a commenter requested that HHSC use **Bureau of Labor Statistics wage classifications** or **State Supported Living Center wages** to calculate the attendant cost component — arguing these would better reflect the actual cost of the direct care workforce.

**HHSC declined.**

Their response, published in the September 5, 2025 Texas Register adoption notice:

> *"HHSC disagrees and declines to revise the rule. HHSC has long relied on a cost report based methodology to establish the methodological cost for the attendant cost components which HHSC believes is more reflective [than] other sources."*

Source: Texas Register, September 5, 2025, Adopted Rules — 1 TAC §355.7052. Full adoption notice at:
- https://www.sos.state.tx.us/texreg/archive/September52025/Adopted%20Rules/1.ADMINISTRATION.html
- PDF: https://www.sos.state.tx.us/texreg/pdf/backview/0905/0905adop.pdf

Rule text as effective September 22, 2025:
- https://texas-sos.appianportalsgov.com/rules-and-meetings?$locale=en_US&interface=VIEW_TAC_SUMMARY&queryAsDate=09%2F22%2F2025&recordId=226016

---

## Why This Matters

### The Circular Loop

HHSC's wage methodology operates as a closed feedback loop:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   1. HHSC sets attendant wage assumption                │
│      using provider cost report data                    │
│              │                                          │
│              ▼                                          │
│   2. Providers receive Medicaid rates                   │
│      based on that assumption                           │
│              │                                          │
│              ▼                                          │
│   3. Providers pay attendants as little                 │
│      as the market will bear                            │
│              │                                          │
│              ▼                                          │
│   4. Providers self-report those low wages              │
│      back to HHSC via cost reports                      │
│              │                                          │
│              ▼                                          │
│   5. HHSC uses those self-reported wages                │
│      to justify the next rate cycle                     │
│              │                                          │
│              └──────────► Back to Step 1                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

There is **no external validation signal** in this loop. The methodology references only its own outputs. An independent data source — BLS Occupational Employment and Wage Statistics — was explicitly offered as an alternative and explicitly rejected.

### What the Independent Data Shows

| Source | Wage | Type |
|--------|------|------|
| HHSC base wage assumption (pre-Sept 2025) | $10.60/hr | Self-referencing (cost report based) |
| HHSC new methodology (post-Sept 2025) | $13.00/hr | Self-referencing (cost report based) |
| BLS OEWS May 2024, SOC 31-1120, Texas | $12.19/hr | Independent, statistically validated |
| CPI-adjusted 2015→2025 equivalent | $14.38/hr | Derived from BLS CPI-U South |

The BLS data is:
- Independently collected via employer survey (not self-reported by Medicaid providers)
- Statistically validated with published confidence intervals
- Covers 314,610 workers in Texas (SOC 31-1120, May 2024)
- Updated annually
- Free, public, machine-readable

HHSC chose to use none of it.

### The Transparency Problem

The cost report data that HHSC says is "more reflective" than BLS:
- Is **not publicly available**. It is stored in STAIRS (transitioning to STEPS in 2026).
- Is **self-reported by providers** who have a direct financial interest in reporting lower attendant costs (lower reported costs = lower accountability for how Medicaid funds are spent).
- Cannot be independently verified by the public, researchers, legislators, or the workers themselves.
- Requires a formal **Texas Public Information Act request** to access, and HHSC may seek an Attorney General ruling to withhold it.

The result is that the wage assumption anchoring reimbursement for over 314,000 Texas home health and personal care aides is derived from a dataset that is not publicly available and cannot be independently verified — while a free, public, annually updated federal dataset covering the same workforce exists and was explicitly offered as an alternative.

---

## What Changed on September 1, 2025

### Rules Repealed
- **§355.112** — Attendant Compensation Rate Enhancement Program (the old Level 1-9 tiered system). Discontinued entirely.
- **§355.722** — Cost reporting methodology for HCS/TxHmL providers (replaced).
- **§355.457** — ICF/IID reimbursement methodology (replaced).
- **§§355.304, 355.306-355.308, 355.320** — Old nursing facility rate methodology sections.

### Rules Created/Amended
- **§355.7052 (NEW)** — "Attendant Cost Determination" — the new rule governing how the attendant cost component is calculated for all LTSS programs. This is the rule where HHSC codified the cost-report-based methodology and rejected BLS data.
- **§355.7051 (AMENDED)** — Retitled to "Base Wage for a Personal Attendant **before** September 1, 2025" — literally timestamping the $10.60 as a historical artifact.
- **Subchapter H title change** — From "Base Wage Requirements for Personal Attendant" to "Attendant Cost Determination."
- **§355.102 (AMENDED)** — Updated cost report training requirements for the STAIRS→STEPS transition.
- **§355.305 (NEW)** — Patient care expense ratio for nursing facilities (SB 457 — requires 80% of the medical assistant reimbursement attributable to patient care go to actual patient care expenses).
- **§355.456 (AMENDED)** — ICF/IID reimbursement methodology updates.

### Key Parameters in New Methodology
- Average attendant hourly wage assumed: **$13.00/hr**
- Payroll taxes and benefits (PTB): **14%** for community-based care, **15%** for facility-based care
- Rate Enhancement program: **Discontinued** (no more voluntary enrollment, no more tiered add-ons)
- Direct Care Spending Requirement: **Discontinued**
- Source: IL 2025-25 (Rider 23 implementation) and the September 5, 2025 adoption notice

---

## Integration Points for the Repo

### 1. METHODOLOGY.md

Add a new section titled **"The Circular Methodology Problem"** after the existing methodology description. This is the project's central finding — it elevates the analysis from "the wage is too low" to "the system that sets the wage is structurally incapable of correcting itself."

Key paragraph to integrate:

> On September 5, 2025, HHSC adopted new rule §355.7052, which governs the attendant cost component for all LTSS programs effective September 1, 2025. During the public comment period, a commenter proposed that HHSC use Bureau of Labor Statistics wage classifications or State Supported Living Center wages to better reflect the actual cost of the direct care workforce. HHSC declined, stating it "has long relied on a cost report based methodology to establish the methodological cost for the attendant cost components which HHSC believes is more reflective [than] other sources." This means the wage assumption that anchors reimbursement for over 314,000 Texas home health and personal care aides is derived exclusively from provider self-reported cost data that is not publicly available, rather than from independently validated federal labor market data that is freely accessible and updated annually.

### 2. README.md — "What We Found" Table

Add a new row:

| What | Detail | Type | Source |
|------|--------|------|--------|
| HHSC rejected BLS data for wage methodology | Declined to use independent labor market data; chose provider self-reported cost reports instead | Source | Texas Register, Sept 5, 2025, §355.7052 adoption |

### 3. references/sources.yaml

```yaml
texas_register_sept_2025_adoption:
  name: "Adopted Rules: 1 TAC Chapter 355 — Reimbursement Rates"
  url: "https://www.sos.state.tx.us/texreg/archive/September52025/Adopted%20Rules/1.ADMINISTRATION.html"
  pdf_url: "https://www.sos.state.tx.us/texreg/pdf/backview/0905/0905adop.pdf"
  accessed: "2026-03-15"
  type: adopted_rule
  effective_date: "2025-09-01"
  published_date: "2025-09-05"
  register_volume: 50
  register_number: 36
  key_sections:
    - "§355.7052 — Attendant Cost Determination (NEW)"
    - "§355.7051 — Base Wage for Personal Attendant before September 1, 2025 (AMENDED)"
    - "§355.112 — Attendant Compensation Rate Enhancement (REPEALED)"
  notes: >
    HHSC declined commenter request to use BLS wage data or State Supported Living Center wages.
    Stated preference for cost-report-based methodology. 21 comments received from 20 organizations
    during comment period ending August 1, 2025.

tac_355_7052_effective_text:
  name: "1 TAC §355.7052 — Attendant Cost Determination (as effective Sept 22, 2025)"
  url: "https://texas-sos.appianportalsgov.com/rules-and-meetings?$locale=en_US&interface=VIEW_TAC_SUMMARY&queryAsDate=09%2F22%2F2025&recordId=226016"
  accessed: "2026-03-15"
  type: administrative_rule
  notes: "TAC viewer requires JavaScript. Archive a copy of the rule text."

texas_register_july_2025_proposed:
  name: "Proposed Rules: 1 TAC Chapter 355 — Reimbursement Rates"
  url: "https://www.sos.state.tx.us/texreg/pdf/backview/0711/0711prop.pdf"
  accessed: "2026-03-15"
  type: proposed_rule
  published_date: "2025-07-11"
  register_volume: 50
  register_number: 28
  notes: "Original proposal. Comment period ended August 1, 2025."
```

### 4. references/rate_methodology.md

Add a section documenting the full rulemaking timeline:

```
## Rulemaking Timeline — Rider 23 / SB 457 Implementation

- 2025-06-11: Proposed rules published (50 TexReg, proposed)
- 2025-07-11: Formal proposal published in Texas Register (50 TexReg 3953)
- 2025-07-16: Public rate hearing held by PFD
- 2025-08-01: Comment period closed (21 comments from 20 organizations)
- 2025-09-01: Effective date for all rule changes
- 2025-09-05: Adopted rules published in Texas Register (50 TexReg, Number 36)
- 2026-early: STAIRS → STEPS transition begins for cost report submission
```

### 5. New Notebook Section or Standalone Notebook

Consider adding a section to the wage analysis notebook (or a new notebook) that:

1. **Visualizes the circular methodology** — a diagram showing the feedback loop
2. **Compares the two approaches side by side:**
   - What the BLS-based methodology would produce (using SOC 31-1120 Texas data, annually updated)
   - What the cost-report-based methodology produces (HHSC's $10.60 → $13.00)
   - The gap between them over time (2015-2025)
3. **Calculates the cumulative underpayment** — if the BLS mean had been used as the base wage since 2015 instead of $10.60, what is the total dollar difference across 314,610 workers?
4. **Shows the information asymmetry** — a table comparing data accessibility:

| Attribute | BLS OEWS | HHSC Cost Reports |
|-----------|----------|-------------------|
| Public access | Yes, free | No, requires PIA request |
| Collection method | Employer survey (independent) | Provider self-report |
| Sample size (TX) | Statistical sample → 314,610 estimate | All Medicaid providers (unknown N) |
| Update frequency | Annual | Biennial |
| Validation | Statistical methodology, published SE | HHSC desk review / field audit |
| Machine-readable | Yes (Excel/CSV from BLS) | No (locked in STAIRS/STEPS) |

### 6. VERIFICATION.md

Add a verification entry for the Texas Register finding:

```
## Circular Methodology Finding (2026-03-15)

Claim: HHSC explicitly rejected the use of BLS wage data in favor of
       provider self-reported cost report data for the attendant cost
       component methodology.

Source: Texas Register, Volume 50, Number 36, September 5, 2025
        Adopted Rules — 1 TAC §355.7052
        Comment-response section

Verification: Direct quote from published adoption notice. The comment
              requested BLS classifications or State Supported Living Center
              wages. HHSC response states preference for "cost report based
              methodology." Verified against PDF at sos.state.tx.us.

Status: VERIFIED — primary source, published by Texas Secretary of State
```

---

## Broader Implications

This finding reframes the entire project. The original thesis was: "HHSC's wage assumption is stale." The updated thesis is:

**HHSC's wage-setting methodology is structurally circular — it uses provider self-reported cost data as both the input and the justification for reimbursement rates, rejected an independently validated alternative when explicitly offered one, and does not make the underlying data available for public scrutiny.**

The $10.60 was never just a stale number. It was the output of a methodology that, by its own structure, references only its own outputs.

---

## Public Records Relevance

HHSC's stated position — that cost report data is the most reliable basis for wage methodology — underscores the public interest in accessing that data. The entire reimbursement structure for over 314,000 workers rests on data that is not currently available for independent verification. A Texas Public Information Act request for provider cost reports was submitted on March 15, 2026. See [references/tpia-request-draft.md](references/tpia-request-draft.md) for details.
