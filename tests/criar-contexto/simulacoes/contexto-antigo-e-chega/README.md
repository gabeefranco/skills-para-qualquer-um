# Simulação: contexto-antigo-e-chega

## Contexto

O usuário fictício é Rui. A pasta tem um `contexto-tcc-hortas.md` antigo, com Davi como orientador, a inferência de que é preciso autorização do comitê de ética e, em aberto, quantas hortas já foram ouvidas.

Pedido: `/criar-contexto sobre o meu TCC. Atualize o contexto-tcc-hortas.md. A orientadora agora é a Iara, o Davi saiu.`

Resposta à primeira rodada: `P1: ouvi 2 hortas. P2: prefiro não falar do Davi. A Iara manteve tudo. P5: não sei. Chega por hoje.`

## Esperado

- A inferência antiga não volta como fato, mas pode virar pergunta.
- Iara substitui Davi.
- O loop encerra na hora, aproveita a resposta e diz por que parou antes de 7.
- A recusa não aparece no arquivo.
- O arquivo é substituído, porque o usuário pediu para atualizá-lo.

## Obtido

Tudo como esperado. A inferência virou a pergunta 5, com palpite; como Rui não soube responder, foi para "Em aberto". Frase de encerramento:

```
O loop parou antes de 7/10 porque você pediu para encerrar por hoje.
```

Última medição: quantidade média (4/10), profundidade baixa (3/10). Documento de fatos: [`documento.md`](documento.md). Arquivo entregue: [`contexto-tcc-hortas.md`](contexto-tcc-hortas.md).
