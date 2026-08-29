# FDP-9 · Eixos 1 e 2 Detalhados — Reativação Poço a Poço + Trunklines 4/6/8"

> **Conceitual** — requer revisão na engenharia básica e de detalhe.
> Gerado em 29/ago/2026 · Gtasck (copiloto do COO)

---

## EIXO 1 · Plano de Reativação Poço a Poço (com AFE individual)

### Premissas aplicadas (regras permanentes do COO)

- **Reativação antes de infill**; sequência La Paz → Mara/Mara West → infills/El Moján.
- **AFE por poço** inclui: xmas tree, válvulas, tubing, rig+packers, elevação (ESP/PCP/ePCP/gas-lift), mob/demob wireline, **teste de 72h** e **rig rate × dias**.
- **Rig liberado 12h** após a bomba entrar e o fluxo de superfície estabilizar → o rig já parte para o próximo poço (atividades em paralelo).
- **Rigs em fases** (não todos de uma vez): 350 hp (somero EOC/PAL), 750 hp (cretáceo/basamento), 1500 hp (profundo).
- **Taxas por método de elevação** (nunca média única).

### Resultado consolidado

| Métrica | Valor |
|---|---:|
| Poços ativos no plano | **40** (1 aguardando abandono: P-52) |
| Produção total estimada | **38.650 BOPD** |
| AFE total | **US$ 51,4 MM** |
| Eficiência média | **752 BOPD/US$MM** |

### Top 10 poços por prioridade

| Poço | Elevação | BOPD | AFE (US$) | Rig | Dias | Prioridade |
|---|---|---:|---:|---|---:|---:|
| P-016 | ESP | 1.900 | 1.861k | 750hp | 12 | 1 |
| P-176 | ESP | 1.900 | 1.861k | 750hp | 12 | 1 |
| P-179 | ESP | 1.900 | 1.861k | 750hp | 12 | 1 |
| P-199A | ESP | 1.900 | 1.861k | 750hp | 12 | 1 |
| P-207 | ESP | 1.900 | 1.861k | 750hp | 12 | 1 |
| P-108 | ESP | 1.900 | 2.140k | 750hp | 12 | 1 |
| P-152 | ESP | 1.900 | 2.140k | 750hp | 12 | 1 |
| P-173 | ESP | 1.900 | 2.140k | 750hp | 12 | 1 |
| P-180 | ESP | 1.900 | 2.140k | 750hp | 12 | 1 |
| P-16 | PCP | 700 | 1.003k | 350hp | 7 | 3 |

> Os 9 poços **categoria 1** (base atual) receberam **ESP** (melhor BOPD/CAPEX) e prioridade 1. Poços com restrição de comunidade/acesso têm AFE +15%; equipamento de superfície não econômico +35%; reparo subsuperfície maior +60%.

### Estrutura de custo AFE por poço (ex.: ESP)

| Componente | US$ |
|---|---:|
| xmas tree | 85.000 |
| válvulas | 22.000 |
| tubing | 95.000 |
| rig + packers | 40.000 |
| elevação (ESP) | 1.140.000 |
| mob/demob wireline | 60.000 |
| teste 72h | 35.000 |
| rig rate (750hp × 12d) | 384.000 |
| **AFE base** | **~1.861.000** |

---

## EIXO 2 · Trunklines Multifásicas 4"/6"/8" (screening)

### Premissas

- **Flex pipe first**; pigável; aço como fallback em árvores, manifolds, nozzles, pig launchers/receivers, ESD, vasos, compressores, flare, NGL e LNG.
- **Velocidade só-líquido NÃO dimensiona linha multifásica** (gate G-04).
- Critérios: erosão API RP 14E (C=100), velocidade mínima ~3 m/s (evitar acúmulo de líquido), máxima ~18 m/s.
- Fluido screening: GOR 310 scf/STB, WC 30%, ρm calculada.

### Resultado do screening

| Cenário | 4" | 6" | 8" |
|---|---|---|---|
| **EPF pequena** (1.500 BOPD) | 1,45 m/s — baixa | 0,61 m/s — baixa | 0,33 m/s — baixa |
| **EPF média** (3.500 BOPD) | **3,38 m/s — OK** | 1,43 m/s — baixa | 0,76 m/s — baixa |
| **EPF grande** (6.000 BOPD) | 5,8 m/s — **EROSÃO** | 2,45 m/s — baixa | 1,30 m/s — baixa |

### Leitura para o COO

1. **Não há diâmetro único** — confirma a regra do FDP (FA-02): comparar 4/6/8" **por EPF/classe de trunk**, não forçar 6" uniforme.
2. **EPF média (~3.500 BOPD):** 4" fica na faixa OK (3,38 m/s); 6" e 8" ficam com velocidade baixa (risco de acúmulo de líquido e slugging).
3. **EPF grande (~6.000 BOPD):** 4" entra em **erosão**; 6" e 8" ficam baixos — indica necessidade de **booster/multiphase pump** para elevar a velocidade ou dividir o fluxo.
4. **EPF pequena:** todos os diâmetros ficam com velocidade baixa — reforça a necessidade do **booster VFD** em cada EPF (já no conceito owner).

> **Importante:** este é um screening homogêneo. O dimensionamento final **exige o modelo transiente** (gates G-04/G-05) com perfil de elevação, curvas de bomba, pressão de chegada no FSB, holdup, slugging e transientes de pigging.

---

## Arquivos gerados

| Arquivo | Conteúdo |
|---|---|
| `plano_reativacao_poco_a_poco.csv` | 41 poços com elevação, BOPD, AFE, rig, dias, prioridade |
| `reativacao_engine.py` | Motor do plano de reativação + AFE |
| `trunkline_screening.json` | Screening 4/6/8" por cenário de EPF |
| `trunkline_engine.py` | Motor do modelo de trunklines |
