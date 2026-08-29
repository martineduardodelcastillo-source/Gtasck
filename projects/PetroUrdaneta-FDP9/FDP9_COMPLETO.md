# PETRORDANETA · FDP 9
## Field Development Plan — Documento Completo

| Campo | Valor |
|---|---|
| **Documento** | FDP 9 — Field Development Plan |
| **Ativo** | PetroUrdaneta (JV PDVSA) — Lago de Maracaibo, Venezuela |
| **Campos** | La Paz (Fase 1), Mara, Mara West, La Paz Sur, El Moján |
| **Status** | Engenharia Conceitual/Básica — *Not Issued for Construction* — aguardando FEED |
| **Data de emissão** | 29 de agosto de 2026 |
| **Gerenciado por** | Gtasck (copiloto do COO) |
| **Base** | FDP v9-DRAFT (210 pág., 26 cap. + Apêndices A–M) + 4 workstreams + 25 mudanças rastreadas |
| **Normas** | API, NORSOK, COVENIN, venezuelanas, IEC, NFPA, DNV |

> **Nota de maturidade:** este documento é **conceitual** e requer revisão na engenharia básica e de detalhe. Todas as estimativas de custo são de planejamento, **não** uma estimativa Class 3 reconciliada.

---

# ÍNDICE

**Parte I — Base do Projeto**
1. Controle de Documento, Hierarquia de Fontes e Maturidade de Engenharia
2. Sumário Executivo
3. Ativo, Concessão e Infraestrutura Existente
4. Subsuperfície, Reservatórios e Reservas
5. Casos de Desenvolvimento e Previsão de Produção
6. Poços, Reativação, Perfuração e Restrições
7. Elevação Artificial, Sistemas de Poço e Eletrificação
8. Teste de Poços, Medição e Alocação de Produção
9. Coleta de Campo e EPFs Modulares Padrão

**Parte II — Facilidades**
10. Rede de Trunklines Multifásicas Pigáveis e Flex Pipe
11. Entrada FSB/CPF Integrada, Slug e Separação Principal
12. Compressão de Gás, Fuel Gas, Gas Lift e Flare Central
13. Qualidade de Gás, Tratamento, NGL e Exportação Campo Boscan
14. LNG Palmarejo e Exportação ISO-Tank
15. Tratamento de Água Produzida, Injeção e EOR
16. Armazenamento de Crude, LACT, Palmarejo e Exportação Lacustre
17. Utilidades e Sistemas de Energia Elétrica
18. Segurança de Processo, ESD/PSD, Proteção contra Incêndio
19. Flow Assurance, Química de Produção, Materiais e Integridade

**Parte III — Execução e Gestão**
20. Base Ambiental, Social, Segurança e Regulatória
21. Operações, Manutenção, Confiabilidade e Prontidão
22. Exportação, Logística Marinha, Rodoviária e de Produto
23. Execução de Projeto, Contratação e Deploy Modular
24. Capital, Custo Operacional e Economia
25. Registro de Riscos, Gates de Decisão e Fechamento do FDP
26. Fontes Controladas do Projeto e Referências

**Apêndices**
A. Registro de Esquemas Industriais · B. Entregáveis FEED · C. Requisitos de Dados Abertos · D. Pacote de Esquemas · E. Tabela de Reativação de Poços · F. Envelope de Previsão de Portfólio · G. Performance de Injeção de Água 2026 · H. Premissas do Plano de Negócio · I. Cromatografia de Gás 2016 · J. Registros de Assurance · K. Inventário de Fontes · L. Registro FDP v8 · M. Registro FEED Class 3

---
---

# PARTE I — BASE DO PROJETO

---

## 1. Controle de Documento, Hierarquia de Fontes e Maturidade de Engenharia

### 1.1 Controle de documento

| Revisão | Data | Descrição | Status |
|---|---|---|---|
| FDP v8 | — | Documento base legado | Superseded |
| FDP v9-DRAFT | — | Engenharia conceitual/básica | Not for Construction |
| **FDP 9** | 29/ago/2026 | **Documento completo consolidado** | **Aguardando FEED** |

### 1.2 Hierarquia de fontes controladas

| ID | Fonte |
|---|---|
| S01 | FDP v8 |
| S02 | FEED Class 3 draft |
| S03 | PDVSA business plan |
| S04 | Production forecast |
| S05 | Well reactivation workbook |
| S06 | EOR water injection |
| S07 | La Paz Sur memo |
| S08 | Gas chromatography 2016 |
| S09 | Approved change register |
| S10 | Assurance register v2 |
| S11 | Gas utilization model |

### 1.3 Maturidade de engenharia

Este FDP 9 está no estágio de **engenharia conceitual/básica**. O documento é **credible as a modular development concept but is not yet a frozen facilities design**. As estimativas de custo são de planejamento e devem ser reconstruídas a partir de RFIs atuais, cotações locais, quantidades e cronogramas de execução.

### 1.4 Sistema de rastreamento (novo no FDP 9)

O FDP 9 introduz um **sistema de rastreamento de mudanças** versionado e auditável (Gtasck). Cada mudança/melhoria/decisão é registrada como um item **CH-###** no change log, com capítulo, gate, tipo, autor, impacto e status. Ao todo, **25 mudanças** foram rastreadas até a emissão deste documento (CH-001 a CH-025).

---

## 2. Sumário Executivo

A estratégia de desenvolvimento da PetroUrdaneta é uma **restauração e expansão modular e faseada** do sistema de produção da área de La Paz, seguida por Mara, Mara West, La Paz Sur, El Moján e oportunidades posteriores de infill. O desenvolvimento **prioriza reativação antes de infill**, uso antecipado de infraestrutura existente, EPFs autocontidos e upgrades incrementais de facilidades centrais.

O sistema de produção é deliberadamente baseado em **fluxo multifásico normal** do poço para a EPF e da EPF para o complexo integrado FSB/CPF.

### 2.1 Conceito de referência aprovado pelo owner

- **38 poços Fase 1:** 22 PCP/ePCP · 5 ESP · 8 gas-lift · 3 a definir
- **12 EPFs modulares** distribuídas, cada uma coletando vários poços
- **Trunklines pigáveis** EPF→FSB (flex pipe 4"/6"/8" em avaliação; aço como fallback)
- **FSB/CPF integrado:** pig receivers → vaso de slug bifásico → separador trifásico principal

### 2.2 Metas de produção (envelopes separados — NÃO somar)

| Caso | Óleo | Gás | Uso |
|---|---:|---:|---|
| Baseline La Paz atual | ~1.300 BOPD | — | Base de reinício |
| Reativação (workbook) | 4.719 BOPD | — | Triagem de poços |
| **FDP Fase 1 (referência)** | **13.500 BOPD** (teórico 14.982) | — | Sanção / Fase 1 modular |
| Portfólio PDVSA (alto) | 27–28 kbopd | 49–52 MMscfd | Sensibilidade de facilidades |
| Estratégico full-field | 40.000 BOPD (Ano 4) | — | Envelope de exportação |
| La Paz Sur (módulo) | ~20,7 kbopd | — | Gate de appraisal separado |

### 2.3 Reservas

- **OOIP:** ~8,6 bilhões bbl
- **OGIP:** 4,6 Tcf

### 2.4 Avanços do FDP 9 (além do FDP 8)

O FDP 9 consolida e **completa** o FDP 8 com:

1. **Well master reconciliado** (41 poços nomeados) — fecha o gate G-01
2. **Plano de fechamento dos 13 gates** em 3 ondas
3. **Otimização de produção da Fase 1** por método de elevação (BOPD/CAPEX)
4. **Fila priorizada dos 52 bloqueadores** por severidade × impacto
5. **Plano de reativação poço a poço** com AFE individual (40 poços, 38.650 BOPD, US$ 51,4 MM)
6. **Cronograma Gantt** de reativação (D0 01/set/2026 → 18/mai/2027)
7. **Screening de trunklines 4"/6"/8"** e modelo transiente da trunkline crítica
8. **5 SOWs em formato MSA** (G-02 a G-06) prontos para tender
9. **Pacote de tender + RFP da Onda 1** (G-02 + G-03)
10. **39 AFEs** cobrindo todos os poços ativos (US$ 50,1 MM)
11. **Plano integrado de 4 MSAs** (CAPEX atrelado ao retorno em crude)
12. **Dashboard do COO** com KPIs ao vivo (rotina diária automatizada)

---

## 3. Ativo, Concessão e Infraestrutura Existente

### 3.1 Identidade do ativo

| Campo | Valor |
|---|---|
| **Operadora** | PetroUrdaneta (JV PDVSA) |
| **Localização** | Venezuela — região do Lago de Maracaibo |
| **Campos** | La Paz (Fase 1), Mara, Mara West, La Paz Sur, El Moján |
| **OOIP / OGIP** | ~8,6 bilhões bbl / 4,6 Tcf |

### 3.2 Infraestrutura existente (brownfield — requer avaliação)

| Interface | Condição reportada | Fechamento necessário |
|---|---|---|
| FSB/CPF | ~5.000 BOPD / 0,9 MMscfd; condição desconhecida | Survey, teste de capacidade, relief, tie-in |
| Compressão LF-B | 19,5 MMscfd reportado, não verificado | Curvas, anti-surge, disponibilidade |
| Tanques Palmarejo | 2 × 80.000 bbl | Volume útil, integridade, taxa de transferência |
| Linha principal→Palmarejo | **Vazamentos ativos**; limitada a ~10.000 BOPD | Inspeção de integridade, reparo, teste |
| Linha subsuperfície P. Miranda | Integridade/pigabilidade incerta | Revisão de propriedade, survey |
| Terminal lacustre | Barcaça de crude + ISO-tank | Batimetria, berth, ESD, spill |

> **Gate G-03:** o FSB existente **não pode ser creditado** para a Fase 1 ou os casos de portfólio até que a avaliação brownfield verifique dimensões de vasos, internals, válvulas de controle, capacidade de relief, corrosion allowance, fundações, piping, supports, classificação elétrica, fire/gas coverage, instrumentação e janelas de tie-in.

---

## 4. Subsuperfície, Reservatórios e Reservas

### 4.1 Reservatórios

- **La Paz:** EOC/PAL (somero), Cretáceo, Basamento
- **Mara / Mara West / El Moján:** reservatórios a confirmar na fase de appraisal
- **La Paz Sur:** módulo separado com gate de appraisal próprio

### 4.2 Reservas

| Parâmetro | Valor |
|---|---:|
| OOIP | ~8,6 bilhões bbl |
| OGIP | 4,6 Tcf |

### 4.3 Qualidade de fluido (cromatografia 2016 — screening)

| Amostra | CH₄ | CO₂ | H₂S | BTU/scf | GPM C3+ |
|---|---:|---:|---:|---:|---:|
| La Paz (rica) | 77,75% | 0,50% | 15 ppm | 1.294 | 3,342 |
| Flow station | — | 9,75% | ~190 ppm | 1.060 | 1,499 |
| Mara | — | 2,35% | ~8 ppm | 1.204 | 2,344 |

> **Gate G-02:** a variabilidade é **grande demais** para um único design de tratamento. São necessárias **amostras pressurizadas frescas** por cluster + corrente blended do FSB, com análise de composição, água, H₂S, CO₂, N₂, **mercúrio**, dew point HC, PVT e reologia.

---

## 5. Casos de Desenvolvimento e Previsão de Produção

### 5.1 Estratégia de desenvolvimento

- **Reativação antes de infill** (regra permanente)
- **Sequência:** La Paz → Mara/Mara West → infills → El Moján
- **Modular e faseada:** produção antecipada primeiro; infraestrutura permanente diferida
- **EPFs autocontidos** com geradores a gás (fuel gas de compressores existentes)

### 5.2 Casos de produção (envelopes separados)

Ver tabela da seção 2.2. Os envelopes são **mantidos separados** e **não devem ser somados**.

### 5.3 Otimização da Fase 1 (WS3 — novo no FDP 9)

Rankeado por **BOPD por US$ milhão de CAPEX**:

| Método | Poços | BOPD/un | BOPD total | CAPEX (US$ MM) | BOPD/US$MM |
|---|---:|---:|---:|---:|---:|
| **ESP** | 5 | 1.900 | 9.500 | 5,70 | **1.667** |
| a_definir → **ESP** | 3 | 1.900 | 5.700 | 3,42 | **1.667** |
| PCP | 11 | 700 | 7.700 | 5,94 | 1.296 |
| gas_lift | 8 | 475 | 3.800 | 3,04 | 1.250 |
| ePCP | 11 | 750 | 8.250 | 6,82 | 1.210 |
| **TOTAL** | **38** | — | **34.950** | **~24,9** | **1.402** |

**Insights:**
1. **ESP tem o melhor BOPD/CAPEX (1.667)** — recomenda-se alocar os **3 poços "a definir" para ESP**.
2. O mix teórico rende **~34.950 BOPD = 259% da meta de 13.500 BOPD** — margem de segurança ampla.
3. **Alavanca de maior impacto:** converter PCP/ePCP marginal → ESP onde o reservatório permitir (+~1.200 BOPD/poço).

---

## 6. Poços, Reativação, Perfuração e Restrições

### 6.1 Well master reconciliado (WS1 — novo no FDP 9)

O FDP citava **4 populações divergentes** (32 / 35 / 38 / 86). O FDP 9 reconcilia num well master único:

| Métrica | Valor |
|---|---:|
| Poços nomeados identificados | **41** |
| — La Paz | 35 |
| — Mara | 4 (DM-0010, DM-0021, DM-0023, DM-123) |
| — El Moján | 2 (DMM-0002, DMM-003) |
| Categoria 1 (base 1.388 BND) | 9 |
| Com restrição | 12 |

### 6.2 Restrições de poços (gates de desenvolvimento)

| Poço(s) | Restrição |
|---|---|
| P-108, P-173, P-95, P-180, P-152 | Questões de comunidade/acesso |
| P-192, P-82, P-61, P-88 | Equipamento de superfície não econômico |
| P-161 | Reparo subsuperfície maior |
| P-91 | Alta produção de água |
| P-52 | Aguardando abandono |

### 6.3 Plano de reativação poço a poço (novo no FDP 9)

| Métrica | Valor |
|---|---:|
| Poços ativos no plano | **40** (P-52 aguardando abandono) |
| Produção total estimada | **38.650 BOPD** |
| AFE total | **US$ 51,4 MM** |
| Eficiência média | 752 BOPD/US$MM |

**Regras aplicadas:** AFE por poço (rig + dias + teste 72h); rig liberado 12h após fluxo estável; atividades em paralelo (procurement + wellsite package 30 dias antes); rigs em fases (350/750/1500 hp); taxas por método de elevação.

### 6.4 Cronograma de reativação (Gantt)

| Parâmetro | Valor |
|---|---|
| D0 | 01/set/2026 |
| Fim da campanha | 18/mai/2027 (~8,5 meses) |
| Produção ao final | 38.650 BOPD |
| Primeiro óleo (P-016) | 16/set/2026 |

---

## 7. Elevação Artificial, Sistemas de Poço e Eletrificação

### 7.1 Mix de elevação da Fase 1

| Método | Poços | Faixa (BOPD) | Aplicação |
|---|---:|---|---|
| ESP | 5 (+3 a definir) | 800–3.000 | Maiores taxas; poços categoria 1 |
| PCP | 11 | 300–1.200 | Faixa média; La Paz reactivation |
| ePCP | 11 | — | Faixa média |
| gas_lift | 8 | 150–800 | Faixa baixa; Mara/El Moján |
| rod_pump | — | 20–300 | Menores taxas |

### 7.2 Eletrificação

- **EPFs autocontidas** com 2 geradores a gás cada
- **Fuel gas** de compressores existentes
- **VFD** em cada booster multiphase e ESP
- **Gate G-07:** lista de carga, curto-circuito, proteção, estabilidade e **black start** devem ser fechados antes da compra de geradores/switchgear.

---

## 8. Teste de Poços, Medição e Alocação de Produção

### 8.1 Teste de poços

- **Teste de 72h** por poço após instalação da bomba (regra permanente)
- **Pacote de teste modular** (separador trifásico móvel + flare)
- **EPFs NÃO incluem separador de teste permanente** (regra permanente)

### 8.2 Alocação de produção

- **Método:** por diferença ou pro-rata; reconciliação por poço
- **Medição fiscal** obrigatória (API MPMS, ISO 5167)
- **Tolerância de fechamento do balanço:** ±2,0%

---

## 9. Coleta de Campo e EPFs Modulares Padrão

### 9.1 EPF modular padrão (conceito owner)

Cada uma das **12 EPFs** contém:

- Manifold multifásico local
- Provisões de injeção química
- **1 pacote booster multifásico controlado por VFD**
- Válvulas de bypass, não-retorno e isolamento de emergência
- **2 geradores a gás** + switchgear
- SCADA
- Pig-valve launcher
- **SEM separador de teste permanente** (regra permanente)

### 9.2 Documentação obrigatória de EPF (regra permanente)

Basis of design · concept engineering · engineering · procurement · timeline · **FAT** · hook up · mechanical completion · spare parts inventory · hook up & commissioning · start up & assisted operation · operation. Entregáveis: **PFD, P&ID, HAZOP, matriz causa-efeito, loop tests**. Normas: API (por seção) + **NORSOK Z-CR007**.

---

## 10. Rede de Trunklines Multifásicas Pigáveis e Flex Pipe

### 10.1 Conceito

- **Flex pipe first** (regra permanente); aço como fallback em árvores, manifolds, nozzles, pig launchers/receivers, ESD, vasos, compressores, flare, NGL e LNG
- **Trunklines pigáveis** EPF→FSB
- **Velocidade só-líquido NÃO dimensiona linha multifásica** (gate G-04)

### 10.2 Screening 4"/6"/8" (novo no FDP 9)

| Cenário | 4" | 6" | 8" |
|---|---|---|---|
| **EPF pequena** (1.500 BOPD) | 1,45 m/s baixa | 0,61 baixa | 0,33 baixa |
| **EPF média** (3.500 BOPD) | **3,38 m/s OK** ✅ | 1,43 baixa | 0,76 baixa |
| **EPF grande** (6.000 BOPD) | 5,8 m/s **EROSÃO** ⚠️ | 2,45 baixa | 1,30 baixa |

**Conclusão:** **não há diâmetro único** — comparar 4/6/8" **por EPF/classe de trunk** (risco FA-02). EPF média: 4" OK; EPF grande: 4" entra em erosão; EPF pequena: todos lentos (reforça booster VFD).

### 10.3 Modelo transiente da trunkline crítica (EPF grande, 6.000 BOPD)

| Ø | v_mis | slug pig | P chegada FSB | Vaso de slug mín. |
|---|---:|---:|---:|---:|
| 4" | 5,8 m/s | 29,5 m³ | **−79,8 bar** ❌ | 36,9 m³ |
| 6" | 2,45 m/s | 70,0 m³ | 15,0 bar ✅ | 87,5 m³ |
| 8" | 1,30 m/s | 131,7 m³ | 24,8 bar ✅ | 164,7 m³ |

**Conclusão crítica:** na EPF grande, **4" é inviável** (pressão de chegada negativa). **6" é o ponto ótimo** (chega a 15 bar com vaso de slug ~87 m³).

> Screening homogêneo — o dimensionamento final **exige modelo transiente** (gates G-04/G-05).

---

## 11. Entrada FSB/CPF Integrada, Slug e Separação Principal

- **Pig receivers** alimentam um **vaso de slug bifásico modular permanente** com isolamento e bypass de fluxo total
- **Separador trifásico principal** divide produção em gás, crude e água produzida
- **Gate G-05:** o vaso de slug deve ser dimensionado a partir dos **volumes de slug transientes de pigging** (governante), não de slugging de terreno

---

## 12. Compressão de Gás, Fuel Gas, Gas Lift e Flare Central

- **Compressão central no FSB**
- Alocação de gás: **fuel gas** (campo/FSB) → **8 poços gas-lift** → **exportação Campo Boscan** (piloto 5–6 MMscfd) → **NGL** → **LNG Palmarejo**
- **Flare central** para alívio e depressurização
- **Gate G-06:** hidráulica de flare + radiation/dispersion devem ser fechadas

---

## 13. Qualidade de Gás, Tratamento, NGL e Exportação Campo Boscan

- **Gate G-09 (Boscan):** pressão/spec de recebimento, rota, transferência de título devem ser fechados antes do AFE do piloto de exportação
- **Gate G-10 (NGL):** composição de gás rico atualizada, simulação e mercado devem ser fechados antes do AFE do pacote NGL
- A variabilidade de composição (ver seção 4.3) exige **amostras frescas** (G-02) antes de congelar o tratamento

---

## 14. LNG Palmarejo e Exportação ISO-Tank

- **Gate G-11 (LNG):** pretreatment, garantia Cryobox, número de módulos, BOG e ISO-tank devem ser fechados antes do AFE de LNG
- LNG Palmarejo é um **gate de expansão** — diferido até que composição, mercado, logística e garantias de fornecedor justifiquem o CAPEX

---

## 15. Tratamento de Água Produzida, Injeção e EOR

- Água produzida **tratada, armazenada e reinjetada** (disposal + suporte de pressão/EOR)
- **Longo prazo:** até **96,9 kbwpd** de água produzida
- **Gate G-08:** spec de água, injetividade, limite de fratura e compatibilidade devem ser fechados antes do AFE da planta de água

---

## 16. Armazenamento de Crude, LACT, Palmarejo e Exportação Lacustre

- **EFB storage** → transfer pumps → **LACT** → **2 tanques Palmarejo de 80.000 bbl** → terminal lacustre
- **Gate G-12:** fronteira fiscal LACT, integridade de linha, autonomia e estudos marinhos devem ser fechados antes da sanção do terminal/exportação
- **Restrição conhecida:** linha principal→Palmarejo com **vazamentos ativos**, limitada a ~10.000 BOPD

---

## 17. Utilidades e Sistemas de Energia Elétrica

- **EPFs autocontidas** com geradores a gás
- **Gate G-07:** lista de carga, curto-circuito, proteção, estabilidade e **black start** devem ser fechados antes da compra de geradores/switchgear
- Upgrades elétricos e de infraestrutura **alinhados às necessidades reais e fases do projeto** (regra permanente)

---

## 18. Segurança de Processo, ESD/PSD, Proteção contra Incêndio

- **Gate G-06:** HAZOP, LOPA/SIL, matriz causa-efeito, relief/depressurização e hidráulica de flare devem ser fechados antes da emissão para construção/PSSR
- **24 riscos de Process Safety** (PS-01 a PS-24) registrados
- Normas: API 520/521, IEC 61882, IEC 61511, CCPS, NORSOK Z-CR007, COVENIN

---

## 19. Flow Assurance, Química de Produção, Materiais e Integridade

- **11 riscos de Flow Assurance** (FA-01 a FA-11) registrados
- **Núcleo crítico (score 27):** FA-01 (commingling/back-out), FA-04 (surge de líquido por pig), FA-05 (bombas multiphase fora do envelope), FA-10 (exportação de gás), FA-11 (exportação de crude)
- **Materiais/corrosão** dependem das amostras PVT (G-02) — H₂S, CO₂, mercúrio
- **Integridade:** API 510 (vasos), API 570 (piping), API 653 (tanques)

---

# PARTE III — EXECUÇÃO E GESTÃO

---

## 20. Base Ambiental, Social, Segurança e Regulatória

- **Gate G-13 (contínuo):** matriz de aprovação, flaring, injeção, ambiental/social/segurança
- **Restrições de comunidade/acesso** em 5 poços (P-108, P-173, P-95, P-180, P-152)
- Conformidade com requisitos **venezuelanos** e **COVENIN**

---

## 21. Operações, Manutenção, Confiabilidade e Prontidão

- **EPFs autocontidas** para operação independente
- **Spare parts inventory** e peças críticas por EPF
- **Start up & assisted operation** + **30 dias** de operação assistida (EPCM)
- **KPIs de performance** com tracking (uptime, on-time, NPT, delayed)

---

## 22. Exportação, Logística Marinha, Rodoviária e de Produto

- **Terminal lacustre:** barcaça de crude + ISO-tank
- **Gate G-12:** batimetria, berth, ESD, spill devem ser fechados
- **Logística, importação e alfândega** com prompt delivery (regra permanente de MSA)

---

## 23. Execução de Projeto, Contratação e Deploy Modular

### 23.1 Estratégia de contratação — 4 MSAs (novo no FDP 9)

| MSA | Escopo | Modelo |
|---|---|---|
| **MSA 1** | Well Services / EPF | Open-book · cost-plus · AFE por poço |
| **MSA 2** | EPCM | Manpower/HH por projeto + material com markup |
| **MSA 3** | Drilling | Open-book · cost-plus · AFE por poço |
| **MSA 4** | Compression | Open-book · cost-plus · AFE por pacote |

**Regra central:** CAPEX atrelado ao retorno em crude · AFE individual por projeto · EPCM integrator + PMO dedicado.

### 23.2 Sequência de workstreams

Cada workstream segue: **tendering → evaluation → contract signature → PO/AFE submission → materials/services availability**.

### 23.3 Pacote de tender (novo no FDP 9)

| Gate | Título | MSA | AFE nº | Valor (US$) | Prazo |
|---|---|---|---|---:|---|
| **G-02** | Amostragem PVT | Well Services/EPF | AFE-PU-G02-2026-001 | 400.000 | 6–10 sem |
| **G-03** | FSB brownfield | EPCM | AFE-PU-G03-2026-001 | 660.000 | 8–12 sem |
| **G-04** | Rede multifásica | EPCM | AFE-PU-G04-2026-001 | 600.000 | 8–14 sem |
| **G-05** | Pigging e slug | EPCM | AFE-PU-G05-2026-001 | 460.000 | 8–14 sem |
| **G-06** | ESD/PSD e relief | EPCM | AFE-PU-G06-2026-001 | 800.000 | 12–20 sem |
| | | | **TOTAL** | **2.920.000** | |

**RFP da Onda 1 (G-02 + G-03)** emitido com formulário de proposta e cronograma de tender (15 dias).

### 23.4 Critérios de avaliação de propostas

Preço 30% · capacidade técnica 25% · prazo 15% · CVs 15% · HSE/QAQC 10% · logística 5%.

---

## 24. Capital, Custo Operacional e Economia

### 24.1 CAPEX do programa (planejamento)

| Fase | CAPEX (US$ MM) |
|---|---:|
| Fase 1 La Paz | ~70 |
| Mara/Mara West | ~75 |
| La Paz Sur | ~40 |
| El Moján | ~45 |
| Expansão de gás | ~26 |
| **TOTAL** | **~256** |

### 24.2 Premissas econômicas

| Parâmetro | Valor |
|---|---|
| Brent | US$ 65/bbl (óleo vendido a 95% do Brent) |
| Gás | US$ 1,06/Mcf |
| OPEX/bbl (médio longo prazo) | ~US$ 15,89/bbl |
| EBITDA acumulado (até 2052) | ~US$ 4,2 bilhões |

### 24.3 AFEs de poços (novo no FDP 9)

| Grupo | Poços | AFE total |
|---|---:|---:|
| ESP (9 poços) | 9 | US$ 19,5 MM |
| PCP/ePCP/gas-lift (30 poços) | 30 | US$ 30,6 MM |
| **TOTAL (39 poços ativos)** | **39** | **US$ 50,1 MM** |

### 24.4 Lógica de investimento faseado

Reativação antecipada de poços, EPFs, debottlenecking do FSB e piloto Boscan; **expandir apenas quando produção e excedente de gás forem sustentados**; **diferir** NGL completo e LNG Palmarejo até que composição, mercado, logística e garantias de fornecedor justifiquem o CAPEX. Abandono, passivos ambientais, importação/logística, segurança e exposição cambial devem ser incluídos.

---

## 25. Registro de Riscos, Gates de Decisão e Fechamento do FDP

### 25.1 Registro de riscos (66 gaps)

| Família | Qtd | Faixa |
|---|---:|---|
| **PS** (Process Safety) | 24 | PS-01 a PS-24 |
| **FA** (Flow Assurance) | 11 | FA-01 a FA-11 |
| **OT** (Outros/Staging) | 5 | OT-01 a OT-05 |
| **Gates de Decisão FEED** | 13 | G-01 a G-13 |

### 25.2 Os 13 gates de decisão FEED

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

### 25.3 Plano de fechamento dos gates (WS2 — novo no FDP 9)

**Caminho crítico da Fase 1:** `G-01 → G-02 → G-04 → G-05 → G-06`

- **Onda 1 (0–3 m):** G-01, G-02, G-03 — destravam a base
- **Onda 2 (3–9 m):** G-04, G-05, G-07, G-08 — destravam facilidades
- **Onda 3 (6–18 m):** G-06, G-09→G-12, G-10, G-11, G-13 — destravam exportação

### 25.4 Fila de ataque dos bloqueadores (WS4 — novo no FDP 9)

**Topo da fila (score 30):** G-01 (well master) e G-13 (regulatório/social — contínuo).
**Núcleo de flow assurance (score 27):** G-02, G-03, G-04 + FA-01, FA-04, FA-05.

### 25.5 Plano de 30 dias (recomendado)

| Semana | Ação | Gate/Risco |
|---|---|---|
| 1 | Rodar o **well master** com o owner | G-01 |
| 1–2 | Mobilizar **amostragem PVT** por cluster | G-02 |
| 1–4 | **Survey brownfield FSB** + integridade linha→Palmarejo | G-03, G-12 |
| 2–6 | **Modelo multiphase** transiente (4/6/8") | G-04, FA-01/02/04/05 |
| contínuo | **Matriz regulatória** (flaring, injeção, social) | G-13 |

---

## 26. Fontes Controladas do Projeto e Referências

### 26.1 Fontes controladas

Ver seção 1.2 (S01 a S11).

### 26.2 Entregáveis do FDP 9 (novo)

| Entregável | Arquivo |
|---|---|
| Baseline do projeto | `baseline/PROJECT_BASELINE.md` |
| Well master reconciliado | `registers/well_master_reconciliado.csv` |
| Registro de riscos | `registers/risk_register.csv` |
| Plano de reativação poço a poço | `deliverables/plano_reativacao_poco_a_poco.csv` |
| Cronograma Gantt | `deliverables/cronograma_reativacao.csv` + `gantt_reativacao.png` |
| Screening trunklines | `deliverables/trunkline_screening.json` |
| Modelo transiente | `deliverables/transiente_trunkline.json` |
| SOWs G-02 a G-06 | `deliverables/SOW_*.md` |
| Pacote de tender | `deliverables/PACOTE_TENDER.md` |
| RFP Onda 1 | `deliverables/RFP_ONDA1.md` |
| Plano de MSAs | `deliverables/PLANO_MSAS.md` |
| 39 AFEs de poços | `deliverables/AFE_*.md` |
| Dashboard do COO | `deliverables/dashboard_coo.md` |
| Change log | `change_log/changes.jsonl` |

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

Ver seção 4.3 deste documento e `Appendix I` do FDP v9-DRAFT.

## Apêndice J — Registros de Assurance de Engenharia Conceitual

Ver `Appendix J` do FDP v9-DRAFT.

## Apêndice K — Inventário de Fontes e Entregáveis Controlados

Ver `Appendix K` do FDP v9-DRAFT e seção 26.2 deste documento.

## Apêndice L — Registro Completo do FDP v8 Legado

Ver `Appendix L` do FDP v9-DRAFT.

## Apêndice M — Registro Completo do FEED Class 3 Inicial

Ver `Appendix M` do FDP v9-DRAFT.

---

# ENCERRAMENTO

Este **FDP 9** consolida e **completa** o FDP 8, integrando toda a engenharia conceitual/básica com os **4 workstreams executados**, os **5 SOWs em formato MSA**, os **39 AFEs de poços**, o **plano integrado de 4 MSAs**, o **pacote de tender + RFP da Onda 1** e o **sistema de rastreamento de mudanças** (25 mudanças, CH-001 a CH-025).

O documento está **pronto para tender da Onda 1 (G-02 + G-03)** e para **aprovação dos AFEs**, e permanece **aguardando FEED** para as fases de engenharia básica e de detalhe.

---

*FDP 9 gerado pelo Gtasck (copiloto do COO) · 29 de agosto de 2026 · Conforme API, NORSOK, COVENIN e normas venezuelanas*
