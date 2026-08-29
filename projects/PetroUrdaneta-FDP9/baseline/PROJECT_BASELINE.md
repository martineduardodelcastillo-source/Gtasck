# PetroUrdaneta — FDP v9 · Baseline do Projeto

> **Fonte:** `PetroUrdaneta_FDP_v9-DRAFT_COMPLETE.docx` (210 páginas, 26 capítulos + Apêndices A–M)
> **Status do documento:** Engenharia Conceitual/Básica — *Not Issued for Construction* — aguardando FEED
> **Data da baseline:** 29 de agosto de 2026
> **Gerenciado por:** Gtasck (copiloto do COO)

---

## 1. Identidade do Ativo

| Campo | Valor |
|---|---|
| **Operadora** | PetroUrdaneta (JV PDVSA) |
| **Localização** | Venezuela — região do Lago de Maracaibo |
| **Campos** | La Paz (Fase 1), Mara, Mara West, La Paz Sur, El Moján |
| **Normas** | API, NORSOK, COVENIN, venezuelanas, IEC, NFPA, DNV |
| **OOIP / OGIP** | ~8,6 bilhões bbl / 4,6 Tcf |

## 2. Metas de Produção (envelopes separados — NÃO somar)

| Caso | Óleo | Gás | Uso |
|---|---:|---:|---|
| Baseline La Paz atual | ~1.300 BOPD | — | Base de reinício |
| Reativação (workbook) | 4.719 BOPD (abertura 12.254 + 1.374 workover) | — | Triagem de poços |
| **FDP Fase 1 (referência)** | **13.500 BOPD** (teórico 14.982) | — | Sanção / Fase 1 modular |
| Portfólio PDVSA (alto) | 27–28 kbopd | 49–52 MMscfd | Sensibilidade de facilidades |
| Estratégico full-field | 40.000 BOPD (Ano 4) | — | Envelope de exportação |
| La Paz Sur (módulo) | ~20,7 kbopd | — | Gate de appraisal separado |
| Água produzida (longo prazo) | — | → 96,9 kbwpd | Expansão de tratamento/injeção |

## 3. Arquitetura da Fase 1 (conceito aprovado pelo owner)

- **38 poços Fase 1:** 22 PCP/ePCP · 5 ESP · 8 gas-lift · 3 a definir
- **12 EPFs modulares** (manifold multiphase + booster VFD + 2 geradores a gás + SCADA + pig launcher) — **sem separador de teste permanente**
- **Trunklines pigáveis** EPF→FSB (flex pipe 4"/6"/8" em avaliação; aço como fallback)
- **FSB/CPF integrado:** pig receivers → vaso de slug bifásico → separador trifásico principal
- **Gás:** compressão central no FSB → fuel gas, 8 poços gas-lift, exportação Campo Boscan (piloto 5–6 MMscfd), futuro NGL e LNG Palmarejo
- **Óleo:** EFB storage → LACT → 2 tanques Palmarejo de 80.000 bbl → terminal lacustre
- **Água:** tratada e reinjetada (disposal + suporte de pressão/EOR)

## 4. Infraestrutura Existente (brownfield — requer avaliação)

| Interface | Condição reportada | Fechamento necessário |
|---|---|---|
| FSB/CPF | ~5.000 BOPD / 0,9 MMscfd; condição desconhecida | Survey, teste de capacidade, relief, tie-in |
| Compressão LF-B | 19,5 MMscfd reportado, não verificado | Curvas, anti-surge, disponibilidade |
| Tanques Palmarejo | 2 × 80.000 bbl | Volume útil, integridade, taxa de transferência |
| Linha principal→Palmarejo | **Vazamentos ativos**; limitada a ~10.000 BOPD | Inspeção de integridade, reparo, teste |
| Linha subsuperfície P. Miranda | Integridade/pigabilidade incerta | Revisão de propriedade, survey |
| Terminal lacustre | Barcaça de crude + ISO-tank | Batimetria, berth, ESD, spill |

## 5. Economia (caso PDVSA/business-plan)

| Parâmetro | Valor |
|---|---|
| CAPEX total do programa | ~US$ 256 milhões |
| — Fase 1 La Paz | ~US$ 70 MM |
| — Mara/Mara West | ~US$ 75 MM |
| — La Paz Sur | ~US$ 40 MM |
| — El Moján | ~US$ 45 MM |
| — Expansão de gás | ~US$ 26 MM |
| Brent | US$ 65/bbl (óleo vendido a 95% do Brent) |
| Gás | US$ 1,06/Mcf |
| OPEX/bbl (médio longo prazo) | ~US$ 15,89/bbl |
| EBITDA acumulado (até 2052) | ~US$ 4,2 bilhões |

> Estes são números de planejamento, **não** uma estimativa Class 3 reconciliada. Custos devem ser reconstruídos a partir de RFIs atuais.

## 6. Registro de Riscos (66 gaps: 52 bloqueadores FDP + 14 gates FEED)

| Família | Qtd | Faixa |
|---|---:|---|
| **PS** (Process Safety) | 24 | PS-01 a PS-24 |
| **FA** (Flow Assurance) | 11 | FA-01 a FA-11 |
| **OT** (Outros/Staging) | 5 | OT-01 a OT-05 |
| **Gates de Decisão FEED** | 13 | G-01 a G-13 |

## 7. Os 13 Gates de Decisão FEED (críticos)

| Gate | Fechamento necessário | Bloqueia |
|---|---|---|
| **G-01** Caso de desenvolvimento controlado | Reconciliar poços, cronogramas, perfis óleo/gás/água | Base FEED de facilidades |
| **G-02** PVT e amostragem de fluidos | Amostras pressurizadas, contaminantes, reologia, dew points | Freeze de bombas/linhas/tratamento |
| **G-03** Capacidade brownfield FSB | Survey, integridade, separação dinâmica, relief | AFE de upgrade do FSB |
| **G-04** Rede multiphase | Modelo estacionário/transiente, survey de rota, comparação 4/6/8" | Compra de trunk/bombas |
| **G-05** Pigging e slug | Programa de pig, volumes de slug transientes, capacidade | Freeze de trunk/vaso de entrada |
| **G-06** ESD/PSD e relief | HAZOP, LOPA/SIL, causa-efeito, flare | Emissão para construção/PSSR |
| **G-07** Energia e black start | Lista de carga, curto-circuito, proteção, estabilidade | Compra de geradores/switchgear |
| **G-08** Injeção de água | Spec de água, injetividade, limite de fratura, compatibilidade | AFE da planta de água |
| **G-09** Interface Boscan | Pressão/spec de recebimento, rota, transferência de título | AFE do piloto de exportação |
| **G-10** Economia NGL | Composição de gás rico atualizada, simulação, mercado | AFE do pacote NGL |
| **G-11** LNG Palmarejo | Pretreatment, garantia Cryobox, nº de módulos, BOG, ISO-tank | AFE de LNG |
| **G-12** Garantia crude/export | Fronteira fiscal LACT, integridade de linha, autonomia, estudos marinhos | Sanção terminal/exportação |
| **G-13** Regulatório/social/segurança | Matriz de aprovação, flaring, injeção, ambiental/social/segurança | Construção e operação de campo |

## 8. Restrições de Poços (gates de desenvolvimento)

| Poço(s) | Restrição |
|---|---|
| P-108, P-173, P-95, P-180, P-152 | Questões de comunidade/acesso |
| P-192, P-82, P-61, P-88 | Equipamento de superfície não econômico |
| P-161 | Reparo subsuperfície maior |
| P-91 | Alta produção de água |
| P-52 | Aguardando abandono |

## 9. Poços identificados no documento

**La Paz (P-…):** P-016, P-16, P-52, P-61, P-63, P-69, P-76, P-77, P-82, P-88, P-91, P-95, P-108, P-152, P-161, P-162, P-163, P-173, P-176, P-179, P-180, P-181, P-182, P-184, P-189, P-190, P-191, P-192, P-195, P-201, P-204, P-205, P-207
**Mara (DM-…):** DM-0010, DM-0021, DM-0023 (+1)

> **Nota:** o FDP cita 4 populações de poços (32 / 35 / 38 / 86 nomes) que **precisam ser reconciliadas** num "well master" controlado — este é o gate G-01.

## 10. Fontes controladas

S01 FDP v8 · S02 FEED Class 3 draft · S03 PDVSA business plan · S04 production forecast · S05 well reactivation · S06 EOR water injection · S07 La Paz Sur memo · S08 gas chromatography 2016 · S09 approved change register · S10 assurance register v2 · S11 gas utilization model
