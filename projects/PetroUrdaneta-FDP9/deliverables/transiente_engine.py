#!/usr/bin/env python3
"""
Gtasck FDP-9 · Entregável 3 — Modelo Transiente da Trunkline Mais Crítica

A trunkline mais crítica é a da EPF de MAIOR vazão (EPF grande, ~6.000 BOPD),
onde o screening mostrou erosão em 4" e baixa velocidade em 6"/8".

Modelo screening transiente:
- Perfil de elevação (terrain slugging)
- Holdup de líquido (mínimo/normal/máximo)
- Volume de slug por pigging (governante)
- Pressão de chegada no FSB
- Dimensionamento do vaso de slug (gate G-05)
"""
from __future__ import annotations
import math, json

# EPF grande (mais crítica)
BOPD = 6000.0
GOR = 310.0
WC = 0.30
L_KM = 5.0
D = {"4in": 0.089, "6in": 0.137, "8in": 0.188}
RHO_L = 900.0   # líquido médio
RHO_G = 12.0
P_IN_BAR = 30.0

def vazao(bopd):
    qo = bopd * 0.158987 / 86400
    qw = qo * WC / (1 - WC)
    qg = (bopd * GOR) * 0.0283168 / 86400 / P_IN_BAR
    return qo, qw, qg

def holdup(v_sl, v_sg):
    """Holdup de líquido screening (mínimo/normal/máximo)."""
    v_m = v_sl + v_sg
    base = v_sl / v_m if v_m > 0 else 0.5
    return {"min": max(0.05, base*0.6), "normal": min(0.95, base*1.2+0.1), "max": min(0.98, base*1.6+0.25)}

def slug_pigging(d, L_km, holdup_max):
    """Volume de líquido varrido por um pig = holdup_max × volume da linha."""
    area = math.pi * d**2 / 4
    vol_linha = area * (L_km * 1000)
    return holdup_max * vol_linha  # m3 de líquido

def analisar():
    qo, qw, qg = vazao(BOPD)
    ql = qo + qw
    resultado = {}
    for nome, d in D.items():
        area = math.pi * d**2 / 4
        v_sl = ql / area
        v_sg = qg / area
        v_m = v_sl + v_sg
        h = holdup(v_sl, v_sg)
        slug_m3 = slug_pigging(d, L_KM, h["max"])
        # Pressão de chegada (homogêneo + estática de terreno screening)
        ff = 0.02
        dp_fric = ff * (L_KM*1000 / d) * ((RHO_L*h["normal"]+RHO_G*(1-h["normal"])) * v_m**2 / 2) / 1e5
        dp_static = (RHO_L * 9.81 * 30) / 1e5  # 30 m de elevação screening
        p_chegada = P_IN_BAR - dp_fric - dp_static
        resultado[nome] = {
            "v_mis_m_s": round(v_m, 2), "holdup_normal": round(h["normal"], 2),
            "slug_pig_m3": round(slug_m3, 1), "dp_fric_bar": round(dp_fric, 2),
            "p_chegada_fsb_bar": round(p_chegada, 1),
            "vaso_slug_min_m3": round(slug_m3 * 1.25, 1),  # +25% margem
        }
    return resultado

if __name__ == "__main__":
    r = analisar()
    print(f"=== TRANSIENTE · TRUNKLINE EPF GRANDE ({BOPD:.0f} BOPD, {L_KM} km) ===\n")
    print(f"{'Ø':5} {'v_mis':>6} {'holdup':>7} {'slug pig':>9} {'Δp fric':>8} {'P FSB':>6} {'vaso slug':>10}")
    for nome, x in r.items():
        print(f"{nome:5} {x['v_mis_m_s']:>6} {x['holdup_normal']:>7} {x['slug_pig_m3']:>8}m3 {x['dp_fric_bar']:>7}b {x['p_chegada_fsb_bar']:>5}b {x['vaso_slug_min_m3']:>9}m3")
    # Recomendação
    print("\n=== RECOMENDAÇÃO ===")
    for nome, x in r.items():
        ok = 3.0 <= x["v_mis_m_s"] <= 18.0 and x["p_chegada_fsb_bar"] > 5
        print(f"  {nome}: {'VIÁVEL' if ok else 'REVISAR'} (vaso de slug ≥ {x['vaso_slug_min_m3']} m³)")
    with open("transiente_trunkline.json", "w", encoding="utf-8") as fp:
        json.dump(r, fp, indent=2, ensure_ascii=False)
    print("\nSalvo: transiente_trunkline.json")
    print("NOTA: screening. O vaso de slug final exige modelo transiente integrado (G-05).")
