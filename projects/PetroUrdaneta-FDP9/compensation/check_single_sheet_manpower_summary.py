from pathlib import Path
from openpyxl import load_workbook

book = Path(__file__).resolve().parent / "manpower_cost_summary_single_sheet.xlsx"
wb = load_workbook(book, data_only=True)
ws = wb["Manpower Cost Summary"]

checks = {
    "gross_m1_m6_month": ws["D13"].value,
    "pu_m1_m6_month": ws["D14"].value,
    "net_m1_m6_month": ws["D15"].value,
    "gross_m7": ws["E13"].value,
    "pu_m7": ws["E14"].value,
    "net_m7": ws["E15"].value,
    "gross_m8_m12_month": ws["F13"].value,
    "pu_m8_m12_month": ws["F14"].value,
    "net_m8_m12_month": ws["F15"].value,
    "gross_year1": ws["G13"].value,
    "pu_year1": ws["G14"].value,
    "net_year1": ws["G15"].value,
    "alan_housing": ws["K24"].value,
    "martin_health_care": ws["I29"].value,
    "martin_year1": ws["O29"].value,
}
for label, value in checks.items():
    print(f"{label}={value}")

assert checks["gross_m1_m6_month"] == 122333.333333333
assert checks["pu_m1_m6_month"] == -48000
assert checks["net_m1_m6_month"] == 74333.3333333333
assert checks["gross_m7"] == 200833.333333333
assert checks["pu_m7"] == -72500
assert checks["net_m7"] == 128333.333333333
assert checks["gross_m8_m12_month"] == 124333.333333333
assert checks["pu_m8_m12_month"] == -50000
assert checks["net_m8_m12_month"] == 74333.3333333333
assert checks["gross_year1"] == 1556500
assert checks["pu_year1"] == -610500
assert checks["net_year1"] == 946000
assert checks["alan_housing"] == 2000
assert checks["martin_health_care"] == 12000
assert checks["martin_year1"] == 192000
print("CALCULATED VALUES VALIDATED")
