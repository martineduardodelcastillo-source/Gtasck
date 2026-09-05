from pathlib import Path
import sys
import uno
from com.sun.star.beans import PropertyValue


BASE = Path(__file__).resolve().parent
BOOK = BASE / "modelo_paquetes_personal_2_etapas.xlsx"

BLUE = 0x0000FF
BLACK = 0x000000
GREEN = 0x008000


def prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p


def find_row(sheet, value, column_index=None):
    cursor = sheet.createCursor()
    cursor.gotoEndOfUsedArea(True)
    address = cursor.RangeAddress
    for row in range(address.StartRow, address.EndRow + 1):
        cols = [column_index] if column_index is not None else range(address.StartColumn, address.EndColumn + 1)
        for col in cols:
            cell = sheet.getCellByPosition(col, row)
            if cell.String.strip() == value:
                return row
    raise ValueError(f"No se encontró {value!r} en {sheet.Name}")


def find_cell(sheet, value):
    cursor = sheet.createCursor()
    cursor.gotoEndOfUsedArea(True)
    address = cursor.RangeAddress
    for row in range(address.StartRow, address.EndRow + 1):
        for col in range(address.StartColumn, address.EndColumn + 1):
            cell = sheet.getCellByPosition(col, row)
            if cell.String.strip() == value:
                return cell
    raise ValueError(f"No se encontró {value!r} en {sheet.Name}")


def find_person_rows(sheet):
    names = {
        "Martin del Castillo",
        "Juan Conde",
        "Alexander Stulme",
        "Félix Valderrama",
        "Alan McKeon",
        "JJI",
        "Marcelo Dantas",
        "Jose Miguel",
        "Leticia Almeida",
        "TBD",
    }
    cursor = sheet.createCursor()
    cursor.gotoEndOfUsedArea(True)
    result = {}
    for row in range(cursor.RangeAddress.StartRow, cursor.RangeAddress.EndRow + 1):
        value = sheet.getCellByPosition(4, row).String.strip()
        if value in names:
            result[value] = row
    return result


def set_note(sheet, cell, text):
    try:
        annotation = cell.getAnnotation()
        if annotation is not None and annotation.getString():
            annotation.setString(text)
            return
    except Exception:
        pass
    annotations = sheet.getAnnotations()
    try:
        annotations.insertNew(cell.CellAddress, text)
    except Exception:
        annotation = cell.getAnnotation()
        annotation.setString(text)


def set_text_input(sheet, ref, value, note):
    cell = sheet.getCellRangeByName(ref)
    cell.String = value
    cell.CharColor = BLUE
    set_note(sheet, cell, note)


def set_value_input(sheet, ref, value, note):
    cell = sheet.getCellRangeByName(ref)
    cell.Value = float(value)
    cell.CharColor = BLUE
    set_note(sheet, cell, note)


def set_formula(sheet, ref, formula, note=None, cross_sheet=False):
    cell = sheet.getCellRangeByName(ref)
    cell.Formula = formula
    cell.CharColor = GREEN if cross_sheet else BLACK
    if note:
        set_note(sheet, cell, note)


def set_formula_cell(cell, formula, cross_sheet=False):
    cell.Formula = formula
    cell.CharColor = GREEN if cross_sheet else BLACK


def xl_row(zero_based_row):
    return zero_based_row + 1


def copy_column_format(sheet, source_col, target_col, start_row, end_row):
    source = sheet.getCellRangeByName(f"{source_col}{start_row}:{source_col}{end_row}")
    destination = sheet.getCellRangeByName(f"{target_col}{start_row}").CellAddress
    sheet.copyRange(destination, source.RangeAddress)


def main():
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local_ctx)
    ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL(
        uno.systemPathToFileUrl(str(BOOK)),
        "_blank",
        0,
        (prop("Hidden", True), prop("ReadOnly", False), prop("UpdateDocMode", 3)),
    )
    if doc is None:
        raise RuntimeError("LibreOffice no pudo abrir el libro")

    try:
        sheets = doc.Sheets
        personal = sheets.getByName("Personal")
        resumen = sheets.getByName("Resumen")
        mensual = sheets.getByName("Mensual")

        header_zero = find_row(personal, "Person", 4)
        total_zero = find_row(personal, "TOTAL — 9 POSICIONES", 3)
        header_row = xl_row(header_zero)
        total_row = xl_row(total_zero)
        people = find_person_rows(personal)
        required = {"Martin del Castillo", "Juan Conde", "Alexander Stulme", "Félix Valderrama", "Alan McKeon", "JJI", "Marcelo Dantas", "Jose Miguel"}
        missing = required - set(people)
        if "Leticia Almeida" not in people and "TBD" not in people:
            missing.add("Leticia Almeida / TBD")
        if missing:
            raise ValueError(f"Personas no encontradas: {sorted(missing)}")

        # Append three auditable benefit columns only if they do not already exist.
        if personal.getCellRangeByName(f"AJ{header_row}").String != "Annual Bonus\nM7+":
            personal.Columns.insertByIndex(35, 3)  # AJ:AL
            for target in ("AJ", "AK", "AL"):
                copy_column_format(personal, "AI", target, header_row, total_row)

        personal.getCellRangeByName(f"AJ{header_row}").String = "Annual Bonus\nM7+"
        personal.getCellRangeByName(f"AK{header_row}").String = "Stock Options\nAnnual Value (TBD)"
        personal.getCellRangeByName(f"AL{header_row}").String = "Vacation\nDays"
        if personal.getCellRangeByName(f"AM{header_row}").String != "Housing M7+\nAnnual Override":
            personal.Columns.insertByIndex(38, 1)  # AM
            copy_column_format(personal, "AL", "AM", header_row, total_row)
        personal.getCellRangeByName(f"AM{header_row}").String = "Housing M7+\nAnnual Override"
        personal.Columns.getByIndex(35).Width = 2800
        personal.Columns.getByIndex(36).Width = 3300
        personal.Columns.getByIndex(37).Width = 2200
        personal.Columns.getByIndex(38).Width = 3000

        # Re-read rows after any column insertion.
        people = find_person_rows(personal)
        rows = {name: xl_row(row) for name, row in people.items()}
        first_data_row = min(rows.values())
        last_data_row = max(rows.values())

        # Default added benefits: no incremental cost unless specifically approved.
        for row in range(first_data_row, last_data_row + 1):
            set_formula(personal, f"AJ{row}", "=0")
            set_formula(personal, f"AK{row}", "=0")
            set_formula(personal, f"AL{row}", "=0")
            set_formula(personal, f"AM{row}", "=0")

        instruction = "Fuente: instrucción de la gerencia recibida el 5 de septiembre de 2026."
        four_month_note = instruction + " Bonus objetivo equivalente a cuatro meses de salario base anual; se acumula desde M7."
        stock_note = instruction + " Stock options incluidas como beneficio, pero su valor anual permanece TBD y se excluye del costo hasta aprobación del plan y valoración."
        vacation_note = instruction + " Se interpretó '13 de vacaciones' como 13 días de vacaciones pagadas; confirmar con Recursos Humanos. No se añade costo separado al salario."

        # Preserve the manual name/status edits observed in the user's workbook.
        if "Leticia Almeida" in rows:
            leticia_row = rows["Leticia Almeida"]
            set_text_input(personal, f"E{leticia_row}", "TBD", instruction + " La posición Operations Support fue renombrada manualmente a TBD en la hoja Resumen.")
            rows["TBD"] = leticia_row
            del rows["Leticia Almeida"]

        # Juan Conde: repatriated in Maracaibo; housing budget may be allowance/staff house/hotel.
        juan = rows["Juan Conde"]
        set_text_input(personal, f"V{juan}", "Repatriado", instruction + " Clasificación confirmada por el usuario.")
        set_text_input(personal, f"W{juan}", "Maracaibo", instruction + " Ciudad presupuestaria inicial; si cambia a Caracas, la fórmula individual elimina housing.")
        set_text_input(personal, f"X{juan}", "Automático", instruction + " Regla individual: Caracas sin housing; Maracaibo con allowance, staff house u hotel.")
        set_formula(personal, f"Y{juan}", f'=IF(X{juan}="Automático";IF(W{juan}="Caracas";"No";IF(W{juan}="Maracaibo";"Sí";IF(W{juan}="Otro";"Sí";"Por definir")));X{juan})')
        set_formula(personal, f"AJ{juan}", f"=F{juan}*4/12", four_month_note)
        set_text_input(personal, f"AK{juan}", "TBD", stock_note)
        set_value_input(personal, f"AL{juan}", 13, vacation_note)
        set_note(personal, personal.getCellRangeByName(f"G{juan}"), instruction + " Housing anual de referencia se usa como presupuesto para allowance, staff house u hotel en Maracaibo.")
        set_note(personal, personal.getCellRangeByName(f"J{juan}"), instruction + " El importe de Vehicle representa transporte provisto por la compañía para ir al trabajo, no un vehículo personal garantizado.")

        # Alexander Stulme: same repatriate benefits, but own home in Maracaibo and no housing.
        alex = rows["Alexander Stulme"]
        set_text_input(personal, f"V{alex}", "Repatriado", instruction + " Clasificación confirmada por el usuario.")
        set_text_input(personal, f"W{alex}", "Maracaibo", instruction + " Vive en su propia casa en Maracaibo.")
        set_text_input(personal, f"X{alex}", "No", instruction + " Sin housing allowance por vivienda propia.")
        set_formula(personal, f"AJ{alex}", f"=F{alex}*4/12", four_month_note)
        set_text_input(personal, f"AK{alex}", "TBD", stock_note)
        set_value_input(personal, f"AL{alex}", 13, vacation_note)
        set_note(personal, personal.getCellRangeByName(f"J{alex}"), instruction + " El importe de Vehicle representa transporte provisto por la compañía para ir al trabajo, no un vehículo personal garantizado.")

        # Félix Valderrama: same package as Juan Conde.
        felix = rows["Félix Valderrama"]
        set_text_input(personal, f"V{felix}", "Repatriado", instruction + " Mismo paquete que Juan Conde.")
        set_text_input(personal, f"W{felix}", "Maracaibo", instruction + " Ciudad presupuestaria inicial; si cambia a Caracas, la fórmula individual elimina housing.")
        set_text_input(personal, f"X{felix}", "Automático", instruction + " Regla individual: Caracas sin housing; Maracaibo con allowance, staff house u hotel.")
        set_formula(personal, f"Y{felix}", f'=IF(X{felix}="Automático";IF(W{felix}="Caracas";"No";IF(W{felix}="Maracaibo";"Sí";IF(W{felix}="Otro";"Sí";"Por definir")));X{felix})')
        set_formula(personal, f"AJ{felix}", f"=F{felix}*4/12", four_month_note)
        set_text_input(personal, f"AK{felix}", "TBD", stock_note)
        set_value_input(personal, f"AL{felix}", 13, vacation_note)
        set_note(personal, personal.getCellRangeByName(f"G{felix}"), instruction + " Housing anual de referencia se usa como presupuesto para allowance, staff house u hotel en Maracaibo.")
        set_note(personal, personal.getCellRangeByName(f"J{felix}"), instruction + " El importe de Vehicle representa transporte provisto por la compañía para ir al trabajo, no un vehículo personal garantizado.")

        # Alan McKeon: expatriate with USD 1,000 monthly housing.
        alan = rows["Alan McKeon"]
        set_text_input(personal, f"V{alan}", "Expatriado", instruction + " Clasificación confirmada por el usuario.")
        set_text_input(personal, f"W{alan}", "Maracaibo", instruction + " Ciudad asumida para el presupuesto de housing indicado.")
        set_text_input(personal, f"X{alan}", "Sí", instruction + " Housing allowance confirmado para condición expatriada.")
        set_value_input(personal, f"G{alan}", 24000, "Fuente: tabla de paquetes suministrada por el usuario el 5 de septiembre de 2026. Housing anual de referencia para la etapa de consultoría M1–M6.")
        set_value_input(personal, f"AM{alan}", 12000, instruction + " Housing allowance expatriado de USD 1,000 por mes desde M7; no modifica la etapa inicial como consultor.")

        # JJI: remote with base compensation only and no benefits.
        jji = rows["JJI"]
        set_text_input(personal, f"V{jji}", "Remote", instruction + " Condición remota confirmada por el usuario; sin beneficios.")
        set_text_input(personal, f"W{jji}", "Remoto", instruction + " No requiere ciudad de residencia de asignación.")
        set_text_input(personal, f"X{jji}", "No", instruction + " Sin housing ni otros beneficios por condición remota.")
        for col, label in (("G", "housing"), ("H", "seguro médico"), ("I", "home leave"), ("J", "vehículo/transporte"), ("K", "Tax & Social empresarial")):
            set_value_input(personal, f"{col}{jji}", 0, instruction + f" JJI trabaja remoto y no recibe {label}.")

        # Preserve the additional manual classifications recorded in Resumen.
        marcelo = rows["Marcelo Dantas"]
        set_text_input(personal, f"V{marcelo}", "On rotation", instruction + " Clasificación preservada de la edición manual de la hoja Resumen; costo provisional igual al paquete fuente.")
        set_text_input(personal, f"W{marcelo}", "Por definir", instruction + " La ciudad no modifica provisionalmente el paquete On rotation.")

        jose = rows["Jose Miguel"]
        set_text_input(personal, f"V{jose}", "Local", instruction + " Clasificación preservada de la edición manual de la hoja Resumen.")
        set_text_input(personal, f"W{jose}", "Maracaibo", instruction + " Ciudad asumida para reflejar el housing allowance existente indicado por el usuario.")
        set_text_input(personal, f"X{jose}", "Sí", instruction + " Se mantiene el housing anual fuente como supuesto; confirmar importe y política.")

        tbd = rows["TBD"]
        set_text_input(personal, f"V{tbd}", "Local", instruction + " Clasificación preservada de la edición manual de la hoja Resumen.")

        # Rebuild package formulas for every person. Local and repatriate employees assume personal tax.
        for row in range(first_data_row, last_data_row + 1):
            effective_housing = f"IF(AM{row}>0;AM{row};G{row})"
            expat_annual = f"F{row}+{effective_housing}+H{row}+I{row}+J{row}+K{row}*Supuestos.$D$14"
            repat_annual = f"F{row}+H{row}+J{row}+K{row}*Supuestos.$D$13+IF(Y{row}=\"No\";0;{effective_housing})+AJ{row}"
            local_annual = f"F{row}+H{row}+J{row}+K{row}*Supuestos.$D$13+IF(Y{row}=\"No\";0;{effective_housing})+AJ{row}"
            remote_annual = f"F{row}"
            rotation_annual = expat_annual
            annual_choice = (
                f'IF(V{row}="Expatriado";{expat_annual};'
                f'IF(V{row}="Repatriado";{repat_annual};'
                f'IF(V{row}="Remote";{remote_annual};'
                f'IF(V{row}="Local";{local_annual};'
                f'IF(V{row}="On rotation";{rotation_annual};0)))))'
            )
            set_formula(personal, f"AA{row}", f"={annual_choice}/12*Supuestos.$D$11", cross_sheet=True)
            set_formula(personal, f"AB{row}", f"=AA{row}+Z{row}")
            set_formula(personal, f"AC{row}", f"=U{row}+AB{row}")
            set_formula(personal, f"AD{row}", f"=M{row}-AC{row}")
            set_formula(personal, f"AE{row}", f"={annual_choice}", cross_sheet=True)
            status = (
                f'=IF(V{row}="Por definir";"Definir paquete";'
                f'IF(OR(V{row}="Remote";V{row}="On rotation");"Completo";'
                f'IF(W{row}="Por definir";"Definir ciudad";'
                f'IF(AND(OR(V{row}="Repatriado";V{row}="Local");Y{row}="Por definir");"Definir vivienda";"Completo"))))'
            )
            set_formula(personal, f"AF{row}", status)
            set_formula(personal, f"AG{row}", f"=U{row}/Supuestos.$D$10", cross_sheet=True)
            set_formula(personal, f"AH{row}", f"=AA{row}/Supuestos.$D$11", cross_sheet=True)
            set_formula(personal, f"AI{row}", f"=AH{row}+Z{row}")

        # Totals for existing calculated columns and new disclosures.
        for col in ("F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "Z", "AA", "AB", "AC", "AD", "AE", "AG", "AH", "AI", "AJ", "AK", "AL", "AM"):
            set_formula(personal, f"{col}{total_row}", f"=SUM({col}{first_data_row}:{col}{last_data_row})")
        personal.getCellRangeByName(f"AL{first_data_row}:AL{total_row}").NumberFormat = personal.getCellRangeByName(f"C{first_data_row}").NumberFormat

        # Expand validations to include the preserved manual categories.
        try:
            package_range = personal.getCellRangeByName(f"V{first_data_row}:V{last_data_row}")
            package_validation = package_range.Validation
            package_validation.Formula1 = '"Expatriado,Repatriado,Remote,On rotation,Local,Por definir"'
            package_range.Validation = package_validation
            city_range = personal.getCellRangeByName(f"W{first_data_row}:W{last_data_row}")
            city_validation = city_range.Validation
            city_validation.Formula1 = '"Caracas,Maracaibo,Otro,Remoto,Por definir"'
            city_range.Validation = city_validation
        except Exception as exc:
            print(f"Advertencia: no se pudo ampliar la validación desplegable: {exc}", file=sys.stderr)

        # Extend print area to the added benefit columns.
        personal.setPrintAreas((personal.getCellRangeByName(f"B2:AM{total_row}").RangeAddress,))

        # Restore the user's edited executive detail as live links to Personal.
        resumen_header_zero = find_row(resumen, "Person", 2)
        resumen_start = xl_row(resumen_header_zero) + 1
        for offset, source_row in enumerate(range(first_data_row, last_data_row + 1)):
            target_row = resumen_start + offset
            for target_col, source_col in (("C", "E"), ("D", "D"), ("E", "V"), ("F", "W"), ("G", "U"), ("H", "AB"), ("I", "AC")):
                set_formula(resumen, f"{target_col}{target_row}", f"=Personal.{source_col}{source_row}", cross_sheet=True)

        # Repoint executive KPIs and scenarios to the actual total/data rows.
        kpis = {
            "Costo anual original": f"=Personal.M{total_row}",
            "Etapa 1 — Consultor M1–M6": f"=Personal.U{total_row}",
            "Etapa 2 — Selección M7–M12": f"=Personal.AB{total_row}",
            "Costo total Año 1": f"=Personal.AC{total_row}",
            "Ahorro / (sobrecosto) vs. fuente": f"=Personal.AD{total_row}",
            "Run-rate anual desde M13": f"=Personal.AE{total_row}",
            "Personas con decisión pendiente": f'=COUNTIF(Personal.AF{first_data_row}:AF{last_data_row};"<>Completo")',
        }
        for label, formula in kpis.items():
            label_cell = find_cell(resumen, label)
            value_cell = resumen.getCellByPosition(label_cell.CellAddress.Column + 1, label_cell.CellAddress.Row)
            set_formula_cell(value_cell, formula, cross_sheet=True)

        scenario_formulas = {
            "Selección actual por persona": (
                f"=Personal.U{total_row}", f"=Personal.AB{total_row}", f"=Personal.AC{total_row}",
                f"=Personal.AD{total_row}", f"=Personal.AE{total_row}",
            ),
            "Todos expatriados — empresa cubre impuesto": (
                f"=Personal.U{total_row}",
                f"=(SUM(Personal.F{first_data_row}:F{last_data_row})+SUM(Personal.G{first_data_row}:G{last_data_row})+SUM(Personal.H{first_data_row}:H{last_data_row})+SUM(Personal.I{first_data_row}:I{last_data_row})+SUM(Personal.J{first_data_row}:J{last_data_row})+SUM(Personal.K{first_data_row}:K{last_data_row})*Supuestos.$D$14)/12*Supuestos.$D$11",
                None, None, None,
            ),
            "Todos repatriados — con housing; empleado paga impuesto": (
                f"=Personal.U{total_row}",
                f"=(SUM(Personal.F{first_data_row}:F{last_data_row})+SUM(Personal.G{first_data_row}:G{last_data_row})+SUM(Personal.H{first_data_row}:H{last_data_row})+SUM(Personal.J{first_data_row}:J{last_data_row})+SUM(Personal.K{first_data_row}:K{last_data_row})*Supuestos.$D$13+SUM(Personal.AJ{first_data_row}:AJ{last_data_row}))/12*Supuestos.$D$11",
                None, None, None,
            ),
            "Todos repatriados — sin housing; empleado paga impuesto": (
                f"=Personal.U{total_row}",
                f"=(SUM(Personal.F{first_data_row}:F{last_data_row})+SUM(Personal.H{first_data_row}:H{last_data_row})+SUM(Personal.J{first_data_row}:J{last_data_row})+SUM(Personal.K{first_data_row}:K{last_data_row})*Supuestos.$D$13+SUM(Personal.AJ{first_data_row}:AJ{last_data_row}))/12*Supuestos.$D$11",
                None, None, None,
            ),
        }
        for label, formulas in scenario_formulas.items():
            row_zero = find_row(resumen, label, 2)
            display_row = row_zero + 1
            if label == "Todos expatriados — empresa cubre impuesto":
                baseline_note = "Fuente: escenario previo del modelo validado antes de las asignaciones individuales del 5 de septiembre de 2026."
                for col, value in zip(("D", "E", "F", "G", "H"), (1045200, 1198400, 2243600, 153200, 2396800)):
                    set_value_input(resumen, f"{col}{display_row}", value, baseline_note)
                continue
            for offset, formula in enumerate(formulas, start=3):
                cell = resumen.getCellByPosition(offset, row_zero)
                if formula is not None:
                    set_formula_cell(cell, formula, cross_sheet=True)
            if label != "Selección actual por persona":
                set_formula_cell(resumen.getCellByPosition(5, row_zero), f"=D{display_row}+E{display_row}")
                set_formula_cell(resumen.getCellByPosition(6, row_zero), f"=Personal.M{total_row}-F{display_row}", cross_sheet=True)
                set_formula_cell(resumen.getCellByPosition(7, row_zero), f"=E{display_row}/Supuestos.$D$11*12", cross_sheet=True)

        # Cost bridge versus the previous all-expatriate Year 1 model.
        bridge_start = 49
        resumen.copyRange(resumen.getCellRangeByName(f"C{bridge_start}").CellAddress, resumen.getCellRangeByName("C40:R40").RangeAddress)
        resumen.getCellRangeByName(f"C{bridge_start}").String = "PUENTE DE COSTO — ESCENARIO PREVIO VS. PAQUETES INDIVIDUALES"
        resumen.copyRange(resumen.getCellRangeByName(f"C{bridge_start + 1}").CellAddress, resumen.getCellRangeByName("C29:G29").RangeAddress)
        for col, value in zip(("C", "D", "E", "F", "G"), ("Person", "Previous Expat Year 1", "Selected Year 1", "Savings / (Overcost)", "Reason")):
            resumen.getCellRangeByName(f"{col}{bridge_start + 1}").String = value

        prior_year1 = {
            "Martin del Castillo": 488000,
            "Juan Conde": 303600,
            "Alexander Stulme": 264000,
            "Félix Valderrama": 303600,
            "Alan McKeon": 264000,
            "JJI": 184000,
            "Marcelo Dantas": 264000,
            "Jose Miguel": 81200,
            "TBD": 91200,
        }
        reasons = {
            "Martin del Castillo": "Sin cambio frente al paquete previo.",
            "Juan Conde": "Ahorro de impuesto y home leave compensado por bonus de 4 meses; neto: sobrecosto.",
            "Alexander Stulme": "Sin housing, impuesto ni home leave; el bonus absorbe la mayor parte del ahorro.",
            "Félix Valderrama": "Ahorro de impuesto y home leave compensado por bonus de 4 meses; neto: sobrecosto.",
            "Alan McKeon": "Housing M7+ baja de $2.000 a $1.000 por mes.",
            "JJI": "Remote con salario base solamente; se eliminan todos los beneficios.",
            "Marcelo Dantas": "On rotation sin cambio provisional de costo.",
            "Jose Miguel": "Local: mantiene housing; empleado asume impuesto personal.",
            "TBD": "Local provisional: se eliminan impuesto empresarial y home leave.",
        }
        ordered_names = ["Martin del Castillo", "Juan Conde", "Alexander Stulme", "Félix Valderrama", "Alan McKeon", "JJI", "Marcelo Dantas", "Jose Miguel", "TBD"]
        currency_format = resumen.getCellRangeByName("G30").NumberFormat
        for offset, name in enumerate(ordered_names, start=2):
            row = bridge_start + offset
            resumen.copyRange(resumen.getCellRangeByName(f"C{row}").CellAddress, resumen.getCellRangeByName("C30:G30").RangeAddress)
            resumen.getCellRangeByName(f"C{row}").String = name
            set_value_input(resumen, f"D{row}", prior_year1[name], "Fuente: costo individual del escenario previo con todas las personas como expatriadas, validado el 5 de septiembre de 2026.")
            source_row = rows[name]
            set_formula(resumen, f"E{row}", f"=Personal.AC{source_row}", cross_sheet=True)
            set_formula(resumen, f"F{row}", f"=D{row}-E{row}")
            resumen.getCellRangeByName(f"G{row}").String = reasons[name]
            resumen.getCellRangeByName(f"G{row}").CharColor = BLACK
            for col in ("D", "E", "F"):
                resumen.getCellRangeByName(f"{col}{row}").NumberFormat = currency_format
            resumen.Rows.getByIndex(row - 1).Height = 750

        bridge_total = bridge_start + 11
        resumen.copyRange(resumen.getCellRangeByName(f"C{bridge_total}").CellAddress, resumen.getCellRangeByName("C30:G30").RangeAddress)
        resumen.getCellRangeByName(f"C{bridge_total}").String = "TOTAL — 9 POSICIONES"
        set_formula(resumen, f"D{bridge_total}", f"=SUM(D{bridge_start + 2}:D{bridge_start + 10})")
        set_formula(resumen, f"E{bridge_total}", f"=SUM(E{bridge_start + 2}:E{bridge_start + 10})")
        set_formula(resumen, f"F{bridge_total}", f"=SUM(F{bridge_start + 2}:F{bridge_start + 10})")
        resumen.getCellRangeByName(f"G{bridge_total}").String = "La reducción neta es limitada porque $72.000 + $60.000 + $72.000 de bonus anual compensan ahorros fiscales y de beneficios."
        for col in ("D", "E", "F"):
            resumen.getCellRangeByName(f"{col}{bridge_total}").NumberFormat = currency_format
        resumen.getCellRangeByName(f"C{bridge_total}:G{bridge_total}").CharWeight = 150
        resumen.Rows.getByIndex(bridge_start - 1).IsStartOfNewPage = True
        resumen.setPrintAreas((resumen.getCellRangeByName(f"B2:R{bridge_total}").RangeAddress,))

        # Monthly tax-treatment labels for the expanded package choices.
        mensual_header_zero = find_row(mensual, "Person", 2)
        mensual_start = xl_row(mensual_header_zero) + 1
        for offset in range(last_data_row - first_data_row + 1):
            row = mensual_start + offset
            tax_text = (
                f'=IF(OR(E{row}="Expatriado";E{row}="On rotation");"Empresa cubre / neutraliza impuesto del país de trabajo";'
                f'IF(OR(E{row}="Repatriado";E{row}="Local");"Empleado asume impuesto personal";'
                f'IF(E{row}="Remote";"Remote — sin beneficios";"Definir paquete")))'
            )
            set_formula(mensual, f"T{row}", tax_text)

        doc.calculateAll()
        doc.store()
        print(BOOK)
    finally:
        doc.close(True)


if __name__ == "__main__":
    main()
