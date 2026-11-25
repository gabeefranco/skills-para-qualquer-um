# Testes da skill criar-contexto

## Automáticos

```bash
python3 -B tests/criar-contexto/test_criar_contexto.py
```

[`test_criar_contexto.py`](test_criar_contexto.py) cobre as skills incluídas no prompt, as permissões para a `criar-contexto` chamar as outras duas, o próprio acionamento explícito e os documentos e arquivos entregues nas simulações. A montagem do prompt é testada em [`test_gerar.py`](../test_gerar.py).

## Simulações

| Cenário | O que exercita | Quantidade | Profundidade |
| --- | --- | --- | --- |
| [`ate-alta`](simulacoes/ate-alta/README.md) | Começo sem contexto, "não sei", senha na resposta e encerramento direto | 1 → 6 → 9 | 1 → 6 → 9 |
| [`contexto-antigo-e-chega`](simulacoes/contexto-antigo-e-chega/README.md) | Contexto antigo como fonte, fato desatualizado, recusa e "chega" | 4 → 4 | 3 → 3 |

Os contextos são fictícios. As simulações foram feitas em 2026-11-25 com o Claude Code (`claude -p`), em sessões separadas daquela em que a skill foi escrita, com as três skills instaladas em `.claude/skills/` e as respostas do usuário escritas por quem criou a skill. Cada cenário rodou uma vez.

Também foram conferidos, em um turno cada:

- **Só a `criar-contexto` instalada:** disse quais skills faltavam e parou.
- **Prompt colado, sem skills nem criação de arquivos:** mediu à mão, com o aviso, e fez as perguntas.

Depois das simulações, o formato da data e a regra para sobrescrever arquivos foram ajustados; por isso, a data de `ate-alta` está no formato antigo.

Não foram simulados: duas rodadas sem subir nota, fila de perguntas vazia, Claude no navegador, ChatGPT e Codex.
