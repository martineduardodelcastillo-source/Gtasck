# Manpower Cost History — Single-Sheet Consolidation

**As of:** 8 September 2026  
**Workbook:** `manpower_cost_summary_single_sheet.xlsx`  
**Scope:** COO excluded and treated separately. All values are in USD.

## Presentation format

The final workbook contains **one compact worksheet** designed to fit on a single Tabloid landscape page. It combines the overall cost by stage, the pending Airswift actions and one person-by-person table. Repeated monthly columns were condensed into **M1–M6 monthly cost**, **M7 cost**, **M8–M12 monthly cost** and **Year 1 cost** so that all decision-useful information is visible together.

## Confirmed employment treatment

The first six months are modeled as international employment through Airswift with **base salary only**. The eight transition-team roles are assumed to work on a **21 days on / 14 days off** rotation. This requires two ticket legs per 35-day cycle, equivalent to **1.71 tickets per person per month** and **13.71 tickets per month** for the eight transition roles. Martin Aguero is already local and has no rotation ticket allowance.

**Ticket cost is excluded** pending Airswift confirmation of travel-booking scope and price. **Health-care cost is also excluded** pending Airswift confirmation of medical coverage, eligibility, insurer and price. Neither tickets nor health care are included in the calculated costs below.

At Month 7, Juan Conde, Alexander Stulme and Félix Valderrama receive a one-time repatriation / localization package equal to **1.5 times monthly salary** and then move to the local framework. Alan McKeon remains an expatriate and receives **$2,000/month housing** from Month 7. Home leave is stated as a benefit only and is not costed.

All local employees receive **30 paid vacation days**, with no incremental cost because salary is assumed to cover the entitlement. This applies to local employees and to repatriates after M7.

Alexander Stulme, Alan McKeon and Martin Aguero are secondees paid by **PU**. The workbook includes all manpower in gross cost, then deducts the PU-paid secondees once to calculate net manpower cost.

**Martin Aguero is already part of the project as a local secondee.** His $180,000 annual salary and 30 paid vacation days are included. PU pays his cost.

## Calculated manpower cost — excluding health care and tickets

| Metric | M1–M6 | M7 | M8–M12 | Year 1 |
|---|---:|---:|---:|---:|
| Gross manpower cost | $114,000.00 | $192,500.00 | $116,000.00 | $1,456,500.00 |
| Less: PU-paid secondees | ($45,000.00) | ($69,500.00) | ($47,000.00) | ($574,500.00) |
| **Net manpower cost** | **$69,000.00** | **$123,000.00** | **$69,000.00** | **$882,000.00** |

## PU-paid allocation by secondee — excluding health care and tickets

| Secondee | Role | Year 1 modeled PU-paid cost | Scope |
|---|---|---:|---|
| Alexander Stulme | PU General Manager | $202,500.00 | Salary and M7 repatriation package |
| Alan McKeon | PU Technical Manager | $192,000.00 | Salary and M7–M12 housing; home leave is not costed |
| Martin Aguero | PU Infra Manager | $180,000.00 | Local secondee salary; paid vacation is covered within salary |
| **Total** |  | **$574,500.00** |  |

## Airswift confirmations required

| Item | Planning assumption | Cost treatment until confirmed |
|---|---|---|
| Medical coverage | Coverage, eligibility, insurer and pricing TBD | Excluded from model |
| Rotation tickets | 21 on / 14 off; 1.71 tickets per transition role per month | Tickets counted, cost excluded from model |

## Controls

The workbook contains a single `Manpower Cost Summary` worksheet, formulas for all stage and annual calculations, source comments on hardcoded inputs, an explicit Airswift action note and a ticket count per person for M1–M6. Automated recalculation and value checks confirm the annual gross cost, PU-paid allocation, net cost and ticket count shown above.
