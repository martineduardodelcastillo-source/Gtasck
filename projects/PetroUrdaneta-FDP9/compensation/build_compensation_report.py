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
    mensual = wb["Mensual"]
    supuestos = wb["Supuestos"]

    expat_tax_factor = float(supuestos["D13"].value)
    repat_tax_factor = float(supuestos["D12"].value)
    rows = []
    for row in range(11, 20):
        person = personal.cell(row, 5).value
        position = personal.cell(row, 4).value
        base = float(personal.cell(row, 6).value)
        housing = float(personal.cell(row, 7).value)
        medical = float(personal.cell(row, 8).value)
        leave = float(personal.cell(row, 9).value)
        vehicle = float(personal.cell(row, 10).value)
        tax = float(personal.cell(row, 11).value)
        consultant_monthly = float(personal.cell(row, 21).value) / 6
        expat_monthly = (base + housing + medical + leave + vehicle + tax * expat_tax_factor) / 12
        repat_housing_monthly = (base + housing + medical + vehicle + tax * repat_tax_factor) / 12
        repat_no_housing_monthly = (base + medical + vehicle + tax * repat_tax_factor) / 12
        rows.append(
            (
                person,
                position,
                consultant_monthly,
                expat_monthly,
                repat_housing_monthly,
                repat_no_housing_monthly,
                consultant_monthly * 6 + expat_monthly * 6,
                consultant_monthly * 6 + repat_housing_monthly * 6,
                consultant_monthly * 6 + repat_no_housing_monthly * 6,
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
    consultant_monthly_total = float(mensual["D27"].value)
    expat_monthly_total = float(mensual["J27"].value)
    repat_housing_monthly_total = float(mensual["J28"].value)
    repat_no_housing_monthly_total = float(mensual["J29"].value)

    lines = [
        "# Recomendación de paquetes de personal en dos etapas",
        "",
        "**Fecha de referencia:** 5 de septiembre de 2026  ",
        "**Alcance:** nueve posiciones del equipo de PetroUrdaneta  ",
        "**Moneda:** dólares estadounidenses (USD)",
        "",
        "## Recomendación ejecutiva",
        "",
        "Se recomienda estructurar el presupuesto individual en dos etapas. Durante los **meses 1 a 6**, cada persona se modela como consultor y recibe el equivalente mensual de compensación base, housing, seguro médico, home leave y vehículo. Conforme a la instrucción gerencial, el modelo asigna **0% de Tax & Social venezolano** en esta etapa. El costo agregado es **" + money(consultant_monthly_total) + " por mes** y **" + money(stage1_total) + " durante los seis meses**.",
        "",
        "Desde el **mes 7**, cada persona debe clasificarse como **repatriado** o **expatriado**. El **expatriado** conserva housing y home leave, y la empresa cubre o neutraliza el impuesto del país de trabajo mediante pago, gross-up o tax equalization. El **repatriado** pasa a condiciones locales: conserva salario base, seguro médico y vehículo; el housing depende de la ciudad; no recibe home leave; y **asume su impuesto personal**. La política inicial propone **Caracas con housing** y **Maracaibo sin housing**, con override individual.",
        "",
        "El libro parte de un escenario conservador con las nueve personas como expatriadas y la ciudad **Por definir**. Los costos únicos de transición se cargan en el mes 7 y comienzan en **$0** hasta recibir cotizaciones.",
        "",
        "## Beneficios: repatriado versus expatriado",
        "",
        "| Elemento | Repatriado | Expatriado | Diferencia práctica |",
        "|---|---|---|---|",
        "| Impuesto del país de trabajo | Lo asume el empleado | La empresa lo cubre o neutraliza | La protección fiscal es el beneficio económico principal del expatriado |",
        "| Housing | Condicional según ciudad o situación individual | Incluido | El expatriado mantiene protección de vivienda |",
        "| Home leave | No incluido | Incluido | El expatriado conserva viajes periódicos al país de origen |",
        "| Seguro médico | Incluido | Incluido | Sin diferencia en el modelo base |",
        "| Vehículo | Incluido | Incluido | Sin diferencia en el modelo base |",
        "| Condición contractual | Local / repatriada | Asignación internacional | Cambian nómina, política de movilidad y responsabilidades fiscales |",
        "| Costos de transición | Repatriación, mudanza y settling-in según cotización | Regularización, asesoría fiscal y movilidad según cotización | Se registran individualmente en M7 |",
        "",
        "> **Interpretación:** decir que el expatriado “no paga impuesto” significa, para este presupuesto, que la empresa protege su ingreso neto frente al impuesto del país de trabajo. No significa que legalmente no exista impuesto ni que no haya obligaciones en el país de origen.",
        "",
        "## Paquetes propuestos",
        "",
        "| Componente | Consultor — M1 a M6 | Repatriado — M7+ | Expatriado — M7+ |",
        "|---|---|---|---|",
        "| Compensación base | Honorario mensual equivalente | Salario local | Salario base de asignación |",
        "| Housing | Incluido por seis meses | Condicional: Caracas Sí / Maracaibo No, editable | Incluido |",
        "| Seguro médico | Incluido | Incluido | Incluido |",
        "| Home leave | Incluido por seis meses | Excluido | Incluido |",
        "| Vehículo | Incluido | Incluido | Incluido |",
        "| Impuesto del país de trabajo | 0% en el presupuesto por instrucción gerencial | Lo asume el empleado; empresa 0% por defecto | La empresa cubre / neutraliza 100% del Tax & Social fuente |",
        "| Costos únicos de transición | No incluidos | Entrada individual en M7 | Entrada individual en M7 |",
        "",
        "## Costo mensual consolidado — nueve posiciones",
        "",
        "| Período / escenario | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | M11 | M12 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        "| Consultor M1–M6 / Todos expatriados M7+ | " + " | ".join([money(consultant_monthly_total)] * 6 + [money(expat_monthly_total)] * 6) + " |",
        "| Consultor M1–M6 / Todos repatriados con housing M7+ | " + " | ".join([money(consultant_monthly_total)] * 6 + [money(repat_housing_monthly_total)] * 6) + " |",
        "| Consultor M1–M6 / Todos repatriados sin housing M7+ | " + " | ".join([money(consultant_monthly_total)] * 6 + [money(repat_no_housing_monthly_total)] * 6) + " |",
        "",
        "Los costos únicos individuales se añaden únicamente a **M7**. Por tanto, el importe real de M7 puede superar los valores recurrentes anteriores cuando se incorporen viajes, mudanza, permisos, asesoría o alojamiento temporal.",
        "",
        "## Comparación de escenarios para las nueve posiciones",
        "",
        "| Escenario | Etapa 1 M1–M6 | Costo Año 1 | Ahorro vs. fuente | Run-rate anual M13+ |",
        "|---|---:|---:|---:|---:|",
        f"| Paquete fuente original | N/A | {money(source_total)} | — | {money(source_total)} |",
        f"| Todos expatriados; empresa cubre impuesto desde M7 | {money(stage1_total)} | {money(expat_year1)} | {money(expat_savings)} | {money(expat_run_rate)} |",
        f"| Todos repatriados con housing; empleado paga impuesto | {money(stage1_total)} | {money(repat_housing_year1)} | {money(repat_housing_savings)} | {money(repat_housing_run_rate)} |",
        f"| Todos repatriados sin housing; empleado paga impuesto | {money(stage1_total)} | {money(repat_no_housing_year1)} | {money(repat_no_housing_savings)} | {money(repat_no_housing_run_rate)} |",
        "",
        "La diferencia entre expatriado y repatriado con housing desde el mes 7 incluye dos componentes: el repatriado no recibe home leave y la empresa deja de soportar el Tax & Social personal. Eliminar housing para el repatriado reduce adicionalmente el costo empresarial.",
        "",
        "## Costo mensual por persona",
        "",
        "| Persona | Posición | Consultor M1–M6 / mes | Expat M7+ / mes | Repat + housing M7+ / mes | Repat sin housing M7+ / mes |",
        "|---|---|---:|---:|---:|---:|",
    ]

    for person, position, consultant, expat, repat_housing, repat_no_housing, *_ in rows:
        lines.append(
            f"| {person} | {position} | {money(consultant)} | {money(expat)} | {money(repat_housing)} | {money(repat_no_housing)} |"
        )

    lines.extend(
        [
            "",
            "## Costo de Año 1 por persona",
            "",
            "Los importes incluyen seis meses como consultor y seis meses bajo el paquete indicado. Excluyen costos únicos de transición.",
            "",
            "| Persona | Posición | Año 1: Expat | Año 1: Repat + housing | Año 1: Repat sin housing |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for person, position, _, _, _, _, expat_year, repat_housing_year, repat_no_housing_year in rows:
        lines.append(
            f"| {person} | {position} | {money(expat_year)} | {money(repat_housing_year)} | {money(repat_no_housing_year)} |"
        )

    lines.extend(
        [
            "",
            "## Decisiones necesarias por persona",
            "",
            "| Decisión | Contenido requerido | Impacto en el modelo |",
            "|---|---|---|",
            "| Paquete desde el mes 7 | Repatriado o Expatriado | Determina housing, home leave y protección fiscal |",
            "| Política fiscal | Gross-up / tax equalization del expatriado y responsabilidad del repatriado | Determina quién soporta el impuesto del país de trabajo |",
            "| Ciudad | Caracas, Maracaibo u otra | Activa la política automática de housing para repatriados |",
            "| Override de vivienda | Automático, Sí o No | Permite reconocer vivienda propia, residencia familiar u otra excepción |",
            "| Costos de transición | Cotización individual | Se añaden a M7: viaje, mudanza, permisos, asesoría y alojamiento temporal |",
            "| Validación jurídica y fiscal | Dictamen local escrito | Confirma autorización, nómina, base imponible, retenciones y cargas patronales |",
            "",
            "## Advertencia de cumplimiento",
            "",
            "> El tratamiento de los meses 1 a 6 como consultoría sin Tax & Social venezolano y la distribución del impuesto entre empresa y empleado son **supuestos presupuestarios instruidos por la gerencia**, no conclusiones legales o fiscales. El estatus de turista no debe asumirse como autorización para trabajar ni como exención tributaria. Antes de implementar pagos o movilizaciones, se requiere asesoría venezolana escrita en materia migratoria, laboral, de nómina, seguridad social e impuestos.",
            "",
            "## Base, supuestos y nivel de confianza",
            "",
            f"**Base.** Los cálculos utilizan los nueve paquetes anuales suministrados, cuyo total verificado es {money(source_total)}. Los importes se prorratean linealmente por mes y no incluyen inflación, devaluación, dependientes ni contingencias no presentes en la fuente.",
            "",
            "**Tiempo.** El Año 1 contiene seis meses de consultoría y seis meses de repatriación o expatriación. Los costos únicos se cargan en M7.",
            "",
            "**Supuestos.** Tax & Social en consultoría es 0%; el expatriado recibe cobertura empresarial equivalente al 100% del Tax & Social fuente; el repatriado asume su impuesto personal y el factor empresarial comienza en 0%; Caracas tiene housing y Maracaibo no para repatriados; home leave se elimina al repatriar.",
            "",
            "**Fuentes y confianza.** La compensación proviene de la imagen suministrada y fue conciliada contra su total. La aritmética tiene confianza alta; la base imponible, las cargas patronales, los costos únicos y el tratamiento jurídico-fiscal requieren dictámenes y cotizaciones.",
            "",
            "**Cumplimiento.** Este documento es una herramienta de planeación presupuestaria y no sustituye asesoría legal, migratoria, laboral o tributaria.",
            "",
        ]
    )

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
