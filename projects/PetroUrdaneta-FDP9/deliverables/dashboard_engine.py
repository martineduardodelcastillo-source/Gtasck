#!/usr/bin/env python3
"""
Gtasck FDP-9 · Dashboard do COO — KPIs ao vivo do projeto
Lê o change log, os registros e os entregáveis e gera um painel de KPIs.
"""
from __future__ import annotations
import json, os, csv
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "..")
CHANGES = os.path.join(PROJ, "change_log", "changes.jsonl")
RISK = os.path.join(PROJ, "registers", "risk_register.csv")
WELLS = os.path.join(PROJ, "registers", "well_master_reconciliado.csv")

def carregar_mudancas():
    if not os.path.exists(CHANGES): return []
    with open(CHANGES, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def kpis():
    mud = carregar_mudancas()
    # Gates
    gates = {}
    with open(RISK, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["id"].startswith("G-"):
                gates[r["id"]] = r["status"]
    gates_fechados = sum(1 for m in mud if m["type"] == "gate_fechado")
    # Poços
    pocos = list(csv.DictReader(open(WELLS, encoding="utf-8-sig"), delimiter=";"))
    # Produção e CAPEX (dos entregáveis)
    return {
        "data": datetime.now(timezone.utc).isoformat()[:10],
        "mudancas_total": len(mud),
        "mudancas_por_tipo": _por_tipo(mud),
        "gates_total": len(gates),
        "gates_fechados": gates_fechados,
        "gates_abertos": len(gates) - gates_fechados,
        "pocos_total": len(pocos),
        "pocos_com_restricao": sum(1 for p in pocos if p["restricao"]),
        "producao_alvo_fase1_bopd": 13500,
        "producao_plano_reativacao_bopd": 38650,
        "capex_plano_reativacao_usd_mm": 51.4,
        "capex_tender_gates_usd_mm": 2.92,
    }

def _por_tipo(mud):
    d = {}
    for m in mud: d[m["type"]] = d.get(m["type"], 0) + 1
    return d

def render_md(k):
    linhas = [
        "# Dashboard do COO · FDP-9 PetroUrdaneta",
        "",
        f"**Atualizado em:** {k['data']}",
        "",
        "## KPIs principais",
        "",
        "| KPI | Valor |",
        "|---|---:|",
        f"| Mudanças rastreadas | {k['mudancas_total']} |",
        f"| Gates FEED fechados | {k['gates_fechados']} / {k['gates_total']} |",
        f"| Gates abertos | {k['gates_abertos']} |",
        f"| Poços no well master | {k['pocos_total']} |",
        f"| Poços com restrição | {k['pocos_com_restricao']} |",
        f"| Produção alvo Fase 1 | {k['producao_alvo_fase1_bopd']:,} BOPD |",
        f"| Produção plano reativação | {k['producao_plano_reativacao_bopd']:,} BOPD |",
        f"| CAPEX plano reativação | US$ {k['capex_plano_reativacao_usd_mm']} MM |",
        f"| CAPEX tender gates (G-02..G-06) | US$ {k['capex_tender_gates_usd_mm']} MM |",
        "",
        "## Mudanças por tipo",
        "",
        "| Tipo | Qtd |",
        "|---|---:|",
    ]
    for t, n in sorted(k['mudancas_por_tipo'].items()):
        linhas.append(f"| {t} | {n} |")
    return "\n".join(linhas) + "\n"

if __name__ == "__main__":
    k = kpis()
    md = render_md(k)
    out = os.path.join(HERE, "dashboard_coo.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    print(md)
    print(f"Salvo: {out}")
