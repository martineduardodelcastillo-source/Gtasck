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
    ("Technical Manager (Geosciences)", "Alan McKeon", "Expat", "Expat", "Fixed", "GREEN — Confirmed", 180000, 12000, "Yes", "PU Technical Manager", "Initial PU secondee. Approved family relocation to Maracaibo; housing and home leave from M7."),
    ("Reservoir Engineer", "JJI", "Local", "Local", "Fixed / Remote", "AMBER — Assumption", 120000, 12000, "No", "—", "Remote designation and local benefit treatment remain subject to confirmation."),
    ("Rig Company Man", "Marcelo Dantas", "Expat", "Expat", "Rotation", "AMBER — Assumption", 180000, 12000, "No", "—", "Rotation is confirmed; expatriate contract treatment remains subject to confirmation."),
    ("Planning & PMO", "Jose Miguel", "Local", "Local", "Fixed", "GREEN — Confirmed", 48000, 8000, "No", "—", "Local / staff-house approach; no cash housing allowance modeled."),
    ("Operations Support", "TBD — Person to be defined", "TBD", "TBD", "TBD", "RED — TBD", 48000, 8000, "No", "—", "Open role; salary and health care are budget placeholders. Contract and benefits remain TBD."),
    ("Infrastructure Manager", "Martin Aguero", "PU Secondment", "PU Secondment", "Fixed", "AMBER — Benefits TBD", 180000, 0, "Yes", "PU Infra Manager", "PU-paid salary known from prior secondments model; health, housing, home leave and other benefits remain TBD."),
]

PROFILE_START = 38
PROFILE_END = PROFILE_START + len(PEOPLE) - 1
PROFILE_TOTAL = PROFILE_END + 1
MONTHLY_START = 52
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
    ws.merge_cells("C3:Q3")
    ws["C3"] = "Petrourdaneta — Manpower Cost Summary, PU Allocation and Contract Packages"
    ws["C3"].fill = PatternFill("solid", fgColor=DARK_GREEN)
    ws["C3"].font = Font(name="Arial", size=16, bold=True, color=WHITE)
    ws["C3"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[3].height = 25
    ws.merge_cells("C5:Q5")
    ws["C5"] = "Single-sheet executive model | Monthly and annual manpower cost | COO excluded and treated separately | USD"
    ws["C5"].font = Font(name="Arial", size=11, bold=True, color=BLACK)
    ws.merge_cells("C6:Q6")
    ws["C6"] = "Blue = hardcoded input | Black = formula | Traffic-light status distinguishes confirmed, assumption and TBD records"
    ws["C6"].font = Font(name="Arial", size=9, italic=True, color="666666")

    ws.merge_cells("C8:Q9")
    ws["C8"] = (
        "BIG NOTE — Alexander Stulme (PU General Manager), Alan McKeon (PU Technical Manager) and Martin Aguero (PU Infra Manager) are initially seconded to Petrourdaneta. "
        "PU pays their costs. The model includes all manpower in gross cost and then deducts PU-paid secondees to calculate net manpower cost. Martin Aguero's $180,000 annual salary is included; his benefits remain TBD. "
        "Planning tax assumption: repatriates becoming local pay individual income tax in their country of origin; no company tax gross-up or double-taxation cost is modeled. Expat tax support is excluded unless separately approved."
    )
    ws["C8"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C8"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C8"].comment = management_note("Tax, payroll, labor-law and residence treatment require legal and tax review before implementation.")
    ws.row_dimensions[8].height = 50

    # Assumptions
    section(ws, 11, "EDITABLE ASSUMPTIONS AND POLICY INPUTS", 3, 7)
    table_header(ws, 12, ["Input", "Value", "Unit", "Application", "Source / Policy Note"], 3)
    assumptions = [
        ("Repatriation package multiple", 1.50, "x monthly salary", "M7 — Juan, Alexander and Félix", "One-time moving, settling-in, temporary lodging, transport and onboarding package."),
        ("Alan housing allowance", 2000, "USD / month", "M7–M12 — family relocation to Maracaibo", "Minimum $2,000/month for future approved family relocation to Maracaibo unless management approves more."),
        ("Alan home leave / trip", 6000, "USD / trip", "M7+ — two trips", "Two home leaves are scheduled in M9 and M12."),
        ("Alan home leave trip 1 month", 9, "Month", "M9", "Editable planning month; must be M7–M12."),
        ("Alan home leave trip 2 month", 12, "Month", "M12", "Editable planning month; must be M7–M12."),
        ("Martin Aguero annual salary", 180000, "USD / year", "PU-paid secondment M1–M12", "Known annual salary from prior secondments model; Martin benefits are not included."),
    ]
    for row, (label, value, unit, application, explanation) in enumerate(assumptions, start=13):
        set_input(ws.cell(row, 3), label, management_note(explanation))
        cell_note = prior_model_note(explanation) if label.startswith("Martin") else management_note(explanation)
        set_input(ws.cell(row, 4), value, cell_note)
        ws.cell(row, 4).number_format = MULTIPLE if row == 13 else (CURRENCY if row in (14, 15, 18) else '#,##0')
        set_input(ws.cell(row, 5), unit, management_note(unit))
        set_input(ws.cell(row, 6), application, management_note(application))
        set_input(ws.cell(row, 7), explanation, management_note(explanation))
        for col in range(3, 8):
            ws.cell(row, col).alignment = Alignment(horizontal="right" if col == 4 else "left", vertical="center", wrap_text=True)
        ws.row_dimensions[row].height = 28
    outline(ws, 12, 18, 3, 7)

    # Executive gross-to-net cost overview
    section(ws, 21, "EXECUTIVE MANPOWER COST OVERVIEW — GROSS, PU-PAID AND NET", 3, 16)
    month_headers = ["Metric", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Year 1"]
    table_header(ws, 22, month_headers, 3, warning_cols=(10,))
    overview_rows = [
        ("Gross manpower cost before PU allocation", "Includes the eight modeled positions plus Martin Aguero's known salary."),
        ("Less: PU-paid secondees", "Alexander, Alan and Martin Aguero are paid by PU and therefore deducted."),
        ("NET manpower cost after PU allocation", "Overall manpower cost remaining after the PU allocation."),
    ]
    for row, (label, explanation) in enumerate(overview_rows, start=23):
        ws.cell(row, 3, label).font = Font(name="Arial", size=10, bold=(row == 25), color=BLACK)
        for month in range(1, 13):
            summary_col = 3 + month  # D:O
            detail_col = 4 + month   # E:P in monthly table
            detail_letter = get_column_letter(detail_col)
            if row == 23:
                formula = f"=SUM({detail_letter}{MONTHLY_START}:{detail_letter}{MONTHLY_END})"
            elif row == 24:
                formula = f"=-SUMIF($D${MONTHLY_START}:$D${MONTHLY_END},\"Yes\",{detail_letter}${MONTHLY_START}:{detail_letter}${MONTHLY_END})"
            else:
                formula = f"={get_column_letter(summary_col)}23+{get_column_letter(summary_col)}24"
            set_formula(ws.cell(row, summary_col), formula, currency_formula_format(row == 23 and month == 1))
            ws.cell(row, summary_col).alignment = Alignment(horizontal="right", vertical="center")
        if row == 23:
            annual_formula = f"=SUM(Q{MONTHLY_START}:Q{MONTHLY_END})"
        elif row == 24:
            annual_formula = f"=-SUMIF($D${MONTHLY_START}:$D${MONTHLY_END},\"Yes\",$Q${MONTHLY_START}:$Q${MONTHLY_END})"
        else:
            annual_formula = "=P23+P24"
        set_formula(ws.cell(row, 16), annual_formula, CURRENCY)
        ws.cell(row, 16).alignment = Alignment(horizontal="right", vertical="center")
        ws.row_dimensions[row].height = 23
    outline(ws, 22, 25, 3, 16)
    for col in range(3, 17):
        ws.cell(25, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))

    # Key output table
    section(ws, 28, "KEY OUTPUTS", 3, 5)
    table_header(ws, 29, ["KPI", "Amount", "Meaning"], 3)
    kpis = [
        ("M1–M6 net monthly manpower cost", "=D25", "Cost after PU-paid secondments."),
        ("M7 net manpower cost", "=J25", "Includes repatriation package and Alan's M7 housing."),
        ("M9 / M12 net manpower cost", "=L25", "Alan home leave is fully paid by PU, so the net cost remains steady."),
        ("Gross Year 1 manpower cost", "=P23", "Includes all modeled manpower, including Martin's known salary."),
        ("PU-paid secondments", "=-P24", "Alexander and Alan's modeled cost plus Martin's salary."),
        ("Net Year 1 manpower cost", "=P25", "Overall Year 1 manpower cost after the PU allocation."),
    ]
    for row, (label, formula, explanation) in enumerate(kpis, start=30):
        ws.cell(row, 3, label).font = Font(name="Arial", size=10, bold=(row == 35), color=BLACK)
        set_formula(ws.cell(row, 4), formula, currency_formula_format(row == 30))
        ws.cell(row, 4).alignment = Alignment(horizontal="right", vertical="center")
        ws.cell(row, 5, explanation).font = Font(name="Arial", size=10, color=BLACK)
        ws.cell(row, 5).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    outline(ws, 29, 35, 3, 5)

    # Profile and benefit table
    section(ws, 36, "PERSONNEL, CONTRACTS AND BENEFITS", 3, 17)
    profile_headers = [
        "#", "Position", "Person", "M1–M6 Contract", "M7+ Basis", "Work Arrangement", "Traffic-Light Status",
        "Annual Base Salary", "Monthly Salary", "Health Care / Year", "M7 One-Time Package", "Housing / Month", "Home Leave / Trip", "PU-Paid?", "PU Appointment / Scope",
    ]
    table_header(ws, 37, profile_headers, 3)
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
            set_formula(ws.cell(row, 10), "=$D$18", CURRENCY)
        else:
            set_input(ws.cell(row, 10), annual_salary, source_note("Base Salary (Annual)", explanation))
            ws.cell(row, 10).number_format = currency_formula_format(row == PROFILE_START)
        set_formula(ws.cell(row, 11), f"=J{row}/12", currency_formula_format(row == PROFILE_START))
        set_input(ws.cell(row, 12), annual_health, management_note("Annual health care from source compensation table. Martin benefits remain TBD."))
        ws.cell(row, 12).number_format = CURRENCY
        set_formula(ws.cell(row, 13), f'=IF(F{row}="Repatriate",$D$13*K{row},0)', CURRENCY)
        set_formula(ws.cell(row, 14), f'=IF(E{row}="Alan McKeon",$D$14,0)', CURRENCY)
        set_formula(ws.cell(row, 15), f'=IF(E{row}="Alan McKeon",$D$15,0)', CURRENCY)
        set_input(ws.cell(row, 16), pu_paid, management_note("PU pays cost for the initial secondees: Alexander, Alan and Martin."))
        set_input(ws.cell(row, 17), pu_scope, management_note(explanation))
        for col in range(3, 18):
            ws.cell(row, col).alignment = Alignment(
                horizontal="right" if col in (10, 11, 12, 13, 14, 15) else "left",
                vertical="center",
                wrap_text=col in (4, 5, 6, 7, 8, 9, 17),
            )
        ws.row_dimensions[row].height = 34
    ws.merge_cells(start_row=PROFILE_TOTAL, start_column=3, end_row=PROFILE_TOTAL, end_column=9)
    ws.cell(PROFILE_TOTAL, 3, "TOTAL GROSS BASE, HEALTH AND M7 BENEFIT INPUTS")
    ws.cell(PROFILE_TOTAL, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    for col in range(10, 16):
        letter = get_column_letter(col)
        set_formula(ws.cell(PROFILE_TOTAL, col), f"=SUM({letter}{PROFILE_START}:{letter}{PROFILE_END})", currency_formula_format(col == 10))
        ws.cell(PROFILE_TOTAL, col).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(PROFILE_TOTAL, 16, "PU allocation shown above")
    ws.cell(PROFILE_TOTAL, 17, "Use monthly table below for total gross and net manpower costs")
    for col in range(3, 18):
        ws.cell(PROFILE_TOTAL, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    outline(ws, 37, PROFILE_TOTAL, 3, 17)

    # Monthly costs by person
    section(ws, 50, "MONTHLY MANPOWER COST BY PERSON — COSTS INCLUDE SALARY, HEALTH AND APPROVED BENEFITS", 3, 17)
    monthly_headers = ["Person", "PU-Paid?", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Year 1 Cost"]
    table_header(ws, 51, monthly_headers, 3, warning_cols=(11,))
    for row, profile_row in enumerate(range(PROFILE_START, PROFILE_END + 1), start=MONTHLY_START):
        set_formula(ws.cell(row, 3), f"=E{profile_row}")
        set_formula(ws.cell(row, 4), f"=P{profile_row}")
        for month, col in enumerate(range(5, 17), start=1):
            if month <= 6:
                formula = f"=$K${profile_row}+$L${profile_row}/12"
            elif month == 7:
                formula = f"=$K${profile_row}+$L${profile_row}/12+$M${profile_row}+$N${profile_row}"
            else:
                formula = (
                    f"=$K${profile_row}+$L${profile_row}/12+$N${profile_row}"
                    f"+IF({month}=$D$16,$O${profile_row},0)+IF({month}=$D$17,$O${profile_row},0)"
                )
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
    outline(ws, 51, MONTHLY_TOTAL, 3, 17)
    ws.conditional_formatting.add(f"Q{MONTHLY_START}:Q{MONTHLY_END}", DataBarRule(start_type="min", end_type="max", color=DARK_GREEN))

    # Closing policy note
    ws.merge_cells("C64:Q66")
    ws["C64"] = (
        "Cost scope and policy: M1–M6 includes salary plus health care. Repatriates receive the one-time M7 transition package. From M7, Alan's approved family relocation package includes $2,000/month housing in Maracaibo and two $6,000 home leaves planned in M9 and M12. "
        "For any future approved family relocation to Maracaibo, model at least $2,000/month housing. Housing, social charges, statutory benefits, transport and tax costs outside the stated assumptions require separate approval and specialist review."
    )
    ws["C64"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C64"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C64"].comment = management_note("This management planning model is not a legal, tax, payroll or immigration determination.")
    ws.row_dimensions[64].height = 42

    # Layout and print configuration
    widths = {
        "C": 8, "D": 32, "E": 26, "F": 17, "G": 18, "H": 18, "I": 20,
        "J": 16, "K": 15, "L": 16, "M": 18, "N": 16, "O": 16, "P": 14, "Q": 28,
    }
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    ws.freeze_panes = "E52"
    ws.auto_filter.ref = f"C51:Q{MONTHLY_END}"
    ws.row_breaks.append(Break(id=49))
    ws.print_area = "B2:Q66"
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
    assert ws["D13"].value == 1.50
    assert ws["D14"].value == 2000
    assert ws["D15"].value == 6000
    assert ws["D18"].value == 180000
    assert ws["E39"].value == "Alexander Stulme"
    assert ws["E41"].value == "Alan McKeon"
    assert ws["E46"].value == "Martin Aguero"
    assert ws["P39"].value == "Yes"
    assert ws["P41"].value == "Yes"
    assert ws["P46"].value == "Yes"
    assert ws["M38"].value == '=IF(F38="Repatriate",$D$13*K38,0)'
    assert ws["N41"].value == '=IF(E41="Alan McKeon",$D$14,0)'
    assert ws["O41"].value == '=IF(E41="Alan McKeon",$D$15,0)'
    assert ws["E52"].value == "=$K$38+$L$38/12"
    assert ws["K52"].value == "=$K$38+$L$38/12+$M$38+$N$38"
    assert ws["M55"].value == "=$K$41+$L$41/12+$N$41+IF(9=$D$16,$O$41,0)+IF(9=$D$17,$O$41,0)"
    assert ws["D23"].value == "=SUM(E52:E60)"
    assert ws["D24"].value == '=-SUMIF($D$52:$D$60,"Yes",E$52:E$60)'
    assert ws["D25"].value == "=D23+D24"
    assert ws["P23"].value == "=SUM(Q52:Q60)"
    assert ws["P24"].value == '=-SUMIF($D$52:$D$60,"Yes",$Q$52:$Q$60)'
    assert ws["P25"].value == "=P23+P24"
    print("VALIDATED: one worksheet | gross includes Martin | PU allocation deducted once | monthly and annual net costs calculated")


if __name__ == "__main__":
    build()
    validate()
