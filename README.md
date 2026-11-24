# Skills pra qualquer um

Skills de IA em português do Brasil, para agentes de código e para o Claude e o ChatGPT no navegador.

## Skills

| Skill | O que faz |
| --- | --- |
| [`me-questione`](skills/me-questione/SKILL.md) | Entrevista você, rodada por rodada, até seu plano, decisão ou ideia ficar bem definido. Só roda quando você chama. |

## Como usar

### Qualquer chat, sem instalar nada

Abra [`prompts/me-questione.md`](prompts/me-questione.md), copie o conteúdo, cole no chat e troque `[descreva aqui]` pela sua ideia. Serve para ChatGPT, Claude, Gemini e outros, em qualquer plano.

### Claude no navegador

1. Baixe o `me-questione.zip` da página **Releases** deste repositório. Não descompacte.
2. Em **Settings > Capabilities**, ative a execução de código e criação de arquivos.
3. Em **Customize > Skills**, clique em **+**, depois em **Create skill** e **Upload a skill**, e envie o ZIP.
4. No chat, escreva: `use a skill me-questione para avaliar esta ideia: ...`

### ChatGPT no navegador

O envio de skills depende do seu plano e do seu workspace. Se **Skills > Create > Upload from your computer** aparecer para você, envie o `me-questione.zip` e chame a skill digitando `@` no chat. Se não aparecer, use o [prompt](prompts/me-questione.md).

### Agentes de código

Copie a pasta `skills/me-questione` para o diretório de skills do seu agente:

| Agente | Diretório pessoal | Como chamar |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `/me-questione` |
| Codex | `~/.agents/skills/` | `$me-questione` |

Outros agentes compatíveis com [Agent Skills](https://agentskills.io) costumam ler `.agents/skills/` no projeto; confira a documentação do seu. Se o agente não aceitar skills, use o prompt.

## Manutenção

Edite somente `skills/<nome>/SKILL.md`; os prompts são gerados a partir dele. A cada push na `main` que altere uma skill, uma GitHub Action atualiza `prompts/`.

Para gerar tudo localmente (Python 3, sem dependências):

```bash
python3 scripts/gerar.py prompts
python3 scripts/gerar.py zips     # salva em dist/
```

O ZIP leva só os campos de frontmatter que o Claude web aceita; por isso, não inclui o `disable-model-invocation`, usado no Claude Code.

Para publicar uma versão com os ZIPs em Releases:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Créditos e licença

`me-questione` é uma tradução e adaptação de `grill-me` e `grilling`, do repositório [mattpocock/skills](https://github.com/mattpocock/skills), de Matt Pocock. As duas foram unidas em uma só. Licença [MIT](LICENSE).
