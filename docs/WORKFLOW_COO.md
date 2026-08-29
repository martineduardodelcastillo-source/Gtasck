# Fluxo de Trabalho do COO — Gtasck

> Como construir operações do zero, rastrear decisões e reportar diariamente.

## Ciclo Diário

```
Manhã:  Alimentar produção → balanço de massa → checar fechamento (±2%)
Tarde:  Registrar decisões → cada decisão vira um registro D### auditável
Noite:  Gerar relatório diário → produção + decisões + riscos críticos
```

## Comandos naturais (via Manus)

| Intenção | Exemplo de comando |
|---|---|
| Construir do zero | "Monte a EPF Fase 1 do zero: PFD, P&ID, HAZOP, AFE dos 5 poços" |
| Registrar decisão | "Registre: aprovei o AFE do PO-01, rationale VPL positivo" |
| Reportar o dia | "Gere o relatório diário de hoje com a produção que te passei" |
| Auditar decisões | "Liste todas as decisões de agosto com impacto de CAPEX" |

## Rastreabilidade

- Cada decisão recebe um **ID sequencial** (D001, D002…) com timestamp UTC
- O log é **append-only** (`decisions.jsonl`) — nada é apagado, tudo é auditável
- O relatório diário cruza **produção + decisões + riscos** em um único documento

## Memória permanente

1. **Conhecimento do Manus** — suas regras de engenharia gravadas no perfil
2. **`config/project_config.yaml`** — fonte da verdade versionada no GitHub
3. **`decisions.jsonl`** — histórico completo de decisões no repo

Para retomar em qualquer sessão: **"Continua o Gtasck"**.
