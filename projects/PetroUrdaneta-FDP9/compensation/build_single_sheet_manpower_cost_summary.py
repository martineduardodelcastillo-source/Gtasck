from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BASE = Path(__file__).resolve().parent
OUT = BASE / "manpower_cost_summary_single_sheet.xlsx"
SOURCE_DATE = "7–8 September 2026"

DARK_GREEN = "135B44"
LIGHT_GREEN = "CFE9E0"
WHITE = "FFFFFF"
BLACK = "000000"
BLUE = "0000FF"
GRID = "B7B7B7"
CURRENCY_FIRST = '$#,##0.0;[Red]($#,##0.0);-'
CURRENCY = '#,##0.0;[Red]($#,##0.0);-'

# Position, person, M1-M6 contract, M7+ basis, annual salary, PU-paid, scope, note
PEOPLE = [
    ("EPCM & Engineering Manager", "Juan Conde", "Repatriate", "Local — Venezuela", 216000, "No", "—", "One-time M7 transition package. Origin-country employee tax assumption; no company gross-up modeled."),
    ("Drilling & Well Services Manager", "Alexander Stulme", "Repatriate", "Local — Venezuela", 180000, "Yes", "PU General Manager", "Initial PU secondee. PU pays modeled cost; one-time M7 transition package applies."),
    ("Operations & Maintenance Manager", "Félix Valderrama", "Repatriate", "Local — Venezuela", 216000, "No", "—", "One-time M7 transition package. Origin-country employee tax assumption; no company gross-up modeled."),
    ("Technical Manager (Geosciences)", "Alan McKeon", "Expat", "Expat", 180000, "Yes", "PU Technical Manager", "Initial PU secondee. Approved family relocation to Maracaibo; $2,000/month housing from M7 and home leave stated as a non-costed benefit."),
    ("Reservoir Engineer", "JJI", "Local", "Local", 120000, "No", "—", "Remote designation and local benefit treatment remain subject to confirmation."),
    ("Rig Company Man", "Marcelo Dantas", "Expat", "Expat", 180000, "No", "—", "Rotation is confirmed; expatriate contract treatment remains subject to confirmation."),
    ("Planning & PMO", "Jose Miguel", "Local", "Local", 48000, "No", "—", "Local / staff-house approach; no cash housing allowance modeled."),
    ("Operations Support", "TBD — Person to be defined", "TBD", "TBD", 48000, "No", "—", "Open role; salary is a budget placeholder. Contract and benefits remain TBD."),
    ("Infrastructure Manager", "Martin Aguero", "Local Secondee", "Local", 180000, "Yes", "PU Infra Manager", "Already assigned to the project as a local secondee. PU pays salary; 30 paid vacation days apply."),
]

TABLE_HEADER_ROW = 20
TABLE_START = 21
TABLE_END = TABLE_START + len(PEOPLE) - 1
TOTAL_ROW = TABLE_END + 1


def note(text):
    return Comment(text, "Manus")


def source_note(field, detail=""):
    return note(
        f"Source: user-provided annual compensation table, reviewed {SOURCE_DATE}; field: {field}. {detail}".strip()
    )


def management_note(detail):
    return note(f"Source: management instruction in this task through {SOURCE_DATE}. {detail}")


def set_input(cell, value, cell_note):
    cell.value = value
    cell.font = Font(name="Arial", size=10, color=BLUE)
    cell.comment = cell_note


def set_formula(cell, formula, number_format=None, cell_note=None):
    cell.value = formula
    cell.font = Font(name="Arial", size=10, color=BLACK)
    if number_format:
        cell.number_format = number_format
    if cell_note:
        cell.comment = cell_note


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
    cell.font = Font(name="Arial", size=11, bold=True, color=BLACK)
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 22


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


def build():
    wb = Workbook()
    ws = wb.active
    ws.title = "Manpower Cost Summary"
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 100
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 3
    widths = {
        "C": 24, "D": 30, "E": 15, "F": 16, "G": 12, "H": 15,
        "I": 15, "J": 14, "K": 14, "L": 14, "M": 15, "N": 15, "O": 16,
    }
    for column, width in widths.items():
        ws.column_dimensions[column].width = width

    # Header
    ws.merge_cells("C3:O3")
    ws["C3"] = "Petrourdaneta — Manpower Cost Summary"
    ws["C3"].fill = PatternFill("solid", fgColor=DARK_GREEN)
    ws["C3"].font = Font(name="Arial", size=16, bold=True, color=WHITE)
    ws["C3"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[3].height = 27
    ws.merge_cells("C5:O5")
    ws["C5"] = "Single-sheet executive model | Overall monthly and annual manpower cost | COO excluded | USD"
    ws["C5"].font = Font(name="Arial", size=11, bold=True, color=BLACK)
    ws.merge_cells("C6:O6")
    ws["C6"] = "Blue = source input | Black = formula | Health-care cost excluded pending Airswift confirmation"
    ws["C6"].font = Font(name="Arial", size=9, italic=True, color="666666")

    ws.merge_cells("C8:O9")
    ws["C8"] = (
        "BIG NOTE — Alexander Stulme, Alan McKeon and Martin Aguero are PU-paid secondees. Martin is already assigned to the project as a local secondee. "
        "Repatriates receive the one-time transition package in M7 and then become local. Alan remains the only expat and receives $2,000/month housing from M7."
    )
    ws["C8"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C8"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C8"].comment = management_note("Tax, payroll, labor-law and residence treatment require legal and tax review before implementation.")
    ws.row_dimensions[8].height = 42

    # Overall cost summary
    section(ws, 11, "OVERALL MANPOWER COST", 3, 7)
    table_header(ws, 12, ["Metric", "M1–M6 / Month", "M7", "M8–M12 / Month", "Year 1"], 3, warning_cols=(5,))
    summary_labels = ["Gross manpower cost", "Less: PU-paid secondees", "NET manpower cost"]
    for row, label in enumerate(summary_labels, start=13):
        ws.cell(row, 3, label).font = Font(name="Arial", size=10, bold=(row == 15), color=BLACK)
        if row == 13:
            formulas = [f"=SUM(L{TABLE_START}:L{TABLE_END})", f"=SUM(M{TABLE_START}:M{TABLE_END})", f"=SUM(N{TABLE_START}:N{TABLE_END})", f"=SUM(O{TABLE_START}:O{TABLE_END})"]
        elif row == 14:
            formulas = [
                f'=-SUMIF($G${TABLE_START}:$G${TABLE_END},"Yes",$L${TABLE_START}:$L${TABLE_END})',
                f'=-SUMIF($G${TABLE_START}:$G${TABLE_END},"Yes",$M${TABLE_START}:$M${TABLE_END})',
                f'=-SUMIF($G${TABLE_START}:$G${TABLE_END},"Yes",$N${TABLE_START}:$N${TABLE_END})',
                f'=-SUMIF($G${TABLE_START}:$G${TABLE_END},"Yes",$O${TABLE_START}:$O${TABLE_END})',
            ]
        else:
            formulas = ["=D13+D14", "=E13+E14", "=F13+F14", "=G13+G14"]
        for col, formula in zip(range(4, 8), formulas):
            set_formula(ws.cell(row, col), formula, CURRENCY_FIRST if row == 13 and col == 4 else CURRENCY)
            ws.cell(row, col).alignment = Alignment(horizontal="right", vertical="center")
        ws.row_dimensions[row].height = 22
    outline(ws, 12, 15, 3, 7)
    for col in range(3, 8):
        ws.cell(15, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))

    # Compact cost policy / Airswift action
    section(ws, 11, "AIRSWHIFT ACTION — HEALTH CARE AND ROTATION", 9, 15)
    ws.merge_cells("I12:O15")
    ws["I12"] = (
        "Health care is excluded from all costs in this model. Airswift should confirm the applicable medical coverage, eligibility, insurer and price before a separate health-care cost is approved and added. "
        "For M1–M6, the eight transition roles are assumed to work 21 days on / 14 days off: 1.71 tickets per person per month, or 13.71 tickets per month in total. Ticket costs are excluded pending Airswift confirmation."
    )
    ws["I12"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["I12"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["I12"].comment = management_note("Health-care scope and pricing are pending confirmation from Airswift and are not included in the model.")
    ws.row_dimensions[12].height = 66

    # Compact personnel and cost table
    section(ws, 18, "PERSONNEL COST, CONTRACT, ROTATION AND BENEFIT SUMMARY", 3, 15)
    headers = [
        "Person", "Position", "M1–M6 Contract", "M7+ Basis", "PU-Paid?", "Tickets / Mo M1–M6", "Annual Salary",
        "M7 Package", "Housing / Month", "M1–M6 / Mo", "M7 Cost", "M8–M12 / Mo", "Year 1 Cost",
    ]
    table_header(ws, TABLE_HEADER_ROW, headers, 3, warning_cols=(12,))

    for idx, record in enumerate(PEOPLE):
        position, person, contract, basis, annual_salary, pu_paid, pu_scope, explanation = record
        row = TABLE_START + idx
        set_input(ws.cell(row, 3), person, source_note("Person", explanation))
        set_input(ws.cell(row, 4), position, source_note("Position", explanation))
        set_input(ws.cell(row, 5), contract, management_note(f"M1–M6 contract: {contract}. {explanation}"))
        set_input(ws.cell(row, 6), basis, management_note(f"M7+ basis: {basis}. {explanation}"))
        set_input(ws.cell(row, 7), pu_paid, management_note("PU pays the costs of Alexander Stulme, Alan McKeon and Martin Aguero as secondees."))
        set_formula(
            ws.cell(row, 8),
            f'=IF(C{row}="Martin Aguero",0,2*30/35)',
            '#,##0.00',
            management_note("M1–M6 rotation assumption: 21 days on / 14 days off. Two ticket legs per 35-day cycle, or 1.71 tickets per month. Martin Aguero is local and has no rotation ticket allowance."),
        )
        set_input(ws.cell(row, 9), annual_salary, source_note("Base Salary (Annual)", explanation))
        ws.cell(row, 9).number_format = CURRENCY_FIRST if idx == 0 else CURRENCY
        set_formula(
            ws.cell(row, 10),
            f'=IF(E{row}="Repatriate",1.5*I{row}/12,0)',
            CURRENCY,
            management_note("One-time M7 repatriation / localization package equals 1.5 times monthly salary for repatriates."),
        )
        set_formula(
            ws.cell(row, 11),
            f'=IF(C{row}="Alan McKeon",2000,0)',
            CURRENCY,
            management_note("Alan McKeon receives $2,000 per month housing from M7 due to family relocation to Maracaibo."),
        )
        set_formula(ws.cell(row, 12), f"=I{row}/12", CURRENCY_FIRST if idx == 0 else CURRENCY)
        set_formula(ws.cell(row, 13), f"=L{row}+J{row}+K{row}", CURRENCY)
        set_formula(ws.cell(row, 14), f"=L{row}+K{row}", CURRENCY)
        set_formula(ws.cell(row, 15), f"=6*L{row}+M{row}+5*N{row}", CURRENCY_FIRST if idx == 0 else CURRENCY)
        for col in range(3, 16):
            ws.cell(row, col).alignment = Alignment(
                horizontal="right" if col in (8, 9, 10, 11, 12, 13, 14, 15) else "left",
                vertical="center",
                wrap_text=col in (3, 4, 5, 6),
            )
        ws.row_dimensions[row].height = 24

    ws.merge_cells(start_row=TOTAL_ROW, start_column=3, end_row=TOTAL_ROW, end_column=7)
    ws.cell(TOTAL_ROW, 3, "TOTAL GROSS MANPOWER COST")
    ws.cell(TOTAL_ROW, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    set_formula(ws.cell(TOTAL_ROW, 8), f"=SUM(H{TABLE_START}:H{TABLE_END})", '#,##0.00')
    for col in range(9, 16):
        letter = get_column_letter(col)
        set_formula(ws.cell(TOTAL_ROW, col), f"=SUM({letter}{TABLE_START}:{letter}{TABLE_END})", CURRENCY_FIRST if col == 9 else CURRENCY)
    for col in range(3, 16):
        ws.cell(TOTAL_ROW, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    ws.row_dimensions[TOTAL_ROW].height = 25
    outline(ws, TABLE_HEADER_ROW, TOTAL_ROW, 3, 15)
    ws.conditional_formatting.add(f"O{TABLE_START}:O{TABLE_END}", DataBarRule(start_type="min", end_type="max", color=DARK_GREEN))

    # References and scope
    section(ws, 33, "REFERENCES AND MODEL SCOPE", 3, 15)
    ws.merge_cells("C34:O36")
    ws["C34"] = (
        "References: user-provided annual compensation table reviewed 7–8 September 2026, and management instructions in this task on contract type, benefits, PU secondments and cost responsibility. "
        "Health care and ticket costs are excluded pending Airswift confirmation of coverage, price and booking scope. The M1–M6 ticket plan assumes 21 days on / 14 days off and 1.71 tickets per transition role per month. This is a management-planning cost model; tax gross-up, statutory contributions, stock options and future bonus plans require separate approval and specialist review."
    )
    ws["C34"].font = Font(name="Arial", size=9, italic=True, color="666666")
    ws["C34"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws.row_dimensions[34].height = 50

    ws.freeze_panes = "C20"
    ws.print_area = "B2:O36"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = 0.20
    ws.page_margins.right = 0.20
    ws.page_margins.top = 0.25
    ws.page_margins.bottom = 0.25
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
    assert "Health care is excluded" in ws["I12"].value
    assert ws["C29"].value == "Martin Aguero"
    assert ws["E29"].value == "Local Secondee"
    assert ws["F29"].value == "Local"
    assert ws["G29"].value == "Yes"
    assert ws["H21"].value == '=IF(C21="Martin Aguero",0,2*30/35)'
    assert ws["J29"].value == '=IF(E29="Repatriate",1.5*I29/12,0)'
    assert ws["K24"].value == '=IF(C24="Alan McKeon",2000,0)'
    assert ws["L21"].value == "=I21/12"
    assert ws["M21"].value == "=L21+J21+K21"
    assert ws["N21"].value == "=L21+K21"
    assert ws["O21"].value == "=6*L21+M21+5*N21"
    assert ws["D13"].value == "=SUM(L21:L29)"
    assert ws["D14"].value == '=-SUMIF($G$21:$G$29,"Yes",$L$21:$L$29)'
    assert ws["E13"].value == "=SUM(M21:M29)"
    assert ws["G13"].value == "=SUM(O21:O29)"
    assert ws["G14"].value == '=-SUMIF($G$21:$G$29,"Yes",$O$21:$O$29)'
    assert ws["G15"].value == "=G13+G14"
    print("VALIDATED: one-sheet workbook | health-care excluded pending Airswift confirmation | costs recalculated")


if __name__ == "__main__":
    build()
    validate()
