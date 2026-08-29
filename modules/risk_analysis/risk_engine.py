#!/usr/bin/env python3
"""
Gtasck Risk Analysis — Matriz de risco 5×5 + Planilha HAZOP (IEC 61882 / CCPS / API 580)

Uso:
    python3 risk_engine.py matrix cenarios.json -o matriz_risco.svg
    python3 risk_engine.py hazop nos.json -o hazop_planilha.csv
"""
from __future__ import annotations
import json, csv, sys, argparse

SEVERITY = ["Insignificante", "Menor", "Moderado", "Maior", "Catastrófico"]
LIKELIHOOD = ["Raro", "Improvável", "Possível", "Provável", "Quase Certo"]
COLORS = {"Baixo": "#2ecc71", "Médio": "#f1c40f", "Alto": "#e67e22", "Crítico": "#e74c3c"}
ACTIONS = {"Baixo": "Aceitar e monitorar", "Médio": "Mitigar em prazo programado",
           "Alto": "Mitigar com prioridade", "Crítico": "Ação imediata / parada"}

def classify(score: int) -> str:
    if score >= 17: return "Crítico"
    if score >= 10: return "Alto"
    if score >= 5:  return "Médio"
    return "Baixo"

def score(sev: int, lik: int) -> int:
    return sev * lik

# ---------------------------------------------------------------
# Matriz 5×5 em SVG
# ---------------------------------------------------------------
def matrix_svg(scenarios: list[dict], title: str) -> str:
    cell, x0, y0 = 110, 220, 80
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="760" viewBox="0 0 900 760">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="450" y="40" font-size="20" font-weight="bold" text-anchor="middle" font-family="Arial">{title}</text>',
        f'<text x="{x0+2.5*cell}" y="{y0+5.6*cell}" font-size="14" text-anchor="middle" font-family="Arial">SEVERIDADE →</text>',
        f'<text x="40" y="{y0+2.5*cell}" font-size="14" text-anchor="middle" font-family="Arial" transform="rotate(-90 40 {y0+2.5*cell})">PROBABILIDADE →</text>',
    ]
    for r in range(5):          # r = likelihood (5 topo → 1 base)
        lik = 5 - r
        for c in range(5):      # c = severity 1..5
            sev = c + 1
            band = classify(score(sev, lik))
            x, y = x0 + c * cell, y0 + r * cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{COLORS[band]}" stroke="white" stroke-width="2"/>')
            parts.append(f'<text x="{x+cell/2}" y="{y+cell/2+5}" font-size="13" text-anchor="middle" font-family="Arial" fill="#222">{sev*lik}</text>')
    for c, s in enumerate(SEVERITY):
        parts.append(f'<text x="{x0+c*cell+cell/2}" y="{y0+5*cell+22}" font-size="11" text-anchor="middle" font-family="Arial">{s}</text>')
    for r in range(5):
        parts.append(f'<text x="{x0-12}" y="{y0+r*cell+cell/2+4}" font-size="11" text-anchor="end" font-family="Arial">{LIKELIHOOD[4-r]}</text>')
    # Plotar cenários
    for sc in scenarios:
        sev, lik, tag = sc["severity"], sc["likelihood"], sc["id"]
        x = x0 + (sev - 1) * cell + cell / 2
        y = y0 + (5 - lik) * cell + cell / 2 - 18
        parts.append(f'<circle cx="{x}" cy="{y}" r="13" fill="#1a1a2e" stroke="white" stroke-width="2"/>')
        parts.append(f'<text x="{x}" y="{y+4}" font-size="11" font-weight="bold" text-anchor="middle" font-family="Arial" fill="white">{tag}</text>')
    # Legenda
    ly = y0 + 5 * cell + 60
    for i, (band, color) in enumerate(COLORS.items()):
        parts.append(f'<rect x="{120+i*180}" y="{ly}" width="18" height="18" fill="{color}"/>')
        parts.append(f'<text x="{144+i*180}" y="{ly+14}" font-size="12" font-family="Arial">{band} — {ACTIONS[band]}</text>')
    parts.append('</svg>')
    return "\n".join(parts)

# ---------------------------------------------------------------
# Planilha HAZOP (IEC 61882)
# ---------------------------------------------------------------
GUIDE_WORDS = {
    "flow": [("Nenhum", "Sem fluxo"), ("Mais", "Fluxo acima do projeto"), ("Menos", "Fluxo abaixo do projeto"),
             ("Reverso", "Fluxo reverso"), ("Outro", "Fluxo para destino errado")],
    "pressure": [("Nenhum", "Vácuo/alívio total"), ("Mais", "Sobrepressão"), ("Menos", "Subpressão")],
    "temperature": [("Mais", "Temperatura alta"), ("Menos", "Temperatura baixa")],
    "level": [("Nenhum", "Nível vazio"), ("Mais", "Nível alto/transbordo"), ("Menos", "Nível baixo")],
}

def hazop_rows(nodes: list[dict]) -> list[dict]:
    rows = []
    for node in nodes:
        param = node.get("parameter", "flow")
        for word, deviation in GUIDE_WORDS.get(param, []):
            rows.append({
                "Nó": node["node"], "Parâmetro": param.capitalize(),
                "Palavra-guia": word, "Desvio": deviation,
                "Causas": node.get("causes", "A levantar em sessão"),
                "Consequências": node.get("consequences", "A levantar em sessão"),
                "Salvaguardas": node.get("safeguards", "A levantar em sessão"),
                "S": "", "P": "", "Risco": "", "Ação Recomendada": "", "Responsável": "",
            })
    return rows

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gtasck Risk Analysis")
    ap.add_argument("mode", choices=["matrix", "hazop"])
    ap.add_argument("input", help="JSON de entrada")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)
    if args.mode == "matrix":
        svg = matrix_svg(data["scenarios"], data.get("title", "Matriz de Risco 5×5"))
        open(args.output, "w", encoding="utf-8").write(svg)
        print(f"Matriz gerada: {args.output} ({len(data['scenarios'])} cenários)")
    else:
        rows = hazop_rows(data["nodes"])
        with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=";")
            w.writeheader(); w.writerows(rows)
        print(f"Planilha HAZOP gerada: {args.output} ({len(rows)} desvios)")
