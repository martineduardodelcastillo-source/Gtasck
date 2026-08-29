#!/usr/bin/env python3
"""
Gtasck Engineering Calcs — Memoriais de cálculo
ASME VIII Div.1 (vasos) · ASME B31.3 (tubulação) · API 650 (tanques) · API 520 (PSV)

Uso:
    python3 calcs_engine.py vessel --P 250 --D 48 --S 20000 --E 0.85 --CA 0.125
    python3 calcs_engine.py pipe --P 740 --D 6.625 --S 20000 --E 1.0 --CA 0.0625
"""
from __future__ import annotations
import argparse, math, json

def vessel_shell_thickness(P: float, R: float, S: float, E: float, CA: float) -> dict:
    """ASME VIII Div.1 UG-27 — casca cilíndrica (circunferencial)."""
    t = (P * R) / (S * E - 0.6 * P) + CA
    return {"formula": "UG-27: t = PR/(SE - 0.6P) + CA", "t_required_in": round(t, 4)}

def vessel_head_thickness(P: float, D: float, S: float, E: float, CA: float) -> dict:
    """ASME VIII Div.1 UG-32 — cabeça semiesférica/elíptica 2:1 (aprox.)."""
    t = (P * D) / (2 * S * E - 0.2 * P) + CA
    return {"formula": "UG-32 (2:1 SE head): t = PD/(2SE - 0.2P) + CA", "t_required_in": round(t, 4)}

def pipe_wall_thickness(P: float, D: float, S: float, E: float, W: float, Y: float, CA: float) -> dict:
    """ASME B31.3 §304.1.2 — tubulação reta sob pressão interna."""
    t = (P * D) / (2 * (S * E * W + P * Y)) + CA
    return {"formula": "B31.3 304.1.2: t = PD/(2(SEW + PY)) + CA", "t_required_in": round(t, 4)}

def tank_shell_thickness(H: float, G: float, D: float, S: float, CA: float) -> dict:
    """API 650 §5.6.3 — método 1 pé (1-foot method), polegadas."""
    t = (2.6 * D * (H - 1) * G) / S + CA
    return {"formula": "API 650 1-ft: t = 2.6·D·(H-1)·G/S + CA", "t_required_in": round(t, 4)}

def psv_orifice_area_gas(W_lb_h: float, C: float, Kd: float, P1_psia: float, Kb: float, M: float, T_R: float, Z: float) -> dict:
    """API 520 §5.6 — área de orifício para gás (fluxo crítico), in²."""
    A = (W_lb_h / (C * Kd * P1_psia * Kb)) * math.sqrt(T_R * Z / M)
    return {"formula": "API 520: A = W/(C·Kd·P1·Kb)·√(TZ/M)", "A_required_in2": round(A, 3)}

MATERIALS = {
    "SA-516-70": {"S_psi": 20000, "uso": "Vasos (ASME VIII)"},
    "SA-106-B":  {"S_psi": 20000, "uso": "Tubulação (B31.3)"},
    "A-36":      {"S_psi": 23200, "uso": "Tanques (API 650)"},
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gtasck Engineering Calcs")
    sub = ap.add_subparsers(dest="calc", required=True)

    v = sub.add_parser("vessel", help="ASME VIII Div.1 — vaso de pressão")
    v.add_argument("--P", type=float, required=True, help="Pressão de projeto (psig)")
    v.add_argument("--D", type=float, required=True, help="Diâmetro interno (in)")
    v.add_argument("--S", type=float, default=20000, help="Tensão admissível (psi)")
    v.add_argument("--E", type=float, default=0.85, help="Eficiência de junta")
    v.add_argument("--CA", type=float, default=0.125, help="Sobre-espessura de corrosão (in)")

    p = sub.add_parser("pipe", help="ASME B31.3 — tubulação")
    p.add_argument("--P", type=float, required=True)
    p.add_argument("--D", type=float, required=True, help="Diâmetro externo (in)")
    p.add_argument("--S", type=float, default=20000)
    p.add_argument("--E", type=float, default=1.0)
    p.add_argument("--W", type=float, default=1.0)
    p.add_argument("--Y", type=float, default=0.4)
    p.add_argument("--CA", type=float, default=0.0625)

    t = sub.add_parser("tank", help="API 650 — tanque atmosférico")
    t.add_argument("--H", type=float, required=True, help="Altura do anel (ft)")
    t.add_argument("--G", type=float, default=1.0, help="Densidade relativa")
    t.add_argument("--D", type=float, required=True, help="Diâmetro do tanque (ft)")
    t.add_argument("--S", type=float, default=23200)
    t.add_argument("--CA", type=float, default=0.0625)

    args = ap.parse_args()
    if args.calc == "vessel":
        R = args.D / 2
        res = {"casca": vessel_shell_thickness(args.P, R, args.S, args.E, args.CA),
               "cabeca_2_1": vessel_head_thickness(args.P, args.D, args.S, args.E, args.CA)}
    elif args.calc == "pipe":
        res = pipe_wall_thickness(args.P, args.D, args.S, args.E, args.W, args.Y, args.CA)
    else:
        res = tank_shell_thickness(args.H, args.G, args.D, args.S, args.CA)
    print(json.dumps(res, indent=2, ensure_ascii=False))
