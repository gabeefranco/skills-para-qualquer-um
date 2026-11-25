#!/usr/bin/env python3
"""Gera os prompts para copiar e colar e os ZIPs das skills.

Uso: python3 scripts/gerar.py prompts|zips
"""

import json
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
# O upload no claude.ai rejeita qualquer campo fora desta lista.
CAMPOS_PADRAO = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
PLUGIN = {
    "name": "skills-para-qualquer-um",
    "description": "Fluxos de trabalho avançados, simplificados para qualquer um conseguir usar.",
    "author": {"name": "Gabriel Franco"},
    "license": "MIT",
}


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


def metadado(frontmatter, nome):
    campo = re.search(rf"^metadata:\n(?:[ ]+.*\n)*?[ ]+{nome}: *(.+)$", frontmatter, re.MULTILINE)
    return campo[1].strip() if campo else None


def gerar_prompt(skill):
    frontmatter, corpo = separar(skill)
    entrada = metadado(frontmatter, "entrada") or "Minha ideia"
    partes = [corpo]
    # O prompt é colado em um chat sem skills, então leva junto as que ele usa.
    for nome in (metadado(frontmatter, "inclui") or "").split(","):
        if nome.strip():
            _, incluido = separar(skill.parent / nome.strip())
            partes.append(f"---\n\n# Instruções da skill {nome.strip()}\n\n{incluido}")
    if len(partes) > 1:
        partes.append("---")
    partes.append(f"{entrada}: [descreva aqui]")
    destino = RAIZ / "prompts" / f"{skill.name}.md"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text("\n\n".join(partes) + "\n", encoding="utf-8")
    return destino


def arquivos_da_skill(skill):
    """Lista (caminho relativo, conteúdo), com o frontmatter reduzido aos campos padrão."""
    frontmatter, corpo = separar(skill)
    skill_md = f"---\n{frontmatter_padrao(frontmatter)}---\n\n{corpo}\n"
    arquivos = []
    for arquivo in sorted(skill.rglob("*")):
        if not arquivo.is_file() or "__pycache__" in arquivo.parts:
            continue
        relativo = arquivo.relative_to(skill)
        conteudo = skill_md.encode() if relativo == Path("SKILL.md") else arquivo.read_bytes()
        arquivos.append((relativo.as_posix(), conteudo))
    return arquivos


def escrever_zip(nome, arquivos):
    destino = RAIZ / "dist" / f"{nome}.zip"
    destino.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as pacote:
        for caminho, conteudo in arquivos:
            info = zipfile.ZipInfo(caminho)
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            pacote.writestr(info, conteudo)
    return destino


def gerar_zip(skill):
    return escrever_zip(skill.name, [(f"{skill.name}/{c}", dados) for c, dados in arquivos_da_skill(skill)])


def gerar_zip_unico(skills):
    """Gera um plugin do Claude com todas as skills."""
    raiz = PLUGIN["name"]
    manifesto = json.dumps(PLUGIN, ensure_ascii=False, indent=2) + "\n"
    arquivos = [
        (f"{raiz}/.claude-plugin/plugin.json", manifesto.encode()),
        (f"{raiz}/LICENSE", (RAIZ / "LICENSE").read_bytes()),
    ]
    for skill in skills:
        arquivos += [(f"{raiz}/skills/{skill.name}/{c}", dados) for c, dados in arquivos_da_skill(skill)]
    return escrever_zip("todas-as-skills", arquivos)


def main():
    geradores = {"prompts": gerar_prompt, "zips": gerar_zip}
    if len(sys.argv) != 2 or sys.argv[1] not in geradores:
        sys.exit(__doc__)
    skills = [skill_md.parent for skill_md in sorted((RAIZ / "skills").glob("*/SKILL.md"))]
    destinos = [geradores[sys.argv[1]](skill) for skill in skills]
    if sys.argv[1] == "zips":
        destinos.append(gerar_zip_unico(skills))
    for destino in destinos:
        print(destino.relative_to(RAIZ))


if __name__ == "__main__":
    main()
