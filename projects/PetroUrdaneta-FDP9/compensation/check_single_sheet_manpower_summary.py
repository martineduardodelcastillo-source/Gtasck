from pathlib import Path
from openpyxl import load_workbook

book = Path(__file__).resolve().parent / "manpower_cost_summary_single_sheet.xlsx"
wb = load_workbook(book, data_only=True)
ws = wb["Manpower Cost Summary"]

checks = {
    "gross_m1": ws["D23"].value,
    "pu_m1_deduction": ws["D24"].value,
    "net_m1": ws["D25"].value,
    "gross_m7": ws["J23"].value,
    "pu_m7_deduction": ws["J24"].value,
    "net_m7": ws["J25"].value,
    "gross_m9": ws["L23"].value,
    "pu_m9_deduction": ws["L24"].value,
    "net_m9": ws["L25"].value,
    "gross_year1": ws["P23"].value,
    "pu_year1_deduction": ws["P24"].value,
    "net_year1": ws["P25"].value,
    "alan_housing": ws["N41"].value,
    "alan_home_leave": ws["O41"].value,
    "martin_year1": ws["Q60"].value,
}
for label, value in checks.items():
    print(f"{label}={value}")

assert checks["gross_m1"] == 121333.333333333
assert checks["pu_m1_deduction"] == -47000
assert checks["net_m1"] == 74333.3333333333
assert checks["gross_m7"] == 199833.333333333
assert checks["pu_m7_deduction"] == -71500
assert checks["net_m7"] == 128333.333333333
assert checks["gross_m9"] == 129333.333333333
assert checks["pu_m9_deduction"] == -55000
assert checks["net_m9"] == 74333.3333333333
assert checks["gross_year1"] == 1556500
assert checks["pu_year1_deduction"] == -610500
assert checks["net_year1"] == 946000
assert checks["alan_housing"] == 2000
assert checks["alan_home_leave"] == 6000
assert checks["martin_year1"] == 180000
print("CALCULATED VALUES VALIDATED")
