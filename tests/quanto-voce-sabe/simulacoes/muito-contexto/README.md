# Simulação: muito-contexto

## Contexto

O usuário é Lia, dona da padaria fictícia Trigo Lento. Os fatos com fonte `memoria.md` vêm de um arquivo de memória; os demais, da conversa. O arquivo traz o preço antigo do plano básico (50 reais), e a conversa traz o novo (60 reais).

Pedido: `quanto-voce-sabe sobre a minha padaria, a Trigo Lento`

## Esperado

- Quantidade alta, calculada pelo script.
- Profundidade alta.
- O preço novo está em Fatos, e o conflito não conta.
- Resumo com no máximo 3 frases e de 3 a 5 perguntas.

## Obtido

Documento: [`documento.md`](documento.md)

````markdown
## O que eu sei sobre a Trigo Lento

**Quantidade:** alta (7/10)
**Profundidade:** alta (9/10)

### Qualidade da memória
Tenho bastante informação, e ela explica como o negócio funciona e por quê. O ponto forte é a decisão sobre entregas, com custos, limites e motivo. A principal lacuna é a visão de longo prazo e os números do negócio.

### O que eu sei
A Trigo Lento é uma padaria artesanal por assinatura, de Lia, com 140 assinantes e capacidade de 80 pães por dia. Houve cancelamentos por atraso, e as entregas dependem só de Caio. Lia decide entre outro entregador, acima do orçamento, e um ponto de retirada gratuito.

### O que ajudaria
1. Quais são a receita e os custos mensais?
2. Quantos assinantes aceitariam retirar o pão no café vizinho?
3. O que você quer da padaria daqui a dois anos?

_Fontes: conversa e memoria.md._
````

### Notas por critério (não mostradas ao usuário)

Essência 2, Contexto 2, Motivos 2, Relações 2, Aplicação 1 (faltam dados para comparar o efeito das opções).
