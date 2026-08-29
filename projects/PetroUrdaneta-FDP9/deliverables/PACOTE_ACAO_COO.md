# FDP-9 PetroUrdaneta · Pacote de Ação do COO

> Consolidação dos 4 workstreams executados em 29/ago/2026.
> Documento de decisão — pronto para revisão e aprovação.

---

## WS1 · Well Master Reconciliado (Gate G-01)

**Problema:** o FDP cita 4 populações de poços divergentes — **32** (FDP v8), **35** (workbook S05), **38** (conceito owner Fase 1) e **86** nomes únicos (modelo binário S04).

**Resultado da reconciliação (well_master_reconciliado.csv):**

| Métrica | Valor |
|---|---:|
| Poços nomeados identificados | **41** |
| — La Paz | 35 |
| — Mara | 4 (DM-0010, DM-0021, DM-0023, DM-123) |
| — El Moján | 2 (DMM-0002, DMM-003) |
| Categoria 1 (base 1.388 BND, dez/2025) | 9 |
| Com restrição (gate de desenvolvimento) | 12 |

**Ação para fechar G-01:** validar com o owner os **38 poços da Fase 1** e mapear os **86 nomes** do modelo binário contra o well master. Custo baixo, 2–4 semanas. **É o gate que destrava toda a base FEED.**

---

## WS2 · Plano de Fechamento dos 13 Gates

**Caminho crítico da Fase 1:** `G-01 → G-02 → G-04 → G-05 → G-06`

**3 ondas:**
- **Onda 1 (0–3 meses):** G-01, G-02, G-03 — destravam a base
- **Onda 2 (3–9 meses):** G-04, G-05, G-07, G-08 — destravam facilidades
- **Onda 3 (6–18 meses):** G-06, G-09, G-10, G-11, G-12, G-13 — destravam exportação/monetização

**Recomendação-chave:** não emitir AFE de trunk/bombas antes de G-04+G-05 (riscos FA-02/FA-04/FA-05).

---

## WS3 · Otimização de Produção da Fase 1 (38 poços)

Rankeado por **BOPD por US$ milhão de CAPEX** (taxas por método de elevação, nunca média única):

| Método | Poços | BOPD/un | BOPD total | CAPEX (US$ MM) | BOPD/US$MM |
|---|---:|---:|---:|---:|---:|
| **ESP** | 5 | 1.900 | 9.500 | 5,70 | **1.667** |
| a_definir → **ESP** | 3 | 1.900 | 5.700 | 3,42 | **1.667** |
| PCP | 11 | 700 | 7.700 | 5,94 | 1.296 |
| gas_lift | 8 | 475 | 3.800 | 3,04 | 1.250 |
| ePCP | 11 | 750 | 8.250 | 6,82 | 1.210 |
| **TOTAL** | **38** | — | **34.950** | **~24,9** | **1.402** |

**Insights para o COO:**
1. **ESP tem o melhor BOPD/CAPEX (1.667)** — recomenda-se alocar os **3 poços "a definir" para ESP**.
2. O mix teórico rende **~34.950 BOPD**, ou **259% da meta de 13.500 BOPD** — há margem para atingir a platô mesmo com poços abaixo do esperado.
3. **Alavanca de maior impacto:** converter poços PCP/ePCP marginais para ESP onde o reservatório permitir (cada conversão ≈ +1.200 BOPD por poço).
4. Respeitar a regra permanente: **reativação antes de infill**; AFE por poço inclui rig + dias + teste de 72h.

---

## WS4 · Fila de Ataque dos Bloqueadores (priorizada)

Score = severidade × impacto-no-gate. **Top 10:**

| # | ID | Score | Bloqueador |
|---:|---|---:|---|
| 1 | **G-01** | 30 | Well master / caso de desenvolvimento controlado |
| 1 | **G-13** | 30 | Regulatório/social/segurança (contínuo) |
| 3 | G-02 | 27 | PVT e amostragem de fluidos |
| 3 | G-03 | 27 | FSB brownfield (capacidade/integridade) |
| 3 | G-04 | 27 | Modelo de rede multiphase |
| 3 | **FA-01** | 27 | Commingling/back-out entre poços |
| 3 | **FA-04** | 27 | Surge de líquido por pig |
| 3 | **FA-05** | 27 | Bombas multiphase fora do envelope |
| 3 | FA-10 | 27 | Exportação de gás (condensação/off-spec) |
| 3 | FA-11 | 27 | Exportação de crude (surge/column separation) |

**Conclusão:** os gates **G-01 e G-13** lideram (score 30). Logo atrás, o cluster **G-02/G-03/G-04 + FA-01/FA-04/FA-05** (score 27) forma o **núcleo de flow assurance** que deve ser atacado em conjunto na Onda 1–2.

---

## Plano de 30 dias (recomendado)

| Semana | Ação | Gate/Risco |
|---|---|---|
| 1 | Aprovar e rodar o **well master** com o owner | G-01 |
| 1–2 | Mobilizar **amostragem PVT** por cluster | G-02 |
| 1–4 | **Survey brownfield do FSB** + integridade da linha→Palmarejo | G-03, G-12 |
| 2–6 | **Modelo multiphase** estacionário/transiente (4/6/8") | G-04, FA-01/02/04/05 |
| contínuo | Iniciar **matriz regulatória** (flaring, injeção, social) | G-13 |

---

## Rastreabilidade

Todas as mudanças deste pacote estão registradas no `change_log` (CH-###) e podem ser reportadas diariamente com:

> *"Gera o status do FDP 9"*
