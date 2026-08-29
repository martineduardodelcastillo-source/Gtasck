#!/usr/bin/env python3
"""
Gtasck FDP-9 Change Tracker — Rastreia mudanças/melhorias do projeto PetroUrdaneta FDP v9
Cada mudança vira um registro versionado e auditável, ligado a um gate/risco/capítulo.

Uso:
    python3 track_engine.py add --title "Reconciliar well master (38 poços)" \
        --chapter 6 --gate G-01 --type correcao --by "Engenharia" \
        --before "4 populações (32/35/38/86)" --after "Well master único controlado"
    python3 track_engine.py list
    python3 track_engine.py report -o daily/fdp9_status.md
"""
from __future__ import annotations
import json, argparse, os
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "changes.jsonl")
VALID_TYPES = ["correcao", "melhoria", "decisao", "gate_fechado", "risco_mitigado", "escopo"]

def _next_id() -> int:
    if not os.path.exists(DB): return 1
    with open(DB, encoding="utf-8") as f:
        return sum(1 for _ in f) + 1

def add_change(title, chapter, gate, ctype, by, before, after, impact="", status="proposta") -> dict:
    e = {"id": f"CH-{_next_id():03d}", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
         "title": title, "chapter": chapter, "gate": gate, "type": ctype,
         "proposed_by": by, "before": before, "after": after, "impact": impact, "status": status}
    with open(DB, "a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e

def load() -> list[dict]:
    if not os.path.exists(DB): return []
    with open(DB, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def report() -> str:
    changes = load()
    by_type = {}
    for c in changes:
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    lines = [
        "# FDP-9 · Status de Mudanças e Melhorias",
        "",
        f"**Gerado em:** {datetime.now(timezone.utc).isoformat()}  ",
        f"**Total de mudanças rastreadas:** {len(changes)}",
        "",
        "## Resumo por tipo",
        "",
        "| Tipo | Qtd |", "|---|---:|",
    ]
    for t, n in sorted(by_type.items()):
        lines.append(f"| {t} | {n} |")
    lines += ["", "## Registro completo", "",
              "| ID | Data | Cap. | Gate | Tipo | Mudança | Status |",
              "|---|---|---|---|---|---|---|"]
    for c in changes:
        d = c["timestamp_utc"][:10]
        lines.append(f"| {c['id']} | {d} | {c['chapter']} | {c['gate']} | {c['type']} | {c['title']} | {c['status']} |")
    return "\n".join(lines)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gtasck FDP-9 Change Tracker")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--chapter", default="")
    a.add_argument("--gate", default="")
    a.add_argument("--type", default="melhoria", choices=VALID_TYPES)
    a.add_argument("--by", default="COO")
    a.add_argument("--before", default="")
    a.add_argument("--after", default="")
    a.add_argument("--impact", default="")
    a.add_argument("--status", default="proposta")
    sub.add_parser("list")
    r = sub.add_parser("report")
    r.add_argument("-o", "--output", default=None)
    args = ap.parse_args()

    if args.cmd == "add":
        e = add_change(args.title, args.chapter, args.gate, args.type, args.by,
                       args.before, args.after, args.impact, args.status)
        print(f"Mudança {e['id']} registrada: {e['title']} [{e['type']}] gate={e['gate']}")
    elif args.cmd == "list":
        for c in load():
            print(f"{c['id']}  [{c['type']:15s}] cap.{c['chapter']:>3} {c['gate']:>5}  {c['title']}  ({c['status']})")
        print(f"\nTotal: {len(load())} mudanças")
    else:
        md = report()
        out = args.output or os.path.join(HERE, "..", "daily", f"fdp9_status_{datetime.now(timezone.utc):%Y-%m-%d}.md")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Relatório de status: {out}")
