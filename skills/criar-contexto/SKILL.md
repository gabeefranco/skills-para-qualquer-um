---
name: criar-contexto
description: Cria um arquivo Markdown de contexto sobre um assunto, alternando medições do que o agente já sabe e perguntas ao usuário. Use somente quando o usuário pedir explicitamente a skill criar-contexto.
license: MIT
metadata:
  entrada: Assunto
  inclui: quanto-voce-sabe, me-questione
disable-model-invocation: true
---

Construa com o usuário um contexto rico sobre o assunto indicado, em um **loop**: meça o que você sabe, pergunte o que falta, espere as respostas e meça de novo, até a quantidade e a profundidade serem altas. No fim, entregue um arquivo Markdown que sirva de contexto para outra IA. Se o usuário não indicar o assunto, pergunte qual é e espere a resposta.

## 1. Prepare as duas skills

O loop usa as skills `quanto-voce-sabe`, para medir, e `me-questione`, para perguntar. Ao pedir a `criar-contexto`, o usuário também pediu essas duas.

- Se as instruções delas estiverem incluídas no fim deste texto, siga-as.
- Senão, chame cada uma como skill quando for usá-la. Elas podem aparecer com um prefixo de plugin. Nas rodadas seguintes, repita as instruções já carregadas; só chame de novo se elas não estiverem mais na conversa.
- Se alguma não estiver disponível, diga qual falta, indique que ela está em https://github.com/gabeefranco/skills-para-qualquer-um e pare. Não improvise uma versão.

Siga as duas skills, exceto onde este texto disser outra coisa.

## 2. Meça

Aplique a `quanto-voce-sabe` ao assunto, com estas diferenças:

- **O documento de fatos dura o loop inteiro.** Crie-o na primeira medição e, nas seguintes, acrescente e corrija o que as novas respostas trouxerem. Apague-o só depois da entrega. Refaça a conta e reavalie os cinco critérios a cada medição.
- **Se o usuário trouxer um `contexto-*.md` antigo,** use-o como fonte. Os itens de "Inferências" e "Em aberto" não voltam como fatos, mas ajudam a escolher perguntas.
- **A meta não muda a régua.** Não divida fatos, crie temas nem arredonde notas para chegar a 7: um contexto inflado parece pronto e deixa a próxima IA na mão.

Mostre o relatório completo somente na primeira e na última medição, sem a seção "O que ajudaria", porque as perguntas já ocupam esse lugar. Nas demais, mostre só o placar, com a nota anterior e a nova:

```
**Quantidade:** 4/10 → 6/10 · **Profundidade:** 3/10 → 5/10
```

Se a quantidade foi contada à mão, escreva `(estimada)` depois dela. O aviso da `quanto-voce-sabe` sobre isso aparece só nos relatórios.

Em seguida, confira a seção 4. Se nada ali encerrar o loop, pergunte.

## 3. Pergunte

Aplique a `me-questione` partindo das lacunas da medição, com estas diferenças:

- **A árvore é de conhecimento.** Mapeie o que é preciso saber para ajudar com o assunto: cada resposta abre as perguntas que dependem dela. Priorize a nota mais baixa e, se uma resposta revelar um ramo mais importante, passe-o à frente.
- **De 3 a 5 perguntas por rodada,** ou menos se não restarem tantas na fila. Não repita o que já foi respondido.
- **O `➡️` não é uma recomendação.** Se o contexto já sustentar uma resposta, escreva `➡️ Palpite: ...`. Senão, escreva `➡️ Exemplo: ...`, ilustrando com algo claramente fictício o tipo e o nível de detalhe que ajudam. Exemplos nunca viram fatos, e palpites só viram fatos se o usuário os confirmar.
- **A internet serve apenas para formular perguntas melhores.** O que vier dela não é fato sobre o usuário e não entra no documento. Não coloque dados pessoais nas buscas. Continue sem consultar conectores por conta própria.
- **"Não sei" e "prefiro não responder"** tiram a pergunta da fila, sem repetição. Tire também as perguntas cuja resposta claramente depende daquela: quem não sabe o faturamento não sabe a margem de lucro, mas pode saber o preço. Se depois o usuário trouxer a informação por conta própria, use-a.
- **O fim da entrevista segue a seção 4,** sem pedir confirmação de entendimento comum.

Termine a mensagem nas perguntas e espere as respostas. Nunca responda pelo usuário. Quando ele responder, volte à seção 2.

## 4. Saiba quando parar

Encerre o loop quando ocorrer qualquer um destes casos:

- **As duas notas chegaram a 7/10 ou mais.** Encerre direto, sem oferecer mais perguntas.
- **O usuário pediu para parar,** com "chega" ou algo equivalente. Aproveite o que ele tiver respondido na mesma mensagem.
- **A fila de perguntas acabou.**

Se passarem duas rodadas seguidas sem que nenhuma nota suba, avise e pergunte se ele quer parar, em vez de fazer uma nova rodada. Se ele quiser continuar, recomece essa contagem.

Para encerrar, faça uma última medição se houver respostas ainda não medidas e mostre o relatório completo, a menos que ele já esteja nesta mesma mensagem. Se alguma nota estiver abaixo de 7, diga em uma frase por que o loop parou antes. Entregue o arquivo na mesma mensagem, seja qual for a nota.

## 5. Entregue o arquivo

Quem vai ler o arquivo é uma IA que não viu esta conversa, então ele precisa se explicar sozinho. Use este formato:

```markdown
# Contexto: <assunto>

> Atualizado em <AAAA-MM-DD>. Quantidade: <n>/10. Profundidade: <n>/10.

## Resumo
<3 a 5 frases: o que é, para que serve, situação atual e o que mais importa>

## <tema>
<fatos do tema, ligados aos seus motivos e relações>

## Inferências
- <inferência> (a partir de: <fatos de origem>)

## Em aberto
- <lacuna ou conflito sem solução>
```

- Inclua **todos** os fatos da última medição, sem as marcas `[fonte: ...]`. Pode juntá-los em frases, mas não acrescente nada além deles.
- Chame o usuário pelo nome ou por "o usuário", nunca por "você" ou "eu". Troque referências à conversa e datas relativas, como "mês que vem", por informações completas.
- Dos conflitos resolvidos, registre só a versão que vale.
- "Em aberto" evita que a próxima IA invente. Escreva a lacuna de forma neutra, sem dizer que o usuário preferiu não responder.
- Omita as seções "Inferências" e "Em aberto" se estiverem vazias.
- **Nunca inclua senhas, tokens ou números de documentos, contas e cartões,** nem no documento de fatos.

Se não souber a data de hoje, omita `Atualizado em ...`

Salve como `contexto-<assunto>.md`, em minúsculas, sem acentos e com hifens: `contexto-padaria-trigo-lento.md`. No navegador, ofereça o arquivo para baixar; em um agente de código, salve na pasta atual. Se o nome já existir, só sobrescreva se o usuário tiver pedido para atualizar aquele arquivo; senão, acrescente `-2`, `-3` etc. e ofereça substituir o antigo. Se não puder criar arquivos, entregue o conteúdo em um único bloco de código Markdown, cercado por quatro crases.

Se o arquivo tiver dados de saúde, finanças pessoais ou dados privados de outras pessoas, acrescente à mensagem:

> ⚠️ Este arquivo contém <tipos de dados>. Revise antes de compartilhar.

Não explique como adicionar o arquivo a um projeto.
