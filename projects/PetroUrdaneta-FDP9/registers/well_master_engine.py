#!/usr/bin/env python3
"""
Gtasck FDP-9 · WS1 — Well Master Reconciliation
Reconcilia as 4 populações divergentes de poços (32 / 35 / 38 / 86) num
"well master" único e controlado, fechando o gate G-01.

Fontes reconciliadas:
  - FDP v8: 32 poços La Paz
  - Workbook de reativação (S05): 35 poços
  - Conceito owner: 38 poços Fase 1
  - Modelo binário (S04): 86 nomes únicos La Paz
  - Plano de negócio PDVSA (S03): 9 cat-1 (base 1.388 BND) + 102 reaberturas + 38 novos
"""
from __future__ import annotations
import csv, os, json

HERE = os.path.dirname(os.path.abspath(__file__))

# Categoria 1 — base produtora atual (1.388 BND, dez/2025) [S03]
CATEGORIA_1 = ["P-016", "P-108", "P-152", "P-173", "P-199A", "P-207", "P-180", "P-179", "P-176"]

# Restrições conhecidas (gates de desenvolvimento) [S05]
RESTRICOES = {
    "P-108": "comunidade_acesso", "P-173": "comunidade_acesso", "P-95": "comunidade_acesso",
    "P-180": "comunidade_acesso", "P-152": "comunidade_acesso",
    "P-192": "equip_superficie_ineconomico", "P-82": "equip_superficie_ineconomico",
    "P-61": "equip_superficie_ineconomico", "P-88": "equip_superficie_ineconomico",
    "P-161": "reparo_subsuperficie_maior", "P-91": "alta_agua", "P-52": "aguardando_abandono",
}

# Método de elevação — conceito owner Fase 1 (38 poços):
# 22 PCP/ePCP, 5 ESP, 8 gas-lift, 3 a definir.
# Poços identificados por nome no documento:
LIFT_KNOWN = {
    "DM-0010": "gas_lift", "DM-0021": "gas_lift", "DM-0023": "gas_lift", "DM-123": "gas_lift",
    "DMM-0002": "gas_lift", "DMM-003": "gas_lift",
}

# Universo de poços nomeados encontrados no FDP v9 (La Paz P-*, Mara DM-*, El Moján DMM-*)
POCOS_IDENTIFICADOS = [
    "P-016","P-16","P-52","P-61","P-63","P-69","P-76","P-77","P-82","P-88","P-91","P-95",
    "P-108","P-152","P-161","P-162","P-163","P-173","P-176","P-179","P-180","P-181","P-182",
    "P-184","P-189","P-190","P-191","P-192","P-195","P-198A","P-199A","P-201","P-204","P-205","P-207",
    "DM-0010","DM-0021","DM-0023","DM-123","DMM-0002","DMM-003",
]

def campo(poco: str) -> str:
    if poco.startswith("DMM"): return "El Moján"
    if poco.startswith("DM"): return "Mara"
    return "La Paz"

def reconcile() -> list[dict]:
    master = []
    for p in POCOS_IDENTIFICADOS:
        master.append({
            "poco": p,
            "campo": campo(p),
            "categoria_1_base": "sim" if p in CATEGORIA_1 else "nao",
            "metodo_elevacao": LIFT_KNOWN.get(p, "a_definir"),
            "restricao": RESTRICOES.get(p, ""),
            "em_operacao": "sim" if p in CATEGORIA_1 else "reativacao",
            "fonte": ";".join(_fontes(p)),
        })
    return master

def _fontes(poco: str) -> list[str]:
    f = []
    if poco in CATEGORIA_1: f.append("S03-cat1")
    if poco in RESTRICOES: f.append("S05-restricao")
    if poco in LIFT_KNOWN: f.append("S03-lift")
    if not f: f.append("v9-nomeado")
    return f

def resumo(master: list[dict]) -> dict:
    return {
        "total_pocos_nomeados": len(master),
        "categoria_1_base": sum(1 for m in master if m["categoria_1_base"] == "sim"),
        "com_restricao": sum(1 for m in master if m["restricao"]),
        "la_paz": sum(1 for m in master if m["campo"] == "La Paz"),
        "mara": sum(1 for m in master if m["campo"] == "Mara"),
        "el_mojan": sum(1 for m in master if m["campo"] == "El Moján"),
        "populacoes_divergentes": {"fdp_v8": 32, "workbook_s05": 35, "owner_fase1": 38, "binario_s04": 86},
        "acao_g01": "Validar well master com owner; confirmar os 38 da Fase 1 e mapear os 86 nomes do modelo binário",
    }

if __name__ == "__main__":
    master = reconcile()
    out = os.path.join(HERE, "well_master_reconciliado.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=master[0].keys(), delimiter=";")
        w.writeheader(); w.writerows(master)
    print(json.dumps(resumo(master), indent=2, ensure_ascii=False))
    print(f"\nWell master: {out}")
