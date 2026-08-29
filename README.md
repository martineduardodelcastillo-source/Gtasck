# Gtasck — Copiloto de Engenharia de Óleo & Gás

> Plataforma de apoio ao COO: geração de P&IDs, análise de risco, cálculos de engenharia e documentação técnica — tudo padronizado e auditável.

## Visão Geral

O **Gtasck** é um conjunto de módulos de engenharia operados pelo Manus (agente de IA) que automatiza os entregáveis técnicos mais consumidos pela operação de O&G:

| Módulo | Função | Normas-base |
|--------|--------|-------------|
| **P&ID Generator** | Gera diagramas P&ID/PFD em SVG/PDF com simbologia ISA-5.1, tagueamento automático, lista de linhas e equipamentos | ISA-5.1, ISO 10628 |
| **Risk Analysis** | Matrizes de risco 5×5, planilhas HAZOP/HAZID, bow-tie, relatórios formatados | API 580/581, IEC 61882, CCPS |
| **Engineering Calcs** | Memoriais de cálculo: vasos de pressão, tubulações, tanques, PSVs | ASME VIII, B31.3/B31.8, API 650/520/521 |
| **COO Dashboard** | KPIs de produção, integridade de ativos, backlog de inspeção, alertas | — |
| **Doc Factory** | Relatórios de integridade, planos de inspeção, memoriais em PDF/DOCX no timbrado da empresa | — |

## Preferências de Engenharia (Configuração Permanente)

Estas diretrizes estão gravadas na configuração do projeto e aplicadas a **todos** os entregáveis:

1. **Flex pipe first** — Priorizar flex pipe em layouts de tubulação e facilidades sempre que possível.
2. **PFDs de alta fidelidade** — PFDs devem ser detalhados e representar fielmente o processo, incluindo: flexpipe pigável, fabricação de spools, válvulas, sidetracks, vasos, e considerações de manutenção/segurança para EPF upstream e downstream.
3. **Conformidade normativa** — Sempre garantir conformidade com normas **API, NORSOK, COVENIN e venezuelanas**.

## Estrutura do Repositório

```
Gtasck/
├── config/                 # Configurações do projeto (normas, unidades, tagueamento)
├── standards/              # Referências normativas organizadas por família
│   ├── api/  ├── asme/  ├── norsok/  ├── covenin/  └── isa/
├── modules/
│   ├── pid_generator/      # Gerador de P&ID/PFD (símbolos, templates, exemplos)
│   ├── risk_analysis/      # Análise de risco (HAZOP, matrizes, bow-tie)
│   ├── eng_calcs/          # Cálculos (ASME VIII, B31.3, API 650, API 520)
│   ├── coo_dashboard/      # KPIs e visão executiva
│   └── doc_factory/        # Geração de documentos no timbrado
├── assets/symbol_library/  # Biblioteca de símbolos ISA-5.1 em SVG
└── docs/                   # Documentação de uso e fluxos de trabalho
```

## Como Usar (via Manus)

Exemplos de comandos naturais que ativam estes módulos:

- *"Gere um P&ID para um separador trifásico com 2 poços de entrada, seguindo ISA-5.1"*
- *"Monte uma planilha HAZOP para o nó 'linha de descarga do separador', guia-word por guia-word"*
- *"Calcule a espessura mínima de um vaso 48\" × 10 ft, P=250 psig, T=200°F, SA-516 Gr.70"*
- *"Gere a matriz de risco 5×5 da unidade X com os 12 cenários que te passei"*
- *"Emita o relatório mensal de integridade no timbrado da empresa"*

## Status dos Módulos

| Módulo | Status |
|--------|--------|
| P&ID Generator | ✅ Núcleo funcional (símbolos ISA-5.1 + gerador SVG) |
| Risk Analysis | ✅ Matriz 5×5 + planilha HAZOP |
| Engineering Calcs | ✅ ASME VIII (espessura de vasos) + B31.3 (tubulação) |
| COO Dashboard | 🚧 Estrutura criada — aguardando fontes de dados |
| Doc Factory | 🚧 Estrutura criada — aguardando timbrado da empresa |

## Próximos Passos

1. Upload de P&IDs reais para calibrar simbologia e tagueamento da empresa
2. Definir fontes de dados (PI System, SAP, Excel) para o dashboard
3. Adicionar timbrado/logotipo para o Doc Factory
