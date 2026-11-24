#!/usr/bin/env python3
"""Gera os prompts para copiar e colar e os ZIPs das skills.

Uso: python3 scripts/gerar.py prompts|zips
"""

import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
# O upload no claude.ai rejeita qualquer campo fora desta lista.
CAMPOS_PADRAO = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def separar(skill):
    texto = (skill / "SKILL.md").read_text(encoding="utf-8")
    _, frontmatter, corpo = texto.split("---\n", 2)
    return frontmatter, corpo.strip()


def frontmatter_padrao(frontmatter):
    linhas = []
    manter = True
    for linha in frontmatter.splitlines():
        # Linhas indentadas continuam o campo anterior.
        if linha and not linha[0].isspace():
            manter = linha.split(":", 1)[0] in CAMPOS_PADRAO
        if manter:
            linhas.append(linha)
    return "\n".join(linhas) + "\n"


def gerar_prompt(skill):
    _, corpo = separar(skill)
    destino = RAIZ / "prompts" / f"{skill.name}.md"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(f"{corpo}\n\nMinha ideia: [descreva aqui]\n", encoding="utf-8")
    return destino


def gerar_zip(skill):
    frontmatter, corpo = separar(skill)
    skill_md = f"---\n{frontmatter_padrao(frontmatter)}---\n\n{corpo}\n"
    destino = RAIZ / "dist" / f"{skill.name}.zip"
    destino.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as pacote:
        for arquivo in sorted(skill.rglob("*")):
            if not arquivo.is_file():
                continue
            relativo = arquivo.relative_to(skill)
            conteudo = skill_md.encode() if relativo == Path("SKILL.md") else arquivo.read_bytes()
            info = zipfile.ZipInfo(f"{skill.name}/{relativo.as_posix()}")
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            pacote.writestr(info, conteudo)
    return destino


def main():
    geradores = {"prompts": gerar_prompt, "zips": gerar_zip}
    if len(sys.argv) != 2 or sys.argv[1] not in geradores:
        sys.exit(__doc__)
    for skill_md in sorted((RAIZ / "skills").glob("*/SKILL.md")):
        destino = geradores[sys.argv[1]](skill_md.parent)
        print(destino.relative_to(RAIZ))


if __name__ == "__main__":
    main()
