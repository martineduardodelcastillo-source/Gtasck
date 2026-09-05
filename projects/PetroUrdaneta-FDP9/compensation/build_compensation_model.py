from pathlib import Path
from datetime import date

from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation


OUT_DIR = Path(__file__).resolve().parent
OUT_FILE = OUT_DIR / "modelo_paquetes_personal_2_etapas.xlsx"
SOURCE_IMAGE = OUT_DIR / "source" / "package_source_2026-09-05.jpeg"

DARK_GREEN = "135B44"
LIGHT_GREEN = "CFE9E0"
LIGHT_GRAY = "E7E5E4"
WHITE = "FFFFFF"
BLACK = "000000"
BLUE = "0000FF"
GREEN = "008000"
RED = "C00000"
GRAY = "666666"
THIN_GRAY = Side(style="thin", color="B7B7B7")
MEDIUM_GREEN = Side(style="medium", color=DARK_GREEN)
DOUBLE_BLACK = Side(style="double", color=BLACK)

CURRENCY_FIRST = '$#,##0.0;($#,##0.0);-'
CURRENCY = '#,##0.0;(#,##0.0);-'
PERCENT = '#,##0.0%'
INTEGER = '#,##0'

SOURCE_DATE = "5 de septiembre de 2026"
SOURCE_NAME = "Tabla de paquetes de personal suministrada por el usuario"

PEOPLE = [
    (1, "COO / PU General Manager", "Martin del Castillo", 360000, 36000, 12000, 20000, 24000, 72000, 524000),
    (2, "EPCM & Engineering Manager", "Juan Conde", 216000, 24000, 12000, 12000, 18000, 43200, 325200),
    (3, "Drilling & Well Services Manager", "Alexander Stulme", 180000, 24000, 12000, 12000, 18000, 36000, 282000),
    (4, "Operations & Maintenance Manager", "Félix Valderrama", 216000, 24000, 12000, 12000, 18000, 43200, 325200),
    (5, "Technical Manager (Geosciences)", "Alan McKeon", 180000, 24000, 12000, 12000, 18000, 36000, 282000),
    (6, "Reservoir Engineer", "JJI", 120000, 18000, 12000, 12000, 12000, 20000, 194000),
    (7, "Rig Company Man", "Marcelo Dantas", 180000, 24000, 12000, 12000, 18000, 36000, 282000),
    (8, "Planning & PMO", "Jose Miguel", 48000, 12000, 8000, 0, 7200, 12000, 87200),
    (9, "Operations Support", "Leticia Almeida", 48000, 12000, 8000, 12000, 7200, 8000, 95200),
]


def source_comment(row_no: int, field: str) -> Comment:
    return Comment(
        f"Fuente: {SOURCE_NAME}. Fecha: {SOURCE_DATE}. Fila {row_no}, campo '{field}'. "
        f"Archivo: {SOURCE_IMAGE.name}.",
        "Manus",
    )


def assumption_comment(text: str) -> Comment:
    return Comment(
        f"Fuente: supuesto presupuestario del modelo preparado el {SOURCE_DATE}. {text}",
        "Manus",
    )


def set_title(ws, title: str, end_col: int):
    for col in range(3, end_col + 1):
        cell = ws.cell(3, col)
        cell.fill = PatternFill("solid", fgColor=DARK_GREEN)
        cell.font = Font(name="Arial", size=16, bold=True, color=WHITE)
        cell.alignment = Alignment(vertical="center")
    ws.merge_cells(start_row=3, start_column=3, end_row=3, end_column=end_col)
    ws.cell(3, 3, title)
    ws.row_dimensions[3].height = 25


def setup_sheet(ws, title: str, subtitle: str, units: str, end_col: int):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 20
    set_title(ws, title, end_col)
    ws.cell(5, 3, subtitle).font = Font(name="Arial", size=11, bold=True, color=BLACK)
    ws.cell(6, 3, units).font = Font(name="Arial", size=10, italic=True, color=GRAY)
    ws.freeze_panes = None
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.oddFooter.center.text = f"{ws.title} | Página &P de &N"
    ws.oddFooter.center.size = 8
    ws.oddFooter.center.color = GRAY


def section_bar(ws, row: int, title: str, start_col: int, end_col: int):
    for col in range(start_col, end_col + 1):
        cell = ws.cell(row, col)
        cell.fill = PatternFill("solid", fgColor=LIGHT_GREEN)
        cell.font = Font(name="Arial", size=10, bold=True, color=BLACK)
        cell.border = Border(bottom=MEDIUM_GREEN)
    ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
    ws.cell(row, start_col, title)
    ws.row_dimensions[row].height = 20


def table_header(ws, row: int, start_col: int, headers):
    for offset, header in enumerate(headers):
        cell = ws.cell(row, start_col + offset, header)
        cell.font = Font(name="Arial", size=9, bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=DARK_GREEN)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(top=MEDIUM_GREEN, bottom=MEDIUM_GREEN)
    ws.row_dimensions[row].height = 34


def format_input(cell, number_format=None, comment=None, alignment=None):
    cell.font = Font(name="Arial", size=10, color=BLUE)
    if number_format:
        cell.number_format = number_format
    if comment:
        cell.comment = comment
    if alignment:
        cell.alignment = alignment


def format_formula(cell, number_format=None, cross_sheet=False, bold=False):
    cell.font = Font(name="Arial", size=10, color=GREEN if cross_sheet else BLACK, bold=bold)
    if number_format:
        cell.number_format = number_format
    cell.alignment = Alignment(horizontal="right", vertical="center")


def apply_body_borders(ws, start_row: int, end_row: int, start_col: int, end_col: int):
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            cell = ws.cell(row, col)
            top = THIN_GRAY if row > start_row else Side(style=None)
            bottom = THIN_GRAY if row < end_row else Side(style="thin", color=BLACK)
            cell.border = Border(top=top, bottom=bottom)


def auto_fit(ws, start_col: int, end_col: int, ranges, min_width=11, max_width=34):
    for col in range(start_col, end_col + 1):
        max_len = 0
        for start_row, end_row in ranges:
            for row in range(start_row, end_row + 1):
                value = ws.cell(row, col).value
                if value is None:
                    continue
                text = str(value)
                if text.startswith("="):
                    text = ws.cell(10, col).value if ws.cell(10, col).value else "0"
                    text = str(text)
                max_len = max(max_len, max(len(line) for line in text.split("\n")))
        ws.column_dimensions[ws.cell(1, col).column_letter].width = min(max(max_len + 2, min_width), max_width)


def build_supuestos(wb):
    ws = wb.create_sheet("Supuestos")
    setup_sheet(
        ws,
        "Supuestos y política de paquetes",
        "Variables editables para el modelo de compensación en dos etapas",
        "USD, salvo indicación contraria | Celdas azules = entradas editables",
        10,
    )

    section_bar(ws, 8, "SUPUESTOS DE DURACIÓN Y FISCALIDAD", 3, 6)
    labels = [
        (9, "Meses de la etapa 1 — Consultor", 6, INTEGER, "Duración solicitada por la gerencia: primeros seis meses como consultor."),
        (10, "Meses de la etapa 2 — Repatriado / Expatriado", 6, INTEGER, "Segundo bloque presupuestario del año: meses 7 a 12."),
        (11, "Factor de Tax & Social en la etapa 1", 0.0, PERCENT, "Supuesto gerencial: no se carga Tax & Social venezolano durante la etapa de consultoría. Requiere validación legal y fiscal independiente."),
    ]
    for row, label, value, fmt, note in labels:
        ws.cell(row, 3, label).font = Font(name="Arial", size=10, color=BLACK)
        ws.cell(row, 4, value)
        format_input(ws.cell(row, 4), fmt, assumption_comment(note), Alignment(horizontal="right", vertical="center"))
    apply_body_borders(ws, 9, 11, 3, 4)

    section_bar(ws, 14, "POLÍTICA AUTOMÁTICA DE VIVIENDA POR CIUDAD", 3, 6)
    table_header(ws, 15, 3, ["Ciudad", "Housing automático", "Racional presupuestario", "Editable"])
    city_rows = [
        ("Caracas", "Sí", "Se presupone allowance si la persona debe residir en Caracas.", "Sí"),
        ("Maracaibo", "No", "Se presupone sin allowance para repatriados radicados en Maracaibo.", "Sí"),
        ("Otro", "Sí", "Enfoque conservador hasta confirmar alojamiento.", "Sí"),
        ("Por definir", "Por definir", "El cálculo conservador incluye vivienda si el paquete es repatriado.", "Sí"),
    ]
    for idx, row_values in enumerate(city_rows, start=16):
        for col, value in enumerate(row_values, start=3):
            ws.cell(idx, col, value)
            ws.cell(idx, col).font = Font(name="Arial", size=10, color=BLACK)
            ws.cell(idx, col).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        format_input(
            ws.cell(idx, 4),
            comment=assumption_comment(
                f"Política automática de vivienda para la ciudad '{row_values[0]}'. Puede modificarse por decisión gerencial."
            ),
            alignment=Alignment(horizontal="center", vertical="center"),
        )
    apply_body_borders(ws, 16, 19, 3, 6)

    section_bar(ws, 22, "COMPONENTES DE CADA PAQUETE", 3, 8)
    table_header(ws, 23, 3, ["Componente", "Consultor M1–M6", "Repatriado M7+", "Expatriado M7+", "Criterio", "Observación"])
    package_rows = [
        ("Compensación base", "Sí — honorario prorrateado", "Sí — salario local", "Sí — salario base", "Valor fuente por persona", "El modelo usa 6/12 del importe anual en cada etapa."),
        ("Housing", "Sí", "Condicional por ciudad / override", "Sí", "Valor fuente por persona", "Caracas = Sí y Maracaibo = No como política inicial editable."),
        ("Seguro médico", "Sí", "Sí", "Sí", "Valor fuente por persona", "Prorrateado por meses."),
        ("Home leave", "Sí", "No", "Sí", "Valor fuente por persona", "Se elimina en el paquete de repatriado."),
        ("Vehículo", "Sí", "Sí", "Sí", "Valor fuente por persona", "Prorrateado por meses."),
        ("Tax & Social", "No", "Sí", "Sí", "Valor fuente por persona", "M1–M6 usa factor 0%; M7+ conserva el valor anual prorrateado."),
        ("Costos únicos de transición", "No incluidos", "Entrada individual", "Entrada individual", "Cotizaciones pendientes", "El modelo parte de $0 hasta recibir presupuestos de viaje, mudanza, permisos y alojamiento temporal."),
    ]
    for r, values in enumerate(package_rows, start=24):
        for c, value in enumerate(values, start=3):
            cell = ws.cell(r, c, value)
            cell.font = Font(name="Arial", size=9, color=BLACK)
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.row_dimensions[r].height = 34
    apply_body_borders(ws, 24, 30, 3, 8)

    section_bar(ws, 33, "ADVERTENCIA DE CUMPLIMIENTO", 3, 10)
    warning = (
        "El tratamiento de los meses 1–6 como consultoría sin Tax & Social venezolano es un supuesto "
        "presupuestario indicado por la gerencia, no una conclusión jurídica. La condición migratoria de turista "
        "no acredita por sí sola autorización para trabajar ni exención fiscal. Antes de implementar el esquema, "
        "se requiere validación escrita de asesores venezolanos de inmigración, derecho laboral, nómina y tributos."
    )
    ws.merge_cells(start_row=34, start_column=3, end_row=36, end_column=10)
    ws.cell(34, 3, warning)
    ws.cell(34, 3).font = Font(name="Arial", size=10, bold=True, color=RED)
    ws.cell(34, 3).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws.row_dimensions[34].height = 30
    ws.row_dimensions[35].height = 30
    ws.row_dimensions[36].height = 30

    ws.print_area = "B2:J36"
    auto_fit(ws, 3, 10, [(9, 11), (15, 19), (23, 30)], min_width=12, max_width=34)
    return ws


def build_personal(wb):
    ws = wb.create_sheet("Personal")
    setup_sheet(
        ws,
        "Modelo de paquetes por persona",
        "Etapa 1: seis meses como consultor | Etapa 2: repatriado o expatriado desde el mes 7",
        "USD | Celdas azules = datos fuente o decisiones editables; fórmulas verdes = vínculos a Supuestos",
        32,
    )

    section_bar(ws, 8, "BASE DE COMPENSACIÓN Y CÁLCULO POR PERSONA", 3, 32)
    headers = [
        "#", "Position", "Person", "Base Salary\nAnnual", "Housing\nAnnual", "Medical\nAnnual", "Home Leave\nAnnual", "Vehicle\nAnnual", "Tax & Social\nAnnual", "Calculated\nAnnual", "Stated\nAnnual", "Variance",
        "Consulting Fee\nM1–M6", "Housing\nM1–M6", "Medical\nM1–M6", "Home Leave\nM1–M6", "Vehicle\nM1–M6", "Tax & Social\nM1–M6", "Stage 1\nTotal",
        "Package\nM7+", "City\nM7+", "Housing\nOverride", "Housing\nFinal", "One-time\nTransition", "Stage 2 Recurring\nM7–M12", "Stage 2\nTotal", "Year 1\nTotal", "Savings vs.\nSource", "Annual Run-rate\nM13+", "Decision\nStatus",
    ]
    table_header(ws, 10, 3, headers)

    package_validation = DataValidation(type="list", formula1='"Expatriado,Repatriado,Por definir"', allow_blank=False)
    city_validation = DataValidation(type="list", formula1='"Caracas,Maracaibo,Otro,Por definir"', allow_blank=False)
    housing_validation = DataValidation(type="list", formula1='"Automático,Sí,No"', allow_blank=False)
    ws.add_data_validation(package_validation)
    ws.add_data_validation(city_validation)
    ws.add_data_validation(housing_validation)

    for excel_row, data in enumerate(PEOPLE, start=11):
        number, position, person, base, housing, medical, leave, vehicle, tax, stated = data
        raw_values = [number, position, person, base, housing, medical, leave, vehicle, tax]
        fields = ["#", "Position", "Person", "Base Salary (Annual)", "Housing (Annual)", "Medical Insurance", "Home Leave", "Company Vehicle", "Tax & Social"]
        for offset, (value, field) in enumerate(zip(raw_values, fields), start=3):
            cell = ws.cell(excel_row, offset, value)
            fmt = CURRENCY_FIRST if offset == 6 else CURRENCY if offset >= 6 else None
            align = Alignment(horizontal="right" if offset >= 6 or offset == 3 else "left", vertical="center")
            format_input(cell, fmt, source_comment(number, field), align)
        ws.cell(excel_row, 12, f"=SUM(F{excel_row}:K{excel_row})")
        format_formula(ws.cell(excel_row, 12), CURRENCY_FIRST)
        ws.cell(excel_row, 13, stated)
        format_input(ws.cell(excel_row, 13), CURRENCY, source_comment(number, "TOTAL Annual Package"), Alignment(horizontal="right", vertical="center"))
        ws.cell(excel_row, 14, f"=L{excel_row}-M{excel_row}")
        format_formula(ws.cell(excel_row, 14), CURRENCY)

        stage1_formulas = {
            15: f"=F{excel_row}/12*'Supuestos'!$D$9",
            16: f"=G{excel_row}/12*'Supuestos'!$D$9",
            17: f"=H{excel_row}/12*'Supuestos'!$D$9",
            18: f"=I{excel_row}/12*'Supuestos'!$D$9",
            19: f"=J{excel_row}/12*'Supuestos'!$D$9",
            20: f"=K{excel_row}/12*'Supuestos'!$D$9*'Supuestos'!$D$11",
            21: f"=SUM(O{excel_row}:T{excel_row})",
        }
        for col, formula in stage1_formulas.items():
            ws.cell(excel_row, col, formula)
            format_formula(ws.cell(excel_row, col), CURRENCY_FIRST if col == 15 else CURRENCY, cross_sheet=(col != 21), bold=(col == 21))

        defaults = {
            22: ("Expatriado", "Clasificación inicial conservadora: se mantiene el paquete fuente hasta que la gerencia designe quién será repatriado."),
            23: ("Por definir", "La ciudad debe decidirse para aplicar la política de vivienda."),
            24: ("Automático", "Usa la política de ciudad de la hoja Supuestos; puede reemplazarse por Sí o No."),
            26: (0, "Entrada pendiente de cotizaciones: mudanza, viaje, permisos, asesoría, alojamiento temporal y settling-in."),
        }
        for col, (value, note) in defaults.items():
            ws.cell(excel_row, col, value)
            fmt = CURRENCY_FIRST if col == 26 else None
            align = Alignment(horizontal="right" if col == 26 else "center", vertical="center")
            format_input(ws.cell(excel_row, col), fmt, assumption_comment(note), align)

        ws.cell(excel_row, 25, f'=IF(X{excel_row}="Automático",IF(W{excel_row}="Caracas","Sí",IF(W{excel_row}="Maracaibo","No",IF(W{excel_row}="Otro","Sí","Por definir"))),X{excel_row})')
        format_formula(ws.cell(excel_row, 25), cross_sheet=False)
        ws.cell(excel_row, 25).alignment = Alignment(horizontal="center", vertical="center")

        stage2 = (
            f'=IF(V{excel_row}="Expatriado",L{excel_row}/12*\'Supuestos\'!$D$10,'
            f'IF(V{excel_row}="Repatriado",(F{excel_row}+H{excel_row}+J{excel_row}+K{excel_row}+'
            f'IF(Y{excel_row}="No",0,G{excel_row}))/12*\'Supuestos\'!$D$10,0))'
        )
        ws.cell(excel_row, 27, stage2)
        format_formula(ws.cell(excel_row, 27), CURRENCY_FIRST, cross_sheet=True)
        ws.cell(excel_row, 28, f"=AA{excel_row}+Z{excel_row}")
        format_formula(ws.cell(excel_row, 28), CURRENCY, bold=True)
        ws.cell(excel_row, 29, f"=U{excel_row}+AB{excel_row}")
        format_formula(ws.cell(excel_row, 29), CURRENCY, bold=True)
        ws.cell(excel_row, 30, f"=M{excel_row}-AC{excel_row}")
        format_formula(ws.cell(excel_row, 30), CURRENCY)
        ws.cell(excel_row, 31, (
            f'=IF(V{excel_row}="Expatriado",M{excel_row},IF(V{excel_row}="Repatriado",'
            f'F{excel_row}+H{excel_row}+J{excel_row}+K{excel_row}+IF(Y{excel_row}="No",0,G{excel_row}),0))'
        ))
        format_formula(ws.cell(excel_row, 31), CURRENCY)
        ws.cell(excel_row, 32, (
            f'=IF(V{excel_row}="Por definir","Definir paquete",IF(W{excel_row}="Por definir","Definir ciudad",'
            f'IF(AND(V{excel_row}="Repatriado",Y{excel_row}="Por definir"),"Definir vivienda","Completo")))'
        ))
        format_formula(ws.cell(excel_row, 32))
        ws.cell(excel_row, 32).alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        package_validation.add(ws.cell(excel_row, 22))
        city_validation.add(ws.cell(excel_row, 23))
        housing_validation.add(ws.cell(excel_row, 24))
        ws.row_dimensions[excel_row].height = 28

    total_row = 21
    ws.cell(total_row, 4, "TOTAL — 9 POSICIONES")
    ws.cell(total_row, 4).font = Font(name="Arial", size=10, bold=True, color=BLACK)
    ws.merge_cells(start_row=total_row, start_column=4, end_row=total_row, end_column=5)
    for col in list(range(6, 22)) + list(range(26, 32)):
        letter = ws.cell(1, col).column_letter
        ws.cell(total_row, col, f"=SUM({letter}11:{letter}19)")
        cross = False
        format_formula(ws.cell(total_row, col), CURRENCY_FIRST if col in (6, 15, 26) else CURRENCY, cross_sheet=cross, bold=True)
    for col in range(3, 33):
        cell = ws.cell(total_row, col)
        cell.border = Border(top=MEDIUM_GREEN, bottom=DOUBLE_BLACK)
    ws.row_dimensions[total_row].height = 24

    ws.conditional_formatting.add(
        "AF11:AF19",
        FormulaRule(formula=['AF11<>"Completo"'], font=Font(color=RED, bold=True)),
    )
    ws.auto_filter.ref = "C10:AF19"
    ws.freeze_panes = "F11"
    ws.print_title_rows = "10:10"
    ws.print_area = "B2:AF21"

    auto_fit(ws, 3, 32, [(10, 21)], min_width=11, max_width=28)
    ws.column_dimensions["D"].width = 33
    ws.column_dimensions["E"].width = 23
    ws.column_dimensions["AF"].width = 18
    return ws


def build_resumen(wb):
    ws = wb.create_sheet("Resumen", 0)
    setup_sheet(
        ws,
        "Resumen ejecutivo — Paquetes de personal",
        "Presupuesto por persona en dos etapas y escenarios de decisión desde el mes 7",
        "USD | Escenarios de repatriación excluyen costos únicos de transición hasta recibir cotizaciones",
        12,
    )

    section_bar(ws, 8, "INDICADORES DEL ESCENARIO SELECCIONADO", 3, 7)
    table_header(ws, 9, 3, ["Indicador", "Valor", "Interpretación", "Fuente", "Estado"])
    kpis = [
        ("Costo anual original", "='Personal'!M21", "Paquete anual fuente para 9 posiciones", "Tabla suministrada", "Referencia"),
        ("Etapa 1 — Consultor M1–M6", "='Personal'!U21", "Todos los componentes no fiscales prorrateados por seis meses", "Modelo", "Calculado"),
        ("Etapa 2 — Selección M7–M12", "='Personal'!AB21", "Paquete y ciudad elegidos por persona, más costos únicos", "Modelo", "Pendiente de decisiones"),
        ("Costo total Año 1", "='Personal'!AC21", "Etapa 1 + etapa 2 seleccionada", "Modelo", "Calculado"),
        ("Ahorro / (sobrecosto) vs. fuente", "='Personal'!AD21", "Costo anual original menos Año 1 seleccionado", "Modelo", "Calculado"),
        ("Run-rate anual desde M13", "='Personal'!AE21", "Costo anual recurrente posterior a la transición", "Modelo", "Calculado"),
        ("Personas con decisión pendiente", '=COUNTIF(\'Personal\'!AF11:AF19,"<>Completo")', "Requieren paquete, ciudad o vivienda", "Modelo", "Acción requerida"),
    ]
    for row_idx, (label, formula, interpretation, source, status) in enumerate(kpis, start=10):
        ws.cell(row_idx, 3, label)
        ws.cell(row_idx, 3).font = Font(name="Arial", size=10, color=BLACK, bold=row_idx in (10, 13, 14, 15))
        ws.cell(row_idx, 4, formula)
        num_fmt = INTEGER if row_idx == 16 else CURRENCY_FIRST
        format_formula(ws.cell(row_idx, 4), num_fmt, cross_sheet=True, bold=row_idx in (10, 13, 14, 15))
        for col, value in zip((5, 6, 7), (interpretation, source, status)):
            ws.cell(row_idx, col, value)
            ws.cell(row_idx, col).font = Font(name="Arial", size=9, color=BLACK)
            ws.cell(row_idx, col).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.row_dimensions[row_idx].height = 30
    apply_body_borders(ws, 10, 16, 3, 7)

    section_bar(ws, 19, "COMPARACIÓN DE ESCENARIOS — 9 POSICIONES", 3, 8)
    table_header(ws, 20, 3, ["Escenario", "Etapa 1 M1–M6", "Etapa 2 M7–M12", "Costo Año 1", "Ahorro vs. fuente", "Run-rate M13+"])
    scenarios = [
        (
            "Selección actual por persona",
            "='Personal'!U21",
            "='Personal'!AB21",
            "='Personal'!AC21",
            "='Personal'!AD21",
            "='Personal'!AE21",
        ),
        (
            "Todos expatriados",
            "='Personal'!U21",
            "='Personal'!M21/12*'Supuestos'!$D$10",
            "=D22+E22",
            "='Personal'!M21-F22",
            "='Personal'!M21",
        ),
        (
            "Todos repatriados — con housing",
            "='Personal'!U21",
            "=(SUM('Personal'!F11:F19)+SUM('Personal'!G11:G19)+SUM('Personal'!H11:H19)+SUM('Personal'!J11:J19)+SUM('Personal'!K11:K19))/12*'Supuestos'!$D$10",
            "=D23+E23",
            "='Personal'!M21-F23",
            "=E23/'Supuestos'!$D$10*12",
        ),
        (
            "Todos repatriados — sin housing",
            "='Personal'!U21",
            "=(SUM('Personal'!F11:F19)+SUM('Personal'!H11:H19)+SUM('Personal'!J11:J19)+SUM('Personal'!K11:K19))/12*'Supuestos'!$D$10",
            "=D24+E24",
            "='Personal'!M21-F24",
            "=E24/'Supuestos'!$D$10*12",
        ),
    ]
    for row_idx, values in enumerate(scenarios, start=21):
        for col_idx, value in enumerate(values, start=3):
            ws.cell(row_idx, col_idx, value)
            if col_idx == 3:
                ws.cell(row_idx, col_idx).font = Font(name="Arial", size=10, color=BLACK, bold=(row_idx == 21))
                ws.cell(row_idx, col_idx).alignment = Alignment(horizontal="left", vertical="center")
            else:
                format_formula(
                    ws.cell(row_idx, col_idx),
                    CURRENCY_FIRST if col_idx == 4 else CURRENCY,
                    cross_sheet=("!" in value),
                    bold=(row_idx == 21),
                )
        ws.row_dimensions[row_idx].height = 24
    apply_body_borders(ws, 21, 24, 3, 8)

    section_bar(ws, 27, "DETALLE EJECUTIVO POR PERSONA", 3, 9)
    table_header(ws, 28, 3, ["Person", "Position", "Package M7+", "City", "Stage 1", "Stage 2", "Year 1"])
    for idx, source_row in enumerate(range(11, 20), start=29):
        formulas = [
            f"='Personal'!E{source_row}",
            f"='Personal'!D{source_row}",
            f"='Personal'!V{source_row}",
            f"='Personal'!W{source_row}",
            f"='Personal'!U{source_row}",
            f"='Personal'!AB{source_row}",
            f"='Personal'!AC{source_row}",
        ]
        for col, formula in enumerate(formulas, start=3):
            ws.cell(idx, col, formula)
            fmt = CURRENCY_FIRST if col == 7 else CURRENCY if col in (8, 9) else None
            format_formula(ws.cell(idx, col), fmt, cross_sheet=True)
            if col <= 6:
                ws.cell(idx, col).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.row_dimensions[idx].height = 24
    apply_body_borders(ws, 29, 37, 3, 9)

    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Costo Año 1 por escenario"
    chart.y_axis.title = "USD"
    chart.x_axis.title = "Escenario"
    data = Reference(ws, min_col=6, min_row=20, max_row=24)
    categories = Reference(ws, min_col=3, min_row=21, max_row=24)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)
    chart.height = 8
    chart.width = 15
    chart.legend = None
    ws.add_chart(chart, "K19")

    section_bar(ws, 40, "DECISIONES NECESARIAS", 3, 12)
    decisions = [
        "1. Designar por persona si desde el mes 7 será Repatriado o Expatriado.",
        "2. Confirmar ciudad de residencia: Caracas, Maracaibo u otra.",
        "3. Validar la política inicial: Caracas con housing; Maracaibo sin housing para repatriados.",
        "4. Incorporar costos únicos cotizados: viaje, mudanza, permisos, asesoría, alojamiento temporal y settling-in.",
        "5. Obtener dictamen escrito de inmigración, laboral y fiscal antes de implementar la etapa de consultoría.",
    ]
    for row_idx, text in enumerate(decisions, start=41):
        ws.merge_cells(start_row=row_idx, start_column=3, end_row=row_idx, end_column=12)
        ws.cell(row_idx, 3, text)
        ws.cell(row_idx, 3).font = Font(name="Arial", size=10, color=BLACK)
        ws.cell(row_idx, 3).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.row_dimensions[row_idx].height = 23

    ws.print_area = "B2:R45"
    auto_fit(ws, 3, 9, [(9, 16), (20, 24), (28, 37)], min_width=12, max_width=32)
    ws.column_dimensions["C"].width = 36
    ws.column_dimensions["D"].width = 20
    ws.column_dimensions["E"].width = 30
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 21
    return ws


def build_definiciones(wb):
    ws = wb.create_sheet("Definiciones")
    setup_sheet(
        ws,
        "Definición de los paquetes",
        "Alcance presupuestario, criterios de clasificación y elementos de transición",
        "Documento de trabajo institucional — sujeto a aprobación legal, fiscal y de Recursos Humanos",
        11,
    )

    sections = [
        (
            8,
            "PAQUETE CONSULTOR — MESES 1 A 6",
            [
                "Relación presupuestaria: honorario de consultoría equivalente a 6/12 del salario base anual de referencia.",
                "Beneficios / reembolsos incluidos: housing, seguro médico, home leave y vehículo, todos prorrateados por seis meses.",
                "Tax & Social venezolano: factor 0% por instrucción gerencial. No constituye opinión jurídica ni fiscal.",
                "Contrato: debe documentar entregables, facturación, moneda, reembolsos, seguros y terminación, sin crear una clasificación laboral incorrecta.",
            ],
        ),
        (
            14,
            "PAQUETE REPATRIADO — DESDE EL MES 7",
            [
                "Compensación recurrente: salario base, seguro médico, vehículo y Tax & Social.",
                "Housing: condicional. Política inicial editable: Caracas = Sí; Maracaibo = No. Un override individual prevalece sobre la regla automática.",
                "Home leave: no se incluye, porque la persona pasa a una condición local / repatriada.",
                "Costos únicos: viaje de retorno, mudanza de efectos personales, permisos, asesoría, alojamiento temporal y settling-in. Se mantienen en $0 hasta contar con cotizaciones.",
                "Uso recomendado: personas que pasan a nómina local venezolana o retornan permanentemente bajo condiciones locales.",
            ],
        ),
        (
            21,
            "PAQUETE EXPATRIADO — DESDE EL MES 7",
            [
                "Compensación recurrente: paquete anual fuente completo prorrateado — salario base, housing, seguro médico, home leave, vehículo y Tax & Social.",
                "Costos únicos: incorporar, cuando correspondan, regularización migratoria, asesoría fiscal, alojamiento temporal y otros costos de movilidad no incluidos en la tabla fuente.",
                "Uso recomendado: personas que conservan una asignación internacional, vínculo de empleo extranjero o política de tax equalization / gross-up.",
            ],
        ),
        (
            26,
            "CRITERIOS DE DECISIÓN POR PERSONA",
            [
                "País y entidad empleadora; nacionalidad y residencia fiscal; duración esperada de la asignación; dependientes acompañantes; ciudad de residencia; disponibilidad de vivienda propia; y política corporativa aplicable.",
                "La decisión no debe basarse solamente en el costo. Debe ser consistente con permisos de trabajo, nómina, seguridad social, retenciones y obligaciones de reporte.",
            ],
        ),
    ]

    for start_row, title, bullets in sections:
        section_bar(ws, start_row, title, 3, 11)
        for offset, text in enumerate(bullets, start=1):
            row = start_row + offset
            ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=11)
            ws.cell(row, 3, f"• {text}")
            ws.cell(row, 3).font = Font(name="Arial", size=10, color=BLACK)
            ws.cell(row, 3).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            ws.row_dimensions[row].height = 34 if len(text) > 165 else 24

    section_bar(ws, 30, "NOTA DE CUMPLIMIENTO", 3, 11)
    note = (
        "La visa o admisión como turista normalmente no debe asumirse como autorización de trabajo. Además, la ausencia de una "
        "carga fiscal venezolana no puede determinarse únicamente por los primeros seis meses o por el estatus migratorio. El archivo "
        "es una herramienta de presupuesto: antes de contratar, movilizar o pagar, solicitar un dictamen local escrito sobre inmigración, "
        "clasificación laboral, establecimiento permanente, retenciones, impuesto sobre la renta y seguridad social."
    )
    ws.merge_cells(start_row=31, start_column=3, end_row=34, end_column=11)
    ws.cell(31, 3, note)
    ws.cell(31, 3).font = Font(name="Arial", size=10, bold=True, color=RED)
    ws.cell(31, 3).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    ws.page_setup.fitToHeight = 1
    ws.print_area = "B2:K34"
    auto_fit(ws, 3, 11, [(8, 34)], min_width=12, max_width=22)
    return ws


def final_checks(wb):
    assert sum(row[-1] for row in PEOPLE) == 2396800
    assert sum(sum(row[3:9]) for row in PEOPLE) == 2396800
    assert sum(row[8] for row in PEOPLE) == 306400
    assert sum(row[6] for row in PEOPLE) == 104000
    assert sum(row[4] for row in PEOPLE) == 198000
    assert SOURCE_IMAGE.exists(), f"Source image missing: {SOURCE_IMAGE}"
    assert wb.sheetnames == ["Resumen", "Supuestos", "Personal", "Definiciones"]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)
    build_supuestos(wb)
    build_personal(wb)
    build_resumen(wb)
    build_definiciones(wb)
    final_checks(wb)
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    wb.save(OUT_FILE)
    print(OUT_FILE)


if __name__ == "__main__":
    main()
