#!/usr/bin/env python3
"""
Gtasck Operations — Decision Log + Daily Operations Report
Rastreia decisões do COO e gera o relatório diário de operações.

Uso:
    python3 ops_engine.py decide --title "Aprovar AFE PO-01" --by "COO" \
        --rationale "VPL positivo, payback 0.14 ano" --impact "CAPEX 1.14M USD"
    python3 ops_engine.py report --date 2026-08-29 -o relatorio_diario.md
"""
from __future__ import annotations
import json, argparse, os
from datetime import datetime, timezone

DB = os.path.join(os.path.dirname(__file__), "decision_log", "decisions.jsonl")

def log_decision(title: str, by: str, rationale: str, impact: str,
                 module: str = "geral", status: str = "aprovada") -> dict:
    ts = datetime.now(timezone.utc).isoformat()
    entry = {"id": _next_id(), "timestamp_utc": ts, "title": title, "decided_by": by,
             "module": module, "rationale": rationale, "impact": impact, "status": status}
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    with open(DB, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def _next_id() -> int:
    if not os.path.exists(DB): return 1
    with open(DB, encoding="utf-8") as f:
        return sum(1 for _ in f) + 1

def load_decisions(date_filter: str | None = None) -> list[dict]:
    if not os.path.exists(DB): return []
    out = []
    with open(DB, encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            if date_filter and not e["timestamp_utc"].startswith(date_filter):
                continue
            out.append(e)
    return out

def daily_report(date: str, production: dict | None = None,
                 risks: list[dict] | None = None) -> str:
    decisions = load_decisions(date)
    lines = [
        f"# Relatório Diário de Operações — {date}",
        "",
        "**Gerado por Gtasck Operations** · COO Office",
        "",
        "## 1. Produção do Dia",
        "",
    ]
    if production:
        lines += [
            "| Métrica | Valor |",
            "|---|---:|",
            f"| Óleo (bpd) | {production.get('oil_bpd', '—')} |",
            f"| Gás (bpd eq.) | {production.get('gas_bpd', '—')} |",
            f"| Água (bpd) | {production.get('water_bpd', '—')} |",
            f"| Fechamento balanço | {production.get('closure_pct', '—')}% |",
            f"| Poços ativos | {production.get('active_wells', '—')} |",
        ]
    else:
        lines.append("_Sem dados de produção alimentados hoje._")
    lines += ["", "## 2. Decisões Registradas", ""]
    if decisions:
        lines += ["| ID | Hora (UTC) | Decisão | Por | Impacto | Status |",
                  "|---:|---|---|---|---|---|"]
        for d in decisions:
            hora = d["timestamp_utc"][11:16]
            lines.append(f"| D{d['id']:03d} | {hora} | {d['title']} | {d['decided_by']} | {d['impact']} | {d['status']} |")
    else:
        lines.append("_Nenhuma decisão registrada nesta data._")
    lines += ["", "## 3. Riscos Críticos/Altos Ativos", ""]
    if risks:
        lines += ["| Cenário | Severidade | Probabilidade | Banda |", "|---|---|---|---|"]
        for r in risks:
            lines.append(f"| {r['id']} | {r['severity']} | {r['likelihood']} | {r.get('band','—')} |")
    else:
        lines.append("_Sem riscos altos/críticos reportados._")
    lines += ["", "---", f"_Relatório gerado em {datetime.now(timezone.utc).isoformat()}_"]
    return "\n".join(lines)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gtasck Operations")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("decide", help="Registrar uma decisão")
    d.add_argument("--title", required=True)
    d.add_argument("--by", required=True)
    d.add_argument("--rationale", default="")
    d.add_argument("--impact", default="")
    d.add_argument("--module", default="geral")
    d.add_argument("--status", default="aprovada")

    r = sub.add_parser("report", help="Gerar relatório diário")
    r.add_argument("--date", required=True, help="AAAA-MM-DD")
    r.add_argument("--production", help="JSON com produção do dia")
    r.add_argument("-o", "--output", default="relatorio_diario.md")

    args = ap.parse_args()
    if args.cmd == "decide":
        e = log_decision(args.title, args.by, args.rationale, args.impact, args.module, args.status)
        print(f"Decisão D{e['id']:03d} registrada: {e['title']}")
    else:
        prod = None
        if args.production:
            with open(args.production, encoding="utf-8") as f:
                prod = json.load(f)
        md = daily_report(args.date, production=prod)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Relatório diário gerado: {args.output}")
