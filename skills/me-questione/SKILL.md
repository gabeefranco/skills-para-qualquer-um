---
name: me-questione
description: Entrevista implacável para lapidar um plano, decisão ou ideia. Use somente quando o usuário pedir explicitamente a skill me-questione.
license: MIT
disable-model-invocation: true
---

Entreviste o usuário de forma implacável até vocês chegarem a um entendimento comum. Mapeie o assunto como uma **árvore de decisões**: cada decisão se ramifica nas decisões que dependem dela.

Percorra a árvore em **rodadas**. A **fronteira** é o conjunto de todas as decisões cujos pré-requisitos já estão resolvidos: as perguntas que você pode fazer _agora_, sem adivinhar respostas que ainda não ouviu. Pergunte a fronteira inteira em uma única rodada: numere cada pergunta e dê a resposta que você recomenda. Depois, espere as respostas do usuário antes da próxima rodada.

Formate cada rodada assim:

```
❓ **P1** - **<título da pergunta>**: <corpo da pergunta, que pode ter vários parágrafos, inclusive alternativas>

➡️ <sua resposta recomendada>

---

❓ **P2** - **<título da pergunta>**: <corpo da pergunta, que pode ter vários parágrafos, inclusive alternativas>

➡️ <sua resposta recomendada>
```

Cada rodada respondida pelo usuário redesenha a árvore: as decisões resolvidas empurram a fronteira para fora e liberam as perguntas que dependiam delas. Recalcule a fronteira e faça a próxima rodada. Uma pergunta cuja resposta depende de outra ainda aberta nesta rodada pertence a uma rodada _posterior_, não a esta.

Descobrir _fatos_ é trabalho seu, nunca do usuário. Quando uma pergunta da fronteira precisar de um fato do ambiente, descubra-o com as ferramentas disponíveis (arquivos, busca na web, subagentes etc.); não pergunte ao usuário nada que você mesmo possa consultar. Se puder pesquisar em paralelo, não trave a rodada: uma pesquisa em andamento é um pré-requisito não resolvido, portanto só as perguntas que dependem dela esperam o resultado; faça agora as demais perguntas da fronteira. Se nenhuma ferramenta alcançar o fato, não invente: declare a suposição que está fazendo ou peça o material necessário. Já as _decisões_ são do usuário: apresente cada uma e espere a resposta.

A sessão termina quando a fronteira está vazia: todos os ramos da árvore de decisões visitados, nada presumido em silêncio. Não execute nada do que foi discutido até o usuário confirmar que vocês chegaram a um entendimento comum.
