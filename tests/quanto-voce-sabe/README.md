# Testes da skill quanto-voce-sabe

## Automáticos

```bash
python3 -B tests/quanto-voce-sabe/test_quantidade.py
```

[`test_quantidade.py`](test_quantidade.py) cobre documento vazio, limites de cada faixa, nota máxima, níveis, repetidos, itens sem fonte, inferências e conflitos ignorados, contagem de palavras, linha de comando e a nota de quantidade dos documentos das simulações.

## Simulações

| Cenário | Quantidade | Profundidade |
| --- | --- | --- |
| [`muito-contexto`](simulacoes/muito-contexto/README.md) | alta (7/10) | alta (9/10) |
| [`pouco-contexto`](simulacoes/pouco-contexto/README.md) | baixa (2/10) | baixa (2/10) |
| [`sem-contexto`](simulacoes/sem-contexto/README.md) | baixa (0/10) | baixa (0/10) |

Os contextos são fictícios. As simulações foram feitas em 2026-11-24 com o Claude Opus 5.5, no papel de agente e na mesma sessão em que a skill foi escrita. São uma checagem do fluxo, não uma avaliação independente: não comprovam o comportamento em outros modelos nem o acionamento da skill. Para avaliar outro modelo, repita o pedido de cada cenário com a skill instalada e compare com o esperado.

As faixas da quantidade são uma escolha inicial, ainda não calibrada com uso real.
