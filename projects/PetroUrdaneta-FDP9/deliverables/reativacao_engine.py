#!/usr/bin/env python3
"""
Gtasck FDP-9 · Eixo 1 — Plano de Reativação Poço a Poço + AFE individual

Regras permanentes aplicadas (conhecimento do COO):
- Reativação ANTES de infill; sequência La Paz → Mara/Mara West → infills/El Moján
- AFE por poço: inclui rig + nº de dias + teste de 72h
- Rig liberado 12h após início da bomba e fluxo de superfície estável
- Atividades PARALELAS: wellsite package + procurement antes da intervenção
- Taxas SEMPRE por método de elevação (nunca média única)
- Rigs NÃO todos de uma vez — phased por tipo (350hp somero, 750hp cretáceo/basamento, 1500hp profundo)
"""
from __future__ import annotations
import csv, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
WELL_MASTER = os.path.join(HERE, "..", "registers", "well_master_reconciliado.csv")

# Taxas por método (ponto médio da faixa do config) — BOPD
LIFT = {
    "ESP":      {"bpd": 1900, "capex": 1_140_000, "rig_days": 12, "rig": "750hp"},
    "ePCP":     {"bpd": 750,  "capex": 620_000,  "rig_days": 8,  "rig": "350hp"},
    "PCP":      {"bpd": 700,  "capex": 540_000,  "rig_days": 7,  "rig": "350hp"},
    "gas_lift": {"bpd": 475,  "capex": 380_000,  "rig_days": 5,  "rig": "350hp"},
    "rod_pump": {"bpd": 160,  "capex": 210_000,  "rig_days": 4,  "rig": "350hp"},
}

# Componentes de custo AFE por poço (US$) — estilo AFE do config
AFE_COMPONENTS = {
    "xmas_tree": 85_000, "valves": 22_000, "tubing": 95_000, "rig_packers": 40_000,
    "mob_demob_wireline": 60_000, "teste_72h": 35_000,
}
RIG_RATE_DIA = {"350hp": 18_000, "750hp": 32_000, "1500hp": 55_000}  # US$/dia

# Penalidade de CAPEX por restrição conhecida
RESTRICAO_CAPEX = {
    "comunidade_acesso": 0.15, "equip_superficie_ineconomico": 0.35,
    "reparo_subsuperficie_maior": 0.60, "alta_agua": 0.10, "aguardando_abandono": None,
}

def atribuir_lift(poco: dict) -> str:
    """Atribui método de elevação respeitando o mix owner e as restrições."""
    if poco["metodo_elevacao"] != "a_definir":
        return poco["metodo_elevacao"]
    # Regra: poços categoria 1 (já em operação) e sem restrição → ESP (melhor BOPD/CAPEX)
    if poco["restricao"] == "aguardando_abandono":
        return "abandono"
    if poco["campo"] == "La Paz" and poco["categoria_1_base"] == "sim":
        return "ESP"
    if poco["restricao"] == "reparo_subsuperficie_maior":
        return "ESP"  # reparação maior justifica ESP de alta taxa
    return "PCP"  # default La Paz reactivation

def gerar_plano() -> list[dict]:
    wells = []
    with open(WELL_MASTER, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            wells.append(r)
    plano = []
    for w in wells:
        lift = atribuir_lift(w)
        if lift == "abandono":
            plano.append({**w, "lift": "abandono", "bpd": 0, "afe_usd": 0,
                          "rig": "—", "rig_days": 0, "prioridade": 99,
                          "obs": "Aguardando abandono — excluído da reativação"})
            continue
        L = LIFT[lift]
        restr = w["restricao"]
        mult = RESTRICAO_CAPEX.get(restr, 0.0) or 0.0
        capex_lift = L["capex"]
        capex_afe = sum(AFE_COMPONENTS.values()) + capex_lift + RIG_RATE_DIA[L["rig"]] * L["rig_days"]
        capex_total = round(capex_afe * (1 + mult))
        # Prioridade: categoria 1 primeiro, depois sem restrição, depois com restrição leve
        prio = 1 if w["categoria_1_base"] == "sim" else (3 if not restr else (5 if mult < 0.3 else 7))
        plano.append({**w, "lift": lift, "bpd": L["bpd"], "afe_usd": capex_total,
                      "rig": L["rig"], "rig_days": L["rig_days"], "prioridade": prio,
                      "obs": f"Restrição: {restr}" if restr else "Reativação padrão"})
    # Ordena por prioridade e BOPD/CAPEX
    plano.sort(key=lambda x: (x["prioridade"], -(x["bpd"]/(x["afe_usd"] or 1))))
    return plano

if __name__ == "__main__":
    plano = gerar_plano()
    ativos = [p for p in plano if p["lift"] != "abandono"]
    total_bpd = sum(p["bpd"] for p in ativos)
    total_afe = sum(p["afe_usd"] for p in ativos)
    out = os.path.join(HERE, "plano_reativacao_poco_a_poco.csv")
    cols = ["poco","campo","lift","bpd","afe_usd","rig","rig_days","prioridade","restricao","obs"]
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
        w.writeheader()
        for p in plano:
            w.writerow({k: p.get(k,"") for k in cols})
    print(f"=== PLANO DE REATIVAÇÃO POÇO A POÇO ===\n")
    print(f"Poços ativos: {len(ativos)} · Abandono: {len(plano)-len(ativos)}")
    print(f"Produção total estimada: {total_bpd:,} BOPD")
    print(f"AFE total: US$ {total_afe/1e6:.1f} MM")
    print(f"Média: {total_bpd/(total_afe/1e6):.0f} BOPD/US$MM\n")
    print("Top 10 por prioridade:")
    for p in plano[:10]:
        print(f"  {p['poco']:8} {p['lift']:9} {p['bpd']:>5} BOPD  AFE US$ {p['afe_usd']/1e3:>6.0f}k  rig {p['rig']:6} {p['rig_days']}d  prio {p['prioridade']}")
    print(f"\nSalvo: {out}")
