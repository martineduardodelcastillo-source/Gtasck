# PETRORDANETA · FDP 9
## Field Development Plan — Documento Completo

| Campo | Valor |
|---|---|
| **Documento** | FDP 9 — Field Development Plan |
| **Ativo** | PetroUrdaneta (JV PDVSA) — Lago de Maracaibo, Venezuela |
| **Campos** | La Paz (Fase 1), Mara, Mara West, La Paz Sur, El Moján |
| **Data de emissão** | 30 de agosto de 2026 |
| **Gerenciado por** | Gtasck (copiloto do COO) |
| **Normas** | API, NORSOK, COVENIN, venezuelanas, IEC 61511, NFPA, DNV |

---

# ÍNDICE

**Parte I — Visão Geral**
1. Sumário Executivo
2. Ativo, Concessão e Infraestrutura Existente
3. Subsuperfície, Reservatórios e Reservas

**Parte II — Processo**
4. Fluxo de Processo (PFD) e Correntes
5. Condições de Operação e Balanço de Massa
6. Facilidades: EPFs, Trunklines, FSB/CPF

**Parte III — Segurança**
7. Classificação de Segurança (SIL) e Elementos de Segurança
8. HAZOP e LOPA
9. Flow Assurance, Materiais e Integridade

**Parte IV — Poços**
10. Poços, Reativação e Elevação Artificial
11. Teste de Poços, Medição e Alocação

**Parte V — Execução**
12. Execução de Projeto, Contratação e Deploy Modular
13. Utilidades e Sistemas de Energia
14. Ambiental, Social, Segurança e Regulatório

**Parte VI — Economia e Gestão**
15. Capital, Custo Operacional e Economia
16. Registro de Riscos e Gates de Decisão
17. Gestão de Projeto e Rastreamento

**Apêndices**
A. Registro de Esquemas · B. Entregáveis FEED · C. Requisitos de Dados · D. Pacote de Esquemas · E. Tabela de Reativação · F. Envelope de Previsão · G. Injeção de Água 2026 · H. Premissas do Plano de Negócio · I. Cromatografia de Gás 2016 · J. Registros de Assurance · K. Inventário de Fontes · L. Registro FDP v8 · M. Registro FEED

---
---

# PARTE I — VISÃO GERAL

---

## 1. Sumário Executivo

A estratégia de desenvolvimento da PetroUrdaneta é uma **restauração e expansão modular e faseada** do sistema de produção da área de La Paz, seguida por Mara, Mara West, La Paz Sur, El Moján e oportunidades posteriores de infill. O desenvolvimento **prioriza reativação antes de infill**, uso antecipado de infraestrutura existente, EPFs autocontidos e upgrades incrementais de facilidades centrais.

O sistema de produção é deliberadamente baseado em **fluxo multifásico normal** do poço para a EPF e da EPF para o complexo integrado FSB/CPF.

### 1.1 Conceito de referência aprovado pelo owner

- **38 poços Fase 1:** 22 PCP/ePCP · 5 ESP · 8 gas-lift · 3 a definir
- **12 EPFs modulares** distribuídas, cada uma coletando vários poços
- **Trunklines pigáveis** EPF→FSB (flex pipe 4"/6"/8" em avaliação; aço como fallback)
- **FSB/CPF integrado:** pig receivers → vaso de slug bifásico → separador trifásico principal

### 1.2 Metas de produção (envelopes separados — NÃO somar)

| Caso | Óleo | Gás | Uso |
|---|---:|---:|---|
| Baseline La Paz atual | ~1.300 BOPD | — | Base de reinício |
| Reativação (workbook) | 4.719 BOPD | — | Triagem de poços |
| **FDP Fase 1 (referência)** | **13.500 BOPD** (teórico 14.982) | — | Sanção / Fase 1 modular |
| Portfólio PDVSA (alto) | 27–28 kbopd | 49–52 MMscfd | Sensibilidade de facilidades |
| Estratégico full-field | 40.000 BOPD (Ano 4) | — | Envelope de exportação |
| La Paz Sur (módulo) | ~20,7 kbopd | — | Gate de appraisal separado |

### 1.3 Reservas

- **OOIP:** ~8,6 bilhões bbl
- **OGIP:** 4,6 Tcf

---

## 2. Ativo, Concessão e Infraestrutura Existente

### 2.1 Identidade do ativo

| Campo | Valor |
|---|---|
| **Operadora** | PetroUrdaneta (JV PDVSA) |
| **Localização** | Venezuela — região do Lago de Maracaibo |
| **Campos** | La Paz (Fase 1), Mara, Mara West, La Paz Sur, El Moján |
| **OOIP / OGIP** | ~8,6 bilhões bbl / 4,6 Tcf |

### 2.2 Infraestrutura existente (brownfield — requer avaliação)

| Interface | Condição reportada | Fechamento necessário |
|---|---|---|
| FSB/CPF | ~5.000 BOPD / 0,9 MMscfd; condição desconhecida | Survey, teste de capacidade, relief, tie-in |
| Compressão LF-B | 19,5 MMscfd reportado, não verificado | Curvas, anti-surge, disponibilidade |
| Tanques Palmarejo | 2 × 80.000 bbl | Volume útil, integridade, taxa de transferência |
| Linha principal→Palmarejo | **Vazamentos ativos**; limitada a ~10.000 BOPD | Inspeção de integridade, reparo, teste |
| Linha subsuperfície P. Miranda | Integridade/pigabilidade incerta | Revisão de propriedade, survey |
| Terminal lacustre | Barcaça de crude + ISO-tank | Batimetria, berth, ESD, spill |

---

## 3. Subsuperfície, Reservatórios e Reservas

### 3.1 Reservatórios

- **La Paz:** EOC/PAL (somero), Cretáceo, Basamento
- **Mara / Mara West / El Moján:** reservatórios a confirmar na fase de appraisal
- **La Paz Sur:** módulo separado com gate de appraisal próprio

### 3.2 Reservas

| Parâmetro | Valor |
|---|---:|
| OOIP | ~8,6 bilhões bbl |
| OGIP | 4,6 Tcf |

### 3.3 Qualidade de fluido (cromatografia 2016 — screening)

| Amostra | CH₄ | CO₂ | H₂S | BTU/scf | GPM C3+ |
|---|---:|---:|---:|---:|---:|
| La Paz (rica) | 77,75% | 0,50% | 15 ppm | 1.294 | 3,342 |
| Flow station | — | 9,75% | ~190 ppm | 1.060 | 1,499 |
| Mara | — | 2,35% | ~8 ppm | 1.204 | 2,344 |

> **Gate G-02:** a variabilidade é **grande demais** para um único design de tratamento. São necessárias **amostras pressurizadas frescas** por cluster + corrente blended do FSB, com análise de composição, água, H₂S, CO₂, N₂, **mercúrio**, dew point HC, PVT e reologia.

---
---

# PARTE II — PROCESSO

---

## 4. Fluxo de Processo (PFD) e Correntes

### 4.1 Visão geral do fluxo

O processo segue o caminho: **poço → EPF → trunkline → FSB/CPF → separação → gás/óleo/água → exportação**.

```
POÇO → EPF (manifold + booster VFD) → TRUNKLINE (flex pipe 4"/6"/8") → FSB/CPF
  → PIG RECEIVER → VASO DE SLUG → SEPARADOR TRIFÁSICO
    → GÁS → compressão → fuel gas / gas lift / Boscan / NGL / LNG
    → ÓLEO → EFB storage → LACT → tanques Palmarejo → terminal lacustre
    → ÁGUA → tratamento → reinjeção (disposal + EOR)
```

### 4.2 Correntes de processo (stream table)

| Corrente | De | Para | Fluido | Vazão | Pressão | Temperatura | Elementos de segurança |
|---|---|---|---|---|---|---|---|
| **S-01** | Poço | EPF manifold | Multifásico (óleo+gás+água) | 300–3.000 BOPD | WHP | T_amb | SCSSV, Wing valve, choke |
| **S-02** | EPF manifold | Booster VFD | Multifásico | 300–3.000 BOPD | P_suc | T_amb | PSV, ESD, LAHH |
| **S-03** | Booster VFD | Trunkline | Multifásico | 300–3.000 BOPD | P_dis | T_amb | PSV, ESD, check valve |
| **S-04** | Trunkline | FSB pig receiver | Multifásico | 1.500–6.000 BOPD | P_arr | T_amb | PSV, ESD, pig signal |
| **S-05** | Pig receiver | Vaso de slug | Multifásico | 1.500–6.000 BOPD | P_arr | T_amb | PSV, ESD, LAHH, bypass |
| **S-06** | Vaso de slug | Separador trifásico | Multifásico | 1.500–6.000 BOPD | P_sep | T_sep | PSV, ESD, LAHH, LALL |
| **S-07** | Separador | Compressão | Gás | 0,9–52 MMscfd | P_sep | T_sep | PSV, ESD, anti-surge |
| **S-08** | Separador | EFB storage | Óleo | 1.300–40.000 BOPD | P_sep | T_sep | PSV, ESD, LAHH |
| **S-09** | Separador | Tratamento de água | Água | → 96,9 kbwpd | P_sep | T_sep | PSV, ESD, LAHH |
| **S-10** | Compressão | Fuel gas / gas lift / Boscan | Gás | 0,9–52 MMscfd | P_dis | T_dis | PSV, ESD, anti-surge |
| **S-11** | EFB storage | LACT → Palmarejo | Óleo | 1.300–40.000 BOPD | P_pump | T_amb | PSV, ESD, LACT |
| **S-12** | Tratamento | Reinjeção | Água | → 96,9 kbwpd | P_inj | T_amb | PSV, ESD, LAHH |

### 4.3 PFD esquemático

> **Nota:** os PFDs esquemáticos são gerados pelo motor de P&ID do Gtasck (ISA-5.1) e estão disponíveis em `modules/pid_generator/examples/`. O PFD da EPF (separador trifásico) já foi gerado e está disponível em `modules/pid_generator/examples/epf_preview.png`.

---

## 5. Condições de Operação e Balanço de Massa

### 5.1 Condições de operação por etapa

| Etapa | Pressão | Temperatura | Vazão |
|---|---|---|---|
| Poço (WHP) | 50–150 psi | T_amb | 300–3.000 BOPD |
| EPF (booster) | 150–300 psi | T_amb | 300–3.000 BOPD |
| Trunkline | 100–250 psi | T_amb | 1.500–6.000 BOPD |
| FSB (separação) | 50–100 psi | 60–80 °C | 1.500–6.000 BOPD |
| Compressão | 100–1.000 psi | 80–120 °C | 0,9–52 MMscfd |
| Exportação | 50–150 psi | T_amb | 1.300–40.000 BOPD |

### 5.2 Balanço de massa (Fase 1)

| Entrada | Vazão | Saída | Vazão |
|---|---:|---|---:|
| Poços (38) | 13.500 BOPD | Óleo (exportação) | 13.500 BOPD |
| | | Gás (fuel + lift + export) | 0,9–52 MMscfd |
| | | Água (reinjeção) | → 96,9 kbwpd |

**Tolerância de fechamento:** ±2,0% (regra permanente).

---

## 6. Facilidades: EPFs, Trunklines, FSB/CPF

### 6.1 EPF modular padrão

Cada uma das **12 EPFs** contém:

- Manifold multifásico local
- Provisões de injeção química
- **1 pacote booster multifásico controlado por VFD**
- Válvulas de bypass, não-retorno e isolamento de emergência
- **2 geradores a gás** + switchgear
- SCADA
- Pig-valve launcher
- **SEM separador de teste permanente** (regra permanente)

### 6.2 Trunklines pigáveis

- **Flex pipe first** (regra permanente); aço como fallback
- **Screening 4"/6"/8":** EPF média (3.500 BOPD) → 4" OK; EPF grande (6.000 BOPD) → 4" erosão, 6" ótimo
- **Modelo transiente:** EPF grande → 6" chega a 15 bar com vaso de slug ~87 m³

### 6.3 FSB/CPF integrado

- **Pig receivers** → **vaso de slug bifásico** → **separador trifásico principal**
- **Compressão central** → fuel gas, gas lift, Boscan, NGL, LNG
- **EFB storage** → LACT → tanques Palmarejo → terminal lacustre
- **Tratamento de água** → reinjeção

---

# PARTE III — SEGURANÇA

---

## 7. Classificação de Segurança (SIL) e Elementos de Segurança

### 7.1 Níveis de SIL (IEC 61511)

| Nível SIL | PFD | RRF | Aplicação típica |
|---|---|---|---|
| **SIL 1** | 0,1–0,01 | 10–100 | Proteção de overflow de tanque, shutdowns básicos |
| **SIL 2** | 0,01–0,001 | 100–1.000 | **ESD de wellheads, sistemas de segurança de fired heaters, proteção de compressores** |
| **SIL 3** | 0,001–0,0001 | 1.000–10.000 | BMS de fornos grandes, HIPPS |
| **SIL 4** | 0,0001–0,00001 | 10.000–100.000 | Nuclear, aviação — raramente em plantas de processo |

### 7.2 Classificação SIL da planta PetroUrdaneta

| SIF | Descrição | SIL alvo | Justificativa |
|---|---|---|---|
| **SIF-01** | ESD de wellhead (SCSSV + wing valve) | **SIL 2** | Padrão O&G; proteção contra overpressure/release |
| **SIF-02** | ESD de EPF (booster + manifold) | **SIL 2** | Proteção contra overpressure/release |
| **SIF-03** | ESD de trunkline (pig receiver) | **SIL 2** | Proteção contra overpressure/release |
| **SIF-04** | ESD de FSB (separador + compressão) | **SIL 2** | Proteção contra overpressure/release |
| **SIF-05** | Anti-surge de compressores | **SIL 2** | Proteção de compressores |
| **SIF-06** | Proteção de flare | **SIL 2** | Proteção contra overpressure |
| **SIF-07** | HIPPS (se aplicável) | **SIL 3** | Se substituir relief convencional |

> **Regra prática:** a maioria das SIFs da planta fica em **SIL 2**; SIL 3 apenas para HIPPS (se aplicável); SIL 4 raramente (redesenhar o processo se LOPA apontar SIL 4).

### 7.3 Elementos de segurança por corrente

| Corrente | Elementos de segurança |
|---|---|
| **S-01** (poço→EPF) | SCSSV, wing valve, choke, PSV |
| **S-02** (EPF manifold→booster) | PSV, ESD, LAHH |
| **S-03** (booster→trunkline) | PSV, ESD, check valve |
| **S-04** (trunkline→FSB) | PSV, ESD, pig signal |
| **S-05** (pig receiver→vaso de slug) | PSV, ESD, LAHH, bypass |
| **S-06** (vaso de slug→separador) | PSV, ESD, LAHH, LALL |
| **S-07** (separador→compressão) | PSV, ESD, anti-surge |
| **S-08** (separador→EFB) | PSV, ESD, LAHH |
| **S-09** (separador→tratamento) | PSV, ESD, LAHH |
| **S-10** (compressão→fuel/lift/Boscan) | PSV, ESD, anti-surge |
| **S-11** (EFB→LACT→Palmarejo) | PSV, ESD, LACT |
| **S-12** (tratamento→reinjeção) | PSV, ESD, LAHH |

---

## 8. HAZOP e LOPA

### 8.1 Processo de determinação de SIL

1. **HAZOP** — identifica desvios, causas, consequências
2. **LOPA** — compara frequência mitigada vs. risco tolerável; o gap determina o SIL
3. **Atribuição de SIL** a cada SIF (sensor + logic solver + final element)
4. **Verificação de SIL** — cálculo quantitativo (fault tolerance, PFD de componentes, proof test interval, diagnostic coverage)

### 8.2 Cadernos de HAZOP (com mitigação por desvio)

Os cadernos de HAZOP são gerados pelo motor de risco do Gtasck e estão disponíveis em `modules/risk_analysis/`. Cada desvio é amarrado a: **causa → consequência → salvaguarda existente → mitigação/ação proposta → responsável → prazo**.

**Exemplo (nó EPF):**

| Desvio | Causa | Consequência | Salvaguarda | Mitigação/Ação | Responsável | Prazo |
|---|---|---|---|---|---|---|
| Alta pressão | Falha de choke | Overpressure no manifold | PSV | Instalar PSV adicional + ESD | Engenharia | 30 dias |
| Baixo fluxo | Bomba parada | Acúmulo de líquido | LAHH | Alarme + trip de booster | Operações | 15 dias |
| Alta temperatura | Falha de resfriamento | Degradação de elastômero | TAH | Alarme + trip | Manutenção | 15 dias |

---

## 9. Flow Assurance, Materiais e Integridade

### 9.1 Riscos de Flow Assurance (FA-01 a FA-11)

| ID | Risco | Mitigação |
|---|---|---|
| FA-01 | Commingling/back-out entre poços | Modelo de rede multiphase (G-04) |
| FA-02 | Dimensionamento de trunk (6" uniforme não provado) | Screening 4/6/8" por EPF (G-04) |
| FA-03 | Flex pipe pigável não qualificado | Qualificação de flex pipe (G-04) |
| FA-04 | Surge de líquido por pig | Modelo transiente de pigging (G-05) |
| FA-05 | Bombas multiphase fora do envelope | Envelope de operação (G-04) |
| FA-06 | Depósitos (cera/hidrato/asfalteno) | Amostras PVT (G-02) |
| FA-07 | Sólidos/integridade (areia/erosão/corrosão) | Amostras PVT (G-02) + integridade (G-03) |
| FA-08 | Qualidade de separação (emulsão/espuma) | Amostras PVT (G-02) |
| FA-09 | Sistema de água (scale/MIC/oxigênio) | Spec de água (G-08) |
| FA-10 | Exportação de gás (condensação/off-spec) | Spec de gás (G-09) |
| FA-11 | Exportação de crude (surge/column separation) | Modelo transiente (G-05) |

### 9.2 Materiais e integridade

- **Materiais/corrosão** dependem das amostras PVT (G-02) — H₂S, CO₂, mercúrio
- **Integridade:** API 510 (vasos), API 570 (piping), API 653 (tanques)

---
---

# PARTE IV — POÇOS

---

## 10. Poços, Reativação e Elevação Artificial

### 10.1 Well master reconciliado

| Métrica | Valor |
|---|---:|
| Poços nomeados identificados | **41** |
| — La Paz | 35 |
| — Mara | 4 (DM-0010, DM-0021, DM-0023, DM-123) |
| — El Moján | 2 (DMM-0002, DMM-003) |
| Categoria 1 (base 1.388 BND) | 9 |
| Com restrição | 12 |

### 10.2 Plano de reativação poço a poço

| Métrica | Valor |
|---|---:|
| Poços ativos no plano | **40** (P-52 aguardando abandono) |
| Produção total estimada | **38.650 BOPD** |
| AFE total | **US$ 51,4 MM** |
| Eficiência média | 752 BOPD/US$MM |

### 10.3 Mix de elevação da Fase 1

| Método | Poços | Faixa (BOPD) | Aplicação |
|---|---:|---|---|
| ESP | 5 (+3 a definir) | 800–3.000 | Maiores taxas; poços categoria 1 |
| PCP | 11 | 300–1.200 | Faixa média; La Paz reactivation |
| ePCP | 11 | — | Faixa média |
| gas_lift | 8 | 150–800 | Faixa baixa; Mara/El Moján |
| rod_pump | — | 20–300 | Menores taxas |

### 10.4 Cronograma de reativação (Gantt)

| Parâmetro | Valor |
|---|---|
| D0 | 01/set/2026 |
| Fim da campanha | 18/mai/2027 (~8,5 meses) |
| Produção ao final | 38.650 BOPD |
| Primeiro óleo (P-016) | 16/set/2026 |

---

## 11. Teste de Poços, Medição e Alocação

### 11.1 Teste de poços

- **Teste de 72h** por poço após instalação da bomba (regra permanente)
- **Pacote de teste modular** (separador trifásico móvel + flare)
- **EPFs NÃO incluem separador de teste permanente** (regra permanente)

### 11.2 Alocação de produção

- **Método:** por diferença ou pro-rata; reconciliação por poço
- **Medição fiscal** obrigatória (API MPMS, ISO 5167)
- **Tolerância de fechamento do balanço:** ±2,0%

---
---

# PARTE V — EXECUÇÃO

---

## 12. Execução de Projeto, Contratação e Deploy Modular

### 12.1 Estratégia de contratação — 4 MSAs

| MSA | Escopo | Modelo |
|---|---|---|
| **MSA 1** | Well Services / EPF | Open-book · cost-plus · AFE por poço |
| **MSA 2** | EPCM | Manpower/HH por projeto + material com markup |
| **MSA 3** | Drilling | Open-book · cost-plus · AFE por poço |
| **MSA 4** | Compression | Open-book · cost-plus · AFE por pacote |

**Regra central:** CAPEX atrelado ao retorno em crude · AFE individual por projeto · EPCM integrator + PMO dedicado.

### 12.2 Pacote de tender

| Gate | Título | MSA | AFE nº | Valor (US$) | Prazo |
|---|---|---|---|---:|---|
| **G-02** | Amostragem PVT | Well Services/EPF | AFE-PU-G02-2026-001 | 400.000 | 6–10 sem |
| **G-03** | FSB brownfield | EPCM | AFE-PU-G03-2026-001 | 660.000 | 8–12 sem |
| **G-04** | Rede multifásica | EPCM | AFE-PU-G04-2026-001 | 600.000 | 8–14 sem |
| **G-05** | Pigging e slug | EPCM | AFE-PU-G05-2026-001 | 460.000 | 8–14 sem |
| **G-06** | ESD/PSD e relief | EPCM | AFE-PU-G06-2026-001 | 800.000 | 12–20 sem |
| | | | **TOTAL** | **2.920.000** | |

### 12.3 RFP da Onda 1 (G-02 + G-03)

Emitido com formulário de proposta e cronograma de tender (15 dias).

---

## 13. Utilidades e Sistemas de Energia

- **EPFs autocontidas** com geradores a gás
- **Gate G-07:** lista de carga, curto-circuito, proteção, estabilidade e **black start** devem ser fechados antes da compra de geradores/switchgear
- Upgrades elétricos e de infraestrutura **alinhados às necessidades reais e fases do projeto** (regra permanente)

---

## 14. Ambiental, Social, Segurança e Regulatório

- **Gate G-13 (contínuo):** matriz de aprovação, flaring, injeção, ambiental/social/segurança
- **Restrições de comunidade/acesso** em 5 poços (P-108, P-173, P-95, P-180, P-152)
- Conformidade com requisitos **venezuelanos** e **COVENIN**

---
---

# PARTE VI — ECONOMIA E GESTÃO

---

## 15. Capital, Custo Operacional e Economia

### 15.1 CAPEX do programa (planejamento)

| Fase | CAPEX (US$ MM) |
|---|---:|
| Fase 1 La Paz | ~70 |
| Mara/Mara West | ~75 |
| La Paz Sur | ~40 |
| El Moján | ~45 |
| Expansão de gás | ~26 |
| **TOTAL** | **~256** |

### 15.2 Premissas econômicas

| Parâmetro | Valor |
|---|---|
| Brent | US$ 65/bbl (óleo vendido a 95% do Brent) |
| Gás | US$ 1,06/Mcf |
| OPEX/bbl (médio longo prazo) | ~US$ 15,89/bbl |
| EBITDA acumulado (até 2052) | ~US$ 4,2 bilhões |

### 15.3 AFEs de poços

| Grupo | Poços | AFE total |
|---|---:|---:|
| ESP (9 poços) | 9 | US$ 19,5 MM |
| PCP/ePCP/gas-lift (30 poços) | 30 | US$ 30,6 MM |
| **TOTAL (39 poços ativos)** | **39** | **US$ 50,1 MM** |

---

## 16. Registro de Riscos e Gates de Decisão

### 16.1 Registro de riscos (66 gaps)

| Família | Qtd | Faixa |
|---|---:|---|
| **PS** (Process Safety) | 24 | PS-01 a PS-24 |
| **FA** (Flow Assurance) | 11 | FA-01 a FA-11 |
| **OT** (Outros/Staging) | 5 | OT-01 a OT-05 |
| **Gates de Decisão FEED** | 13 | G-01 a G-13 |

### 16.2 Os 13 gates de decisão FEED

| Gate | Fechamento necessário | Bloqueia |
|---|---|---|
| **G-01** | Caso de desenvolvimento controlado | Base FEED de facilidades |
| **G-02** | PVT e amostragem de fluidos | Freeze de bombas/linhas/tratamento |
| **G-03** | Capacidade brownfield FSB | AFE de upgrade do FSB |
| **G-04** | Rede multiphase | Compra de trunk/bombas |
| **G-05** | Pigging e slug | Freeze de trunk/vaso de entrada |
| **G-06** | ESD/PSD e relief | Emissão para construção/PSSR |
| **G-07** | Energia e black start | Compra de geradores/switchgear |
| **G-08** | Injeção de água | AFE da planta de água |
| **G-09** | Interface Boscan | AFE do piloto de exportação |
| **G-10** | Economia NGL | AFE do pacote NGL |
| **G-11** | LNG Palmarejo | AFE de LNG |
| **G-12** | Garantia crude/export | Sanção terminal/exportação |
| **G-13** | Regulatório/social/segurança | Construção e operação de campo |

### 16.3 Plano de fechamento dos gates

**Caminho crítico da Fase 1:** `G-01 → G-02 → G-04 → G-05 → G-06`

- **Onda 1 (0–3 m):** G-01, G-02, G-03 — destravam a base
- **Onda 2 (3–9 m):** G-04, G-05, G-07, G-08 — destravam facilidades
- **Onda 3 (6–18 m):** G-06, G-09→G-12, G-10, G-11, G-13 — destravam exportação

---

## 17. Gestão de Projeto e Rastreamento

### 17.1 Sistema de rastreamento

O FDP 9 introduz um **sistema de rastreamento de mudanças** versionado e auditável (Gtasck). Cada mudança/melhoria/decisão é registrada como um item **CH-###** no change log, com capítulo, gate, tipo, autor, impacto e status.

### 17.2 Dashboard do COO

O dashboard do COO é regenerado automaticamente a cada mudança e está disponível em `deliverables/dashboard_coo.md`. KPIs: mudanças rastreadas, gates fechados, poços, produção, CAPEX.

### 17.3 Rotina diária automatizada

O dashboard é regenerado automaticamente **todo dia às 10h** (America/Sao_Paulo) e commitado no repo.

---
---

# APÊNDICES

## Apêndice A — Registro de Esquemas Industriais

Ver `Appendix A` do FDP v9-DRAFT (registro completo de esquemas industriais).

## Apêndice B — Entregáveis FEED Requeridos

Ver `Appendix B` do FDP v9-DRAFT.

## Apêndice C — Requisitos de Dados Abertos

Ver `Appendix C` do FDP v9-DRAFT.

## Apêndice D — Pacote de Esquemas Industriais

Ver `Appendix D` do FDP v9-DRAFT.

## Apêndice E — Tabela Detalhada de Reativação de Poços

Ver `registers/well_master_reconciliado.csv` e `deliverables/plano_reativacao_poco_a_poco.csv` (FDP 9).

## Apêndice F — Envelope de Previsão de Portfólio

Ver `Appendix F` do FDP v9-DRAFT.

## Apêndice G — Performance de Injeção de Água 2026

Ver `Appendix G` do FDP v9-DRAFT.

## Apêndice H — Premissas do Plano de Negócio PDVSA–PetroUrdaneta

Ver `Appendix H` do FDP v9-DRAFT.

## Apêndice I — Cromatografia de Gás 2016 (Screening)

Ver seção 3.3 deste documento e `Appendix I` do FDP v9-DRAFT.

## Apêndice J — Registros de Assurance de Engenharia

Ver `Appendix J` do FDP v9-DRAFT.

## Apêndice K — Inventário de Fontes e Entregáveis Controlados

Ver `Appendix K` do FDP v9-DRAFT e seção 17 deste documento.

## Apêndice L — Registro Completo do FDP v8 Legado

Ver `Appendix L` do FDP v9-DRAFT.

## Apêndice M — Registro Completo do FEED

Ver `Appendix M` do FDP v9-DRAFT.

---

# ENCERRAMENTO

Este **FDP 9** consolida e **completa** o FDP 8, integrando toda a engenharia com os **4 workstreams executados**, os **5 SOWs em formato MSA**, os **39 AFEs de poços**, o **plano integrado de 4 MSAs**, o **pacote de tender + RFP da Onda 1** e o **sistema de rastreamento de mudanças** (26 mudanças, CH-001 a CH-026).

O documento está **pronto para tender da Onda 1 (G-02 + G-03)** e para **aprovação dos AFEs**.

---

*FDP 9 gerado pelo Gtasck (copiloto do COO) · 30 de agosto de 2026 · Conforme API, NORSOK, COVENIN, IEC 61511 e normas venezuelanas*
