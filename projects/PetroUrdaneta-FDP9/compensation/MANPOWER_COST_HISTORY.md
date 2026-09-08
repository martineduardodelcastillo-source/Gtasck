# Manpower Cost History — Single-Sheet Consolidation

**As of:** 8 September 2026  
**Workbook:** `manpower_cost_summary_single_sheet.xlsx`  
**Scope:** COO excluded and treated separately. All values are in USD.

## Confirmed employment treatment

The workbook has **no editable assumptions section**. The policy and benefits below are the approved planning treatment built directly into the model.

The first six months are modeled as international employment through Airswift with base salary and health care. At Month 7, Juan Conde, Alexander Stulme and Félix Valderrama receive a one-time repatriation / localization package equal to **1.5 times monthly salary** and then move to the local framework. Health care applies to everyone during the full year.

Alan McKeon remains an expatriate. From Month 7, he receives **$2,000/month housing** in Maracaibo. Home leave is a stated benefit only and is not costed in the workbook.

All local employees receive **30 paid vacation days**, with no incremental cost because salary is assumed to cover the entitlement. This applies to local employees and to repatriates after M7.

Alexander Stulme, Alan McKeon and Martin Aguero are secondees paid by **PU**. The workbook includes all manpower in gross cost, then deducts the PU-paid secondees once to calculate net manpower cost.

**Martin Aguero is already part of the project as a local secondee.** His $180,000 annual salary, $12,000 health-care budget and 30 paid vacation days are included. PU pays his cost.

## Calculated manpower cost

| Metric | M1–M6 | M7 | M8–M12 | Year 1 |
|---|---:|---:|---:|---:|
| Gross manpower cost | $122,333.33 | $200,833.33 | $124,333.33 | $1,556,500.00 |
| Less: PU-paid secondees | ($48,000.00) | ($72,500.00) | ($50,000.00) | ($610,500.00) |
| **Net manpower cost** | **$74,333.33** | **$128,333.33** | **$74,333.33** | **$946,000.00** |

## PU-paid allocation by secondee

| Secondee | Role | Year 1 modeled PU-paid cost | Scope |
|---|---|---:|---|
| Alexander Stulme | PU General Manager | $214,500.00 | Salary, health care and M7 repatriation package |
| Alan McKeon | PU Technical Manager | $204,000.00 | Salary, health care and M7–M12 housing; home leave is not costed |
| Martin Aguero | PU Infra Manager | $192,000.00 | Local secondee salary, health care and 30 paid vacation days |
| **Total** |  | **$610,500.00** |  |

## Controls

The workbook contains a single `Manpower Cost Summary` worksheet, formulas for all monthly and annual calculations, source comments on hardcoded inputs, and a traffic-light status column. Automated recalculation and value checks confirm the annual gross cost, PU-paid allocation and net cost shown above.
