from pathlib import Path
from math import isclose
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
    "tickets_juan": ws["H21"].value,
    "tickets_martin": ws["H29"].value,
    "tickets_total_month": ws["H30"].value,
    "martin_year1": ws["O29"].value,
    "airswift_action": ws["I12"].value,
}
for label, value in checks.items():
    print(f"{label}={value}")

assert checks["gross_m1_m6_month"] == 114000
assert checks["pu_m1_m6_month"] == -45000
assert checks["net_m1_m6_month"] == 69000
assert checks["gross_m7"] == 192500
assert checks["pu_m7"] == -69500
assert checks["net_m7"] == 123000
assert checks["gross_m8_m12_month"] == 116000
assert checks["pu_m8_m12_month"] == -47000
assert checks["net_m8_m12_month"] == 69000
assert checks["gross_year1"] == 1456500
assert checks["pu_year1"] == -574500
assert checks["net_year1"] == 882000
assert checks["alan_housing"] == 2000
assert isclose(checks["tickets_juan"], 60 / 35, abs_tol=1e-9)
assert checks["tickets_martin"] == 0
assert isclose(checks["tickets_total_month"], 8 * 60 / 35, abs_tol=1e-9)
assert checks["martin_year1"] == 180000
assert "Health care is excluded" in checks["airswift_action"]
assert "1.71 tickets" in checks["airswift_action"]
print("CALCULATED VALUES VALIDATED")
