# Manpower Cost History — Single-Sheet Consolidation

**As of:** 7 September 2026  
**Workbook:** `manpower_cost_summary_single_sheet.xlsx`  
**Scope:** COO excluded and treated separately. All values are in USD.

## Reported inputs and management decisions

The source compensation table supplied in the task provided annual base salaries and annual medical-insurance budgets for eight listed roles after excluding the COO. The consolidated model adds **Martin Aguero** as a separate PU-paid Infrastructure Manager secondment with known annual base salary of **$180,000** from the previously approved secondments model. Martin's medical, housing, home-leave and other benefits remain **TBD** and are excluded from the current cost allocation.

Alexander Stulme, Alan McKeon and Martin Aguero are initial Petrourdaneta secondees whose costs are paid by **PU**. The consolidated model includes their cost in gross manpower and deducts it once as the PU-paid allocation to calculate net manpower cost.

The recurring M1–M6 cost basis is salary plus health care. Repatriates receive a one-time M7 transition package equal to **1.50x monthly salary**. Alan McKeon receives approved expatriate benefits from M7: **$2,000/month** housing for family relocation to Maracaibo, plus **two $6,000 home leaves** scheduled in M9 and M12. A future approved family relocation to Maracaibo should be modeled with minimum housing of **$2,000/month** unless management approves more.

For repatriates becoming local, the planning assumption is that the employee bears individual income tax in the country of origin. The model includes neither company tax gross-up nor double-taxation cost. Expat tax support is outside the model unless separately approved. These are management planning assumptions and require legal, payroll and tax validation before implementation.

## Calculated manpower cost

| Metric | M1–M6 | M7 | M8 / M10 / M11 | M9 / M12 | Year 1 |
|---|---:|---:|---:|---:|---:|
| Gross manpower cost | $121,333.33 | $199,833.33 | $123,333.33 | $129,333.33 | $1,556,500.00 |
| Less: PU-paid secondees | ($47,000.00) | ($71,500.00) | ($49,000.00) | ($55,000.00) | ($610,500.00) |
| **Net manpower cost** | **$74,333.33** | **$128,333.33** | **$74,333.33** | **$74,333.33** | **$946,000.00** |

## PU-paid allocation by secondee

| Secondee | Role | Year 1 modeled PU-paid cost | Scope |
|---|---|---:|---|
| Alexander Stulme | PU General Manager | $214,500.00 | Salary, health care and M7 repatriation package |
| Alan McKeon | PU Technical Manager | $216,000.00 | Salary, health care, M7–M12 housing and two home leaves |
| Martin Aguero | PU Infra Manager | $180,000.00 | Salary only; benefits remain TBD |
| **Total** |  | **$610,500.00** |  |

## Controls

The workbook contains a single `Manpower Cost Summary` worksheet, formulas for all monthly and annual calculations, source comments on hardcoded inputs, and a traffic-light status column. Automated recalculation and value checks confirmed that the annual gross cost, PU-paid allocation and net cost reconcile to the values above.
