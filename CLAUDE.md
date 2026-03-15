# Texas HHCS — ICF/IID & HCS Provider Economics Investigation

## Project Purpose

Data science investigation into the economics of Texas Medicaid-funded IDD (Intellectual and Developmental Disabilities) services. Focus areas:

1. **Provider economics** — How ICF/IID and HCS providers earn revenue, what their costs look like, and where the squeeze happens
2. **Wage analysis** — Why direct care worker wages are stuck at $10.60–$13/hr despite life-or-death responsibilities
3. **Legislative funding** — How HHSC budgets and Medicaid reimbursement rates have changed over the last decade
4. **Access & waitlists** — Interest list dynamics, LIDDA gatekeeping, and family navigation

## Domain Glossary

| Term | Meaning |
|------|---------|
| **ICF/IID** | Intermediate Care Facility for Individuals with Intellectual Disabilities — 24-hour supervised residential Medicaid provider |
| **HCS** | Home and Community-based Services waiver — community-based Medicaid waiver for IDD supports |
| **TxHmL** | Texas Home Living waiver — lighter-touch community waiver |
| **HHSC** | Health and Human Services Commission — Texas state agency overseeing Medicaid programs |
| **LIDDA** | Local Intellectual and Developmental Disability Authority — local gatekeepers for IDD eligibility and waiver interest lists |
| **QIDP** | Qualified Intellectual Disability Professional — required staff role in ICF/IID |
| **LOC** | Level of Care — assessment determining eligibility (LOC I, LOC VIII for ICF) |
| **GAA** | General Appropriations Act — Texas biennial budget law |
| **LBB** | Legislative Budget Board — produces rider packets and budget analysis |
| **TMHP** | Texas Medicaid & Healthcare Partnership — claims/billing portal |
| **PPP** | Paycheck Protection Program — COVID-era SBA loans (relevant for provider verification) |

## Stack

- **Python 3.12** via `uv`
- **Jupyter notebooks** for exploration and analysis
- **pandas / numpy** for data manipulation
- **matplotlib / seaborn / plotly** for visualization
- **requests / beautifulsoup4 / tabula-py** for web scraping and PDF extraction
- **ruff** for linting

## Directory Structure

```
data/raw/          — Downloaded source files (CSVs, PDFs, rate schedules)
data/processed/    — Cleaned and transformed datasets
notebooks/         — Jupyter notebooks (numbered: 01_, 02_, etc.)
src/texas_hhcs/    — Reusable Python modules
reports/           — Final outputs, charts, policy briefs
references/        — Citation index and source documentation
```

## Data Rules

1. **No PII** — Never include client-identifiable data (names, SSNs, Medicaid IDs)
2. **Cite everything** — Every factual claim must trace to:
   - A rate document or fee schedule
   - A budget line item (GAA/LBB)
   - A reputable news investigation or government report
3. **Source files go in `data/raw/`** with descriptive names
4. **Log all sources** in `references/sources.yaml` with URLs and access dates

## Key Public Data Sources

- **HHSC Provider Lookup**: hhs.texas.gov provider search
- **LBB Rider Packets**: lbb.texas.gov appropriations bills (Article II)
- **TMHP Fee Schedules**: tmhp.com rate/fee information
- **SBA PPP Data**: federalpay.org and SBA FOIA datasets
- **Texas Comptroller**: comptroller.texas.gov cash reports
- **News**: KERA News, Texas Tribune, Texas Standard, Houston Chronicle, Express-News

## Commands

```bash
uv sync                    # Install dependencies
uv run jupyter notebook    # Launch Jupyter
uv run pytest              # Run tests
uv run ruff check .        # Lint
```

## Notebook Conventions

- Name format: `##_short_description.ipynb`
- Each notebook starts with a markdown cell stating its purpose and data sources
- Import shared utilities from `src/texas_hhcs/`
- Document assumptions in markdown cells before calculation cells
