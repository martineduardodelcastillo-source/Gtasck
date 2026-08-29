#!/usr/bin/env python3
"""
Gtasck FDP-9 · WS4 — Priorização dos bloqueadores FDP
Cruza severidade × impacto-em-gate × esforço para rankear os 52 bloqueadores
(24 PS + 11 FA + 5 OT) e os 13 gates. Saída: fila de ataque priorizada.
"""
from __future__ import annotations
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
RISK_CSV = os.path.join(HERE, "..", "registers", "risk_register.csv")

# Peso de "bloqueia" — quanto mais a jusante no caminho crítico, maior a prioridade
PESO_BLOQUEIO = {
    "Base FEED de facilidades": 10, "Freeze de bombas/linhas/tratamento": 9,
    "AFE de upgrade do FSB": 9, "Compra de trunk/bombas": 9,
    "Freeze de trunk/vaso de entrada": 8, "Emissão para construção/PSSR": 8,
    "Compra de geradores/switchgear": 7, "AFE da planta de água": 7,
    "AFE do piloto de exportação": 6, "Sanção terminal/exportação": 8,
    "AFE do pacote NGL": 5, "AFE de LNG": 5, "Construção e operação de campo": 10,
    "FEED blocker": 9, "Screening only": 4, "Qualified option": 5, "Data absent": 7,
    "Scope conflict": 6, "Source reconciliation": 8,
}
PESO_SEV = {"Alta": 3, "Média": 2, "Baixa": 1}

def priorizar() -> list[dict]:
    rows = []
    with open(RISK_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            sev = PESO_SEV.get(r["severidade"], 1)
            bloq = PESO_BLOQUEIO.get(r["bloqueia"], 5)
            score = sev * bloq
            rows.append({**r, "score": score})
    rows.sort(key=lambda x: -x["score"])
    return rows

if __name__ == "__main__":
    rows = priorizar()
    print("=== WS4 · FILA DE ATAQUE PRIORIZADA (top 20) ===\n")
    print(f"{'#':>2} {'ID':6} {'Fam':4} {'Sev':6} {'Score':>5}  Título")
    for i, r in enumerate(rows[:20], 1):
        print(f"{i:>2} {r['id']:6} {r['familia'][:4]:4} {r['severidade']:6} {r['score']:>5}  {r['titulo'][:52]}")
    print(f"\nTotal de itens priorizados: {len(rows)}")
    out = os.path.join(HERE, "ws4_fila_priorizada.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=";")
        w.writeheader(); w.writerows(rows)
    print(f"Salvo: {out}")
