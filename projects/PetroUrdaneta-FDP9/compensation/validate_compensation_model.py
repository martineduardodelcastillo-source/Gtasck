from pathlib import Path
from math import isclose

from openpyxl import load_workbook


BASE = Path(__file__).resolve().parent
BOOK = BASE / "modelo_paquetes_personal_2_etapas.xlsx"
SOURCE = BASE / "source" / "package_source_2026-09-05.jpeg"


def close(actual, expected, label):
    assert actual is not None, f"{label}: valor calculado ausente"
    assert isclose(float(actual), float(expected), rel_tol=0, abs_tol=0.01), (
        f"{label}: esperado {expected}, obtenido {actual}"
    )


def main():
    assert BOOK.exists(), f"No existe {BOOK}"
    assert SOURCE.exists(), f"No existe {SOURCE}"

    formula_wb = load_workbook(BOOK, data_only=False)
    value_wb = load_workbook(BOOK, data_only=True)
    assert formula_wb.sheetnames == ["Resumen", "Supuestos", "Personal", "Mensual", "Definiciones"]

    personal = value_wb["Personal"]
    resumen = value_wb["Resumen"]
    mensual = value_wb["Mensual"]
    supuestos = value_wb["Supuestos"]
    personal_formulas = formula_wb["Personal"]

    assert 'V11="Expatriado"' in personal_formulas["AA11"].value
    assert 'V11="Repatriado"' in personal_formulas["AA11"].value
    assert personal_formulas["AH11"].value.replace("'", "") == "=AA11/Supuestos!$D$10"
    assert personal_formulas["AI11"].value == "=AH11+Z11"

    close(supuestos["D12"].value, 0, "Factor empresa — repatriado")
    close(supuestos["D13"].value, 1, "Factor empresa — expatriado")
    close(personal["L21"].value, 2_396_800, "Paquete anual calculado")
    close(personal["M21"].value, 2_396_800, "Paquete anual declarado")
    close(personal["N21"].value, 0, "Variación fuente")
    close(personal["U21"].value, 1_045_200, "Etapa 1")
    close(personal["AB21"].value, 1_198_400, "Etapa 2 seleccionada")
    close(personal["AC21"].value, 2_243_600, "Año 1 seleccionado")
    close(personal["AD21"].value, 153_200, "Ahorro Año 1 seleccionado")
    close(personal["AE21"].value, 2_396_800, "Run-rate seleccionado")
    close(personal["AG21"].value, 174_200, "Personal — mensual consultor consolidado")
    close(personal["AH21"].value, 199_733.333333, "Personal — mensual M7+ seleccionado")
    close(personal["AI21"].value, 199_733.333333, "Personal — M7 con transición")
    close(personal["AG11"].value, 37_666.666667, "Martin — mensual consultor")
    close(personal["AH11"].value, 43_666.666667, "Martin — mensual M7+ expatriado")
    close(personal["AI11"].value, 43_666.666667, "Martin — M7 con transición")

    close(resumen["F22"].value, 2_243_600, "Todos expatriados — Año 1")
    close(resumen["F23"].value, 2_038_400, "Todos repatriados con housing — Año 1")
    close(resumen["G23"].value, 358_400, "Todos repatriados con housing — ahorro")
    close(resumen["H23"].value, 1_986_400, "Todos repatriados con housing — run-rate")
    close(resumen["F24"].value, 1_939_400, "Todos repatriados sin housing — Año 1")
    close(resumen["G24"].value, 457_400, "Todos repatriados sin housing — ahorro")
    close(resumen["H24"].value, 1_788_400, "Todos repatriados sin housing — run-rate")

    for cell in ("D27", "E27", "F27", "G27", "H27", "I27"):
        close(mensual[cell].value, 174_200, f"Consultoría mensual consolidada {cell}")
    for cell in ("J27", "K27", "L27", "M27", "N27", "O27"):
        close(mensual[cell].value, 199_733.333333, f"Expatriados mensuales {cell}")
    for cell in ("J28", "K28", "L28", "M28", "N28", "O28"):
        close(mensual[cell].value, 165_533.333333, f"Repatriados con housing mensuales {cell}")
    for cell in ("J29", "K29", "L29", "M29", "N29", "O29"):
        close(mensual[cell].value, 149_033.333333, f"Repatriados sin housing mensuales {cell}")
    close(mensual["P27"].value, 2_243_600, "Mensual — Año 1 expatriados")
    close(mensual["P28"].value, 2_038_400, "Mensual — Año 1 repatriados con housing")
    close(mensual["P29"].value, 1_939_400, "Mensual — Año 1 repatriados sin housing")
    close(mensual["S21"].value, personal["AC21"].value, "Detalle mensual vs. Personal")

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

    assert formula_count >= 500, f"Número inesperado de fórmulas: {formula_count}"
    assert not error_cells, f"Errores de fórmula: {error_cells}"
    assert not uncached_formula_cells, f"Fórmulas sin valor calculado: {uncached_formula_cells[:20]}"
    assert not blue_without_comment, f"Entradas azules sin comentario: {blue_without_comment[:20]}"
    assert len(formula_wb["Personal"].data_validations.dataValidation) == 3

    print("VALIDATION PASSED")
    print(f"Formulas checked: {formula_count}")
    print("Source total: $2,396,800")
    print("Monthly consultant total M1–M6: $174,200")
    print("Monthly expatriate total M7–M12: $199,733.33")
    print("Monthly repatriate total with housing M7–M12: $165,533.33")
    print("Monthly repatriate total without housing M7–M12: $149,033.33")
    print("Year 1 — all expatriates: $2,243,600")
    print("Year 1 — all repatriates with housing: $2,038,400")
    print("Year 1 — all repatriates without housing: $1,939,400")


if __name__ == "__main__":
    main()
