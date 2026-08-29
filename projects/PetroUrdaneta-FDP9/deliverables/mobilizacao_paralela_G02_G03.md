# Mobilização Paralela · Gates G-02 + G-03 (Onda 1)

> **Recomendação aprovada pelo COO:** mobilizar G-02 (PVT) e G-03 (FSB brownfield) **em paralelo**.
> Data de emissão: 29/ago/2026 · Gtasck

---

## 1. Lógica da paralelização

Os dois gates são **independentes entre si** e ambos estão no topo do caminho crítico da Onda 1. Rodá-los em paralelo **corta o prazo total da Onda 1 pela metade** (de ~20 semanas sequenciais para ~10–12 semanas paralelas).

```
        Semana:  1   2   3   4   5   6   7   8   9  10  11  12
G-02 PVT        [==amostragem==][===lab===][relatório]
G-03 FSB        [survey][integridade][capacidade][relief][relatório]
                 └────────────── AMBOS FECHAM ~semana 10-12 ──────────────┘
```

## 2. Cronograma integrado

| Semana | G-02 (PVT) | G-03 (FSB brownfield) |
|---|---|---|
| 1 | Plano de amostragem + seleção de poços | Survey dimensional + dados históricos |
| 2–3 | Mobilização de amostragem pressurizada | Inspeção de integridade (NDT, API 510/570) |
| 3–5 | Coleta (5 clusters + FSB) | Teste de capacidade + separação dinâmica |
| 5–8 | Análise laboratorial completa | Avaliação de relief + causa-efeito |
| 9–10 | Relatório PVT + reconciliação | Relatório brownfield + decisão |
| **10–12** | **G-02 FECHADO** | **G-03 FECHADO** |

## 3. Recursos e custo consolidado

| Recurso | G-02 | G-03 | Total |
|---|---:|---:|---:|
| Custo | US$ 400k | US$ 600k | **US$ 1,0 MM** |
| Equipe principal | Reservatórios + Lab | Integridade + Processo | — |
| Equipe de apoio | Operações | Process Safety + Engenharia | — |
| Prazo | 6–10 sem | 8–12 sem | **~10–12 sem (paralelo)** |

## 4. Governança da mobilização

| Item | Definição |
|---|---|
| **Sponsor** | COO |
| **Coordenação** | Engenharia (single point of accountability) |
| **Reunião de status** | Semanal (15 min) — G-02 + G-03 juntos |
| **Rastreamento** | Change log do Gtasck (cada marco vira CH-###) |
| **Critério de fechamento** | Relatório aprovado pelo owner + alimenta gates a jusante |

## 5. Riscos da paralelização e mitigação

| Risco | Mitigação |
|---|---|
| Competição por recursos de campo | Equipes distintas (Reservatórios vs. Integridade) |
| Atraso de laboratório (G-02) | Contratar lab com SLA; amostras em lotes |
| Acesso ao FSB em operação (G-03) | Janelas de inspeção sem parada; tie-in windows |
| Escopo creep | Change control via Gtasck (cada mudança = CH-###) |

## 6. O que acontece ao fechar G-02 + G-03

Com os dois gates fechados (~semana 10–12), o projeto destrava **simultaneamente**:

- **G-04** (rede multiphase) — precisa do PVT (G-02)
- **G-06** (ESD/relief) — precisa do brownfield (G-03)
- **G-08** (água) — precisa do PVT (G-02)
- **G-09** (Boscan) — precisa do PVT (G-02)
- **G-12** (crude/export) — precisa do brownfield (G-03)
- **AFE de upgrade do FSB** — precisa do brownfield (G-03)

> **Resultado:** fechar G-02 + G-03 em paralelo destrava **6 frentes** e o AFE do FSB — é a jogada de maior alavanca de toda a Onda 1.

## 7. Próximo passo imediato

1. **Aprovar** este plano de mobilização (COO).
2. **Emitir ordem de serviço** para as duas equipes (via MSA well services/EPF e EPCM).
3. **Registrar** o início no change log do Gtasck.
