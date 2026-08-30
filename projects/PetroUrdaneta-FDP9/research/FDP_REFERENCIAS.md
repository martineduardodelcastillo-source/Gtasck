# Referências de FDP — Pesquisa de Melhores Práticas

> Pesquisa conduzida em 30/ago/2026 para reconstruir o FDP 9 com o mais alto padrão de engenharia.

---

## 1. Estrutura padrão de um FDP (indústria)

Fontes: LinkedIn (Fabricio Sierra), NSTA (UK), Scribd, SlideShare, Opus Kinetic.

Um FDP completo deve conter, em sequência lógica:

1. **Avaliação Geológica e Geofísica** — dados sísmicos, well logs, amostras de núcleo; mapear arquitetura do reservatório (porosidade, permeabilidade, saturação)
2. **Engenharia de Reservatório** — modelar comportamento do reservatório, prever resposta a métodos de extração, estimar volumes recuperáveis, selecionar técnicas de recuperação
3. **Perfuração e Completação** — número, tipo (vertical/horizontal/multilateral), trajetória e localização de poços; planos de perfuração e completação
4. **Facilidades e Infraestrutura** — plantas de processamento, pipelines, armazenamento, transporte; infraestrutura auxiliar (água, energia, estradas)
5. **Conformidade Ambiental e Regulatória** — EIAs, licenças, medidas de mitigação
6. **Análise Econômica** — CAPEX/OPEX, análise de sensibilidade, NPV, IRR, payback
7. **Gestão de Riscos** — riscos técnicos, de mercado, operacionais; estratégias de mitigação; avaliações periódicas
8. **Gestão de Projeto** — marcos, coordenação de recursos, controles de projeto, monitoramento e relatórios

## 2. Níveis de SIL (IEC 61511)

Fonte: Stepin Engineering (guia completo de SIL).

| Nível SIL | PFD | RRF | Aplicação típica |
|---|---|---|---|
| **SIL 1** | 0,1–0,01 | 10–100 | Proteção de overflow de tanque, shutdowns básicos |
| **SIL 2** | 0,01–0,001 | 100–1.000 | **ESD de wellheads, sistemas de segurança de fired heaters, proteção de compressores** |
| **SIL 3** | 0,001–0,0001 | 1.000–10.000 | BMS de fornos grandes, HIPPS |
| **SIL 4** | 0,0001–0,00001 | 10.000–100.000 | Nuclear, aviação — raramente em plantas de processo |

**Processo de determinação de SIL:**
1. **HAZOP** — identifica desvios, causas, consequências
2. **LOPA** — compara frequência mitigada vs. risco tolerável; o gap determina o SIL
3. **Atribuição de SIL** a cada SIF (sensor + logic solver + final element)
4. **Verificação de SIL** — cálculo quantitativo (fault tolerance, PFD de componentes, proof test interval, diagnostic coverage)

**Regra prática para O&G:** a maioria das SIFs fica em **SIL 2**; SIL 3 para HIPPS/BMS; SIL 4 raramente (redesenhar o processo se LOPA apontar SIL 4).

## 3. PFD (Process Flow Diagram)

Fonte: silsafe.net.

> "Um PFD é o desenho de alto nível mostrando os principais equipamentos, correntes de processo e balanço de massa geral, um nível acima do P&ID."

Um PFD deve mostrar:
- **Principais equipamentos** (vasos, separadores, bombas, compressores, tanques)
- **Correntes de processo** (com número, de onde vem, para onde vai)
- **Balanço de massa** (vazões, pressões, temperaturas por corrente)
- **Elementos de segurança** (PSVs, ESDs, alarmes, interlocks)

## 4. NORSOK P-001 (Process Design)

Fonte: NORSOK P-001.

Requisitos para design de piping e equipamento de processo topside:
- Pressão e temperatura de design
- Isolamento de equipamento
- Line sizing
- Proteção contra sobrepressão
- Seleção de materiais

## 5. Sequência lógica de um FDP legível

Baseado na pesquisa, a sequência lógica de um FDP legível é:

1. **Sumário Executivo** — visão geral, metas, estratégia
2. **Ativo e Reservatório** — geologia, reservas, fluidos
3. **Processo** — PFDs, correntes, condições de operação, balanço de massa
4. **Facilidades** — EPFs, trunklines, FSB/CPF, utilidades
5. **Segurança** — SIL, elementos de segurança, HAZOP, LOPA
6. **Poços** — reativação, perfuração, elevação artificial
7. **Execução** — contratação, cronograma, logística
8. **Economia** — CAPEX, OPEX, NPV, IRR
9. **Riscos** — registro de riscos, gates de decisão
10. **Gestão** — governança, rastreamento, relatórios
