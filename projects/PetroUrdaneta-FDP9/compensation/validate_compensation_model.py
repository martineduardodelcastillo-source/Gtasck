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
    assert formula_wb.sheetnames == ["Resumen", "Supuestos", "Personal", "Definiciones"]

    personal = value_wb["Personal"]
    resumen = value_wb["Resumen"]

    close(personal["L21"].value, 2_396_800, "Paquete anual calculado")
    close(personal["M21"].value, 2_396_800, "Paquete anual declarado")
    close(personal["N21"].value, 0, "Variación fuente")
    close(personal["U21"].value, 1_045_200, "Etapa 1")
    close(personal["AB21"].value, 1_198_400, "Etapa 2 seleccionada")
    close(personal["AC21"].value, 2_243_600, "Año 1 seleccionado")
    close(personal["AD21"].value, 153_200, "Ahorro Año 1 seleccionado")
    close(personal["AE21"].value, 2_396_800, "Run-rate seleccionado")

    close(resumen["F22"].value, 2_243_600, "Todos expatriados — Año 1")
    close(resumen["F23"].value, 2_191_600, "Todos repatriados con housing — Año 1")
    close(resumen["G23"].value, 205_200, "Todos repatriados con housing — ahorro")
    close(resumen["H23"].value, 2_292_800, "Todos repatriados con housing — run-rate")
    close(resumen["F24"].value, 2_092_600, "Todos repatriados sin housing — Año 1")
    close(resumen["G24"].value, 304_200, "Todos repatriados sin housing — ahorro")
    close(resumen["H24"].value, 2_094_800, "Todos repatriados sin housing — run-rate")

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

    assert formula_count >= 200, f"Número inesperado de fórmulas: {formula_count}"
    assert not error_cells, f"Errores de fórmula: {error_cells}"
    assert not uncached_formula_cells, f"Fórmulas sin valor calculado: {uncached_formula_cells[:20]}"
    assert not blue_without_comment, f"Entradas azules sin comentario: {blue_without_comment[:20]}"
    assert len(formula_wb["Personal"].data_validations.dataValidation) == 3

    print("VALIDATION PASSED")
    print(f"Formulas checked: {formula_count}")
    print("Source total: $2,396,800")
    print("Stage 1 (6-month consultant): $1,045,200")
    print("Year 1 — all expatriates: $2,243,600")
    print("Year 1 — all repatriates with housing: $2,191,600")
    print("Year 1 — all repatriates without housing: $2,092,600")


if __name__ == "__main__":
    main()
