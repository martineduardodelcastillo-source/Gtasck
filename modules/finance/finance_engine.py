#!/usr/bin/env python3
"""
Gtasck Finance — Economia de projetos O&G para o COO
AFE por poço · VPL (NPV) · TIR (IRR) · Payback · Lifting cost ($/bbl)

Regras permanentes (config/project_config.yaml):
- AFE individual por poço; CAPEX atrelado ao retorno em crude
- Taxas de produção SEMPRE por método de elevação (ESP/PCP/GL/rod) — nunca média única
- Estratégia de contratação: 4 MSAs (well services+EPF, EPCM, drilling, compression)

Uso:
    python3 finance_engine.py afe afe_poco.json
    python3 finance_engine.py economics projeto.json
"""
from __future__ import annotations
import json, argparse

WELL_COST_COMPONENTS = ["xmas_tree", "valves", "tubing", "rig_packers",
                        "artificial_lift", "mob_demob_wireline"]

def afe_total(components: dict) -> dict:
    """Soma o AFE do poço e valida componentes obrigatórios."""
    missing = [c for c in WELL_COST_COMPONENTS if c not in components]
    total = sum(components.values())
    return {"total_usd": round(total, 2),
            "componentes_faltantes": missing,
            "completo": not missing}

def npv(rate: float, cashflows: list[float]) -> float:
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cashflows))

def irr(cashflows: list[float], lo: float = -0.9, hi: float = 10.0, tol: float = 1e-6) -> float:
    """TIR por bisseção."""
    f = lambda r: npv(r, cashflows)
    if f(lo) * f(hi) > 0: return float("nan")
    for _ in range(200):
        mid = (lo + hi) / 2
        if abs(f(mid)) < tol: return mid
        if f(lo) * f(mid) < 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2

def payback(cashflows: list[float]) -> float:
    cum = 0.0
    for i, cf in enumerate(cashflows):
        prev = cum; cum += cf
        if cum >= 0 and i > 0:
            return round(i - 1 + (-prev / cf), 2)
    return float("inf")

def economics(capex: float, annual_oil_bbl: float, price_usd_bbl: float,
              opex_usd_bbl: float, years: int, rate: float) -> dict:
    net_annual = annual_oil_bbl * (price_usd_bbl - opex_usd_bbl)
    cfs = [-capex] + [net_annual] * years
    return {
        "capex_usd": capex,
        "receita_liquida_anual_usd": round(net_annual, 0),
        "vpl_usd": round(npv(rate, cfs), 0),
        "tir_pct": round(irr(cfs) * 100, 1),
        "payback_anos": payback(cfs),
        "lifting_cost_usd_bbl": opex_usd_bbl,
        "taxa_desconto_pct": rate * 100,
    }

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gtasck Finance")
    ap.add_argument("mode", choices=["afe", "economics"])
    ap.add_argument("input", help="JSON de entrada")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        d = json.load(f)
    if args.mode == "afe":
        print(json.dumps(afe_total(d["components"]), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(economics(d["capex_usd"], d["annual_oil_bbl"], d["price_usd_bbl"],
                                   d["opex_usd_bbl"], d["years"],
                                   d.get("discount_rate", 0.12)), indent=2, ensure_ascii=False))
