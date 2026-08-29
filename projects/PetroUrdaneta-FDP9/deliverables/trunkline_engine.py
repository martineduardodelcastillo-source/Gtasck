#!/usr/bin/env python3
"""
Gtasck FDP-9 · Eixo 2 — Modelo de Dimensionamento de Trunklines Multifásicas 4"/6"/8"

Screening de velocidade/erosão/queda de pressão por diâmetro para as 12 trunklines
EPF→FSB. Respeita: flex pipe first, pigabilidade, e a regra de que velocidade só-líquido
NÃO dimensiona linha multifásica (gate G-04).

Critérios (screening):
- Velocidade de erosão (API RP 14E): ve = C / sqrt(rho_m)
- Velocidade mínima para evitar acúmulo de líquido: ~3 m/s (multifásico)
- Velocidade máxima recomendada: ~18 m/s (multifásico)
- Queda de pressão estimada (homogêneo, screening)
"""
from __future__ import annotations
import math, json

# Fluido médio La Paz (screening a partir do FDP)
RHO_O = 880.0      # kg/m3 (25°API)
RHO_G = 12.0       # kg/m3 (a ~30 bar)
RHO_W = 1025.0     # kg/m3
GOR = 310.0        # scf/STB (La Paz Sur) — screening
WC = 0.30          # water cut médio (screening)
C_EROSION = 100.0  # API RP 14E (contínuo, sólidos) — screening

# Diâmetros internos (m) — flex pipe / aço
DIAMETROS = {"4in": 0.089, "6in": 0.137, "8in": 0.188}

def vazao_mis(bopd: float) -> dict:
    """Converte BOPD em vazões de fase (m3/s) e mistura."""
    qo = bopd * 0.158987 / 86400          # m3/s óleo
    qw = qo * WC / (1 - WC)               # m3/s água
    qg_scfd = bopd * GOR / 35.3147        # scf/d → ... (GOR scf/STB)
    qg = (bopd * GOR) * 0.0283168 / 86400 # m3/s gás (std)
    # gás em condições de linha (~30 bar): comprime ~30x
    qg_line = qg / 30.0
    ql = qo + qw
    qm = ql + qg_line
    rho_m = (ql * (RHO_O*(1-WC) + RHO_W*WC) + qg_line * RHO_G) / qm
    return {"qo": qo, "qw": qw, "qg_line": qg_line, "ql": ql, "qm": qm, "rho_m": rho_m}

def analisar(bopd: float) -> list[dict]:
    f = vazao_mis(bopd)
    ve = C_EROSION / math.sqrt(f["rho_m"])  # velocidade de erosão
    out = []
    for nome, d in DIAMETROS.items():
        area = math.pi * d**2 / 4
        v = f["qm"] / area
        # Queda de pressão homogênea (Fanning, f~0.02, L=5 km screening)
        L = 5000.0
        ff = 0.02
        dp = ff * (L / d) * (f["rho_m"] * v**2 / 2) / 1e5  # bar
        status = "OK"
        if v < 3.0: status = "BAIXA (acúmulo líquido)"
        if v > ve: status = "EROSÃO"
        if v > 18.0: status = "ALTA DEMAIS"
        out.append({"diametro": nome, "v_mis": round(v,2), "v_erosao": round(ve,2),
                    "dp_bar_5km": round(dp,2), "status": status})
    return out

if __name__ == "__main__":
    print("=== TRUNKLINES 4\"/6\"/8\" · SCREENING MULTIFÁSICO ===")
    print(f"Fluido: GOR {GOR} scf/STB · WC {WC*100:.0f}% · ρm screening\n")
    cenarios = {"EPF pequena (1.500 BOPD)": 1500, "EPF média (3.500 BOPD)": 3500, "EPF grande (6.000 BOPD)": 6000}
    resultado = {}
    for nome, bopd in cenarios.items():
        print(f"--- {nome} ---")
        print(f"{'Ø':5} {'v(m/s)':>7} {'v_eros':>7} {'Δp bar/5km':>11}  status")
        linhas = analisar(bopd)
        resultado[nome] = linhas
        for r in linhas:
            print(f"{r['diametro']:5} {r['v_mis']:>7} {r['v_erosao']:>7} {r['dp_bar_5km']:>11}  {r['status']}")
        print()
    with open("trunkline_screening.json", "w", encoding="utf-8") as fp:
        json.dump(resultado, fp, indent=2, ensure_ascii=False)
    print("Salvo: trunkline_screening.json")
    print("\nNOTA: screening homogêneo. O dimensionamento final exige modelo transiente (G-04/G-05).")
