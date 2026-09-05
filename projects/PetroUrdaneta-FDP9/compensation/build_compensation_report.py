from pathlib import Path
from openpyxl import load_workbook


BASE = Path(__file__).resolve().parent
BOOK = BASE / "modelo_paquetes_personal_2_etapas.xlsx"
REPORT = BASE / "RECOMENDACION_PAQUETES_PERSONAL.md"


def money(value):
    amount = float(value)
    if amount < 0:
        return f"(${abs(amount):,.0f})"
    return f"${amount:,.0f}"


def locate_people(ws):
    result = {}
    for row in range(1, ws.max_row + 1):
        value = ws.cell(row, 5).value
        if isinstance(value, str) and value.strip() in {
            "Martin del Castillo", "Juan Conde", "Alexander Stulme", "Félix Valderrama",
            "Alan McKeon", "JJI", "Marcelo Dantas", "Jose Miguel", "TBD",
        }:
            result[value.strip()] = row
    return result


def total_row(ws):
    for row in range(1, ws.max_row + 1):
        if ws.cell(row, 4).value == "TOTAL — 9 POSICIONES":
            return row
    raise ValueError("No se encontró la fila total")


def main():
    wb = load_workbook(BOOK, data_only=True)
    personal = wb["Personal"]
    people = locate_people(personal)
    total = total_row(personal)

    rows = []
    for person, row in sorted(people.items(), key=lambda item: personal.cell(item[1], 3).value):
        stock = personal[f"AK{row}"].value
        stock_display = "TBD" if stock == "TBD" else money(stock or 0)
        rows.append(
            {
                "person": person,
                "position": personal[f"D{row}"].value,
                "package": personal[f"V{row}"].value,
                "city": personal[f"W{row}"].value,
                "housing": personal[f"Y{row}"].value,
                "monthly_consultant": personal[f"AG{row}"].value,
                "monthly_selected": personal[f"AH{row}"].value,
                "year1": personal[f"AC{row}"].value,
                "bonus": personal[f"AJ{row}"].value or 0,
                "stock": stock_display,
                "vacation": personal[f"AL{row}"].value or 0,
            }
        )

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
    bridge_reasons = {
        "Martin del Castillo": "Sin cambio.",
        "Juan Conde": "El bonus de 4 meses supera el ahorro fiscal y de home leave.",
        "Alexander Stulme": "Sin housing, impuesto ni home leave; el bonus absorbe parte del ahorro.",
        "Félix Valderrama": "El bonus de 4 meses supera el ahorro fiscal y de home leave.",
        "Alan McKeon": "Housing M7+ baja de $2.000 a $1.000 por mes.",
        "JJI": "Remote con salario base solamente.",
        "Marcelo Dantas": "Sin cambio provisional.",
        "Jose Miguel": "Local con housing; impuesto personal a su cargo.",
        "TBD": "Local provisional sin impuesto empresarial ni home leave.",
    }

    source_total = personal[f"M{total}"].value
    stage1 = personal[f"U{total}"].value
    stage2 = personal[f"AB{total}"].value
    year1 = personal[f"AC{total}"].value
    savings = personal[f"AD{total}"].value
    run_rate = personal[f"AE{total}"].value
    monthly_stage1 = personal[f"AG{total}"].value
    monthly_stage2 = personal[f"AH{total}"].value
    bonus_total = personal[f"AJ{total}"].value

    lines = [
        "# Paquetes individuales de personal — escenario seleccionado",
        "",
        "**Fecha de referencia:** 5 de septiembre de 2026  ",
        "**Moneda:** dólares estadounidenses (USD)  ",
        "**Alcance:** nueve posiciones",
        "",
        "## Resumen ejecutivo",
        "",
        f"El escenario seleccionado cuesta **{money(monthly_stage1)} por mes durante M1–M6** y **{money(monthly_stage2)} por mes recurrente desde M7**. La etapa 1 totaliza **{money(stage1)}**, la etapa 2 totaliza **{money(stage2)}** y el costo del Año 1 es **{money(year1)}**, antes de valorar stock options y costos únicos de transición. Frente al paquete anual fuente de **{money(source_total)}**, el ahorro presupuestario de Año 1 es **{money(savings)}**. El run-rate anual desde M13 es **{money(run_rate)}**.",
        "",
        "## Por qué el costo no bajó más",
        "",
        "La comparación directa debe hacerse contra el escenario anterior de Año 1, que costaba **$2.243.600** con las nueve personas como expatriadas desde M7. El escenario individual actualizado cuesta **" + money(year1) + "**, por lo que la reducción neta es **$75.200**. El ahorro es menor de lo esperado porque los bonus anuales de Juan, Alexander y Félix suman **$204.000**; durante M7–M12 se reconoce un costo de **$102.000**, que compensa gran parte del ahorro por impuestos, home leave y housing.",
        "",
        "| Persona | Año 1 anterior | Año 1 seleccionado | Ahorro / (sobrecosto) | Explicación |",
        "|---|---:|---:|---:|---|",
    ]
    selected_by_name = {item["person"]: item for item in rows}
    for name in ("Martin del Castillo", "Juan Conde", "Alexander Stulme", "Félix Valderrama", "Alan McKeon", "JJI", "Marcelo Dantas", "Jose Miguel", "TBD"):
        selected = selected_by_name[name]["year1"]
        difference = prior_year1[name] - selected
        lines.append(f"| {name} | {money(prior_year1[name])} | {money(selected)} | {money(difference)} | {bridge_reasons[name]} |")

    lines.extend([
        "",
        "## Asignaciones y beneficios confirmados",
        "",
        "| Persona | Condición M7+ | Ciudad | Housing | Mensual M1–M6 | Mensual M7+ | Año 1 | Bonus anual | Stock options | Vacaciones |",
        "|---|---|---|---|---:|---:|---:|---:|---|---:|",
    ])
    for item in rows:
        lines.append(
            f"| {item['person']} | {item['package']} | {item['city']} | {item['housing']} | "
            f"{money(item['monthly_consultant'])} | {money(item['monthly_selected'])} | {money(item['year1'])} | "
            f"{money(item['bonus'])} | {item['stock']} | {int(item['vacation'])} días |"
        )

    lines.extend(
        [
            "",
            "## Tratamiento individual",
            "",
            "### Juan Conde",
            "",
            "Juan queda como **repatriado en Maracaibo**. En Maracaibo se incluye el housing anual fuente como presupuesto para **allowance, staff house u hotel**; si la ciudad cambia a Caracas, su fórmula individual elimina housing. Juan asume su impuesto personal en Venezuela. Conserva seguro médico y transporte provisto por la compañía para ir al trabajo. Se incluye un bonus objetivo de **cuatro meses de salario**, equivalente a **$72.000 anuales**, 13 días de vacaciones pagadas y stock options con valor **TBD**.",
            "",
            "### Alexander Stulme",
            "",
            "Alexander queda como **repatriado en Maracaibo**, con el mismo esquema general de beneficios que Juan, pero vive en su propia casa y por tanto **no recibe housing**. Asume su impuesto personal, conserva seguro médico y transporte corporativo al trabajo, recibe un bonus objetivo de cuatro meses equivalente a **$60.000 anuales**, 13 días de vacaciones pagadas y stock options con valor TBD.",
            "",
            "### Félix Valderrama",
            "",
            "Félix queda con el mismo paquete de Juan: **repatriado en Maracaibo**, housing para allowance, staff house u hotel; impuesto personal a su cargo; seguro médico; transporte corporativo al trabajo; bonus objetivo de cuatro meses equivalente a **$72.000 anuales**; 13 días de vacaciones y stock options TBD.",
            "",
            "### Alan McKeon",
            "",
            "Alan permanece **expatriado** y su housing se ajusta a **$1.000 mensuales / $12.000 anuales**. Conserva seguro médico, home leave, vehículo y protección fiscal empresarial del paquete expatriado.",
            "",
            "### JJI",
            "",
            "JJI queda como **Remote** y recibe únicamente compensación base. El modelo elimina housing, seguro médico, home leave, vehículo/transporte y Tax & Social empresarial. Su costo es **$10.000 por mes**.",
            "",
            "### Jose Miguel",
            "",
            "Jose Miguel queda como **Local en Maracaibo**. Se mantiene provisionalmente el housing anual fuente de **$12.000 / $1.000 por mes**, conforme a la indicación de que ya existe un housing allowance. Debe confirmarse el importe y la política aplicable.",
            "",
            "## Supuestos pendientes",
            "",
            f"El bonus anual total divulgado es **{money(bonus_total)}**; durante M7–M12 se acumula la mitad de ese valor. Las stock options de Juan, Alexander y Félix están incluidas como beneficio, pero no tienen valoración aprobada y por ello se excluyen del costo. Se interpretó “13 de vacaciones” como **13 días de vacaciones pagadas** sin costo adicional separado del salario. Marcelo Dantas conserva provisionalmente la categoría **On rotation**, y Operations Support permanece como **TBD / Local**, preservando las ediciones manuales del usuario.",
            "",
            "## Advertencia de cumplimiento",
            "",
            "> La asignación de impuestos, clasificación laboral, base imponible de beneficios, tratamiento del bonus, vacaciones, stock options y cargas patronales requiere validación escrita de asesores venezolanos y de Recursos Humanos. Este archivo es una herramienta presupuestaria, no una opinión jurídica o fiscal.",
            "",
            "## Base y confianza",
            "",
            f"**Base.** Se preservó la versión del Excel modificada por el usuario y se archivó una copia previa a esta actualización. El paquete fuente declarado continúa en {money(source_total)}.",
            "",
            "**Confianza.** La aritmética y las fórmulas tienen confianza alta. Housing de Jose Miguel, formato de alojamiento de Juan/Félix, valoración de stock options, costos únicos y días de vacaciones requieren confirmación documental.",
            "",
        ]
    )

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
