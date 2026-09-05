from pathlib import Path
from openpyxl import load_workbook


BASE = Path(__file__).resolve().parent
BOOK = BASE / "modelo_paquetes_personal_2_etapas.xlsx"
REPORT = BASE / "RECOMENDACION_PAQUETES_PERSONAL.md"


def money(value):
    return f"${value:,.0f}"


def main():
    wb = load_workbook(BOOK, data_only=True)
    personal = wb["Personal"]
    resumen = wb["Resumen"]

    rows = []
    for row in range(11, 20):
        person = personal.cell(row, 5).value
        position = personal.cell(row, 4).value
        stage1 = float(personal.cell(row, 21).value)
        expat_stage2 = float(personal.cell(row, 13).value) / 2
        repat_with_housing_stage2 = (
            float(personal.cell(row, 6).value)
            + float(personal.cell(row, 7).value)
            + float(personal.cell(row, 8).value)
            + float(personal.cell(row, 10).value)
            + float(personal.cell(row, 11).value)
        ) / 2
        repat_without_housing_stage2 = repat_with_housing_stage2 - float(personal.cell(row, 7).value) / 2
        rows.append(
            (
                person,
                position,
                stage1,
                stage1 + expat_stage2,
                stage1 + repat_with_housing_stage2,
                stage1 + repat_without_housing_stage2,
            )
        )

    source_total = float(personal["M21"].value)
    stage1_total = float(personal["U21"].value)
    expat_year1 = float(resumen["F22"].value)
    repat_housing_year1 = float(resumen["F23"].value)
    repat_no_housing_year1 = float(resumen["F24"].value)
    expat_savings = float(resumen["G22"].value)
    repat_housing_savings = float(resumen["G23"].value)
    repat_no_housing_savings = float(resumen["G24"].value)
    expat_run_rate = float(resumen["H22"].value)
    repat_housing_run_rate = float(resumen["H23"].value)
    repat_no_housing_run_rate = float(resumen["H24"].value)

    lines = [
        "# Recomendación de paquetes de personal en dos etapas",
        "",
        "**Fecha de referencia:** 5 de septiembre de 2026  ",
        "**Alcance:** nueve posiciones del equipo de PetroUrdaneta  ",
        "**Moneda:** dólares estadounidenses (USD)",
        "",
        "## Recomendación ejecutiva",
        "",
        "Se recomienda estructurar el presupuesto individual en dos etapas. Durante los **meses 1 a 6**, cada persona se modela como consultor y recibe el equivalente a seis meses de compensación base más seis meses de housing, seguro médico, home leave y vehículo. Conforme a la instrucción gerencial, el modelo asigna **0% de Tax & Social venezolano** en esta etapa. El costo agregado de los primeros seis meses es **" + money(stage1_total) + "**.",
        "",
        "Desde el **mes 7**, cada persona debe clasificarse como **repatriado** o **expatriado**. Para repatriados, se recomienda conservar salario base, seguro médico, vehículo y Tax & Social; eliminar home leave; y condicionar housing a la residencia. La política presupuestaria inicial propone **Caracas con housing** y **Maracaibo sin housing**, con posibilidad de override individual. Para expatriados, se recomienda conservar el paquete fuente completo, incluyendo housing y home leave.",
        "",
        "El libro parte de un enfoque conservador: las nueve personas aparecen inicialmente como expatriadas y la ciudad queda **Por definir**, evitando subestimar costos antes de tomar las decisiones individuales. Los costos únicos de transición se mantienen en **$0** hasta contar con cotizaciones.",
        "",
        "## Paquetes propuestos",
        "",
        "| Componente | Consultor — M1 a M6 | Repatriado — M7+ | Expatriado — M7+ |",
        "|---|---:|---:|---:|",
        "| Compensación base | 6/12 del valor anual, tratada como honorario | Incluida | Incluida |",
        "| Housing | Incluido por seis meses | Condicional: Caracas Sí / Maracaibo No, editable | Incluido |",
        "| Seguro médico | Incluido | Incluido | Incluido |",
        "| Home leave | Incluido por seis meses | Excluido | Incluido |",
        "| Vehículo | Incluido | Incluido | Incluido |",
        "| Tax & Social venezolano | 0% por supuesto gerencial | Incluido | Incluido |",
        "| Costos únicos de transición | No incluidos | Entrada individual pendiente | Entrada individual pendiente |",
        "",
        "## Comparación de escenarios para las nueve posiciones",
        "",
        "| Escenario | Etapa 1 M1–M6 | Costo Año 1 | Ahorro vs. fuente | Run-rate anual M13+ |",
        "|---|---:|---:|---:|---:|",
        f"| Paquete fuente original | N/A | {money(source_total)} | — | {money(source_total)} |",
        f"| Todos expatriados desde M7 | {money(stage1_total)} | {money(expat_year1)} | {money(expat_savings)} | {money(expat_run_rate)} |",
        f"| Todos repatriados con housing desde M7 | {money(stage1_total)} | {money(repat_housing_year1)} | {money(repat_housing_savings)} | {money(repat_housing_run_rate)} |",
        f"| Todos repatriados sin housing desde M7 | {money(stage1_total)} | {money(repat_no_housing_year1)} | {money(repat_no_housing_savings)} | {money(repat_no_housing_run_rate)} |",
        "",
        "El escenario de expatriados produce un ahorro de Año 1 de **" + money(expat_savings) + "**, generado por no aplicar Tax & Social durante los primeros seis meses. La repatriación con housing añade un ahorro de **" + money(repat_housing_savings - expat_savings) + "** frente al escenario expatriado, al eliminar home leave durante los meses 7 a 12. La repatriación sin housing añade otros **" + money(repat_no_housing_savings - repat_housing_savings) + "** de ahorro en el mismo período.",
        "",
        "## Costo de Año 1 por persona",
        "",
        "Los importes siguientes incluyen los seis meses iniciales como consultor y seis meses bajo el paquete indicado. Excluyen costos únicos de transición.",
        "",
        "| Persona | Posición | Etapa 1 M1–M6 | Año 1: Expat | Año 1: Repat + housing | Año 1: Repat sin housing |",
        "|---|---|---:|---:|---:|---:|",
    ]

    for person, position, stage1, expat, repat_housing, repat_no_housing in rows:
        lines.append(
            f"| {person} | {position} | {money(stage1)} | {money(expat)} | {money(repat_housing)} | {money(repat_no_housing)} |"
        )

    lines.extend(
        [
            "",
            "## Decisiones necesarias por persona",
            "",
            "| Decisión | Contenido requerido | Impacto en el modelo |",
            "|---|---|---|",
            "| Paquete desde el mes 7 | Repatriado o Expatriado | Determina si se mantiene home leave y la estructura internacional |",
            "| Ciudad | Caracas, Maracaibo u otra | Activa la política automática de housing para repatriados |",
            "| Override de vivienda | Automático, Sí o No | Permite reconocer vivienda propia, residencia familiar u otra excepción |",
            "| Costos de transición | Cotización individual | Añade viaje, mudanza, permisos, asesoría y alojamiento temporal |",
            "| Validación jurídica y fiscal | Dictamen local escrito | Confirma autorización de trabajo, clasificación, nómina, retenciones y seguridad social |",
            "",
            "## Advertencia de cumplimiento",
            "",
            "> El tratamiento de los meses 1 a 6 como consultoría sin Tax & Social venezolano es un **supuesto presupuestario instruido por la gerencia**, no una conclusión legal o fiscal. El estatus de turista no debe asumirse por sí solo como autorización para trabajar ni como exención tributaria. Antes de implementar pagos o movilizaciones, se requiere asesoría venezolana escrita en materia migratoria, laboral, de nómina, seguridad social e impuestos.",
            "",
            "## Base, supuestos y nivel de confianza",
            "",
            f"**Base.** Los cálculos utilizan los nueve paquetes anuales de la tabla suministrada, cuyo total verificado es {money(source_total)}. Los importes se prorratean linealmente por mes y no incluyen inflación, devaluación, gross-up adicional, dependientes ni contingencias no presentes en la fuente.",
            "",
            "**Tiempo.** El modelo se preparó con fecha de referencia 5 de septiembre de 2026 y representa un Año 1 compuesto por seis meses de consultoría y seis meses de repatriación o expatriación.",
            "",
            "**Supuestos.** Tax & Social en la etapa de consultoría es 0%; Caracas tiene housing y Maracaibo no tiene housing para repatriados; home leave se elimina al repatriar; y los costos únicos de transición comienzan en $0 hasta ser cotizados.",
            "",
            "**Fuentes y confianza.** Los valores de compensación provienen exclusivamente de la imagen suministrada por el usuario y fueron conciliados contra el total indicado. La confianza en la aritmética es alta; la confianza en los costos únicos y en el tratamiento jurídico-fiscal es baja hasta recibir cotizaciones y dictámenes profesionales.",
            "",
            "**Cumplimiento.** Este documento es una herramienta de planeación presupuestaria y no sustituye asesoría legal, migratoria, laboral o tributaria.",
            "",
        ]
    )

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
