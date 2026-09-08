from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.pagebreak import Break

BASE = Path(__file__).resolve().parent
OUT = BASE / "manpower_cost_summary_single_sheet.xlsx"
SOURCE_IMAGE = "/home/ubuntu/upload/pasted_file_yfFQ2v_image.png"
SOURCE_DATE = "7 September 2026"

DARK_GREEN = "135B44"
LIGHT_GREEN = "CFE9E0"
WHITE = "FFFFFF"
BLACK = "000000"
BLUE = "0000FF"
GRID = "B7B7B7"
STATUS_GREEN = "E8F5E9"
STATUS_AMBER = "FFF3E0"
STATUS_RED = "FFCCBC"
CURRENCY_FIRST = '$#,##0.0;[Red]($#,##0.0);-'
CURRENCY = '#,##0.0;[Red]($#,##0.0);-'
MULTIPLE = '0.00x'

# position, person, M1-M6 contract, M7+ basis, arrangement, status, annual salary, annual health, PU-paid, PU appointment, note
PEOPLE = [
    ("EPCM & Engineering Manager", "Juan Conde", "Repatriate", "Local — Venezuela", "Fixed", "GREEN — Confirmed", 216000, 12000, "No", "—", "One-time M7 transition package. Origin-country employee tax assumption; no company gross-up modeled."),
    ("Drilling & Well Services Manager", "Alexander Stulme", "Repatriate", "Local — Venezuela", "Fixed", "GREEN — Confirmed", 180000, 12000, "Yes", "PU General Manager", "Initial PU secondee. PU pays modeled cost; one-time M7 transition package applies."),
    ("Operations & Maintenance Manager", "Félix Valderrama", "Repatriate", "Local — Venezuela", "Fixed", "GREEN — Confirmed", 216000, 12000, "No", "—", "One-time M7 transition package. Origin-country employee tax assumption; no company gross-up modeled."),
    ("Technical Manager (Geosciences)", "Alan McKeon", "Expat", "Expat", "Fixed", "GREEN — Confirmed", 180000, 12000, "Yes", "PU Technical Manager", "Initial PU secondee. Approved family relocation to Maracaibo; housing from M7 and home leave stated as a non-costed benefit."),
    ("Reservoir Engineer", "JJI", "Local", "Local", "Fixed / Remote", "AMBER — Assumption", 120000, 12000, "No", "—", "Remote designation and local benefit treatment remain subject to confirmation."),
    ("Rig Company Man", "Marcelo Dantas", "Expat", "Expat", "Rotation", "AMBER — Assumption", 180000, 12000, "No", "—", "Rotation is confirmed; expatriate contract treatment remains subject to confirmation."),
    ("Planning & PMO", "Jose Miguel", "Local", "Local", "Fixed", "GREEN — Confirmed", 48000, 8000, "No", "—", "Local / staff-house approach; no cash housing allowance modeled."),
    ("Operations Support", "TBD — Person to be defined", "TBD", "TBD", "TBD", "RED — TBD", 48000, 8000, "No", "—", "Open role; salary and health care are budget placeholders. Contract and benefits remain TBD."),
    ("Infrastructure Manager", "Martin Aguero", "Local Secondee", "Local", "Fixed", "GREEN — Confirmed", 180000, 12000, "Yes", "PU Infra Manager", "Already assigned to the project as a local secondee. PU pays salary and health care; 30 paid vacation days apply."),
]

PROFILE_START = 29
PROFILE_END = PROFILE_START + len(PEOPLE) - 1
PROFILE_TOTAL = PROFILE_END + 1
MONTHLY_START = 43
MONTHLY_END = MONTHLY_START + len(PEOPLE) - 1
MONTHLY_TOTAL = MONTHLY_END + 1


# ---------- Style and audit helpers ----------
def note(text):
    return Comment(text, "Manus")


def source_note(field, detail=""):
    return note(f"Source: compensation table image {Path(SOURCE_IMAGE).name}, provided {SOURCE_DATE}; field: {field}. {detail}".strip())


def management_note(detail):
    return note(f"Source: management instruction in this task through {SOURCE_DATE}. {detail}")


def prior_model_note(detail):
    return note(
        "Source: existing workbook modelo_paquetes_personal_2_etapas.xlsx, worksheet Secondments PU, reviewed 7 September 2026. "
        + detail
    )


def set_input(cell, value, cell_note):
    cell.value = value
    cell.font = Font(name="Arial", size=10, color=BLUE)
    cell.comment = cell_note


def set_formula(cell, formula, number_format=None):
    cell.value = formula
    cell.font = Font(name="Arial", size=10, color=BLACK)
    if number_format:
        cell.number_format = number_format


def table_header(ws, row, labels, start_col=3, warning_cols=()):
    for col, label in enumerate(labels, start=start_col):
        cell = ws.cell(row, col, label)
        cell.fill = PatternFill("solid", fgColor="FFF3E0" if col in warning_cols else LIGHT_GREEN)
        cell.font = Font(name="Arial", size=10, bold=True, color=BLACK)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(bottom=Side(style="medium", color=DARK_GREEN))
    ws.row_dimensions[row].height = 34


def section(ws, row, label, start_col, end_col):
    ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
    cell = ws.cell(row, start_col, label)
    cell.fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    cell.font = Font(name="Arial", size=10, bold=True, color=BLACK)
    cell.alignment = Alignment(horizontal="left", vertical="center")


def outline(ws, first_row, last_row, first_col, last_col):
    for row in range(first_row, last_row + 1):
        for col in range(first_col, last_col + 1):
            cell = ws.cell(row, col)
            cell.border = Border(
                left=Side(style="thin", color=GRID) if col == first_col else Side(style=None),
                right=Side(style="thin", color=GRID) if col == last_col else Side(style=None),
                top=Side(style="thin", color=GRID),
                bottom=Side(style="thin", color=GRID),
            )


def status_fill(status):
    if status.startswith("GREEN"):
        return STATUS_GREEN
    if status.startswith("AMBER"):
        return STATUS_AMBER
    return STATUS_RED


def currency_formula_format(first=False):
    return CURRENCY_FIRST if first else CURRENCY


# ---------- Build workbook ----------
def build():
    wb = Workbook()
    ws = wb.active
    ws.title = "Manpower Cost Summary"
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 20

    # Header
    ws.merge_cells("C3:R3")
    ws["C3"] = "Petrourdaneta — Manpower Cost Summary, PU Allocation and Contract Packages"
    ws["C3"].fill = PatternFill("solid", fgColor=DARK_GREEN)
    ws["C3"].font = Font(name="Arial", size=16, bold=True, color=WHITE)
    ws["C3"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[3].height = 25
    ws.merge_cells("C5:R5")
    ws["C5"] = "Single-sheet executive model | Monthly and annual manpower cost | COO excluded and treated separately | USD"
    ws["C5"].font = Font(name="Arial", size=11, bold=True, color=BLACK)
    ws.merge_cells("C6:R6")
    ws["C6"] = "Blue = hardcoded input | Black = formula | Traffic-light status distinguishes confirmed, assumption and TBD records"
    ws["C6"].font = Font(name="Arial", size=9, italic=True, color="666666")

    ws.merge_cells("C8:R9")
    ws["C8"] = (
        "BIG NOTE — Alexander Stulme (PU General Manager), Alan McKeon (PU Technical Manager) and Martin Aguero (PU Infra Manager) are initially seconded to Petrourdaneta. "
        "PU pays their costs. The model includes all manpower in gross cost and then deducts PU-paid secondees to calculate net manpower cost. Martin Aguero is already assigned to the project as a local secondee; his salary, health care and 30 paid vacation days are included. "
        "Planning tax assumption: repatriates becoming local pay individual income tax in their country of origin; no company tax gross-up or double-taxation cost is modeled. Expat tax support is excluded unless separately approved."
    )
    ws["C8"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C8"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C8"].comment = management_note("Tax, payroll, labor-law and residence treatment require legal and tax review before implementation.")
    ws.row_dimensions[8].height = 50

    # Executive gross-to-net cost overview
    section(ws, 11, "EXECUTIVE MANPOWER COST OVERVIEW — GROSS, PU-PAID AND NET", 3, 16)
    month_headers = ["Metric", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Year 1"]
    table_header(ws, 12, month_headers, 3, warning_cols=(10,))
    overview_rows = [
        ("Gross manpower cost before PU allocation", "Includes the eight modeled positions plus Martin Aguero's local secondee salary and health care."),
        ("Less: PU-paid secondees", "Alexander, Alan and Martin Aguero are paid by PU and therefore deducted."),
        ("NET manpower cost after PU allocation", "Overall manpower cost remaining after the PU allocation."),
    ]
    for row, (label, explanation) in enumerate(overview_rows, start=13):
        ws.cell(row, 3, label).font = Font(name="Arial", size=10, bold=(row == 15), color=BLACK)
        for month in range(1, 13):
            summary_col = 3 + month  # D:O
            detail_col = 4 + month   # E:P in monthly table
            detail_letter = get_column_letter(detail_col)
            if row == 13:
                formula = f"=SUM({detail_letter}{MONTHLY_START}:{detail_letter}{MONTHLY_END})"
            elif row == 14:
                formula = f"=-SUMIF($D${MONTHLY_START}:$D${MONTHLY_END},\"Yes\",{detail_letter}${MONTHLY_START}:{detail_letter}${MONTHLY_END})"
            else:
                formula = f"={get_column_letter(summary_col)}13+{get_column_letter(summary_col)}14"
            set_formula(ws.cell(row, summary_col), formula, currency_formula_format(row == 23 and month == 1))
            ws.cell(row, summary_col).alignment = Alignment(horizontal="right", vertical="center")
        if row == 13:
            annual_formula = f"=SUM(Q{MONTHLY_START}:Q{MONTHLY_END})"
        elif row == 14:
            annual_formula = f"=-SUMIF($D${MONTHLY_START}:$D${MONTHLY_END},\"Yes\",$Q${MONTHLY_START}:$Q${MONTHLY_END})"
        else:
            annual_formula = "=P13+P14"
        set_formula(ws.cell(row, 16), annual_formula, CURRENCY)
        ws.cell(row, 16).alignment = Alignment(horizontal="right", vertical="center")
        ws.row_dimensions[row].height = 23
    outline(ws, 12, 15, 3, 16)
    for col in range(3, 17):
        ws.cell(15, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))

    # Key output table
    section(ws, 18, "KEY OUTPUTS", 3, 5)
    table_header(ws, 19, ["KPI", "Amount", "Meaning"], 3)
    kpis = [
        ("M1–M6 net monthly manpower cost", "=D15", "Cost after PU-paid secondees."),
        ("M7 net manpower cost", "=J15", "Includes repatriation package and Alan's M7 housing."),
        ("M8–M12 net monthly manpower cost", "=K15", "Salary, health care and Alan's housing; home leave is stated but not costed."),
        ("Gross Year 1 manpower cost", "=P13", "Includes all modeled manpower, including Martin's local secondee package."),
        ("PU-paid secondees", "=-P14", "Alexander and Alan's modeled cost plus Martin's salary and health care."),
        ("Net Year 1 manpower cost", "=P15", "Overall Year 1 manpower cost after the PU allocation."),
    ]
    for row, (label, formula, explanation) in enumerate(kpis, start=20):
        ws.cell(row, 3, label).font = Font(name="Arial", size=10, bold=(row == 25), color=BLACK)
        set_formula(ws.cell(row, 4), formula, currency_formula_format(row == 20))
        ws.cell(row, 4).alignment = Alignment(horizontal="right", vertical="center")
        ws.cell(row, 5, explanation).font = Font(name="Arial", size=10, color=BLACK)
        ws.cell(row, 5).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    outline(ws, 19, 25, 3, 5)

    # Profile and benefit table
    section(ws, 27, "PERSONNEL, CONTRACTS AND BENEFITS", 3, 18)
    profile_headers = [
        "#", "Position", "Person", "M1–M6 Contract", "M7+ Basis", "Work Arrangement", "Traffic-Light Status",
        "Annual Base Salary", "Monthly Salary", "Health Care / Year", "M7 One-Time Package", "Housing / Month", "Home Leave", "Local Paid Vacation / Days", "PU-Paid?", "PU Appointment / Scope",
    ]
    table_header(ws, PROFILE_START - 1, profile_headers, 3)
    for row, record in enumerate(PEOPLE, start=PROFILE_START):
        position, person, contract, basis, arrangement, status, annual_salary, annual_health, pu_paid, pu_scope, explanation = record
        set_input(ws.cell(row, 3), row - PROFILE_START + 1, source_note("row number"))
        set_input(ws.cell(row, 4), position, source_note("Position"))
        person_note = prior_model_note(explanation) if person == "Martin Aguero" else (management_note(explanation) if "TBD" in person else source_note("Person"))
        set_input(ws.cell(row, 5), person, person_note)
        set_input(ws.cell(row, 6), contract, management_note(f"M1–M6 contract: {contract}"))
        set_input(ws.cell(row, 7), basis, management_note(f"M7+ basis: {basis}"))
        set_input(ws.cell(row, 8), arrangement, management_note(f"Work arrangement: {arrangement}"))
        set_input(ws.cell(row, 9), status, management_note(f"Status: {status}. {explanation}"))
        ws.cell(row, 9).fill = PatternFill("solid", fgColor=status_fill(status))
        if person == "Martin Aguero":
            set_formula(ws.cell(row, 10), "=180000", CURRENCY)
        else:
            set_input(ws.cell(row, 10), annual_salary, source_note("Base Salary (Annual)", explanation))
            ws.cell(row, 10).number_format = currency_formula_format(row == PROFILE_START)
        set_formula(ws.cell(row, 11), f"=J{row}/12", currency_formula_format(row == PROFILE_START))
        set_input(ws.cell(row, 12), annual_health, management_note("Annual health care from source compensation table. Martin receives the same health-care treatment as all employees."))
        ws.cell(row, 12).number_format = CURRENCY
        set_formula(ws.cell(row, 13), f'=IF(F{row}="Repatriate",1.5*K{row},0)', CURRENCY)
        set_formula(ws.cell(row, 14), f'=IF(E{row}="Alan McKeon",2000,0)', CURRENCY)
        set_formula(ws.cell(row, 15), f'=IF(E{row}="Alan McKeon","Home leave","—")')
        set_formula(ws.cell(row, 16), f'=IF(OR(G{row}="Local — Venezuela",G{row}="Local"),30,0)', '#,##0')
        set_input(ws.cell(row, 17), pu_paid, management_note("PU pays cost for the initial secondees: Alexander, Alan and Martin."))
        set_input(ws.cell(row, 18), pu_scope, management_note(explanation))
        for col in range(3, 19):
            ws.cell(row, col).alignment = Alignment(
                horizontal="right" if col in (10, 11, 12, 13, 14, 16) else "left",
                vertical="center",
                wrap_text=col in (4, 5, 6, 7, 8, 9, 15, 18),
            )
        ws.row_dimensions[row].height = 34
    ws.merge_cells(start_row=PROFILE_TOTAL, start_column=3, end_row=PROFILE_TOTAL, end_column=9)
    ws.cell(PROFILE_TOTAL, 3, "TOTAL GROSS BASE, HEALTH AND M7 BENEFIT INPUTS")
    ws.cell(PROFILE_TOTAL, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    for col in range(10, 15):
        letter = get_column_letter(col)
        set_formula(ws.cell(PROFILE_TOTAL, col), f"=SUM({letter}{PROFILE_START}:{letter}{PROFILE_END})", currency_formula_format(col == 10))
        ws.cell(PROFILE_TOTAL, col).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(PROFILE_TOTAL, 15, "Home leave stated; no cost")
    set_formula(ws.cell(PROFILE_TOTAL, 16), f"=SUM(P{PROFILE_START}:P{PROFILE_END})", '#,##0')
    ws.cell(PROFILE_TOTAL, 17, "PU allocation shown above")
    ws.cell(PROFILE_TOTAL, 18, "Use monthly table below for total gross and net manpower costs")
    for col in range(3, 19):
        ws.cell(PROFILE_TOTAL, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    outline(ws, PROFILE_START - 1, PROFILE_TOTAL, 3, 18)

    # Monthly costs by person
    section(ws, 41, "MONTHLY MANPOWER COST BY PERSON — COSTS INCLUDE SALARY, HEALTH AND APPROVED BENEFITS", 3, 17)
    monthly_headers = ["Person", "PU-Paid?", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Year 1 Cost"]
    table_header(ws, MONTHLY_START - 1, monthly_headers, 3, warning_cols=(11,))
    for row, profile_row in enumerate(range(PROFILE_START, PROFILE_END + 1), start=MONTHLY_START):
        set_formula(ws.cell(row, 3), f"=E{profile_row}")
        set_formula(ws.cell(row, 4), f"=Q{profile_row}")
        for month, col in enumerate(range(5, 17), start=1):
            if month <= 6:
                formula = f"=$K${profile_row}+$L${profile_row}/12"
            elif month == 7:
                formula = f"=$K${profile_row}+$L${profile_row}/12+$M${profile_row}+$N${profile_row}"
            else:
                formula = f"=$K${profile_row}+$L${profile_row}/12+$N${profile_row}"
            set_formula(ws.cell(row, col), formula, currency_formula_format(row == MONTHLY_START and month == 1))
            ws.cell(row, col).alignment = Alignment(horizontal="right", vertical="center")
        set_formula(ws.cell(row, 17), f"=SUM(E{row}:P{row})", currency_formula_format(row == MONTHLY_START))
        ws.cell(row, 3).alignment = Alignment(horizontal="left", vertical="center")
        ws.cell(row, 4).alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[row].height = 22
    ws.merge_cells(start_row=MONTHLY_TOTAL, start_column=3, end_row=MONTHLY_TOTAL, end_column=4)
    ws.cell(MONTHLY_TOTAL, 3, "TOTAL GROSS MANPOWER COST")
    ws.cell(MONTHLY_TOTAL, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    for col in range(5, 18):
        letter = get_column_letter(col)
        set_formula(ws.cell(MONTHLY_TOTAL, col), f"=SUM({letter}{MONTHLY_START}:{letter}{MONTHLY_END})", currency_formula_format(col == 5))
        ws.cell(MONTHLY_TOTAL, col).alignment = Alignment(horizontal="right", vertical="center")
    for col in range(3, 18):
        ws.cell(MONTHLY_TOTAL, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    ws.row_dimensions[MONTHLY_TOTAL].height = 28
    outline(ws, MONTHLY_START - 1, MONTHLY_TOTAL, 3, 17)
    ws.conditional_formatting.add(f"Q{MONTHLY_START}:Q{MONTHLY_END}", DataBarRule(start_type="min", end_type="max", color=DARK_GREEN))

    # Closing policy note
    ws.merge_cells("C54:R56")
    ws["C54"] = (
        "Cost scope and policy: health care applies to everyone. M1–M6 includes salary plus health care. Repatriates receive the one-time M7 transition package and are then local. "
        "Alan remains an expat and receives $2,000/month housing in Maracaibo from M7. Home leave is stated as a benefit but no cost is included. All local employees, including repatriates after M7, receive 30 paid vacation days; salary is assumed to cover this entitlement. Housing, social charges, statutory benefits, transport and tax costs outside the stated assumptions require separate approval and specialist review."
    )
    ws["C54"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C54"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C54"].comment = management_note("This management planning model is not a legal, tax, payroll or immigration determination.")
    ws.row_dimensions[54].height = 42

    # Layout and print configuration
    widths = {
        "C": 8, "D": 32, "E": 26, "F": 17, "G": 18, "H": 18, "I": 20,
        "J": 16, "K": 15, "L": 16, "M": 18, "N": 16, "O": 16, "P": 18, "Q": 14, "R": 28,
    }
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    ws.freeze_panes = f"E{MONTHLY_START}"
    ws.auto_filter.ref = f"C{MONTHLY_START - 1}:Q{MONTHLY_END}"
    ws.row_breaks.append(Break(id=40))
    ws.print_area = "B2:R56"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.center.text = "Manpower Cost Summary | Page &P of &N"
    ws.oddFooter.center.size = 8

    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    wb.save(OUT)
    print(OUT)


def validate():
    wb = load_workbook(OUT, data_only=False)
    assert wb.sheetnames == ["Manpower Cost Summary"]
    ws = wb.active
    assert ws["C3"].value.startswith("Petrourdaneta")
    assert ws["E30"].value == "Alexander Stulme"
    assert ws["E32"].value == "Alan McKeon"
    assert ws["E37"].value == "Martin Aguero"
    assert ws["F37"].value == "Local Secondee"
    assert ws["G37"].value == "Local"
    assert ws["Q30"].value == "Yes"
    assert ws["Q32"].value == "Yes"
    assert ws["Q37"].value == "Yes"
    assert ws["M29"].value == '=IF(F29="Repatriate",1.5*K29,0)'
    assert ws["N32"].value == '=IF(E32="Alan McKeon",2000,0)'
    assert ws["O32"].value == '=IF(E32="Alan McKeon","Home leave","—")'
    assert ws["P29"].value == '=IF(OR(G29="Local — Venezuela",G29="Local"),30,0)'
    assert ws["P37"].value == '=IF(OR(G37="Local — Venezuela",G37="Local"),30,0)'
    assert ws["E43"].value == "=$K$29+$L$29/12"
    assert ws["K43"].value == "=$K$29+$L$29/12+$M$29+$N$29"
    assert ws["M46"].value == "=$K$32+$L$32/12+$N$32"
    assert ws["D13"].value == "=SUM(E43:E51)"
    assert ws["D14"].value == '=-SUMIF($D$43:$D$51,"Yes",E$43:E$51)'
    assert ws["D15"].value == "=D13+D14"
    assert ws["P13"].value == "=SUM(Q43:Q51)"
    assert ws["P14"].value == '=-SUMIF($D$43:$D$51,"Yes",$Q$43:$Q$51)'
    assert ws["P15"].value == "=P13+P14"
    print("VALIDATED: one worksheet | no editable assumptions | Martin is local PU secondee | monthly and annual net costs calculated")


if __name__ == "__main__":
    build()
    validate()
