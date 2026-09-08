# Manpower Cost History — Single-Sheet Consolidation

**As of:** 8 September 2026  
**Workbook:** `manpower_cost_summary_single_sheet.xlsx`  
**Scope:** COO excluded and treated separately. All values are in USD.

## Presentation format

The final workbook contains **one compact worksheet** designed to fit on a single Tabloid landscape page. It combines the overall cost by stage, the pending Airswift and Barbara actions and one person-by-person table. Repeated monthly columns were condensed into **M1–M6 monthly cost**, **M7 cost**, **M8–M12 monthly cost** and **Year 1 cost** so that all decision-useful information is visible together.

## Confirmed employment treatment

The first six months are modeled as international employment through Airswift with **base salary only**. The eight transition-team roles are assumed to work on a **21 days on / 14 days off** rotation. This requires two ticket legs per 35-day cycle, equivalent to **1.71 tickets per person per month** and **13.71 tickets per month** for the eight transition roles. Martin Aguero is already local and has no rotation ticket allowance.

**Ticket cost is excluded** pending Airswift confirmation of travel-booking scope and price. **Health-care cost is also excluded** pending Airswift confirmation of medical coverage, eligibility, insurer and price. Neither tickets nor health care are included in the calculated costs below.

At Month 7, Juan Conde, Alexander Stulme and Félix Valderrama receive a one-time repatriation / localization package equal to **1.5 times monthly salary** and then move to the local framework. Alan McKeon remains an expatriate and receives **$2,000/month housing** from Month 7. Home leave is stated as a benefit only and is not costed.

All local employees receive **30 paid vacation days**, with no incremental cost because salary is assumed to cover the entitlement. This applies to local employees and to repatriates after M7.

Alexander Stulme, Alan McKeon and Martin Aguero are secondees. The **net-cost calculation deducts only an indicative 60% reimbursement of their relevant base salaries**; it does not deduct 100% of their costs. The $324,000 reimbursement is a working assumption pending Barbara's confirmation of eligibility, documentation, process and any reimbursement cap.

**Martin Aguero is already part of the project as a local secondee.** His $180,000 annual salary and 30 paid vacation days are included.

## Calculated manpower cost — excluding health care and tickets

| Metric | M1–M6 | M7 | M8–M12 | Year 1 |
|---|---:|---:|---:|---:|
| Gross manpower cost | $114,000.00 | $192,500.00 | $116,000.00 | $1,456,500.00 |
| Less: indicative PU salary-share reimbursement (60% of relevant base salary) | ($27,000.00) | ($27,000.00) | ($27,000.00) | ($324,000.00) |
| **Net manpower cost** | **$87,000.00** | **$165,500.00** | **$89,000.00** | **$1,132,500.00** |

## Secondee salary-share reimbursement — working assumption

| Secondee | Relevant annual base salary | 60% provisional reimbursement | Scope |
|---|---:|---:|---|
| Alexander Stulme | $180,000.00 | $108,000.00 | Salary share only; M7 package is not reimbursed in the model |
| Alan McKeon | $180,000.00 | $108,000.00 | Salary share only; housing is not reimbursed in the model |
| Martin Aguero | $180,000.00 | $108,000.00 | Salary share only |
| **Total** | **$540,000.00** | **$324,000.00** | Pending Barbara's confirmation and any cap |

## Airswift and Barbara confirmations required

| Item | Planning assumption | Current model treatment |
|---|---|---|
| Medical coverage | Coverage, eligibility, insurer and pricing TBD | Excluded from model |
| Rotation tickets | 21 on / 14 off; 1.71 tickets per transition role per month | Tickets counted, cost excluded from model |
| Secondee reimbursement | 60% of relevant secondee base salaries | Provisional $324,000 deduction; pending Barbara's confirmation of eligibility and any cap |

## Controls

The workbook contains a single `Manpower Cost Summary` worksheet, formulas for all stage and annual calculations, source comments on hardcoded inputs, an explicit Airswift action note, a ticket count per person for M1–M6 and a 60% salary-share indicator for the secondees. Automated recalculation and value checks confirm the annual gross cost, provisional reimbursement, net cost and ticket count shown above.
