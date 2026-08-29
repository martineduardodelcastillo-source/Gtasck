#!/usr/bin/env python3
"""
Gtasck FDP-9 · Entregável 1 — Cronograma de Reativação (Gantt) dos 40 poços

Regras permanentes:
- Rigs em FASES (não todos de uma vez): 350hp, 750hp, 1500hp
- Atividades PARALELAS: wellsite package + procurement ANTES da intervenção
- Rig liberado 12h após fluxo estável → parte para o próximo poço
- Teste de 72h por poço (rig-independent após liberação)
"""
from __future__ import annotations
import csv, os, json
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PLANO = os.path.join(HERE, "plano_reativacao_poco_a_poco.csv")

START = date(2026, 9, 1)          # D0 da campanha
PROCUREMENT_LEAD = 30             # dias de procurement/wellsite package (paralelo)
RIG_MOVE = 2                      # dias de movimentação entre poços
TEST_72H = 3                      # teste de 72h (3 dias)

# Rigs disponíveis por tipo (phased) — 1 rig por tipo no início
RIGS = {"750hp": {"livre_em": START}, "350hp": {"livre_em": START}, "1500hp": {"livre_em": START}}

def carregar() -> list[dict]:
    with open(PLANO, encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f, delimiter=";") if r["lift"] != "abandono"]
    rows.sort(key=lambda x: int(x["prioridade"]))
    return rows

def agendar() -> list[dict]:
    cron = []
    for w in carregar():
        rig = w["rig"]
        rig_days = int(w["rig_days"])
        livre = RIGS[rig]["livre_em"]
        # Procurement/wellsite package em paralelo (termina antes do rig chegar)
        proc_ini = livre - timedelta(days=PROCUREMENT_LEAD)
        if proc_ini < START: proc_ini = START
        ini = livre
        fim_rig = ini + timedelta(days=rig_days)
        # Rig liberado 12h após fluxo estável → próximo poço
        RIGS[rig]["livre_em"] = fim_rig + timedelta(days=RIG_MOVE)
        fim_teste = fim_rig + timedelta(days=TEST_72H)
        cron.append({
            "poco": w["poco"], "campo": w["campo"], "lift": w["lift"], "rig": rig,
            "procurement_inicio": proc_ini.isoformat(),
            "intervencao_inicio": ini.isoformat(), "intervencao_fim": fim_rig.isoformat(),
            "teste_72h_fim": fim_teste.isoformat(), "bpd": w["bpd"], "afe_usd": w["afe_usd"],
        })
    return cron

if __name__ == "__main__":
    cron = agendar()
    fim = max(c["teste_72h_fim"] for c in cron)
    total_bpd = sum(int(c["bpd"]) for c in cron)
    out = os.path.join(HERE, "cronograma_reativacao.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cron[0].keys(), delimiter=";")
        w.writeheader(); w.writerows(cron)
    print("=== CRONOGRAMA DE REATIVAÇÃO (40 poços) ===\n")
    print(f"Início (D0): {START}  ·  Fim da campanha: {fim}")
    print(f"Produção total ao final: {total_bpd:,} BOPD\n")
    print("Primeiros 8 poços:")
    for c in cron[:8]:
        print(f"  {c['poco']:8} {c['lift']:9} rig {c['rig']:6}  {c['intervencao_inicio']} → {c['intervencao_fim']}  (+72h: {c['teste_72h_fim']})")
    print(f"\nSalvo: {out}")
    with open("cronograma_reativacao.json", "w", encoding="utf-8") as fp:
        json.dump(cron, fp, indent=2, ensure_ascii=False)
