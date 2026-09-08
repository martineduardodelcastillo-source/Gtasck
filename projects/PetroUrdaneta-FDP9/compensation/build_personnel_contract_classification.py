from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


BASE = Path(__file__).resolve().parent
OUT = BASE / "personnel_base_salary_contract_types.xlsx"
SOURCE_IMAGE = Path("/home/ubuntu/upload/pasted_file_yfFQ2v_image.png")
SOURCE_DATE = "7 September 2026"

DARK_GREEN = "135B44"
LIGHT_GREEN = "CFE9E0"
WHITE = "FFFFFF"
BLUE = "0000FF"
BLACK = "000000"
GREEN = "008000"
GRID = "B7B7B7"
WARNING = "FFF2CC"
CURRENCY_FIRST = '$#,##0.0;[Red]($#,##0.0);-'
CURRENCY = '#,##0.0;[Red](#,##0.0);-'

# number, position, person, annual base salary, M1-M6 contract, work arrangement, status, notes
PEOPLE = [
    (1, "EPCM & Engineering Manager", "Juan Conde", 216000, "Repatriate", "Fixed", "Confirmed", "Repatriate; transitions to Local — Venezuela from M7 after the one-time transition package."),
    (2, "Drilling & Well Services Manager", "Alexander Stulme", 180000, "Repatriate", "Fixed", "Confirmed", "Repatriate; initially appointed General Manager of PU on secondment; transitions to Local — Venezuela from M7 after the one-time transition package."),
    (3, "Operations & Maintenance Manager", "Félix Valderrama", 216000, "Repatriate", "Fixed", "Confirmed", "Repatriate; transitions to Local — Venezuela from M7 after the one-time transition package."),
    (4, "Technical Manager (Geosciences)", "Alan McKeon", 180000, "Expat", "Fixed", "Confirmed", "Expat; initially appointed Technical Manager of PU on secondment. From M7: $2,000/month housing allowance and two home leaves."),
    (5, "Reservoir Engineer", "JJI", 120000, "Local", "Fixed", "Assumption", "Remote role. Local / Fixed is an editable assumption pending confirmation."),
    (6, "Rig Company Man", "Marcelo Dantas", 180000, "Expat", "Rotation", "Assumption", "Rotation confirmed from prior instructions; Expat contract is an editable assumption."),
    (7, "Planning & PMO", "Jose Miguel", 48000, "Local", "Fixed", "Confirmed", "Local in Maracaibo or staff house; no cash housing allowance by default."),
    (8, "Operations Support", "TBD — Person to be defined", 48000, "TBD", "TBD", "Assumption", "Open position. Person, contract type, work arrangement and benefits are to be defined. Salary remains a budget placeholder from the source table."),
]

# Planning assumptions for the M7 one-time Repatriation / Localisation Transition Package.
# Each item is expressed as a multiple of the employee's monthly base salary and is editable.
REPATRIATION_COMPONENTS = [
    ("Moving & household-goods support", 0.50, "M7", "One-time allowance / reimbursement", "Packing, shipment, excess baggage and local move-related costs.", "Use documented reimbursement or capped allowance; exclude any recurring storage."),
    ("Settling-in & incidental expenses", 0.50, "M7", "One-time allowance", "Utilities, connection charges, phone / internet setup and small household items.", "Capped allowance for incidentals not reimbursed elsewhere."),
    ("Temporary lodging & local setup", 0.25, "M7", "One-time allowance / direct payment", "Initial hotel or staff-house transition and practical local setup.", "Use direct company payment where possible; do not duplicate approved housing."),
    ("Local transport & first-mile setup", 0.15, "M7", "One-time allowance", "Arrival transport, local mobility and initial work-access setup.", "One-time transition support; company commuting transport remains a separate local benefit."),
    ("Documentation, payroll & tax onboarding", 0.10, "M7", "Direct payment / reimbursement", "Local documentation, payroll onboarding and transition tax consultation.", "Prefer direct payment or reimbursement against documentation."),
]
CORE_TRANSITION_MULTIPLIER = sum(component[1] for component in REPATRIATION_COMPONENTS)

# Alan McKeon's approved expatriate benefits from M7 onward.
# Home leave timing is a planning schedule and remains editable in the Alan Expat Package tab.
ALAN_HOUSING_ALLOWANCE_MONTHLY = 2_000
ALAN_HOME_LEAVE_PER_TRIP = 6_000
ALAN_HOME_LEAVE_TRIPS = 2
ALAN_HOME_LEAVE_MONTHS = (9, 12)
ALAN_EXPAT_SCHEDULE_START = 15
MARTIN_AGUERO_ANNUAL_SALARY = 180_000
MARTIN_AGUERO_MONTHLY_SALARY = MARTIN_AGUERO_ANNUAL_SALARY / 12

# Annual medical insurance budget from the source compensation table.
# Operations Support retains the source budget only as a placeholder until the person is selected.
MEDICAL_INSURANCE_ANNUAL = {
    "Juan Conde": 12000,
    "Alexander Stulme": 12000,
    "Félix Valderrama": 12000,
    "Alan McKeon": 12000,
    "JJI": 12000,
    "Marcelo Dantas": 12000,
    "Jose Miguel": 8000,
    "TBD — Person to be defined": 8000,
}

DATA_START = 9
DATA_END = DATA_START + len(PEOPLE) - 1
TOTAL_ROW = DATA_END + 1
SUMMARY_SECTION_ROW = TOTAL_ROW + 3
SUMMARY_HEADER_ROW = SUMMARY_SECTION_ROW + 1
SUMMARY_FIRST_ROW = SUMMARY_HEADER_ROW + 1
SUMMARY_LAST_ROW = SUMMARY_FIRST_ROW + 8


def source_comment(field, extra=""):
    return Comment(
        f"Source: compensation table image {SOURCE_IMAGE.name}, provided {SOURCE_DATE}; field: {field}. {extra}".strip(),
        "Manus",
    )


def instruction_comment(text):
    return Comment(
        f"Source: management instructions in this task through {SOURCE_DATE}. {text}",
        "Manus",
    )


def compliance_comment(text):
    return Comment(
        "Compliance context: Venezuelan labor rules apply to employment relationships performed in Venezuela regardless of nationality. "
        "Source: Embassy of Spain in Caracas, 'Trabajar' (accessed 7 September 2026), summarizing LOTTT. "
        f"{text}",
        "Manus",
    )


def set_input(cell, value, comment):
    cell.value = value
    cell.font = Font(name="Arial", size=10, color=BLUE)
    cell.comment = comment


def set_formula(cell, formula, number_format=None, cross_sheet=False):
    cell.value = formula
    cell.font = Font(name="Arial", size=10, color=GREEN if cross_sheet else BLACK)
    if number_format:
        cell.number_format = number_format


def title_block(ws, title, subtitle, units, end_col):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 20
    ws.merge_cells(start_row=3, start_column=3, end_row=3, end_column=end_col)
    ws.cell(3, 3, title)
    ws.cell(3, 3).fill = PatternFill("solid", fgColor=DARK_GREEN)
    ws.cell(3, 3).font = Font(name="Arial", size=16, bold=True, color=WHITE)
    ws.cell(3, 3).alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[3].height = 25
    ws.merge_cells(start_row=5, start_column=3, end_row=5, end_column=end_col)
    ws.cell(5, 3, subtitle)
    ws.cell(5, 3).font = Font(name="Arial", size=11, bold=True, color=BLACK)
    ws.merge_cells(start_row=6, start_column=3, end_row=6, end_column=end_col)
    ws.cell(6, 3, units)
    ws.cell(6, 3).font = Font(name="Arial", size=9, italic=True, color="666666")


def header_row(ws, row, start_col, headers):
    for col, header in enumerate(headers, start=start_col):
        cell = ws.cell(row, col, header)
        cell.fill = PatternFill("solid", fgColor=LIGHT_GREEN)
        cell.font = Font(name="Arial", size=10, bold=True, color=BLACK)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(bottom=Side(style="medium", color=DARK_GREEN))
    ws.row_dimensions[row].height = 34


def apply_borders(ws, start_row, end_row, start_col, end_col):
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            cell = ws.cell(row, col)
            cell.border = Border(
                left=Side(style="thin", color=GRID) if col == start_col else Side(style=None),
                right=Side(style="thin", color=GRID) if col == end_col else Side(style=None),
                top=Side(style="thin", color=GRID),
                bottom=Side(style="thin", color=GRID),
            )


def autofit(ws, start_col, end_col, start_row, end_row):
    for col in range(start_col, end_col + 1):
        max_len = 0
        for row in range(start_row, end_row + 1):
            value = ws.cell(row, col).value
            if value is not None:
                max_len = max(max_len, len(str(value)))
        ws.column_dimensions[get_column_letter(col)].width = min(max(max_len + 3, 12), 38)


def build_personnel(wb):
    ws = wb.active
    ws.title = "Personnel"
    title_block(
        ws,
        "Personnel — Monthly Base Salary and Contract Classification",
        "COO / PU General Manager excluded and treated separately | Repatriates transition to Local — Venezuela from M7 after a one-time transition bonus",
        "USD | M1–M12 = annual base salary / 12 | One-time transition bonus is not included in monthly base salary | 8 people only",
        25,
    )

    headers = [
        "#",
        "Position",
        "Person",
        "Contract Type M1–M6",
        "Expatriate?",
        "Work Arrangement",
        "M7+ Employment Basis",
        "One-Time Transition Bonus (M7)",
        "Classification Status",
        "Notes",
        "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12",
        "Base Salary Annual",
    ]
    header_row(ws, 8, 3, headers)

    for row, record in enumerate(PEOPLE, start=DATA_START):
        number, position, person, annual_salary, contract_type, arrangement, status, notes = record
        set_input(ws.cell(row, 3), number, source_comment("row number"))
        set_input(ws.cell(row, 4), position, source_comment("Position"))
        person_comment = (
            instruction_comment("Leticia Almeida has been removed. Operations Support is an open position and the person is to be defined.")
            if person.startswith("TBD")
            else source_comment("Person")
        )
        set_input(ws.cell(row, 5), person, person_comment)
        set_input(
            ws.cell(row, 6), contract_type,
            instruction_comment("M1–M6 contract type must be Expat, Repatriate or Local. Edit if management confirms a different classification."),
        )
        set_formula(ws.cell(row, 7), f'=IF(F{row}="Expat","Yes","No")')
        set_input(
            ws.cell(row, 8), arrangement,
            instruction_comment("Work arrangement must be Fixed or Rotation. Remote is documented in Notes, not treated as a fourth contract type."),
        )
        set_formula(ws.cell(row, 9), f'=IF(F{row}="Repatriate","Local — Venezuela",F{row})')
        bonus = f"Eligible — one-time; {CORE_TRANSITION_MULTIPLIER:.2f}x monthly salary" if contract_type == "Repatriate" else "Not applicable"
        set_input(
            ws.cell(row, 10), bonus,
            instruction_comment(
                "For Repatriates: a single one-time M7 localisation / repatriation package. The core package is currently set at 1.50 months of monthly base salary, "
                "with components and caps on the Repatriation Package tab. It does not recur and is excluded from M1–M12 base salary. "
                "Payroll treatment and any statutory salary impact require Venezuelan legal, tax and HR confirmation."
            ),
        )
        set_input(
            ws.cell(row, 11), status,
            instruction_comment("Confirmed means directly established in prior instructions; Assumption remains editable and requires confirmation."),
        )
        set_input(ws.cell(row, 12), notes, instruction_comment(notes))
        set_input(ws.cell(row, 25), annual_salary, source_comment("Base Salary (Annual)"))
        ws.cell(row, 25).number_format = CURRENCY_FIRST if row == DATA_START else CURRENCY

        for col in range(13, 25):
            set_formula(ws.cell(row, col), f"=$Y{row}/12", CURRENCY_FIRST if row == DATA_START and col == 13 else CURRENCY)
        for col in range(3, 26):
            ws.cell(row, col).alignment = Alignment(
                horizontal="right" if col == 3 or col >= 13 else "center" if col in (6, 7, 8, 9, 10, 11) else "left",
                vertical="center",
                wrap_text=col in (4, 9, 10, 12),
            )
        ws.row_dimensions[row].height = 32

    ws.merge_cells(start_row=TOTAL_ROW, start_column=3, end_row=TOTAL_ROW, end_column=12)
    ws.cell(TOTAL_ROW, 3, f"TOTAL — {len(PEOPLE)} PEOPLE (COO EXCLUDED)")
    ws.cell(TOTAL_ROW, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    for col in range(13, 25):
        letter = get_column_letter(col)
        set_formula(ws.cell(TOTAL_ROW, col), f"=SUM({letter}{DATA_START}:{letter}{DATA_END})", CURRENCY_FIRST if col == 13 else CURRENCY)
    set_formula(ws.cell(TOTAL_ROW, 25), f"=SUM(Y{DATA_START}:Y{DATA_END})", CURRENCY_FIRST)
    for col in range(3, 26):
        ws.cell(TOTAL_ROW, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
        if col >= 13:
            ws.cell(TOTAL_ROW, col).alignment = Alignment(horizontal="right", vertical="center")

    ws.merge_cells(start_row=SUMMARY_SECTION_ROW, start_column=3, end_row=SUMMARY_SECTION_ROW, end_column=25)
    ws.cell(SUMMARY_SECTION_ROW, 3, "CLASSIFICATION SUMMARY")
    ws.cell(SUMMARY_SECTION_ROW, 3).fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    ws.cell(SUMMARY_SECTION_ROW, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    header_row(ws, SUMMARY_HEADER_ROW, 3, ["Metric", "Count", "Meaning"])
    summary = [
        ("Expat", f'=COUNTIF(F{DATA_START}:F{DATA_END},"Expat")', "M1–M6 contract type Expat"),
        ("Repatriate", f'=COUNTIF(F{DATA_START}:F{DATA_END},"Repatriate")', "Transition to Local — Venezuela from M7"),
        ("Local", f'=COUNTIF(F{DATA_START}:F{DATA_END},"Local")', "Local contract from M1 through M12"),
        ("Contract type TBD", f'=COUNTIF(F{DATA_START}:F{DATA_END},"TBD")', "Open position; contract type is to be defined"),
        ("Fixed", f'=COUNTIF(H{DATA_START}:H{DATA_END},"Fixed")', "Fixed work arrangement"),
        ("Rotation", f'=COUNTIF(H{DATA_START}:H{DATA_END},"Rotation")', "Rotation work arrangement"),
        ("Work arrangement TBD", f'=COUNTIF(H{DATA_START}:H{DATA_END},"TBD")', "Open position; work arrangement is to be defined"),
        ("One-time transition packages", f'=COUNTIF(J{DATA_START}:J{DATA_END},"Eligible*")', f"M7 only; core package = {CORE_TRANSITION_MULTIPLIER:.2f}x monthly salary"),
        ("Assumptions to confirm", f'=COUNTIF(K{DATA_START}:K{DATA_END},"Assumption")', "Editable classifications requiring confirmation"),
    ]
    for row, (metric, formula, meaning) in enumerate(summary, start=SUMMARY_FIRST_ROW):
        ws.cell(row, 3, metric).font = Font(name="Arial", size=10, color=BLACK)
        set_formula(ws.cell(row, 4), formula, '#,##0')
        ws.cell(row, 5, meaning).font = Font(name="Arial", size=10, color=BLACK)
    apply_borders(ws, SUMMARY_HEADER_ROW, SUMMARY_FIRST_ROW + len(summary) - 1, 3, 5)

    contract_validation = DataValidation(type="list", formula1='"Expat,Repatriate,Local,TBD"', allow_blank=False)
    arrangement_validation = DataValidation(type="list", formula1='"Fixed,Rotation,TBD"', allow_blank=False)
    status_validation = DataValidation(type="list", formula1='"Confirmed,Assumption"', allow_blank=False)
    ws.add_data_validation(contract_validation)
    ws.add_data_validation(arrangement_validation)
    ws.add_data_validation(status_validation)
    contract_validation.add(f"F{DATA_START}:F{DATA_END}")
    arrangement_validation.add(f"H{DATA_START}:H{DATA_END}")
    status_validation.add(f"K{DATA_START}:K{DATA_END}")
    ws.conditional_formatting.add(
        f"K{DATA_START}:K{DATA_END}",
        FormulaRule(formula=[f'K{DATA_START}="Assumption"'], fill=PatternFill("solid", fgColor=WARNING)),
    )
    ws.conditional_formatting.add(
        f"F{DATA_START}:F{DATA_END}",
        FormulaRule(formula=[f'F{DATA_START}="TBD"'], fill=PatternFill("solid", fgColor=WARNING)),
    )
    ws.conditional_formatting.add(
        f"H{DATA_START}:H{DATA_END}",
        FormulaRule(formula=[f'H{DATA_START}="TBD"'], fill=PatternFill("solid", fgColor=WARNING)),
    )

    apply_borders(ws, 8, DATA_END, 3, 25)
    ws.freeze_panes = "M9"
    autofit(ws, 3, 25, 8, SUMMARY_LAST_ROW)
    ws.column_dimensions["D"].width = max(ws.column_dimensions["D"].width, 38)
    ws.column_dimensions["E"].width = max(ws.column_dimensions["E"].width, 24)
    ws.column_dimensions["J"].width = 29
    ws.column_dimensions["L"].width = 38
    for col in range(13, 26):
        ws.column_dimensions[get_column_letter(col)].width = 14
    ws.print_area = f"B2:Y{SUMMARY_LAST_ROW}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.center.text = "Personnel | Page &P of &N"
    ws.oddFooter.center.size = 8


def build_rules(wb):
    ws = wb.create_sheet("Contract Rules")
    title_block(
        ws,
        "Contract and Benefit Rules by Stage",
        "Default policy view — individual packages may override these rules | One Operations Support position remains open (TBD)",
        "M1–M6 is initial stage | From M7 Repatriates operate as Local — Venezuela | Policy is subject to legal and HR validation",
        13,
    )

    headers = [
        "Contract Type M1–M6",
        "M1–M6 Benefits",
        "M7+ Employment Basis",
        "M7+ Medical",
        "M7+ Housing",
        "M7+ Tax Treatment",
        "M7+ Costed Benefits",
        "One-Time Transition Bonus (M7)",
        "Default Status",
        "Policy Notes",
        "People Count",
    ]
    header_row(ws, 8, 3, headers)
    rules = [
        (
            "Expat",
            "Medical insurance only",
            "Continues as Expat assignment",
            "Health care costed monthly",
            "Alan exception: $2,000/month from M7 for approved family relocation to Maracaibo; otherwise separate approval required",
            "No expat tax support or gross-up is modeled unless separately approved",
            "Salary + health care; Alan exception includes housing and two home leaves from M7",
            "Not applicable",
            "Provisional",
            "No universal oil-and-gas benefit grid; package must reflect role, location and contract.",
        ),
        (
            "Repatriate",
            "Medical insurance only",
            "Local — Venezuela from M7; document local payroll / employment basis",
            "Health care costed monthly",
            "Not costed in Monthly Costs; separate approval required",
            "Employee assumed to pay individual income tax in country of origin; no company tax gross-up or double-taxation cost modeled",
            "Salary + health care only in Monthly Costs; statutory and other benefits are outside this cost model",
            f"Eligible once at M7; core package = {CORE_TRANSITION_MULTIPLIER:.2f}x monthly salary; not recurring; see Repatriation Package",
            "Confirmed policy direction",
            "One-time package covers moving, settling-in, temporary lodging, transport and onboarding support—not an annual incentive. Legal review determines salary and tax treatment.",
        ),
        (
            "Local",
            "Medical insurance only",
            "Local — Venezuela",
            "Health care costed monthly",
            "Not costed in Monthly Costs; separate approval required",
            "Employee assumed to pay individual income tax in country of origin; no company tax gross-up or double-taxation cost modeled",
            "Salary + health care only in Monthly Costs; statutory and other benefits are outside this cost model",
            "Not applicable",
            "Provisional",
            "No international home leave or expat allowance by default.",
        ),
        (
            "TBD",
            "Not defined until person and contract are approved",
            "Not defined",
            "Not defined",
            "Not defined",
            "Not defined",
            "Not defined",
            "Not applicable",
            "Open position",
            "Operations Support headcount is budgeted, but the person, contract type and benefits remain to be defined.",
        ),
    ]
    for row, record in enumerate(rules, start=9):
        for col, value in enumerate(record, start=3):
            comment = compliance_comment(
                "The local payroll and benefit treatment must be reviewed by Venezuelan labor, tax and HR advisers before implementation."
            ) if col in (5, 8, 9, 10) else instruction_comment(f"Default contract rule: {value}")
            set_input(ws.cell(row, col), value, comment)
            ws.cell(row, col).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        set_formula(ws.cell(row, 13), f'=COUNTIF(Personnel!F{DATA_START}:F{DATA_END},C{row})', '#,##0', cross_sheet=True)
        ws.cell(row, 13).alignment = Alignment(horizontal="right", vertical="center")
        ws.row_dimensions[row].height = 75
    apply_borders(ws, 8, 12, 3, 13)

    ws.merge_cells("C14:M14")
    ws["C14"] = "WORK ARRANGEMENT RULES"
    ws["C14"].fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    ws["C14"].font = Font(name="Arial", size=10, bold=True, color=BLACK)
    header_row(ws, 15, 3, ["Work Arrangement", "Application", "M1–M6", "M7+ Housing / Lodging", "M7+ Travel / Leave", "Notes", "People Count"])
    arrangements = [
        (
            "Fixed", "Continuous assignment to the role", "Medical insurance only", "Based on contract type, city and approved package", "According to contract type / local policy", "JJI is Fixed but Remote; Remote is noted separately.", f'=COUNTIF(Personnel!H{DATA_START}:H{DATA_END},C16)'
        ),
        (
            "Rotation", "Roster-based presence in Venezuela", "Medical insurance only", "Hotel, staff house or rotational lodging; avoid duplicate permanent housing", "Rotation roster travel replaces or supplements home leave only if approved", "Marcelo Dantas is currently shown as Rotation.", f'=COUNTIF(Personnel!H{DATA_START}:H{DATA_END},C17)'
        ),
        (
            "TBD", "To be determined with the selected Operations Support employee", "Not defined", "Not defined", "Not defined", "Operations Support is an open position.", f'=COUNTIF(Personnel!H{DATA_START}:H{DATA_END},C18)'
        ),
    ]
    for row, record in enumerate(arrangements, start=16):
        for col, value in enumerate(record[:6], start=3):
            set_input(ws.cell(row, col), value, instruction_comment(f"Default work-arrangement rule: {value}"))
            ws.cell(row, col).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        set_formula(ws.cell(row, 9), record[6], '#,##0', cross_sheet=True)
        ws.cell(row, 9).alignment = Alignment(horizontal="right", vertical="center")
        ws.row_dimensions[row].height = 58
    apply_borders(ws, 15, 18, 3, 9)

    ws.merge_cells("C20:M23")
    ws["C20"] = (
        "Policy decision recorded: every Repatriate receives only a one-time M7 transition / repatriation package and thereafter is treated as Local — Venezuela. "
        f"The current core package is {CORE_TRANSITION_MULTIPLIER:.2f} months of monthly base salary and is itemised on the Repatriation Package tab. It is not a recurring bonus and is excluded from the monthly base salary. "
        "For repatriates becoming local, the planning assumption is that individual income tax is due in the employee's country of origin; no company tax gross-up or double-taxation cost is modeled. "
        "The amount, whether it is salary for Venezuelan labor purposes, the payroll / tax / social-security treatment, "
        "immigration status, and local statutory benefits must be approved by Venezuelan legal, tax and HR advisers before implementation. Venezuelan rules apply to employment relationships performed in Venezuela, irrespective of nationality."
    )
    ws["C20"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C20"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C20"].comment = compliance_comment("The Company policy transition does not replace a legal classification or payroll review.")

    autofit(ws, 3, 13, 8, 23)
    for col in range(3, 13):
        ws.column_dimensions[get_column_letter(col)].width = min(max(ws.column_dimensions[get_column_letter(col)].width, 18), 29)
    ws.column_dimensions["L"].width = 31
    ws.column_dimensions["M"].width = 14
    ws.print_area = "B2:M23"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.center.text = "Contract Rules | Page &P of &N"
    ws.oddFooter.center.size = 8


def build_repatriation_package(wb):
    ws = wb.create_sheet("Repatriation Package")
    title_block(
        ws,
        "One-Time Repatriation / Localisation Transition Package",
        "M7 only — moving, settling-in and onboarding costs | Excludes recurring benefits and approved housing",
        "USD | Editable assumptions in blue | Multipliers are expressed as months of monthly base salary",
        10,
    )

    ws.merge_cells("C8:J8")
    ws["C8"] = "CORE PACKAGE COMPONENTS — APPLIES ONLY TO REPATRIATES UPON LOCALISATION IN M7"
    ws["C8"].fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    ws["C8"].font = Font(name="Arial", size=10, bold=True, color=BLACK)
    component_headers = ["Component", "Months of Monthly Salary", "Timing", "Payment Method", "Included Costs", "Policy Treatment"]
    header_row(ws, 9, 3, component_headers)
    component_start = 10
    component_end = component_start + len(REPATRIATION_COMPONENTS) - 1
    for row, (component, multiplier, timing, payment_method, included, treatment) in enumerate(REPATRIATION_COMPONENTS, start=component_start):
        set_input(ws.cell(row, 3), component, instruction_comment(f"Core transition package component: {component}"))
        set_input(ws.cell(row, 4), multiplier, instruction_comment("Editable planning multiplier expressed in months of the employee's monthly base salary."))
        ws.cell(row, 4).number_format = '0.00x'
        set_input(ws.cell(row, 5), timing, instruction_comment("Paid or reimbursed once at localisation in M7."))
        set_input(ws.cell(row, 6), payment_method, instruction_comment("Use direct payment or documented reimbursement where practical; do not duplicate other approved benefits."))
        set_input(ws.cell(row, 7), included, instruction_comment(included))
        set_input(ws.cell(row, 8), treatment, compliance_comment("Confirm local payroll, tax and salary-character treatment before payment."))
        for col in range(3, 9):
            ws.cell(row, col).alignment = Alignment(horizontal="right" if col == 4 else "left", vertical="center", wrap_text=True)
        ws.row_dimensions[row].height = 40
    core_total_row = component_end + 1
    ws.cell(core_total_row, 3, "TOTAL CORE PACKAGE")
    ws.cell(core_total_row, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    set_formula(ws.cell(core_total_row, 4), f"=SUM(D{component_start}:D{component_end})", '0.00x')
    for col in range(3, 9):
        ws.cell(core_total_row, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    apply_borders(ws, 9, core_total_row, 3, 8)

    excluded_header_row = core_total_row + 3
    ws.merge_cells(start_row=excluded_header_row, start_column=3, end_row=excluded_header_row, end_column=8)
    ws.cell(excluded_header_row, 3, "EXCLUDED FROM THE ONE-TIME PACKAGE — MANAGED SEPARATELY")
    ws.cell(excluded_header_row, 3).fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    ws.cell(excluded_header_row, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    excluded = [
        ("Base salary", "Already reflected in M1–M12; not a transition cost."),
        ("Medical insurance", "M1–M6 and M7+ benefit; not part of the one-time package."),
        ("Housing / staff house / hotel", "Approved separately by city and individual package; do not duplicate in the allowance."),
        ("Company transport to work", "Ongoing local benefit, where approved; not a transition payment."),
        ("Home leave, stock options, annual incentive and vacation", "Only where separately approved; not included in the repatriation package."),
        ("Venezuelan statutory payroll benefits and taxes", "Apply according to local legal, tax and payroll review."),
    ]
    header_row(ws, excluded_header_row + 1, 3, ["Excluded Item", "Reason"])
    for row, (item, reason) in enumerate(excluded, start=excluded_header_row + 2):
        set_input(ws.cell(row, 3), item, instruction_comment(f"Excluded from one-time package: {item}"))
        set_input(ws.cell(row, 4), reason, instruction_comment(reason))
        ws.cell(row, 3).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.cell(row, 4).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.row_dimensions[row].height = 30
    apply_borders(ws, excluded_header_row + 1, excluded_header_row + 1 + len(excluded), 3, 4)

    calc_header_row = excluded_header_row + len(excluded) + 4
    ws.merge_cells(start_row=calc_header_row, start_column=3, end_row=calc_header_row, end_column=10)
    ws.cell(calc_header_row, 3, "M7 TRANSITION PACKAGE CALCULATION — REPATRIATES ONLY")
    ws.cell(calc_header_row, 3).fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    ws.cell(calc_header_row, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    calc_headers = ["Person", "Position", "Monthly Base Salary", "Core Package Multiple", "One-Time Package Cost", "M7 Employment Basis", "Approval Status", "Notes"]
    header_row(ws, calc_header_row + 1, 3, calc_headers)

    eligible_people = [record for record in PEOPLE if record[4] == "Repatriate"]
    calc_start = calc_header_row + 2
    for row, record in enumerate(eligible_people, start=calc_start):
        _, position, person, annual_salary, _, _, _, notes = record
        set_input(ws.cell(row, 3), person, instruction_comment("Eligible Repatriate identified from Personnel; package is paid once at M7."))
        set_input(ws.cell(row, 4), position, source_comment("Position"))
        set_formula(ws.cell(row, 5), f"=VLOOKUP(C{row},Personnel!$E${DATA_START}:$Y${DATA_END},21,FALSE)/12", CURRENCY_FIRST if row == calc_start else CURRENCY, cross_sheet=True)
        set_formula(ws.cell(row, 6), f"=$D${core_total_row}", '0.00x')
        set_formula(ws.cell(row, 7), f"=E{row}*F{row}", CURRENCY_FIRST if row == calc_start else CURRENCY)
        set_formula(ws.cell(row, 8), f"=VLOOKUP(C{row},Personnel!$E${DATA_START}:$I${DATA_END},5,FALSE)", cross_sheet=True)
        set_input(ws.cell(row, 9), "Pending individual approval", instruction_comment("Amount, approval and payroll treatment remain subject to Venezuelan legal, tax and HR review."))
        set_input(ws.cell(row, 10), "Core 1.50x package; benefits and housing remain outside this calculation.", instruction_comment("No recurring payment. No housing, medical, statutory benefits or tax gross-up included."))
        for col in range(3, 11):
            ws.cell(row, col).alignment = Alignment(horizontal="right" if col in (5, 6, 7) else "left", vertical="center", wrap_text=True)
        ws.row_dimensions[row].height = 34
    calc_end = calc_start + len(eligible_people) - 1
    calc_total_row = calc_end + 1
    ws.cell(calc_total_row, 3, "TOTAL ONE-TIME M7 PACKAGE")
    ws.cell(calc_total_row, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    set_formula(ws.cell(calc_total_row, 7), f"=SUM(G{calc_start}:G{calc_end})", CURRENCY_FIRST)
    for col in range(3, 11):
        ws.cell(calc_total_row, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    apply_borders(ws, calc_header_row + 1, calc_total_row, 3, 10)

    ws.merge_cells(start_row=calc_total_row + 3, start_column=3, end_row=calc_total_row + 5, end_column=10)
    ws.cell(calc_total_row + 3, 3, (
        "Policy guardrail: the package is a one-time M7 transition support. Use the component-level multipliers above as planning assumptions; "
        "pay direct suppliers or reimburse documented costs where possible, and do not duplicate approved housing, hotel, staff-house, medical or transport benefits. "
        "Before payment, Venezuelan legal, tax and HR advisers must confirm the correct payroll, tax, social-security and salary-character treatment."
    ))
    ws.cell(calc_total_row + 3, 3).font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws.cell(calc_total_row + 3, 3).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws.cell(calc_total_row + 3, 3).comment = compliance_comment("The package is a company policy item, not a determination of legal or tax treatment.")

    autofit(ws, 3, 10, 8, calc_total_row + 5)
    ws.column_dimensions["C"].width = 32
    ws.column_dimensions["D"].width = 28
    ws.column_dimensions["E"].width = 16
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 38
    ws.column_dimensions["H"].width = 30
    ws.column_dimensions["I"].width = 24
    ws.column_dimensions["J"].width = 36
    ws.print_area = f"B2:J{calc_total_row + 5}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.center.text = "Repatriation Package | Page &P of &N"
    ws.oddFooter.center.size = 8


def build_alan_expat_package(wb):
    ws = wb.create_sheet("Alan Expat Package", 2)
    title_block(
        ws,
        "Alan McKeon — Expatriate Package from M7",
        "Family relocation to Maracaibo | Housing allowance and two home leaves are costed from M7 onward",
        "USD | Inputs in blue are editable | Housing minimum for approved family relocation to Maracaibo = $2,000/month",
        9,
    )

    header_row(ws, 8, 3, ["Benefit / Assumption", "Value", "Unit", "Timing", "Cost Treatment", "Approval / Notes"])
    package_rows = [
        ("Housing allowance", ALAN_HOUSING_ALLOWANCE_MONTHLY, "USD / month", "M7–M12", "Included in Monthly Costs", "Approved minimum for Alan's family relocation to Maracaibo."),
        ("Home leave per trip", ALAN_HOME_LEAVE_PER_TRIP, "USD / trip", "M7+", "Included in Monthly Costs", "Two home leaves per year; timing is editable below."),
        ("Home leaves per year", ALAN_HOME_LEAVE_TRIPS, "Trips", "M7+", "Included in Monthly Costs", "Use trip count to calculate annual cost."),
        ("Home leave trip 1 month", ALAN_HOME_LEAVE_MONTHS[0], "Month", "M9", "Included in Monthly Costs", "Editable planning month; must be between M7 and M12."),
        ("Home leave trip 2 month", ALAN_HOME_LEAVE_MONTHS[1], "Month", "M12", "Included in Monthly Costs", "Editable planning month; must be between M7 and M12."),
        ("Family relocation city", "Maracaibo", "City", "M7+", "Housing allowance applies", "Housing minimum of $2,000/month applies to approved family relocation in Maracaibo."),
    ]
    for row, (benefit, value, unit, timing, treatment, note) in enumerate(package_rows, start=9):
        set_input(ws.cell(row, 3), benefit, instruction_comment(f"Alan expatriate package input: {benefit}"))
        set_input(ws.cell(row, 4), value, instruction_comment(note))
        if isinstance(value, (int, float)) and row in (9, 10):
            ws.cell(row, 4).number_format = CURRENCY
        elif isinstance(value, (int, float)):
            ws.cell(row, 4).number_format = '#,##0'
        set_input(ws.cell(row, 5), unit, instruction_comment(unit))
        set_input(ws.cell(row, 6), timing, instruction_comment(timing))
        set_input(ws.cell(row, 7), treatment, instruction_comment(treatment))
        set_input(ws.cell(row, 8), note, instruction_comment(note))
        for col in range(3, 9):
            ws.cell(row, col).alignment = Alignment(horizontal="right" if col == 4 and isinstance(value, (int, float)) else "left", vertical="center", wrap_text=True)
        ws.row_dimensions[row].height = 34
    apply_borders(ws, 8, 14, 3, 8)

    ws.merge_cells("C17:I17")
    ws["C17"] = "M7–M12 COST SUMMARY"
    ws["C17"].fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    ws["C17"].font = Font(name="Arial", size=10, bold=True, color=BLACK)
    header_row(ws, 18, 3, ["Metric", "Amount", "Calculation / Meaning"])
    summary = [
        ("Housing, M7–M12", "=D9*6", "Six months at the approved $2,000/month housing allowance."),
        ("Home leave, M7–M12", "=D10*D11", "Two trips at the approved $6,000 per trip."),
        ("Total Alan expat benefits", "=D19+D20", "Housing plus home leaves, excluding salary and health care."),
    ]
    for row, (metric, formula, meaning) in enumerate(summary, start=19):
        ws.cell(row, 3, metric).font = Font(name="Arial", size=10, color=BLACK)
        set_formula(ws.cell(row, 4), formula, CURRENCY_FIRST if row == 19 else CURRENCY)
        ws.cell(row, 5, meaning).font = Font(name="Arial", size=10, color=BLACK)
        ws.cell(row, 5).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    apply_borders(ws, 18, 21, 3, 5)

    ws.merge_cells("C24:I26")
    ws["C24"] = (
        "Policy note: for Alan McKeon's approved family relocation to Maracaibo, the model includes a minimum $2,000/month housing allowance from M7 and two $6,000 home leaves. "
        "For any future approved family relocation to Maracaibo, apply at least the same $2,000/month housing allowance unless management approves a higher package. "
        "Tax, social charges and any payroll treatment are not modeled here and require specialist review."
    )
    ws["C24"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C24"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C24"].comment = compliance_comment("Expatriate benefits must be implemented through the approved contract and payroll process.")

    autofit(ws, 3, 9, 8, 26)
    ws.column_dimensions["C"].width = 28
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 16
    ws.column_dimensions["F"].width = 13
    ws.column_dimensions["G"].width = 24
    ws.column_dimensions["H"].width = 42
    ws.print_area = "B2:I26"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.center.text = "Alan Expat Package | Page &P of &N"
    ws.oddFooter.center.size = 8


def build_pu_secondments(wb):
    ws = wb.create_sheet("PU Secondments", 4)
    title_block(
        ws,
        "PU-Paid Secondments and Net Cost after Secondments",
        "Alexander Stulme, Alan McKeon and Martin Aguero initially serve as Petrourdaneta secondees — PU pays their costs",
        "USD | Gross cost less PU-paid secondments = net cost | Martin Aguero salary of $180,000/year is included; his benefits remain TBD",
        19,
    )

    ws.merge_cells("C7:S9")
    ws["C7"] = (
        "BIG NOTE — Initial PU Secondments: Alexander Stulme (General Manager), Alan McKeon (Technical Manager) and Martin Aguero (Infra Manager) are secondees in Petrourdaneta. "
        "PU pays their costs. This sheet deducts the known modeled costs for Alexander and Alan and deducts Martin Aguero's known $180,000 annual salary ($15,000/month) from the gross Monthly Costs to provide the net cost. Martin's medical, housing, home leave and other benefits remain TBD and are not deducted until entered. "
        "For repatriates becoming local, individual income tax is assumed to be the employee's responsibility in the country of origin; no company tax gross-up or double-taxation cost is modeled. Expat tax support remains outside the model unless separately approved."
    )
    ws["C7"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C7"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws["C7"].comment = compliance_comment("Tax treatment, residence and payroll obligations require legal and tax review; this is a management planning assumption only.")

    headers = ["Person", "Initial PU Role", "PU Cost Status", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Year 1 PU-Paid Cost"]
    header_row(ws, 11, 3, headers)
    secondments = [
        ("Alexander Stulme", "General Manager", "Known — calculated from Monthly Costs"),
        ("Alan McKeon", "Technical Manager", "Known — calculated from Monthly Costs, including expat benefits"),
        ("Martin Aguero", "Infra Manager", "Salary known — $180,000/year; benefits TBD and excluded"),
    ]
    lookup_month_indexes = [8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21]
    for row, (person, role, status) in enumerate(secondments, start=12):
        set_input(ws.cell(row, 3), person, instruction_comment("Initial PU secondment as confirmed by management."))
        set_input(ws.cell(row, 4), role, instruction_comment("PU role as confirmed by management."))
        set_input(ws.cell(row, 5), status, instruction_comment(status))
        for month, (col, lookup_index) in enumerate(zip(range(6, 18), lookup_month_indexes), start=1):
            if person == "Martin Aguero":
                set_input(ws.cell(row, col), MARTIN_AGUERO_MONTHLY_SALARY, instruction_comment("Known PU-paid salary: $180,000/year or $15,000/month. Medical, housing, home leave and other benefits remain TBD and are excluded."))
            else:
                set_formula(ws.cell(row, col), f"=VLOOKUP($C{row},'Monthly Costs'!$C${DATA_START}:$X${DATA_END},{lookup_index},FALSE)", CURRENCY_FIRST if row == 12 and month == 1 else CURRENCY, cross_sheet=True)
            ws.cell(row, col).number_format = CURRENCY
        set_formula(ws.cell(row, 18), f"=SUM(F{row}:Q{row})", CURRENCY_FIRST if row == 12 else CURRENCY)
        for col in range(3, 19):
            ws.cell(row, col).alignment = Alignment(horizontal="right" if col >= 6 else "left", vertical="center", wrap_text=True)
        ws.row_dimensions[row].height = 42

    secondment_total_row = 15
    ws.merge_cells(start_row=secondment_total_row, start_column=3, end_row=secondment_total_row, end_column=5)
    ws.cell(secondment_total_row, 3, "TOTAL PU-PAID SECONDMENT COST")
    ws.cell(secondment_total_row, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    for col in range(6, 19):
        letter = get_column_letter(col)
        set_formula(ws.cell(secondment_total_row, col), f"=SUM({letter}12:{letter}14)", CURRENCY_FIRST if col == 6 else CURRENCY)
        ws.cell(secondment_total_row, col).alignment = Alignment(horizontal="right", vertical="center")
    for col in range(3, 19):
        ws.cell(secondment_total_row, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
    apply_borders(ws, 11, secondment_total_row, 3, 18)

    ws.merge_cells("C18:S18")
    ws["C18"] = "GROSS TO NET MONTHLY AND ANNUAL COST — AFTER KNOWN PU-PAID SECONDMENTS"
    ws["C18"].fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    ws["C18"].font = Font(name="Arial", size=10, bold=True, color=BLACK)
    header_row(ws, 19, 3, ["Metric", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Year 1"])
    monthly_cost_columns = list(range(10, 16)) + [18] + list(range(19, 24))
    for row, metric in enumerate(["Gross Monthly Costs", "Less: PU-Paid Secondments", "Net Cost after Known PU Secondments"], start=20):
        ws.cell(row, 3, metric).font = Font(name="Arial", size=10, bold=(row == 22), color=BLACK)
        for offset, monthly_col in enumerate(monthly_cost_columns, start=4):
            monthly_letter = get_column_letter(monthly_col)
            secondment_letter = get_column_letter(5 + (offset - 3))
            if row == 20:
                formula = f"='Monthly Costs'!{monthly_letter}{TOTAL_ROW}"
            elif row == 21:
                formula = f"={secondment_letter}{secondment_total_row}"
            else:
                formula = f"={get_column_letter(offset)}20-{get_column_letter(offset)}21"
            set_formula(ws.cell(row, offset), formula, CURRENCY_FIRST if row == 20 and offset == 4 else CURRENCY, cross_sheet=True)
            ws.cell(row, offset).alignment = Alignment(horizontal="right", vertical="center")
    set_formula(ws.cell(20, 16), f"='Monthly Costs'!X{TOTAL_ROW}", CURRENCY_FIRST, cross_sheet=True)
    set_formula(ws.cell(21, 16), f"=R{secondment_total_row}", CURRENCY)
    set_formula(ws.cell(22, 16), "=P20-P21", CURRENCY)
    apply_borders(ws, 19, 22, 3, 16)
    for col in range(3, 17):
        ws.cell(22, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))

    ws.merge_cells("C25:S27")
    ws["C25"] = (
        "Net cost is provisional. It deducts the known PU-paid modeled costs for Alexander Stulme and Alan McKeon, plus Martin Aguero's known $15,000/month salary. "
        "Martin Aguero's health care, housing, home leave and any other approved benefits remain to be defined; once entered, they will reduce the net monthly and annual budget further."
    )
    ws["C25"].font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws["C25"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    autofit(ws, 3, 19, 11, 27)
    ws.column_dimensions["C"].width = 24
    ws.column_dimensions["D"].width = 24
    ws.column_dimensions["E"].width = 38
    for col in range(6, 19):
        ws.column_dimensions[get_column_letter(col)].width = 14
    ws.print_area = "B2:S27"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.center.text = "PU Secondments | Page &P of &N"
    ws.oddFooter.center.size = 8


def build_monthly_costs(wb):
    ws = wb.create_sheet("Monthly Costs", 1)
    title_block(
        ws,
        "Monthly Personnel Cost — Salary, Health Care, M7 Transition and Alan Expat Benefits",
        "M1–M6 = Salary + Health Care | M7 includes Repatriation Package and Alan housing | M8–M12 include approved Alan expatriate benefits",
        "USD | Housing is $2,000/month from M7 for Alan's family relocation to Maracaibo | Two $6,000 home leaves scheduled in M9 and M12",
        27,
    )

    headers = [
        "Person", "Position", "M1–M6 Contract", "M7+ Employment Basis", "Salary / Month", "Health Care / Year", "Health Care / Month",
        "M1\nSalary + Health", "M2\nSalary + Health", "M3\nSalary + Health", "M4\nSalary + Health", "M5\nSalary + Health", "M6\nSalary + Health",
        "M7\nOne-Time Package", "M7\nRecurring Cost", "M7\nTotal Cost",
        "M8\nTotal Cost", "M9\nTotal Cost", "M10\nTotal Cost", "M11\nTotal Cost", "M12\nTotal Cost", "Year 1\nTotal Cost",
        "M7+ Housing\n/ Month", "Home Leave\n/ Trip", "Family Relocation\n/ City",
    ]
    header_row(ws, 8, 3, headers)
    for col in range(16, 19):
        ws.cell(8, col).fill = PatternFill("solid", fgColor=WARNING)

    for row, record in enumerate(PEOPLE, start=DATA_START):
        _, position, person, _, _, _, _, _ = record
        set_input(ws.cell(row, 3), person, instruction_comment("Linked by name to the Personnel classification; this cost view excludes the COO."))
        set_input(ws.cell(row, 4), position, source_comment("Position"))
        set_formula(ws.cell(row, 5), f"=VLOOKUP(C{row},Personnel!$E${DATA_START}:$I${DATA_END},2,FALSE)", cross_sheet=True)
        set_formula(ws.cell(row, 6), f"=VLOOKUP(C{row},Personnel!$E${DATA_START}:$I${DATA_END},5,FALSE)", cross_sheet=True)
        set_formula(ws.cell(row, 7), f"=VLOOKUP(C{row},Personnel!$E${DATA_START}:$Y${DATA_END},21,FALSE)/12", CURRENCY_FIRST if row == DATA_START else CURRENCY, cross_sheet=True)
        set_input(
            ws.cell(row, 8), MEDICAL_INSURANCE_ANNUAL[person],
            source_comment("Medical Insurance (Annual)", "Operations Support amount is retained only as a budget placeholder until the person is selected."),
        )
        ws.cell(row, 8).number_format = CURRENCY
        set_formula(ws.cell(row, 9), f"=H{row}/12", CURRENCY)
        set_formula(ws.cell(row, 25), f'=IF(C{row}="Alan McKeon",\'Alan Expat Package\'!$D$9,0)', CURRENCY, cross_sheet=True)
        set_formula(ws.cell(row, 26), f'=IF(C{row}="Alan McKeon",\'Alan Expat Package\'!$D$10,0)', CURRENCY, cross_sheet=True)
        set_formula(ws.cell(row, 27), f'=IF(C{row}="Alan McKeon",\'Alan Expat Package\'!$D$14,"Not applicable")', cross_sheet=True)
        for col in range(10, 16):
            set_formula(ws.cell(row, col), f"=$G{row}+$I{row}", CURRENCY_FIRST if row == DATA_START and col == 10 else CURRENCY)
        set_formula(ws.cell(row, 16), f'=IF($E{row}="Repatriate",$G{row}*\'Repatriation Package\'!$D$15,0)', CURRENCY_FIRST if row == DATA_START else CURRENCY, cross_sheet=True)
        set_formula(ws.cell(row, 17), f"=$G{row}+$I{row}+$Y{row}", CURRENCY_FIRST if row == DATA_START else CURRENCY)
        set_formula(ws.cell(row, 18), f"=P{row}+Q{row}", CURRENCY_FIRST if row == DATA_START else CURRENCY)
        for month, col in zip(range(8, 13), range(19, 24)):
            home_leave = f"+IF({month}='Alan Expat Package'!$D$12,$Z{row},0)+IF({month}='Alan Expat Package'!$D$13,$Z{row},0)"
            set_formula(ws.cell(row, col), f"=$G{row}+$I{row}+$Y{row}{home_leave}", CURRENCY_FIRST if row == DATA_START and col == 19 else CURRENCY, cross_sheet=True)
        set_formula(ws.cell(row, 24), f"=SUM(J{row}:O{row})+R{row}+SUM(S{row}:W{row})", CURRENCY_FIRST if row == DATA_START else CURRENCY)
        for col in range(3, 28):
            ws.cell(row, col).alignment = Alignment(
                horizontal="right" if col in range(7, 27) else "left",
                vertical="center",
                wrap_text=col in (3, 4, 5, 6, 27),
            )
        for col in range(16, 19):
            ws.cell(row, col).fill = PatternFill("solid", fgColor="FFF2CC")
        ws.row_dimensions[row].height = 32

    ws.merge_cells(start_row=TOTAL_ROW, start_column=3, end_row=TOTAL_ROW, end_column=6)
    ws.cell(TOTAL_ROW, 3, "TOTAL — 8 POSITIONS (COO EXCLUDED)")
    ws.cell(TOTAL_ROW, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    for col in range(7, 27):
        letter = get_column_letter(col)
        set_formula(ws.cell(TOTAL_ROW, col), f"=SUM({letter}{DATA_START}:{letter}{DATA_END})", CURRENCY_FIRST if col == 7 else CURRENCY)
        ws.cell(TOTAL_ROW, col).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(TOTAL_ROW, 27, "Alan family relocation to Maracaibo")
    ws.cell(TOTAL_ROW, 27).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    ws.cell(TOTAL_ROW, 27).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    for col in range(3, 28):
        ws.cell(TOTAL_ROW, col).border = Border(top=Side(style="medium", color=BLACK), bottom=Side(style="double", color=BLACK))
        if col in range(16, 19):
            ws.cell(TOTAL_ROW, col).fill = PatternFill("solid", fgColor="FFF2CC")

    summary_title_row = TOTAL_ROW + 3
    ws.merge_cells(start_row=summary_title_row, start_column=3, end_row=summary_title_row, end_column=8)
    ws.cell(summary_title_row, 3, "COST SUMMARY")
    ws.cell(summary_title_row, 3).fill = PatternFill("solid", fgColor=LIGHT_GREEN)
    ws.cell(summary_title_row, 3).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    header_row(ws, summary_title_row + 1, 3, ["Metric", "Amount", "Formula / Meaning"])
    summary = [
        ("Monthly salary", f"=G{TOTAL_ROW}", "Recurring base salary cost"),
        ("Monthly health care", f"=I{TOTAL_ROW}", "Recurring medical insurance cost"),
        ("M1–M6 recurring monthly cost", f"=J{TOTAL_ROW}", "Salary + health care before M7"),
        ("M7 one-time package", f"=P{TOTAL_ROW}", "Repatriation / localisation package for the three repatriates"),
        ("Alan M7+ housing allowance", f"=Y{TOTAL_ROW}", "Six months at $2,000/month for family relocation to Maracaibo"),
        ("Alan home leave cost", f"=Z{TOTAL_ROW}*{ALAN_HOME_LEAVE_TRIPS}", "Two trips at $6,000 each, scheduled in M9 and M12"),
        ("M7 recurring cost", f"=Q{TOTAL_ROW}", "Salary + health care plus Alan's approved housing allowance"),
        ("M7 total cost", f"=R{TOTAL_ROW}", "One-time package + recurring M7 cost"),
        ("Year 1 recurring cost", f"=SUM(J{TOTAL_ROW}:O{TOTAL_ROW})+Q{TOTAL_ROW}+SUM(S{TOTAL_ROW}:W{TOTAL_ROW})", "Salary + health care, Alan housing from M7 and two home leaves"),
        ("Year 1 one-time package", f"=P{TOTAL_ROW}", "M7 transition package only"),
        ("Year 1 total personnel cost", f"=X{TOTAL_ROW}", "All modeled salary, health care, Alan expat benefits and the one-time M7 package"),
    ]
    for row, (metric, formula, meaning) in enumerate(summary, start=summary_title_row + 2):
        ws.cell(row, 3, metric).font = Font(name="Arial", size=10, color=BLACK)
        set_formula(ws.cell(row, 4), formula, CURRENCY_FIRST if row == summary_title_row + 2 else CURRENCY)
        ws.cell(row, 5, meaning).font = Font(name="Arial", size=10, color=BLACK)
        ws.cell(row, 5).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    apply_borders(ws, summary_title_row + 1, summary_title_row + 1 + len(summary), 3, 5)

    ws.merge_cells(start_row=summary_title_row, start_column=10, end_row=summary_title_row + 4, end_column=27)
    ws.cell(summary_title_row, 10, (
        "Cost basis: from M7 onward, the recurring model is Salary + Health Care for all personnel, plus Alan McKeon's approved $2,000/month housing allowance for family relocation to Maracaibo. "
        "Alan also receives two $6,000 home leaves, planned in M9 and M12. M7 separately adds the one-time Repatriation / Localisation Transition Package for eligible Repatriates. "
        "Housing for any future family relocation to Maracaibo should be modeled at a minimum of $2,000/month after management approval. Tax, social charges, statutory benefits, transport, hotel/staff house and any other benefits remain outside this Monthly Costs view unless separately approved."
    ))
    ws.cell(summary_title_row, 10).font = Font(name="Arial", size=10, bold=True, color="C00000")
    ws.cell(summary_title_row, 10).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws.cell(summary_title_row, 10).comment = compliance_comment("This cost view is a management planning model and is not a payroll or statutory-benefit determination.")

    apply_borders(ws, 8, DATA_END, 3, 27)
    ws.freeze_panes = "J9"
    autofit(ws, 3, 27, 8, summary_title_row + 1 + len(summary))
    ws.column_dimensions["C"].width = 25
    ws.column_dimensions["D"].width = 34
    ws.column_dimensions["E"].width = 17
    ws.column_dimensions["F"].width = 22
    for col in range(7, 27):
        ws.column_dimensions[get_column_letter(col)].width = 15
    ws.column_dimensions["X"].width = 17
    ws.column_dimensions["Y"].width = 16
    ws.column_dimensions["Z"].width = 16
    ws.column_dimensions["AA"].width = 28
    ws.print_area = f"B2:AA{summary_title_row + 1 + len(summary)}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.center.text = "Monthly Costs | Page &P of &N"
    ws.oddFooter.center.size = 8


def build():
    if not SOURCE_IMAGE.exists():
        raise FileNotFoundError(SOURCE_IMAGE)
    wb = Workbook()
    build_personnel(wb)
    build_monthly_costs(wb)
    build_alan_expat_package(wb)
    build_repatriation_package(wb)
    build_pu_secondments(wb)
    build_rules(wb)
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    wb.save(OUT)
    print(OUT)


def validate():
    wb = load_workbook(OUT, data_only=False)
    assert wb.sheetnames == ["Personnel", "Monthly Costs", "Alan Expat Package", "Repatriation Package", "PU Secondments", "Contract Rules"]
    ws = wb["Personnel"]
    expected_names = [record[2] for record in PEOPLE]
    expected_salaries = [record[3] for record in PEOPLE]
    assert [ws[f"E{row}"].value for row in range(DATA_START, DATA_END + 1)] == expected_names
    assert [ws[f"Y{row}"].value for row in range(DATA_START, DATA_END + 1)] == expected_salaries
    assert sum(expected_salaries) == 1_188_000
    for col in range(13, 25):
        assert ws.cell(9, col).value == "=$Y9/12"
    assert ws["G9"].value == '=IF(F9="Expat","Yes","No")'
    assert ws["I9"].value == '=IF(F9="Repatriate","Local — Venezuela",F9)'
    assert ws["J9"].value == f"Eligible — one-time; {CORE_TRANSITION_MULTIPLIER:.2f}x monthly salary"
    assert ws["J12"].value == "Not applicable"
    assert ws[f"E{DATA_END}"].value == "TBD — Person to be defined"
    assert ws[f"F{DATA_END}"].value == "TBD"
    assert ws[f"H{DATA_END}"].value == "TBD"
    assert [ws[f"F{row}"].value for row in range(DATA_START, DATA_END + 1)].count("Expat") == 2
    assert [ws[f"F{row}"].value for row in range(DATA_START, DATA_END + 1)].count("Repatriate") == 3
    assert [ws[f"F{row}"].value for row in range(DATA_START, DATA_END + 1)].count("Local") == 2
    assert [ws[f"F{row}"].value for row in range(DATA_START, DATA_END + 1)].count("TBD") == 1
    assert [ws[f"H{row}"].value for row in range(DATA_START, DATA_END + 1)].count("Rotation") == 1
    assert [ws[f"H{row}"].value for row in range(DATA_START, DATA_END + 1)].count("Fixed") == 6
    assert [ws[f"H{row}"].value for row in range(DATA_START, DATA_END + 1)].count("TBD") == 1
    rules = wb["Contract Rules"]
    assert [rules[f"C{row}"].value for row in range(9, 13)] == ["Expat", "Repatriate", "Local", "TBD"]
    assert rules["J10"].value.startswith("Eligible once at M7")
    package = wb["Repatriation Package"]
    component_start = 10
    component_end = component_start + len(REPATRIATION_COMPONENTS) - 1
    core_total_row = component_end + 1
    excluded_header_row = core_total_row + 3
    calc_header_row = excluded_header_row + len([
        "Base salary", "Medical insurance", "Housing / staff house / hotel", "Company transport to work", "Home leave, stock options, annual incentive and vacation", "Venezuelan statutory payroll benefits and taxes",
    ]) + 4
    calc_start = calc_header_row + 2
    assert package[f"D{component_end}"].value == 0.10
    assert package[f"D{core_total_row}"].value == f"=SUM(D{component_start}:D{component_end})"
    assert package[f"F{calc_start}"].value == f"=$D${core_total_row}"
    assert package[f"G{calc_start}"].value == f"=E{calc_start}*F{calc_start}"
    assert package[f"H{calc_start}"].value == f"=VLOOKUP(C{calc_start},Personnel!$E${DATA_START}:$I${DATA_END},5,FALSE)"
    assert len([record for record in PEOPLE if record[4] == "Repatriate"]) == 3
    assert CORE_TRANSITION_MULTIPLIER == 1.50
    monthly = wb["Monthly Costs"]
    assert monthly["H9"].value == 12000
    assert monthly["I9"].value == "=H9/12"
    assert monthly["J9"].value == "=$G9+$I9"
    assert monthly["P9"].value == '=IF($E9="Repatriate",$G9*\'Repatriation Package\'!$D$15,0)'
    assert monthly["Q9"].value == "=$G9+$I9+$Y9"
    assert monthly["R9"].value == "=P9+Q9"
    assert monthly[f"P{TOTAL_ROW}"].value == f"=SUM(P{DATA_START}:P{DATA_END})"
    assert monthly[f"X{TOTAL_ROW}"].value == f"=SUM(X{DATA_START}:X{DATA_END})"
    assert monthly["Y12"].value == "=IF(C12=\"Alan McKeon\",'Alan Expat Package'!$D$9,0)"
    assert monthly["Z12"].value == "=IF(C12=\"Alan McKeon\",'Alan Expat Package'!$D$10,0)"
    assert monthly["AA12"].value == "=IF(C12=\"Alan McKeon\",'Alan Expat Package'!$D$14,\"Not applicable\")"
    assert sum(MEDICAL_INSURANCE_ANNUAL.values()) == 88_000
    alan_package = wb["Alan Expat Package"]
    assert alan_package["D9"].value == ALAN_HOUSING_ALLOWANCE_MONTHLY
    assert alan_package["D10"].value == ALAN_HOME_LEAVE_PER_TRIP
    assert alan_package["D11"].value == ALAN_HOME_LEAVE_TRIPS
    assert alan_package["D12"].value == ALAN_HOME_LEAVE_MONTHS[0]
    assert alan_package["D13"].value == ALAN_HOME_LEAVE_MONTHS[1]
    assert alan_package["D14"].value == "Maracaibo"
    secondments = wb["PU Secondments"]
    assert [secondments[f"C{row}"].value for row in range(12, 15)] == ["Alexander Stulme", "Alan McKeon", "Martin Aguero"]
    assert secondments["F14"].value == MARTIN_AGUERO_MONTHLY_SALARY
    assert secondments["D22"].value == "=D20-D21"
    assert secondments["P22"].value == "=P20-P21"
    print("VALIDATED: 8 positions (COO excluded; Operations Support person TBD) | Alan housing and home leaves included | known PU-paid secondments deducted from net cost")


if __name__ == "__main__":
    build()
    validate()
