#!/usr/bin/env python3
"""
Gtasck FDP-9 · Gerador de AFEs para os 31 poços PCP/gas-lift restantes
Lê o plano de reativação e gera AFE individual por poço (não-ESP).
"""
from __future__ import annotations
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
PLANO = os.path.join(HERE, "plano_reativacao_poco_a_poco.csv")

# Componentes AFE por método (US$)
COMPONENTES = {
    "PCP":      {"xmas": 85_000, "valv": 22_000, "tubing": 95_000, "rig_packers": 40_000, "lift": 540_000, "mob": 60_000, "teste": 35_000, "rig_dias": 7,  "rig_rate": 18_000},
    "ePCP":     {"xmas": 85_000, "valv": 22_000, "tubing": 95_000, "rig_packers": 40_000, "lift": 620_000, "mob": 60_000, "teste": 35_000, "rig_dias": 8,  "rig_rate": 18_000},
    "gas_lift": {"xmas": 85_000, "valv": 22_000, "tubing": 95_000, "rig_packers": 40_000, "lift": 380_000, "mob": 60_000, "teste": 35_000, "rig_dias": 5,  "rig_rate": 18_000},
    "rod_pump": {"xmas": 85_000, "valv": 22_000, "tubing": 95_000, "rig_packers": 40_000, "lift": 210_000, "mob": 60_000, "teste": 35_000, "rig_dias": 4,  "rig_rate": 18_000},
}
RESTRICAO_MULT = {"comunidade_acesso": 0.15, "equip_superficie_ineconomico": 0.35, "reparo_subsuperficie_maior": 0.60, "alta_agua": 0.10}

TEMPLATE = """# AFE — Autorização para Despesa · Poço {poco}

| Campo | Valor |
|---|---|
| **AFE nº** | AFE-PU-2026-{num} |
| **Poço** | {poco} (Campo {campo}, Venezuela) |
| **Tipo** | Reativação + elevação por **{lift}** |
| **Data** | 29 de agosto de 2026 |
| **Status** | Para aprovação do COO |

---

## 1. Objetivo

Reativar o poço {poco} com elevação por **{lift}**, visando **{bpd} BOPD**.

## 2. Estimativa de custo (AFE)

| # | Componente | US$ |
|---|---|---:|
| 1 | Xmas tree | {xmas:,} |
| 2 | Válvulas | {valv:,} |
| 3 | Tubing | {tubing:,} |
| 4 | Rig + packers | {rig_packers:,} |
| 5 | Elevação {lift} | {lift_cost:,} |
| 6 | Mob/demob wireline | {mob:,} |
| 7 | Teste 72h | {teste:,} |
| 8 | Rig 350hp × {rig_dias} dias @ ${rig_rate:,}/dia | {rig_total:,} |
{linha_restricao}| | **TOTAL AFE** | **US$ {total:,}** |

{nota_restricao}
## 3. Produção e retorno

| Parâmetro | Valor |
|---|---:|
| Produção estimada | {bpd} BOPD |
| Receita (a US$ 61,75/bbl) | ~US$ {receita:,}/dia |
| Payback simples do AFE | ~{payback} dias |

## 4. Aprovação

| Papel | Nome | Assinatura | Data |
|---|---|---|---|
| Engenharia | | | |
| Operações | | | |
| **COO** | | | |

*AFE gerado pelo Gtasck · Projeto PetroUrdaneta FDP-9*
"""

def carregar():
    with open(PLANO, encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f, delimiter=";")]
    return [r for r in rows if r["lift"] not in ("ESP", "abandono")]

def gerar(r, num):
    lift = r["lift"]
    c = COMPONENTES[lift]
    restr = r["restricao"]
    mult = RESTRICAO_MULT.get(restr, 0.0)
    rig_total = c["rig_dias"] * c["rig_rate"]
    subtotal = c["xmas"] + c["valv"] + c["tubing"] + c["rig_packers"] + c["lift"] + c["mob"] + c["teste"] + rig_total
    conting = round(subtotal * mult)
    total = subtotal + conting
    bpd = int(r["bpd"])
    receita = round(bpd * 61.75)
    payback = round(total / receita) if receita else 0
    if restr:
        linha_restricao = f"| 9 | Contingência restrição ({restr}) | {conting:,} |\n"
        nota_restricao = f"> **Nota:** poço com restrição de **{restr}** → contingência de +{int(mult*100)}% aplicada.\n\n"
    else:
        linha_restricao = ""
        nota_restricao = "> **Nota:** poço sem restrição conhecida → sem contingência adicional.\n\n"
    return TEMPLATE.format(poco=r["poco"], campo=r["campo"], lift=lift, num=f"{num:03d}",
                           bpd=bpd, xmas=c["xmas"], valv=c["valv"], tubing=c["tubing"],
                           rig_packers=c["rig_packers"], lift_cost=c["lift"], mob=c["mob"],
                           teste=c["teste"], rig_dias=c["rig_dias"], rig_rate=c["rig_rate"],
                           rig_total=rig_total, linha_restricao=linha_restricao,
                           nota_restricao=nota_restricao, total=total, receita=receita, payback=payback), total

if __name__ == "__main__":
    rows = carregar()
    total_geral = 0
    for i, r in enumerate(rows, start=10):
        md, total = gerar(r, i)
        out = os.path.join(HERE, f"AFE_{r['poco']}.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(md)
        total_geral += total
    print(f"AFEs gerados: {len(rows)} poços (PCP/ePCP/gas-lift/rod)")
    print(f"Total: US$ {total_geral:,} (US$ {total_geral/1e6:.2f} MM)")
