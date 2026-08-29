#!/usr/bin/env python3
"""
Gtasck Mass & Production Balance — Balanço de massa e alocação de produção
Fechamento de balanço (±2%), alocação por poço, reconciliação fiscal.

Uso:
    python3 balance_engine.py exemplo_planta.json -o balanco.csv
"""
from __future__ import annotations
import json, csv, argparse

def closure_pct(entradas: float, saidas: float) -> float:
    if entradas == 0: return 0.0
    return round((entradas - saidas) / entradas * 100, 2)

def balance(streams: list[dict], tolerance: float = 2.0) -> dict:
    ent = sum(s["flow_bpd"] for s in streams if s["direction"] == "in")
    sai = sum(s["flow_bpd"] for s in streams if s["direction"] == "out")
    cl = closure_pct(ent, sai)
    return {
        "total_entrada_bpd": round(ent, 1),
        "total_saida_bpd": round(sai, 1),
        "fechamento_pct": cl,
        "status": "OK" if abs(cl) <= tolerance else "FORA DA TOLERÂNCIA",
        "tolerancia_pct": tolerance,
    }

def allocate_by_well(wells: list[dict], fiscal_total_bpd: float) -> list[dict]:
    """Alocação pro-rata: distribui o total fiscal medido entre os poços
    conforme a produção estimada de cada um (por método de elevação)."""
    est_total = sum(w["estimated_bpd"] for w in wells)
    out = []
    for w in wells:
        frac = w["estimated_bpd"] / est_total if est_total else 0
        out.append({**w, "allocated_bpd": round(fiscal_total_bpd * frac, 1),
                    "allocation_factor": round(frac, 4)})
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gtasck Mass & Production Balance")
    ap.add_argument("input", help="JSON com streams e/ou poços")
    ap.add_argument("-o", "--output", default="balanco.csv")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    resumo = balance(data.get("streams", []), data.get("tolerance_pct", 2.0))
    print("=== BALANÇO DE MASSA ===")
    print(json.dumps(resumo, indent=2, ensure_ascii=False))

    rows = []
    if "wells" in data and "fiscal_total_bpd" in data:
        alloc = allocate_by_well(data["wells"], data["fiscal_total_bpd"])
        print("\n=== ALOCAÇÃO POR POÇO (pro-rata fiscal) ===")
        for a in alloc:
            print(f"  {a['well']:12s} [{a['lift']:9s}] est={a['estimated_bpd']:7.1f} → alocado={a['allocated_bpd']:7.1f} bpd")
        rows = alloc

    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=";")
            w.writeheader(); w.writerows(rows)
    print(f"\nPlanilha: {args.output}")
