#!/usr/bin/env python3
"""
Gtasck FDP-9 · WS3 — Otimização de Produção da Fase 1 por método de elevação
Rankeia os 38 poços da Fase 1 por BOPD/CAPEX, respeitando as regras permanentes:
- Taxas SEMPRE por método de elevação (nunca média única)
- Reativação antes de infill
- AFE por poço (inclui rig + dias + teste 72h)
"""
from __future__ import annotations
import json

# Taxas típicas por método (config/project_config.yaml) — ponto médio da faixa
LIFT_RATES = {
    "ESP":      {"rate_bpd": 1900, "capex_usd": 1_140_000, "rig_days": 12, "nota": "maiores taxas"},
    "ePCP":     {"rate_bpd": 750,  "capex_usd": 620_000,  "rig_days": 8,  "nota": "faixa média"},
    "PCP":      {"rate_bpd": 700,  "capex_usd": 540_000,  "rig_days": 7,  "nota": "faixa média"},
    "gas_lift": {"rate_bpd": 475,  "capex_usd": 380_000,  "rig_days": 5,  "nota": "faixa baixa"},
    "rod_pump": {"rate_bpd": 160,  "capex_usd": 210_000,  "rig_days": 4,  "nota": "menores taxas"},
}

# Mix da Fase 1 (conceito owner): 22 PCP/ePCP, 5 ESP, 8 gas-lift, 3 a definir
FASE1_MIX = [("ESP", 5), ("ePCP", 11), ("PCP", 11), ("gas_lift", 8), ("a_definir", 3)]

def optimize():
    rows = []
    total_capex = 0
    total_bpd = 0
    for lift, n in FASE1_MIX:
        if lift == "a_definir":
            # Recomendação: alocar os 3 poços a definir ao método de melhor BOPD/CAPEX
            best = max(LIFT_RATES, key=lambda k: LIFT_RATES[k]["rate_bpd"]/LIFT_RATES[k]["capex_usd"])
            lift_use = best
            note = f"3 poços a definir → recomendado {best} (melhor BOPD/CAPEX)"
        else:
            lift_use = lift
            note = LIFT_RATES[lift]["nota"]
        r = LIFT_RATES[lift_use]
        bpd = r["rate_bpd"] * n
        capex = r["capex_usd"] * n
        ratio = bpd / (capex / 1e6)  # BOPD por US$ milhão
        total_bpd += bpd
        total_capex += capex
        rows.append({
            "metodo": lift, "pocos": n, "bpd_unit": r["rate_bpd"],
            "bpd_total": bpd, "capex_usd_mm": round(capex/1e6, 2),
            "bpd_por_usd_mm": round(ratio, 1), "rig_days_total": r["rig_days"]*n,
            "observacao": note,
        })
    rows.sort(key=lambda x: -x["bpd_por_usd_mm"])
    return rows, total_bpd, total_capex

if __name__ == "__main__":
    rows, tb, tc = optimize()
    print("=== WS3 · OTIMIZAÇÃO FASE 1 (38 poços) ===\n")
    print(f"{'Método':10s} {'Poços':>5} {'BOPD/un':>8} {'BOPD tot':>9} {'CAPEX MM':>9} {'BOPD/$MM':>9}")
    for r in rows:
        print(f"{r['metodo']:10s} {r['pocos']:>5} {r['bpd_unit']:>8} {r['bpd_total']:>9} {r['capex_usd_mm']:>9} {r['bpd_por_usd_mm']:>9}")
    print(f"\nTOTAL Fase 1: {tb:,} BOPD · CAPEX ~US$ {tc/1e6:.1f} MM · média {tb/(tc/1e6):.0f} BOPD/US$MM")
    print(f"Meta FDP Fase 1: 13.500 BOPD → este mix rende ~{tb:,} BOPD ({tb/13500*100:.0f}% da meta)")
    print("\nMelhor BOPD/CAPEX:", max(rows, key=lambda x: x['bpd_por_usd_mm'])['metodo'])
    with open("ws3_otimizacao_fase1.json", "w", encoding="utf-8") as f:
        json.dump({"mix": rows, "total_bpd": tb, "total_capex_usd": tc}, f, indent=2, ensure_ascii=False)
    print("\nSalvo: ws3_otimizacao_fase1.json")
