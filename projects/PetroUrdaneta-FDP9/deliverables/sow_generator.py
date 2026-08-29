#!/usr/bin/env python3
"""
Gtasck FDP-9 · Gerador de SOWs em formato MSA para gates G-04, G-05, G-06
Reutiliza a estrutura MSA aprovada (open-book, cost-plus, AFE separado).
"""
from __future__ import annotations
import os

HERE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = """# STATEMENT OF WORK (SOW) · MSA — Gate {gate}
## {titulo} · PetroUrdaneta FDP-9

| Campo | Valor |
|---|---|
| **SOW nº** | SOW-PU-{gate_clean}-2026-001 |
| **MSA de referência** | {msa} |
| **Contratante (Company)** | PetroUrdaneta (COO Office) |
| **Contratada (Contractor)** | [a definir por tender] |
| **Modelo** | Open-book MSA · cost-plus · AFE separado |
| **Data de emissão** | 29 de agosto de 2026 |

---

## 1. OBJETIVO E ESCOPO

{objetivo}

**Incluído no escopo:**
{escopo}

**Excluído do escopo (a solicitar em markup):** serviços e materiais não listados, a fornecer em base **cost-plus** conforme cláusula 8.

## 2. CONFORMIDADE

Este SOW está em conformidade com o **FDP v9** e baseado no **work program** aprovado. Normas aplicáveis: {normas}.

## 3. TABELA DE PREÇO POR UNIDADE (PRICE PER UNIT TABLE)

| Item | Descrição | Unidade | Qtd | Preço unit. (US$) | Total (US$) |
|---|---|---|---:|---:|---:|
{precos}
| | | | | **TOTAL** | **{total}** |

> Serviços/materiais não previstos: **cost-plus** com markup de **[10]%** sobre custo comprovado (open-book).

## 4. CRONOGRAMA (engineering design + execution time)

| Fase | Atividade | Duração |
|---|---|---|
{cronograma}
| | **TOTAL** | **{prazo}** |

## 5. KPIs DE PERFORMANCE E MODELO DE PENALIDADE

| KPI | Meta | Medição | Penalidade |
|---|---|---|---|
| **Uptime** | ≥ 97% | horas operacionais / programadas | -2% do valor mensal por ponto abaixo |
| **On-time delivery** | ≥ 95% | marcos no prazo / total | -1% por marco atrasado |
| **NPT** | ≤ 5% | horas NPT / totais | -1% por ponto acima |
| **Delayed vs. on-time** | on-time | data de entrega vs. cronograma | -0,5%/semana (cap 10%) |

**Tracking methodology:** registro diário de uptime/NPT; reconciliação semanal; relatório mensal de KPI.

## 6. INVESTIGAÇÃO DE INCIDENTES E QAQC

- **Near misses e acidentes:** notificação em 24h; investigação raiz-causa em 72h; relatório em 7 dias.
- **QAQC de equipamento:** certificados de calibração válidos; parâmetros QAQC por equipamento.
- **Failure mode investigation:** processo formal; **equipment replacement clause** — substituição em 48h sem custo adicional.

## 7. EQUIPAMENTO DA CONTRATADA (tabela)

| Equipamento | Capacidade | Ano de fabricação | Última manutenção |
|---|---|---|---|
{equipamento}

## 8. LOGÍSTICA, IMPORTAÇÃO E ALFÂNDEGA

A Contratada é responsável por **logística, importação e desembaraço aduaneiro** de todo o equipamento, com **prompt delivery**. Prazos de importação reportados semanalmente.

## 9. SUBCONTRATADOS

Subcontratados **aprovados previamente** pela Company e gerenciados integralmente pela Contratada. Serviços/equipamentos subcontratados em base **cost-plus** com o markup da cláusula 3.

## 10. PESSOAL DE BACK OFFICE (mobilização + CVs)

| Função | Qtd | Alocação | CV anexo |
|---|---:|---|---|
{pessoal}

## 11. EPCM INTEGRATOR E PMO

O **EPCM integrator** nomeado é **[a nomear]**. O **PMO** designado será alocado **diretamente ao projeto** e planejará em conjunto com todos os demais workstreams.

## 12. AFE (Authorization for Expenditure)

Este projeto é tratado como **AFE separado** (ver formulário AFE anexo). **AFE nº:** AFE-PU-{gate_clean}-2026-001 · **Valor:** US$ {total}.

## 13. CLÁUSULAS PADRÃO MSA

Incorporam-se as cláusulas padrão de MSA: confidencialidade, propriedade intelectual, indenização, seguro, força maior, rescisão, lei aplicável e resolução de disputas.

---

## APROVAÇÃO

| Papel | Nome | Assinatura | Data |
|---|---|---|---|
| Company — Engenharia | | | |
| Company — Contratos | | | |
| **Company — COO** | | | |
| Contractor — Representative | | | |

*SOW gerado pelo Gtasck · Conforme MSA Tender Document Requirements (open-book, cost-plus, AFE separado)*

## Referências

- FDP v9-DRAFT COMPLETE (documento base do projeto)
- Normas: {normas}
"""

GATES = {
    "G-04": {
        "titulo": "Modelo de Rede Multifásica (Estacionário/Transiente + 4/6/8\")",
        "msa": "MSA EPCM",
        "objetivo": "Construir o **modelo de rede multifásica** estacionário e transiente para fechamento do gate G-04, comparando diâmetros 4\"/6\"/8\" por EPF/classe de trunk e definindo os envelopes das bombas multiphase.",
        "escopo": "- Modelo estacionário/transiente da rede (well→EPF→FSB)\n- Survey de rota e perfil de elevação\n- Comparação 4\"/6\"/8\" por EPF/classe de trunk\n- Envelopes de operação das bombas multiphase (GVF, viscosidade, areia, turndown)\n- Relatório de dimensionamento + recomendação por trunk",
        "normas": "API RP 14E, ASME B31.3/B31.8, NORSOK Z-CR007, COVENIN",
        "precos": "| 3.1 | Mob/demob equipe de modelagem | lump sum | 1 | 50.000 | 50.000 |\n| 3.2 | Survey de rota + perfil de elevação | por trunk | 12 | 15.000 | 180.000 |\n| 3.3 | Modelo estacionário/transiente (software + engenharia) | lump sum | 1 | 220.000 | 220.000 |\n| 3.4 | Comparação 4/6/8\" + envelopes de bomba | lump sum | 1 | 100.000 | 100.000 |\n| 3.5 | Relatório de dimensionamento | lump sum | 1 | 50.000 | 50.000 |",
        "total": "600.000",
        "cronograma": "| 1 | Survey de rota + perfil | 3 sem |\n| 2 | Modelo estacionário/transiente | 6 sem |\n| 3 | Comparação 4/6/8\" + envelopes | 3 sem |\n| 4 | Relatório | 2 sem |",
        "prazo": "8–14 semanas",
        "equipamento": "| Estação de modelagem (OLGA/LEAP/PIPESIM) | licença transiente | [ano] | [data] |\n| GPS/GIS de survey | ±0,1 m | [ano] | [data] |",
        "pessoal": "| Project Manager | 1 | dedicado | sim |\n| Engenheiro de flow assurance | 2 | dedicado | sim |\n| Especialista em transientes | 1 | dedicado | sim |\n| Topógrafo | 2 | campo | sim |",
    },
    "G-05": {
        "titulo": "Pigging e Dimensionamento de Slug (Vaso de Entrada)",
        "msa": "MSA EPCM",
        "objetivo": "Definir o **programa de pigging** e dimensionar o **vaso de slug** de entrada do FSB para fechamento do gate G-05, a partir dos volumes de slug transientes e da capacidade do separador.",
        "escopo": "- Programa de pigging (tipo, frequência, velocidade controlada)\n- Modelo transiente de pigging (volumes de slug)\n- Dimensionamento do vaso de slug (working/surge volume)\n- Lógica de transferência de líquido + bypass\n- Relatório de pigging + slug + freeze de trunk/vaso",
        "normas": "API RP 14E, ASME B31.3/B31.8, NORSOK Z-CR007, COVENIN",
        "precos": "| 3.1 | Mob/demob equipe | lump sum | 1 | 40.000 | 40.000 |\n| 3.2 | Modelo transiente de pigging | lump sum | 1 | 180.000 | 180.000 |\n| 3.3 | Dimensionamento do vaso de slug | lump sum | 1 | 120.000 | 120.000 |\n| 3.4 | Programa de pigging + lógica | lump sum | 1 | 80.000 | 80.000 |\n| 3.5 | Relatório + freeze | lump sum | 1 | 40.000 | 40.000 |",
        "total": "460.000",
        "cronograma": "| 1 | Modelo transiente de pigging | 5 sem |\n| 2 | Dimensionamento do vaso de slug | 3 sem |\n| 3 | Programa de pigging + lógica | 3 sem |\n| 4 | Relatório + freeze | 2 sem |",
        "prazo": "8–14 semanas",
        "equipamento": "| Estação de modelagem transiente | licença | [ano] | [data] |\n| Pig de inspeção (referência) | conforme trunk | [ano] | [data] |",
        "pessoal": "| Project Manager | 1 | dedicado | sim |\n| Engenheiro de flow assurance | 2 | dedicado | sim |\n| Especialista em pigging | 1 | dedicado | sim |",
    },
    "G-06": {
        "titulo": "ESD/PSD e Relief (HAZOP, LOPA/SIL, Causa-Efeito, Flare)",
        "msa": "MSA EPCM",
        "objetivo": "Executar o pacote de **process safety** para fechamento do gate G-06: HAZOP, LOPA/SIL, matriz causa-efeito, relief/depressurização e hidráulica de flare.",
        "escopo": "- HAZOP (todos os nós)\n- LOPA/SIL (funções SIF)\n- Matriz causa-efeito (ESD/PSD)\n- Relief/depressurização (API 520/521)\n- Hidráulica de flare + radiation/dispersion\n- Relatório de process safety + emissão para construção/PSSR",
        "normas": "API 520/521, IEC 61882, IEC 61511, CCPS, NORSOK Z-CR007, COVENIN",
        "precos": "| 3.1 | Mob/demob equipe de process safety | lump sum | 1 | 60.000 | 60.000 |\n| 3.2 | HAZOP (todos os nós) | por nó | 20 | 12.000 | 240.000 |\n| 3.3 | LOPA/SIL | por SIF | 15 | 10.000 | 150.000 |\n| 3.4 | Matriz causa-efeito + relief/depressurização | lump sum | 1 | 180.000 | 180.000 |\n| 3.5 | Hidráulica de flare + radiation | lump sum | 1 | 120.000 | 120.000 |\n| 3.6 | Relatório + emissão PSSR | lump sum | 1 | 50.000 | 50.000 |",
        "total": "800.000",
        "cronograma": "| 1 | HAZOP | 6 sem |\n| 2 | LOPA/SIL | 4 sem |\n| 3 | Causa-efeito + relief | 5 sem |\n| 4 | Flare + radiation | 3 sem |\n| 5 | Relatório + PSSR | 2 sem |",
        "prazo": "12–20 semanas",
        "equipamento": "| Estação HAZOP/LOPA (PHA-Pro ou similar) | licença | [ano] | [data] |\n| Software de flare (FlareSim ou similar) | licença | [ano] | [data] |",
        "pessoal": "| Project Manager | 1 | dedicado | sim |\n| Facilitador HAZOP | 1 | dedicado | sim |\n| Especialista LOPA/SIL | 1 | dedicado | sim |\n| Engenheiro de relief/flare | 2 | dedicado | sim |\n| HSE officer | 1 | campo | sim |",
    },
}

def gerar(gate: str) -> str:
    g = GATES[gate]
    return TEMPLATE.format(gate=gate, gate_clean=gate.replace("-", ""), **g)

if __name__ == "__main__":
    for gate in GATES:
        md = gerar(gate)
        out = os.path.join(HERE, f"SOW_{gate.replace('-','')}.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"SOW gerado: {out}")
