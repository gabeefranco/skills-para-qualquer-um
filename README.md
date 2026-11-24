# Skills para qualquer um

Skills de IA em português do Brasil, para agentes de código e para o Claude e o ChatGPT no navegador.

## Skills

| Skill | O que faz |
| --- | --- |
| [`me-questione`](skills/me-questione/SKILL.md) | Entrevista você, rodada por rodada, até seu plano, decisão ou ideia ficar bem definido. Só roda quando você chama. |
| [`quanto-voce-sabe`](skills/quanto-voce-sabe/SKILL.md) | Mede, de 0 a 10, a quantidade e a profundidade do que a IA sabe sobre um assunto seu e sugere o que informar. Só roda quando você chama. |

## Como usar

### Qualquer chat, sem instalar nada

Abra o prompt da skill em [`prompts/`](prompts), copie o conteúdo, cole no chat e troque `[descreva aqui]` pela sua ideia ou assunto. Serve para ChatGPT, Claude, Gemini e outros, em qualquer plano.

### Todas as skills de uma vez

O `todas-as-skills.zip`, na página **Releases**, reúne todas as skills em um plugin do Claude:

- **Claude no navegador (planos pagos):** em **Customize > Plugins**, clique em **Add**, depois em **Upload plugin**, e envie o ZIP sem descompactar. Ative também a execução de código.
- **Claude Code:** `claude --plugin-dir todas-as-skills.zip` carrega o plugin só naquela sessão. As skills são chamadas com o prefixo do plugin: `/skills-para-qualquer-um:me-questione`.
- **Outros agentes:** descompacte e copie as pastas que estão em `skills/` para o diretório de skills do agente.

A importação desse ZIP no ChatGPT não foi confirmada. Lá, e no Claude gratuito, use os ZIPs individuais ou os prompts.

### Claude no navegador

1. Baixe o ZIP da skill, como `me-questione.zip`, da página **Releases** deste repositório. Não descompacte.
2. Em **Settings > Capabilities**, ative a execução de código e criação de arquivos.
3. Em **Customize > Skills**, clique em **+**, depois em **Create skill** e **Upload a skill**, e envie o ZIP.
4. No chat, escreva: `use a skill me-questione para avaliar esta ideia: ...` ou `use a skill quanto-voce-sabe sobre ...`

### ChatGPT no navegador

O envio de skills depende do seu plano e do seu workspace. Se **Skills > Create > Upload from your computer** aparecer para você, envie o ZIP da skill e chame a skill digitando `@` no chat. Se não aparecer, use o [prompt](prompts).

### Agentes de código

Copie a pasta da skill, como `skills/me-questione`, para o diretório de skills do seu agente:

| Agente | Diretório pessoal | Como chamar |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `/me-questione`, `/quanto-voce-sabe` |
| Codex | `~/.agents/skills/` | `$me-questione`, `$quanto-voce-sabe` |

Outros agentes compatíveis com [Agent Skills](https://agentskills.io) costumam ler `.agents/skills/` no projeto; confira a documentação do seu. Se o agente não aceitar skills, use o prompt.

## Manutenção

Edite somente `skills/<nome>/SKILL.md`; os prompts são gerados a partir dele. A cada push na `main` que altere uma skill, uma GitHub Action atualiza `prompts/`.

O prompt termina com `Minha ideia: [descreva aqui]`. Para trocar o rótulo, defina `entrada` em `metadata`, no frontmatter da skill.

Para gerar tudo localmente (Python 3, sem dependências):

```bash
python3 scripts/gerar.py prompts
python3 scripts/gerar.py zips     # salva em dist/: um ZIP por skill e o todas-as-skills.zip
```

Os ZIPs levam só os campos de frontmatter que o Claude web aceita; por isso, não incluem o `disable-model-invocation`, usado no Claude Code.

Os testes ficam em [`tests/`](tests/README.md) e rodam a cada push e pull request. A release só é publicada se passarem.

Para publicar uma versão com os ZIPs em Releases:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Créditos e licença

`me-questione` é uma tradução e adaptação de `grill-me` e `grilling`, do repositório [mattpocock/skills](https://github.com/mattpocock/skills), de Matt Pocock. As duas foram unidas em uma só. `quanto-voce-sabe` é original. Licença [MIT](LICENSE).
