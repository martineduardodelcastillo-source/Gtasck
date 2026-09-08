from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.pagebreak import Break

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

# Position, person, M1-M6 contract, M7+ basis, annual salary, PU salary share, note
PEOPLE = [
    ("EPCM & Engineering Manager", "Juan Conde", "Repatriate", "Local — Venezuela", 216000, "—", "One-time M7 transition package. Origin-country employee tax assumption; no company gross-up modeled."),
    ("Drilling & Well Services Manager", "Alexander Stulme", "Repatriate", "Local — Venezuela", 180000, "60%", "Initial secondee. 60% salary-share reimbursement is a working assumption pending Barbara's confirmation and any cap."),
    ("Operations & Maintenance Manager", "Félix Valderrama", "Repatriate", "Local — Venezuela", 216000, "—", "One-time M7 transition package. Origin-country employee tax assumption; no company gross-up modeled."),
    ("Technical Manager (Geosciences)", "Alan McKeon", "Expat", "Expat", 180000, "60%", "Initial secondee. $2,000/month housing from M7; home leave stated but not costed. 60% salary-share reimbursement pending Barbara's confirmation and any cap."),
    ("Reservoir Engineer", "JJI", "Local", "Local", 120000, "—", "Remote designation and local benefit treatment remain subject to confirmation."),
    ("Rig Company Man", "Marcelo Dantas", "Expat", "Expat", 180000, "—", "Rotation is confirmed; expatriate contract treatment remains subject to confirmation."),
    ("Planning & PMO", "Jose Miguel", "Local", "Local", 48000, "—", "Local / staff-house approach; no cash housing allowance modeled."),
    ("Operations Support", "TBD — Person to be defined", "TBD", "TBD", 48000, "—", "Open role; salary is a budget placeholder. Contract and benefits remain TBD."),
    ("Infrastructure Manager", "Martin Aguero", "Local Secondee", "Local", 180000, "60%", "Already assigned to the project as a local secondee. 60% salary-share reimbursement is a working assumption pending Barbara's confirmation and any cap."),
]

CONTRACT_HEADER = 20
CONTRACT_START = 21
CONTRACT_END = CONTRACT_START + len(PEOPLE) - 1
CONTRACT_TOTAL = CONTRACT_END + 1
COST_HEADER = 36
COST_START = 37
COST_END = COST_START + len(PEOPLE) - 1
COST_TOTAL = COST_END + 1


def note(text):
    return Comment(text, "Manus")


def source_note(field, detail=""):
    return note(f"Source: user-provided annual compensation table, reviewed {SOURCE_DATE}; field: {field}. {detail}".strip())


def management_note(detail):
    return note(f"Source: management instruction in this task through {SOURCE_DATE}. {detail}")


def set_input(cell, value, cell_note):
    cell.value = value
    cell.font = Font(name="Arial", size=11, color=BLUE)
    cell.comment = cell_note


def set_formula(cell, formula, number_format=None, cell_note=None):
    cell.value = formula
    cell.font = Font(name="Arial", size=11, color=BLACK)
    if number_format:
        cell.number_format = number_format
    if cell_note:
        cell.comment = cell_note


def table_header(ws, row, labels, start_col=3, warning_cols=()):
    for col, label in enumerate(labels, start=start_col):
        cell = ws.cell(row, col, label)
        cell.fill = PatternFill("solid", fgColor="FFF3E0" if col in warning_cols else LIGHT_GREEN)
        cell.font = Font(name="Arial", size=11, bold=True, color=BLACK)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(bottom=Side(style="medium", color=DARK_GREEN))
    ws.row_dimensions[row].height = 38


def section(ws, row, label, start_col, end_col):
    ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
    cell = ws.cell(row, start_col, label)
    cell.fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    cell.font = Font(name="Arial", size=12, bold=True, color=BLACK)
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 24


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
    ws.sheet_view.zoomScale = 110
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 3
    widths = {
        "C": 27, "D": 33, "E": 18, "F": 19, "G": 15, "H": 17,
        "I": 16, "J": 16, "K": 16, "L": 16, "M": 16, "N": 16,
    }
    for column, width in widths.items():
        ws.column_dimensions[column].width = width

    # Header
    ws.merge_cells("C3:N3")
    ws["C3"] = "Petrourdaneta — Manpower Cost Summary"
    ws["C3"].fill = PatternFill("solid", fgColor=DARK_GREEN)
    ws["C3"].font = Font(name="Arial", size=17, bold=True, color=WHITE)
    ws["C3"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[3].height = 29
    ws.merge_cells("C5:N5")
    ws["C5"] = "Single-sheet executive model | Overall monthly and annual manpower cost | COO excluded | USD"
    ws["C5"].font = Font(name="Arial", size=12, bold=True, color=BLACK)
    ws.merge_cells("C6:N6")
    ws["C6"] = "Blue = source input | Black = formula | Health care and ticket costs excluded pending Airswift confirmation"
    ws["C6"].font = Font(name="Arial", size=10, italic=True, color="666666")

    ws.merge_cells("C8:N9")
    ws["C8"] = (
        "BIG NOTE — Alexander Stulme, Alan McKeon and Martin Aguero are secondees. Net cost deducts an indicative 60% reimbursement of their base salaries only, "
        "pending Barbara's confirmation of eligibility and any cap. Repatriates receive the one-time M7 package and then become local. Alan remains an expat with $2,000/month housing from M7."
    )
    ws["C8"].font = Font(name="Arial", size=11, bold=True, color="C00000")
    ws["C8"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C8"].comment = management_note("Tax, payroll, labor-law, secondee reimbursement and residence treatment require review before implementation.")
    ws.row_dimensions[8].height = 48

    # Overall cost summary
    section(ws, 11, "OVERALL MANPOWER COST", 3, 7)
    table_header(ws, 12, ["Metric", "M1–M6 / Month", "M7", "M8–M12 / Month", "Year 1"], 3, warning_cols=(5,))
    labels = ["Gross manpower cost", "Less: PU salary share @60%", "NET manpower cost"]
    for row, label in enumerate(labels, start=13):
        ws.cell(row, 3, label).font = Font(name="Arial", size=11, bold=(row == 15), color=BLACK)
        if row == 13:
            formulas = [f"=SUM(G{COST_START}:G{COST_END})", f"=SUM(H{COST_START}:H{COST_END})", f"=SUM(I{COST_START}:I{COST_END})", f"=SUM(J{COST_START}:J{COST_END})"]
        elif row == 14:
            formulas = [
                f'=-SUMIF($G${CONTRACT_START}:$G${CONTRACT_END},"60%",$D${COST_START}:$D${COST_END})*60%/12',
                f'=-SUMIF($G${CONTRACT_START}:$G${CONTRACT_END},"60%",$D${COST_START}:$D${COST_END})*60%/12',
                f'=-SUMIF($G${CONTRACT_START}:$G${CONTRACT_END},"60%",$D${COST_START}:$D${COST_END})*60%/12',
                f'=-SUMIF($G${CONTRACT_START}:$G${CONTRACT_END},"60%",$D${COST_START}:$D${COST_END})*60%',
            ]
        else:
            formulas = ["=D13+D14", "=E13+E14", "=F13+F14", "=G13+G14"]
        for col, formula in zip(range(4, 8), formulas):
            set_formula(ws.cell(row, col), formula, CURRENCY_FIRST if row == 13 and col == 4 else CURRENCY)
            ws.cell(row, col).alignment = Alignment(horizontal="right", vertical="center")
        ws.row_dimensions[row].height = 25
    outline(ws, 12, 15, 3, 7)
    for col in range(3, 8):
        ws.cell(15, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))

    # Airswift / Barbara action box
    section(ws, 11, "AIRSWHIFT AND BARBARA ACTIONS", 10, 14)
    ws.merge_cells("J12:N15")
    ws["J12"] = (
        "Airswift: confirm medical coverage, eligibility, insurer, pricing and ticket booking / fare scope. Health care and ticket costs are not included. "
        "Rotation planning assumes 21 days on / 14 days off: 1.71 tickets per transition role per month, 13.71 tickets monthly in total. "
        "Barbara: confirm the 60% secondee base-salary reimbursement, eligibility and any cap."
    )
    ws["J12"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["J12"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["J12"].comment = management_note("Airswift and Barbara actions remain pending; associated costs and reimbursement limits require confirmation.")
    ws.row_dimensions[12].height = 76

    # Contract / rotation table
    section(ws, 18, "PERSONNEL, CONTRACT AND ROTATION PLAN", 3, 8)
    contract_headers = ["Person", "Position", "M1–M6 Contract", "M7+ Basis", "PU Salary Share", "Tickets / Mo M1–M6"]
    table_header(ws, CONTRACT_HEADER, contract_headers, 3)
    for idx, record in enumerate(PEOPLE):
        position, person, contract, basis, annual_salary, pu_share, explanation = record
        row = CONTRACT_START + idx
        values = [person, position, contract, basis, pu_share]
        fields = ["Person", "Position", "M1–M6 Contract", "M7+ Basis", "PU Salary Share"]
        for col, value, field in zip(range(3, 8), values, fields):
            if field in {"M1–M6 Contract", "M7+ Basis", "PU Salary Share"}:
                cell_note = management_note(explanation)
            else:
                cell_note = source_note(field, explanation)
            set_input(ws.cell(row, col), value, cell_note)
        set_formula(
            ws.cell(row, 8),
            f'=IF(C{row}="Martin Aguero",0,2*30/35)',
            '#,##0.00',
            management_note("M1–M6 rotation assumption: 21 days on / 14 days off. Two ticket legs per 35-day cycle, or 1.71 tickets per month. Martin Aguero is local and has no rotation tickets."),
        )
        for col in range(3, 9):
            ws.cell(row, col).alignment = Alignment(horizontal="right" if col == 8 else "left", vertical="center", wrap_text=True)
        ws.row_dimensions[row].height = 30
    ws.merge_cells(start_row=CONTRACT_TOTAL, start_column=3, end_row=CONTRACT_TOTAL, end_column=7)
    ws.cell(CONTRACT_TOTAL, 3, "TOTAL TICKETS / MONTH M1–M6")
    ws.cell(CONTRACT_TOTAL, 3).font = Font(name="Arial", size=11, bold=True, color=BLACK)
    set_formula(ws.cell(CONTRACT_TOTAL, 8), f"=SUM(H{CONTRACT_START}:H{CONTRACT_END})", '#,##0.00')
    for col in range(3, 9):
        ws.cell(CONTRACT_TOTAL, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    outline(ws, CONTRACT_HEADER, CONTRACT_TOTAL, 3, 8)

    # Cost table
    section(ws, 34, "MANPOWER COST BY PERSON — HEALTH CARE AND TICKETS EXCLUDED", 3, 10)
    cost_headers = ["Person", "Annual Salary", "M7 Package", "Housing / Month", "M1–M6 / Mo", "M7 Cost", "M8–M12 / Mo", "Year 1 Cost"]
    table_header(ws, COST_HEADER, cost_headers, 3, warning_cols=(7,))
    for idx, record in enumerate(PEOPLE):
        position, person, contract, basis, annual_salary, pu_share, explanation = record
        row = COST_START + idx
        contract_row = CONTRACT_START + idx
        set_formula(ws.cell(row, 3), f"=C{contract_row}")
        set_input(ws.cell(row, 4), annual_salary, source_note("Base Salary (Annual)", explanation))
        ws.cell(row, 4).number_format = CURRENCY_FIRST if idx == 0 else CURRENCY
        set_formula(
            ws.cell(row, 5),
            f'=IF(E{contract_row}="Repatriate",1.5*D{row}/12,0)',
            CURRENCY,
            management_note("One-time M7 repatriation / localization package equals 1.5 times monthly salary for repatriates."),
        )
        set_formula(
            ws.cell(row, 6),
            f'=IF(C{row}="Alan McKeon",2000,0)',
            CURRENCY,
            management_note("Alan McKeon receives $2,000 per month housing from M7 due to family relocation to Maracaibo."),
        )
        set_formula(ws.cell(row, 7), f"=D{row}/12", CURRENCY_FIRST if idx == 0 else CURRENCY)
        set_formula(ws.cell(row, 8), f"=G{row}+E{row}+F{row}", CURRENCY)
        set_formula(ws.cell(row, 9), f"=G{row}+F{row}", CURRENCY)
        set_formula(ws.cell(row, 10), f"=6*G{row}+H{row}+5*I{row}", CURRENCY_FIRST if idx == 0 else CURRENCY)
        for col in range(3, 11):
            ws.cell(row, col).alignment = Alignment(horizontal="right" if col >= 4 else "left", vertical="center")
        ws.row_dimensions[row].height = 28
    ws.merge_cells(start_row=COST_TOTAL, start_column=3, end_row=COST_TOTAL, end_column=3)
    ws.cell(COST_TOTAL, 3, "TOTAL GROSS COST")
    ws.cell(COST_TOTAL, 3).font = Font(name="Arial", size=11, bold=True, color=BLACK)
    for col in range(4, 11):
        letter = get_column_letter(col)
        set_formula(ws.cell(COST_TOTAL, col), f"=SUM({letter}{COST_START}:{letter}{COST_END})", CURRENCY_FIRST if col == 4 else CURRENCY)
    for col in range(3, 11):
        ws.cell(COST_TOTAL, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    outline(ws, COST_HEADER, COST_TOTAL, 3, 10)
    ws.conditional_formatting.add(f"J{COST_START}:J{COST_END}", DataBarRule(start_type="min", end_type="max", color=DARK_GREEN))

    # Reference / scope
    section(ws, 50, "REFERENCES AND MODEL SCOPE", 3, 10)
    ws.merge_cells("C51:J54")
    ws["C51"] = (
        "References: user-provided annual compensation table reviewed 7–8 September 2026, and management instructions in this task. Health care and ticket costs are excluded pending Airswift confirmation. "
        "Net cost deducts only 60% of relevant secondee base salaries as a provisional reimbursement; Barbara must confirm eligibility and any cap. Performance bonuses and stock options are not included."
    )
    ws["C51"].font = Font(name="Arial", size=10, italic=True, color="666666")
    ws["C51"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws.row_dimensions[51].height = 58

    ws.freeze_panes = "C20"
    ws.print_area = "B2:N54"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = 0.20
    ws.page_margins.right = 0.20
    ws.page_margins.top = 0.25
    ws.page_margins.bottom = 0.25
    ws.oddFooter.center.text = "Manpower Cost Summary | Page &P of &N"
    ws.oddFooter.center.size = 8
    ws.row_breaks.append(Break(id=33))

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
    assert ws["C29"].value == "Martin Aguero"
    assert ws["E29"].value == "Local Secondee"
    assert ws["F29"].value == "Local"
    assert ws["G29"].value == "60%"
    assert ws["H21"].value == '=IF(C21="Martin Aguero",0,2*30/35)'
    assert ws["E45"].value == '=IF(E29="Repatriate",1.5*D45/12,0)'
    assert ws["F40"].value == '=IF(C40="Alan McKeon",2000,0)'
    assert ws["G37"].value == "=D37/12"
    assert ws["H37"].value == "=G37+E37+F37"
    assert ws["I37"].value == "=G37+F37"
    assert ws["J37"].value == "=6*G37+H37+5*I37"
    assert ws["D13"].value == "=SUM(G37:G45)"
    assert ws["D14"].value == '=-SUMIF($G$21:$G$29,"60%",$D$37:$D$45)*60%/12'
    assert ws["G13"].value == "=SUM(J37:J45)"
    assert ws["G14"].value == '=-SUMIF($G$21:$G$29,"60%",$D$37:$D$45)*60%'
    assert ws["G15"].value == "=G13+G14"
    print("VALIDATED: one readable worksheet | separate contract and cost tables | 60% salary share calculated")


if __name__ == "__main__":
    build()
    validate()
