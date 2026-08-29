#!/usr/bin/env python3
"""
Gtasck FDP-9 · Gerador de AFEs para os próximos 8 poços ESP
P-176, P-179, P-199A, P-207, P-108, P-152, P-173, P-180
"""
from __future__ import annotations
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Dados dos 8 poços ESP (do plano de reativação)
POCOS = [
    {"poco": "P-176",  "restricao": "",                  "afe": 2047100, "prio": 1},
    {"poco": "P-179",  "restricao": "",                  "afe": 2047100, "prio": 1},
    {"poco": "P-199A", "restricao": "",                  "afe": 2047100, "prio": 1},
    {"poco": "P-207",  "restricao": "",                  "afe": 2047100, "prio": 1},
    {"poco": "P-108",  "restricao": "comunidade_acesso", "afe": 2329100, "prio": 1},
    {"poco": "P-152",  "restricao": "comunidade_acesso", "afe": 2329100, "prio": 1},
    {"poco": "P-173",  "restricao": "comunidade_acesso", "afe": 2329100, "prio": 1},
    {"poco": "P-180",  "restricao": "comunidade_acesso", "afe": 2329100, "prio": 1},
]

TEMPLATE = """# AFE — Autorização para Despesa · Poço {poco}

| Campo | Valor |
|---|---|
| **AFE nº** | AFE-PU-2026-{num} |
| **Poço** | {poco} (Campo La Paz, Venezuela) |
| **Tipo** | Reativação + conversão para **ESP** |
| **Categoria** | 1 (base produtora atual) |
| **Data** | 29 de agosto de 2026 |
| **Status** | Para aprovação do COO |

---

## 1. Objetivo

Reativar o poço {poco} e convertê-lo para elevação por **ESP**, visando **1.900 BOPD**. O poço é categoria 1 e faz parte da base de 1.388 BND.

## 2. Estimativa de custo (AFE)

| # | Componente | US$ |
|---|---|---:|
| 1 | Xmas tree | 85.000 |
| 2 | Válvulas | 22.000 |
| 3 | Tubing | 95.000 |
| 4 | Rig + packers | 40.000 |
| 5 | Elevação ESP (motor+bomba+cabo+VFD) | 1.140.000 |
| 6 | Mob/demob wireline | 60.000 |
| 7 | Teste 72h (pacote modular + flare) | 35.000 |
| 8 | Rig 750hp × 12 dias @ $32.000/dia | 384.000 |
| 9 | Catering + manning + serviços extras (10%) | 186.100 |
{linha_restricao}| | **TOTAL AFE** | **US$ {total:,}** |

{nota_restricao}
## 3. Produção e retorno

| Parâmetro | Valor |
|---|---:|
| Produção estimada | 1.900 BOPD |
| Receita (a US$ 61,75/bbl) | ~US$ 117.300/dia |
| Payback simples do AFE | ~{payback} dias |

## 4. Aprovação

| Papel | Nome | Assinatura | Data |
|---|---|---|---|
| Engenharia | | | |
| Operações | | | |
| **COO** | | | |

*AFE gerado pelo Gtasck · Projeto PetroUrdaneta FDP-9*
"""

def gerar(p, num):
    restr = p["restricao"]
    if restr:
        linha_restricao = f"| 10 | Contingência restrição ({restr}) | 282.000 |\n"
        nota_restricao = f"> **Nota:** poço com restrição de **{restr}** → contingência de +15% aplicada.\n\n"
    else:
        linha_restricao = ""
        nota_restricao = "> **Nota:** poço sem restrição conhecida → sem contingência adicional.\n\n"
    payback = round(p["afe"] / 117300)
    return TEMPLATE.format(poco=p["poco"], num=f"{num:03d}", total=p["afe"],
                           linha_restricao=linha_restricao, nota_restricao=nota_restricao,
                           payback=payback)

if __name__ == "__main__":
    total = 0
    for i, p in enumerate(POCOS, start=2):
        md = gerar(p, i)
        out = os.path.join(HERE, f"AFE_{p['poco']}.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(md)
        total += p["afe"]
        print(f"AFE gerado: {out} (US$ {p['afe']:,})")
    print(f"\nTotal dos 8 AFEs: US$ {total:,} (US$ {total/1e6:.2f} MM)")
