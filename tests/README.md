# Testes

Para rodar tudo (Python 3, sem dependências):

```bash
sh tests/rodar.sh
```

Os testes do repositório ficam na raiz desta pasta; os de cada skill, em `tests/<nome-da-skill>/`. Todos ficam fora de `skills/` para não entrar nos ZIPs.

| Teste | O que cobre |
| --- | --- |
| [`test_gerar.py`](test_gerar.py) | ZIPs individuais, ZIP único e prompts gerados por `scripts/gerar.py`. |
| [`quanto-voce-sabe/`](quanto-voce-sabe/README.md) | Fórmula da quantidade e simulações da skill `quanto-voce-sabe`. |
