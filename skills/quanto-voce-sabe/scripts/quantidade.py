#!/usr/bin/env python3
"""Calcula a nota de quantidade (0 a 10) de um documento de memória.

Uso: python3 quantidade.py <documento.md>   (use - para ler da entrada padrão)
"""

import re
import sys
from pathlib import Path

# Cada número é o mínimo necessário para ganhar mais um ponto.
LIMITES_FATOS = (1, 3, 6, 11, 21, 36, 56)
LIMITES_TEMAS = (2, 5)
LIMITES_PALAVRAS = (300,)

FONTE = re.compile(r"\s*\[fonte:\s*[^\]\s][^\]]*\][\s.]*$", re.IGNORECASE)


def pontos(valor, limites):
    return sum(valor >= limite for limite in limites)


def nivel(nota):
    if nota <= 3:
        return "baixa"
    return "média" if nota <= 6 else "alta"


def ler_itens(texto):
    """Devolve (tema, item) para cada item de lista da seção Fatos."""
    itens = []
    em_fatos = False
    tema = None
    for linha in texto.splitlines():
        titulo = re.match(r"(#{1,6})\s+(.+?)\s*#*\s*$", linha)
        if titulo:
            if len(titulo[1]) <= 2:
                em_fatos = len(titulo[1]) == 2 and titulo[2].casefold() == "fatos"
                tema = None
            elif len(titulo[1]) == 3:
                tema = titulo[2].casefold()
            continue
        if not em_fatos:
            continue
        item = re.match(r"\s*(?:[-*+]|\d+[.)])\s+(.+)", linha)
        if item:
            itens.append([tema, item[1].strip()])
        elif itens and linha[:1].isspace() and linha.strip():
            # Linha indentada continua o item anterior.
            itens[-1][1] += " " + linha.strip()
    return itens


def medir(texto):
    vistos = set()
    por_tema = {}
    palavras = sem_fonte = sem_tema = repetidos = 0
    for tema, item in ler_itens(texto):
        if not FONTE.search(item):
            sem_fonte += 1
            continue
        termos = re.findall(r"\w+(?:[-'’.,]\w+)*", FONTE.sub("", item).casefold())
        chave = " ".join(termos)
        if not chave:
            continue
        if chave in vistos:
            repetidos += 1
            continue
        vistos.add(chave)
        palavras += len(termos)
        if tema is None:
            sem_tema += 1
        else:
            por_tema[tema] = por_tema.get(tema, 0) + 1
    fatos = len(vistos)
    temas = sum(total >= 2 for total in por_tema.values())
    nota = pontos(fatos, LIMITES_FATOS) + pontos(temas, LIMITES_TEMAS) + pontos(palavras, LIMITES_PALAVRAS)
    return {
        "nota": nota,
        "nivel": nivel(nota),
        "fatos": fatos,
        "temas": temas,
        "palavras": palavras,
        "repetidos": repetidos,
        "sem_fonte": sem_fonte,
        "sem_tema": sem_tema,
    }


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if sys.argv[1] == "-":
        texto = sys.stdin.buffer.read().decode("utf-8-sig")
    else:
        texto = Path(sys.argv[1]).read_text(encoding="utf-8-sig")
    sys.stdout.reconfigure(encoding="utf-8")
    if not re.search(r"^##\s+fatos\s*#*\s*$", texto, re.IGNORECASE | re.MULTILINE):
        sys.exit("Erro: o documento precisa de uma seção '## Fatos'.")
    m = medir(texto)
    print(f"Quantidade: {m['nivel']} ({m['nota']}/10)")
    print(f"Fatos únicos: {m['fatos']}")
    print(f"Temas com 2 ou mais fatos: {m['temas']}")
    print(f"Palavras nos fatos: {m['palavras']}")
    if m["repetidos"]:
        print(f"Repetidos ignorados: {m['repetidos']}")
    if m["sem_fonte"]:
        print(f"Aviso: {m['sem_fonte']} item(ns) sem [fonte: ...] não contaram.")
    if m["sem_tema"]:
        print(f"Aviso: {m['sem_tema']} fato(s) fora de um tema (###).")


if __name__ == "__main__":
    main()
