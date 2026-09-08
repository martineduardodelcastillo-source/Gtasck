from pathlib import Path
import uno
from com.sun.star.beans import PropertyValue


BASE = Path(__file__).resolve().parent
BOOK = BASE / "modelo_paquetes_personal_2_etapas.xlsx"
BLUE = 0x0000FF
BLACK = 0x000000
GREEN = 0x008000

PEOPLE = [
    "Martin del Castillo",
    "Juan Conde",
    "Alexander Stulme",
    "Félix Valderrama",
    "Alan McKeon",
    "JJI",
    "Marcelo Dantas",
    "Jose Miguel",
    "TBD",
]


def prop(name, value):
    item = PropertyValue()
    item.Name = name
    item.Value = value
    return item


def find_row(sheet, value, col_index=None, start=0):
    cursor = sheet.createCursor()
    cursor.gotoEndOfUsedArea(True)
    area = cursor.RangeAddress
    cols = [col_index] if col_index is not None else range(area.StartColumn, area.EndColumn + 1)
    for row in range(max(start, area.StartRow), area.EndRow + 1):
        for col in cols:
            if sheet.getCellByPosition(col, row).String.strip() == value:
                return row + 1
    raise ValueError(f"No se encontró {value!r} en {sheet.Name}")


def find_person_rows(sheet, person_col_index):
    result = {}
    cursor = sheet.createCursor()
    cursor.gotoEndOfUsedArea(True)
    area = cursor.RangeAddress
    for row in range(area.StartRow, area.EndRow + 1):
        person = sheet.getCellByPosition(person_col_index, row).String.strip()
        if person in PEOPLE:
            result[person] = row + 1
    return result


def note(sheet, cell, text):
    try:
        annotation = cell.getAnnotation()
        if annotation is not None and annotation.getString():
            annotation.setString(text)
            return
    except Exception:
        pass
    try:
        sheet.getAnnotations().insertNew(cell.CellAddress, text)
    except Exception:
        cell.getAnnotation().setString(text)


def set_text(sheet, ref, value, text=None):
    cell = sheet.getCellRangeByName(ref)
    cell.String = value
    cell.CharColor = BLUE if text else BLACK
    if text:
        note(sheet, cell, text)


def set_value(sheet, ref, value, text=None):
    cell = sheet.getCellRangeByName(ref)
    cell.Value = float(value)
    cell.CharColor = BLUE if text else BLACK
    if text:
        note(sheet, cell, text)


def set_formula(sheet, ref, formula, cross=False):
    cell = sheet.getCellRangeByName(ref)
    cell.Formula = formula
    cell.CharColor = GREEN if cross else BLACK


def col_letter(number):
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def main():
    ctx0 = uno.getComponentContext()
    resolver = ctx0.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", ctx0)
    ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL(
        uno.systemPathToFileUrl(str(BOOK)),
        "_blank",
        0,
        (prop("Hidden", True), prop("ReadOnly", False), prop("UpdateDocMode", 3)),
    )
    if doc is None:
        raise RuntimeError("No se pudo abrir el libro")

    instruction = (
        "Fuente: instrucción de gerencia recibida el 5 de septiembre de 2026. "
        "La persona se presupone local o alojada en staff house de PU; no recibe housing allowance en efectivo. "
        "Los costos operativos de la staff house, si existen, se presupuestarán separadamente."
    )
    martin_salary_note = (
        "Fuente: edición del usuario del 5 de septiembre de 2026 en el informe institucional: "
        "salario anual de Martin Aguero $180.000. Se refleja como costo adicional de secondment separado del paquete de nueve posiciones."
    )

    try:
        sheets = doc.Sheets
        personal = sheets.getByName("Personal")
        personal_rows = find_person_rows(personal, 4)  # E
        if set(personal_rows) != set(PEOPLE):
            raise ValueError(f"Filas de Personal incompletas: {personal_rows}")
        data_rows = [personal_rows[name] for name in PEOPLE]
        first_data, last_data = min(data_rows), max(data_rows)
        total_row = find_row(personal, "TOTAL — 9 POSICIONES", 3)  # D

        # Staff-house/local assumption: no cash housing allowance.
        for person in ("Jose Miguel", "TBD"):
            row = personal_rows[person]
            set_text(personal, f"M{row}", "Local", instruction)
            set_text(personal, f"N{row}", "Maracaibo", instruction)
            set_value(personal, f"O{row}", 0, instruction)

        # Repair all calculated rows in Personal using the actual row positions.
        for row in data_rows:
            set_value(
                personal,
                f"V{row}",
                30,
                "Fuente: edición directa del usuario del 5 de septiembre de 2026. Se preservan 30 días de vacaciones.",
            )
            set_formula(personal, f"I{row}", f"=F{row}/12")
            set_formula(personal, f"J{row}", f"=G{row}/12")
            set_formula(personal, f"K{row}", f"=SUM(I{row}:J{row})")
            set_formula(personal, f"L{row}", f"=K{row}*6")
            set_formula(personal, f"W{row}", f"=SUM(F{row};O{row}:T{row})/12")
            set_formula(personal, f"X{row}", f"=W{row}*6")
            set_formula(personal, f"Y{row}", f"=L{row}+X{row}")
            set_formula(personal, f"AA{row}", f"=Z{row}-Y{row}")
            set_formula(personal, f"AB{row}", f"=SUM(F{row};O{row}:T{row})")

        for col in ("F", "G", "I", "J", "K", "L", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB"):
            set_formula(personal, f"{col}{total_row}", f"=SUM({col}{first_data}:{col}{last_data})")

        # Repair Monthly using its actual header and total rows.
        mensual = sheets.getByName("Mensual")
        monthly_header = find_row(mensual, "Person", 2)  # C
        monthly_first = monthly_header + 1
        monthly_total = monthly_first + len(PEOPLE)
        monthly_headers = [
            "Person", "Package M7+", "M1", "M2", "M3", "M4", "M5", "M6",
            "M7", "M8", "M9", "M10", "M11", "M12", "Year 1",
            "Monthly change M7 vs. M6", "Tax treatment M7+",
        ]
        for col, value in enumerate(monthly_headers, start=3):
            mensual.getCellByPosition(col - 1, monthly_header - 1).String = value
        for offset, person in enumerate(PEOPLE):
            target = monthly_first + offset
            source = personal_rows[person]
            set_formula(mensual, f"C{target}", f"=Personal.E{source}", cross=True)
            set_formula(mensual, f"D{target}", f"=Personal.M{source}", cross=True)
            for col in range(5, 11):
                set_formula(mensual, f"{col_letter(col)}{target}", f"=Personal.K{source}", cross=True)
            for col in range(11, 17):
                set_formula(mensual, f"{col_letter(col)}{target}", f"=Personal.W{source}", cross=True)
            set_formula(mensual, f"Q{target}", f"=SUM(E{target}:P{target})")
            set_formula(mensual, f"R{target}", f"=K{target}-J{target}")
            set_formula(
                mensual,
                f"S{target}",
                f'=IF(OR(D{target}="Expatriado";D{target}="On rotation");"Empresa cubre impuesto";IF(OR(D{target}="Repatriado";D{target}="Local");"Empleado asume impuesto";IF(D{target}="Remote";"Sin beneficio fiscal";"Definir")))',
            )
        mensual.getCellRangeByName(f"C{monthly_total}").String = "TOTAL — 9 POSICIONES"
        for col in range(5, 19):
            letter = col_letter(col)
            set_formula(mensual, f"{letter}{monthly_total}", f"=SUM({letter}{monthly_first}:{letter}{monthly_total - 1})")

        # Repair Benefits references while preserving the user's 30-day vacation edits.
        beneficios = sheets.getByName("Beneficios M7+")
        benefit_header = find_row(beneficios, "Person", 2)  # C
        benefit_first = benefit_header + 1
        benefit_headers = [
            "Person", "Package", "City", "Housing", "Medical", "Home Leave",
            "Transport", "Employer Tax", "Bonus", "Stock Options", "Vacation Days",
        ]
        for col, value in enumerate(benefit_headers, start=3):
            beneficios.getCellByPosition(col - 1, benefit_header - 1).String = value
        for offset, person in enumerate(PEOPLE):
            target = benefit_first + offset
            source = personal_rows[person]
            for col, source_col in enumerate(("E", "M", "N", "O", "P", "Q", "R", "S", "T", "U"), start=3):
                set_formula(beneficios, f"{col_letter(col)}{target}", f"=Personal.{source_col}{source}", cross=True)
            # Preserve the user's manual change: 30 vacation days in the Benefits sheet.
            set_value(
                beneficios,
                f"M{target}",
                30,
                "Fuente: edición directa del usuario del 5 de septiembre de 2026. Se preservan 30 días en la hoja Beneficios M7+.",
            )

        # Repair all Summary references dynamically.
        resumen = sheets.getByName("Resumen")
        kpis = {
            "Costo mensual M1–M6": f"=Personal.K{total_row}",
            "Bloque 1 — seis meses": f"=Personal.L{total_row}",
            "Costo mensual M7+": f"=Personal.W{total_row}",
            "Bloque 2 — seis meses": f"=Personal.X{total_row}",
            "Costo total Año 1": f"=Personal.Y{total_row}",
            "Paquete fuente anual": f"=Personal.Z{total_row}",
            "Ahorro Año 1 vs. fuente": f"=Personal.AA{total_row}",
            "Run-rate anual M13+": f"=Personal.AB{total_row}",
        }
        for label, formula in kpis.items():
            row = find_row(resumen, label, 2)  # C
            set_formula(resumen, f"D{row}", formula, cross=True)

        detail_section = find_row(resumen, "DOS PUNTOS DE COSTO POR PERSONA", 2)
        detail_header = detail_section + 1
        for col, value in enumerate(("Person", "Position", "Monthly M1–M6", "6M Cost M1–M6", "Package M7+", "Monthly M7+", "6M Cost M7–M12", "Year 1"), start=3):
            resumen.getCellByPosition(col - 1, detail_header - 1).String = value
        for offset, person in enumerate(PEOPLE):
            target = detail_header + 1 + offset
            source = personal_rows[person]
            for col, source_col in enumerate(("E", "D", "K", "L", "M", "W", "X", "Y"), start=3):
                set_formula(resumen, f"{col_letter(col)}{target}", f"=Personal.{source_col}{source}", cross=True)

        savings_section = find_row(resumen, "AHORRO POR PERSONA VS. PAQUETE FUENTE", 2)
        savings_header = savings_section + 1
        for col, value in enumerate(("Person", "Source Annual Package", "Year 1 Cost", "Savings", "Primary driver", "Status", "Notes"), start=3):
            resumen.getCellByPosition(col - 1, savings_header - 1).String = value
        for offset, person in enumerate(PEOPLE):
            target = savings_header + 1 + offset
            source = personal_rows[person]
            for col, source_col in enumerate(("E", "Z", "Y", "AA"), start=3):
                set_formula(resumen, f"{col_letter(col)}{target}", f"=Personal.{source_col}{source}", cross=True)
        # Update the two specific drivers/statuses without touching other user edits.
        for offset, person in enumerate(PEOPLE):
            if person in ("Jose Miguel", "TBD"):
                target = savings_header + 1 + offset
                resumen.getCellRangeByName(f"G{target}").String = "Local o staff house; sin housing allowance en efectivo."
                resumen.getCellRangeByName(f"H{target}").String = "Asumido"

        # Preserve the user's report edit for Martin Aguero: annual salary $180,000.
        secondments = sheets.getByName("Secondments PU")
        secondment_rows = {
            person: find_row(secondments, person, 2)
            for person in ("Alexander Stulme", "Alan McKeon", "Martin Aguero")
        }
        martin_row = secondment_rows["Martin Aguero"]
        set_value(secondments, f"G{martin_row}", 180000, martin_salary_note)
        set_formula(secondments, f"H{martin_row}", f"=G{martin_row}/12")
        set_formula(secondments, f"I{martin_row}", f"=H{martin_row}*6")
        secondments.getCellRangeByName(f"J{martin_row}").String = "Costo adicional de PU; separado del paquete de 9 posiciones"
        second_total = find_row(secondments, "TOTAL CONOCIDO", 2)
        set_formula(secondments, f"G{second_total}", f"=SUM(G{min(secondment_rows.values())}:G{max(secondment_rows.values())})")
        set_formula(secondments, f"H{second_total}", f"=SUM(H{min(secondment_rows.values())}:H{max(secondment_rows.values())})")
        set_formula(secondments, f"I{second_total}", f"=SUM(I{min(secondment_rows.values())}:I{max(secondment_rows.values())})")
        secondments.getCellRangeByName(f"J{second_total}").String = "Incluye Martin Aguero; no duplicar Alexander y Alan"
        old_subtitle = "USD | Martin Aguero permanece TBD y está excluido de los totales conocidos"
        try:
            subtitle_row = find_row(secondments, old_subtitle, 2)
            secondments.getCellRangeByName(f"C{subtitle_row}").String = "USD | Martin Aguero es un costo adicional separado del paquete de nueve posiciones"
        except ValueError:
            pass
        old_note = "• Martin Aguero es una asignación adicional. Su salario no se incorpora al costo de nueve posiciones hasta recibir el importe."
        try:
            note_row = find_row(secondments, old_note, 2)
            secondments.getCellRangeByName(f"C{note_row}").String = "• Martin Aguero es una asignación adicional con salario anual de $180.000; se presenta separado del costo de nueve posiciones."
        except ValueError:
            pass

        secondment_section = find_row(resumen, "SECONDMENTS INICIALES — SALARIO PAGADO POR PU", 2)
        secondment_header = secondment_section + 1
        for col, value in enumerate(("Person", "Initial PU Appointment", "Arrangement", "Salary Payer", "Annual Base Salary", "Monthly Salary", "6M Salary", "Treatment"), start=3):
            resumen.getCellByPosition(col - 1, secondment_header - 1).String = value
        ordered_secondments = ["Alexander Stulme", "Alan McKeon", "Martin Aguero"]
        for offset, person in enumerate(ordered_secondments):
            target = secondment_header + 1 + offset
            source = secondment_rows[person]
            for col, source_col in enumerate(("C", "D", "E", "F", "G", "H", "I", "J"), start=3):
                set_formula(resumen, f"{col_letter(col)}{target}", f"='Secondments PU'.{source_col}{source}", cross=True)
        summary_total = secondment_header + 4
        for col, source_col in enumerate(("C", "D", "E", "F", "G", "H", "I", "J"), start=3):
            set_formula(resumen, f"{col_letter(col)}{summary_total}", f"='Secondments PU'.{source_col}{second_total}", cross=True)

        doc.calculateAll()
        doc.store()
        print(BOOK)
    finally:
        doc.close(True)


if __name__ == "__main__":
    main()
