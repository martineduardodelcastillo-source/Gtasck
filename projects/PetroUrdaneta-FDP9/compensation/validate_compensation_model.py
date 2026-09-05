from pathlib import Path
from math import isclose

from openpyxl import load_workbook


BASE = Path(__file__).resolve().parent
BOOK = BASE / "modelo_paquetes_personal_2_etapas.xlsx"
SOURCE = BASE / "source" / "package_source_2026-09-05.jpeg"
BACKUP = BASE / "backups" / "modelo_paquetes_personal_2_etapas_before_personnel_assignments_2026-09-05.xlsx"


def close(actual, expected, label, tolerance=0.01):
    assert actual is not None, f"{label}: valor calculado ausente"
    assert isclose(float(actual), float(expected), rel_tol=0, abs_tol=tolerance), (
        f"{label}: esperado {expected}, obtenido {actual}"
    )


def locate_person_rows(ws):
    names = {
        "Martin del Castillo",
        "Juan Conde",
        "Alexander Stulme",
        "Félix Valderrama",
        "Alan McKeon",
        "JJI",
        "Marcelo Dantas",
        "Jose Miguel",
        "TBD",
    }
    result = {}
    for row in range(1, ws.max_row + 1):
        value = ws.cell(row, 5).value
        if isinstance(value, str) and value.strip() in names:
            result[value.strip()] = row
    return result


def locate_total_row(ws):
    for row in range(1, ws.max_row + 1):
        if ws.cell(row, 4).value == "TOTAL — 9 POSICIONES":
            return row
    raise AssertionError("No se encontró la fila total en Personal")


def value_right_of_label(ws, label):
    for row in ws.iter_rows():
        for cell in row:
            if cell.value == label:
                return ws.cell(cell.row, cell.column + 1).value
    raise AssertionError(f"No se encontró la etiqueta {label!r} en {ws.title}")


def main():
    assert BOOK.exists(), f"No existe {BOOK}"
    assert SOURCE.exists(), f"No existe {SOURCE}"
    assert BACKUP.exists(), f"No existe el respaldo {BACKUP}"

    formula_wb = load_workbook(BOOK, data_only=False)
    value_wb = load_workbook(BOOK, data_only=True)
    assert formula_wb.sheetnames == ["Resumen", "Supuestos", "Personal", "Mensual", "Definiciones"]

    personal_f = formula_wb["Personal"]
    personal = value_wb["Personal"]
    rows = locate_person_rows(personal)
    total_row = locate_total_row(personal)
    assert set(rows) == {
        "Martin del Castillo", "Juan Conde", "Alexander Stulme", "Félix Valderrama",
        "Alan McKeon", "JJI", "Marcelo Dantas", "Jose Miguel", "TBD",
    }

    juan = rows["Juan Conde"]
    alex = rows["Alexander Stulme"]
    felix = rows["Félix Valderrama"]
    alan = rows["Alan McKeon"]
    jji = rows["JJI"]
    marcelo = rows["Marcelo Dantas"]
    jose = rows["Jose Miguel"]
    tbd = rows["TBD"]

    assert personal[f"V{juan}"].value == "Repatriado"
    assert personal[f"W{juan}"].value == "Maracaibo"
    assert personal[f"Y{juan}"].value == "Sí"
    close(personal[f"AJ{juan}"].value, 72_000, "Juan — bonus anual")
    assert personal[f"AK{juan}"].value == "TBD"
    close(personal[f"AL{juan}"].value, 13, "Juan — días de vacaciones")
    close(personal[f"AH{juan}"].value, 28_500, "Juan — costo mensual M7+")

    assert personal[f"V{alex}"].value == "Repatriado"
    assert personal[f"W{alex}"].value == "Maracaibo"
    assert personal[f"Y{alex}"].value == "No"
    close(personal[f"AJ{alex}"].value, 60_000, "Alexander — bonus anual")
    assert personal[f"AK{alex}"].value == "TBD"
    close(personal[f"AL{alex}"].value, 13, "Alexander — días de vacaciones")
    close(personal[f"AH{alex}"].value, 22_500, "Alexander — costo mensual M7+")

    assert personal[f"V{felix}"].value == "Repatriado"
    assert personal[f"W{felix}"].value == "Maracaibo"
    assert personal[f"Y{felix}"].value == "Sí"
    close(personal[f"AJ{felix}"].value, 72_000, "Félix — bonus anual")
    assert personal[f"AK{felix}"].value == "TBD"
    close(personal[f"AL{felix}"].value, 13, "Félix — días de vacaciones")
    close(personal[f"AH{felix}"].value, 28_500, "Félix — costo mensual M7+")

    assert personal[f"V{alan}"].value == "Expatriado"
    close(personal[f"G{alan}"].value, 24_000, "Alan — housing anual de consultoría")
    close(personal[f"AM{alan}"].value, 12_000, "Alan — housing anual M7+")
    close(personal[f"AH{alan}"].value, 22_500, "Alan — costo mensual M7+")

    assert personal[f"V{jji}"].value == "Remote"
    for col, label in (("G", "housing"), ("H", "medical"), ("I", "home leave"), ("J", "vehicle"), ("K", "tax")):
        close(personal[f"{col}{jji}"].value, 0, f"JJI — {label}")
    close(personal[f"AG{jji}"].value, 10_000, "JJI — mensual consultor")
    close(personal[f"AH{jji}"].value, 10_000, "JJI — mensual remote")

    assert personal[f"V{marcelo}"].value == "On rotation"
    assert personal[f"V{jose}"].value == "Local"
    assert personal[f"Y{jose}"].value == "Sí"
    assert personal[f"V{tbd}"].value == "Local"

    close(personal[f"L{total_row}"].value, 2_322_800, "Paquete anual calculado tras cambios de beneficios")
    close(personal[f"M{total_row}"].value, 2_396_800, "Paquete anual fuente declarado")
    close(personal[f"N{total_row}"].value, -74_000, "Variación vs. fuente")
    close(personal[f"U{total_row}"].value, 1_018_200, "Etapa 1 seleccionada")
    close(personal[f"AB{total_row}"].value, 1_150_200, "Etapa 2 seleccionada")
    close(personal[f"AC{total_row}"].value, 2_168_400, "Año 1 seleccionado")
    close(personal[f"AD{total_row}"].value, 228_400, "Ahorro Año 1 vs. fuente")
    close(personal[f"AE{total_row}"].value, 2_300_400, "Run-rate seleccionado")
    close(personal[f"AG{total_row}"].value, 169_700, "Mensual consultor consolidado")
    close(personal[f"AH{total_row}"].value, 191_700, "Mensual M7+ seleccionado")
    close(personal[f"AJ{total_row}"].value, 204_000, "Bonus anual total")
    close(personal[f"AL{total_row}"].value, 39, "Vacaciones totales divulgadas")
    close(personal[f"AM{total_row}"].value, 12_000, "Housing anual override total M7+")

    mensual = value_wb["Mensual"]
    # The detailed monthly schedule must reconcile to Personal by person and year.
    monthly_person_rows = {}
    for row in range(1, mensual.max_row + 1):
        value = mensual.cell(row, 3).value
        if isinstance(value, str) and value.strip() in rows:
            monthly_person_rows[value.strip()] = row
    assert set(monthly_person_rows) == set(rows)
    for person, p_row in rows.items():
        m_row = monthly_person_rows[person]
        close(mensual[f"S{m_row}"].value, personal[f"AC{p_row}"].value, f"Mensual vs. Personal — {person}")

    selected_monthly_row = None
    for row in range(1, mensual.max_row + 1):
        if mensual.cell(row, 3).value == "Selección actual por persona":
            selected_monthly_row = row
            break
    assert selected_monthly_row is not None
    close(mensual[f"D{selected_monthly_row}"].value, 169_700, "Mensual consolidado M1")
    close(mensual[f"J{selected_monthly_row}"].value, 191_700, "Mensual consolidado M7")
    close(mensual[f"P{selected_monthly_row}"].value, 2_168_400, "Mensual consolidado Año 1")

    resumen = value_wb["Resumen"]
    close(value_right_of_label(resumen, "Etapa 1 — Consultor M1–M6"), 1_018_200, "Resumen — Etapa 1")
    close(value_right_of_label(resumen, "Etapa 2 — Selección M7–M12"), 1_150_200, "Resumen — Etapa 2")
    close(value_right_of_label(resumen, "Costo total Año 1"), 2_168_400, "Resumen — Año 1")

    bridge_start = None
    for row in range(1, resumen.max_row + 1):
        if resumen.cell(row, 3).value == "PUENTE DE COSTO — ESCENARIO PREVIO VS. PAQUETES INDIVIDUALES":
            bridge_start = row
            break
    assert bridge_start is not None
    bridge_total = bridge_start + 11
    close(resumen[f"D{bridge_total}"].value, 2_243_600, "Puente — escenario previo")
    close(resumen[f"E{bridge_total}"].value, 2_168_400, "Puente — escenario seleccionado")
    close(resumen[f"F{bridge_total}"].value, 75_200, "Puente — ahorro neto")
    close(resumen[f"F{bridge_start + 3}"].value, -8_400, "Puente — Juan sobrecosto")
    close(resumen[f"F{bridge_start + 5}"].value, -8_400, "Puente — Félix sobrecosto")

    formula_count = 0
    error_cells = []
    uncached_formula_cells = []
    blue_without_comment = []
    for sheet_name in formula_wb.sheetnames:
        fws = formula_wb[sheet_name]
        vws = value_wb[sheet_name]
        for row in fws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    formula_count += 1
                    cached = vws[cell.coordinate].value
                    if isinstance(cached, str) and cached.startswith("#"):
                        error_cells.append(f"{sheet_name}!{cell.coordinate}={cached}")
                    if cached is None:
                        uncached_formula_cells.append(f"{sheet_name}!{cell.coordinate}")
                color = cell.font.color
                if color and color.type == "rgb" and color.rgb and color.rgb[-6:].upper() == "0000FF":
                    if cell.comment is None:
                        blue_without_comment.append(f"{sheet_name}!{cell.coordinate}")

    assert formula_count >= 545, f"Número inesperado de fórmulas: {formula_count}"
    assert not error_cells, f"Errores de fórmula: {error_cells}"
    assert not uncached_formula_cells, f"Fórmulas sin valor calculado: {uncached_formula_cells[:20]}"
    assert not blue_without_comment, f"Entradas azules sin comentario: {blue_without_comment[:20]}"

    print("VALIDATION PASSED")
    print(f"Formulas checked: {formula_count}")
    print("Selected Stage 1: $1,018,200")
    print("Selected Stage 2: $1,150,200")
    print("Selected Year 1: $2,168,400")
    print("Selected monthly M7+: $191,700")
    print("Annual bonus disclosed: $204,000")
    print("Stock options: TBD and excluded from cost")


if __name__ == "__main__":
    main()
