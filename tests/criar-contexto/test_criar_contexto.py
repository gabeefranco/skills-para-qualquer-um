import re
import sys
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "skills" / "quanto-voce-sabe" / "scripts"))
import gerar
import quantidade

SKILL = RAIZ / "skills" / "criar-contexto"
USADAS = ("quanto-voce-sabe", "me-questione")


class TestCriarContexto(unittest.TestCase):
    def test_inclui_as_duas_skills(self):
        frontmatter, corpo = gerar.separar(SKILL)
        self.assertEqual(gerar.metadado(frontmatter, "inclui"), ", ".join(USADAS))
        for nome in USADAS:
            self.assertIn(f"`{nome}`", corpo)

    def test_skills_usadas_podem_ser_chamadas(self):
        for nome in USADAS:
            frontmatter, _ = gerar.separar(RAIZ / "skills" / nome)
            self.assertNotIn("disable-model-invocation", frontmatter, nome)
            self.assertIn("ou quando a skill criar-contexto a chamar", frontmatter, nome)
            codex = (RAIZ / "skills" / nome / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn("allow_implicit_invocation: true", codex, nome)

    def test_so_roda_quando_chamada(self):
        frontmatter, _ = gerar.separar(SKILL)
        self.assertIn("disable-model-invocation: true", frontmatter)
        codex = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", codex)

    def test_simulacoes(self):
        for pasta, nota in (("ate-alta", 9), ("contexto-antigo-e-chega", 4)):
            simulacao = AQUI / "simulacoes" / pasta
            documento = (simulacao / "documento.md").read_text(encoding="utf-8")
            self.assertEqual(quantidade.medir(documento)["nota"], nota, pasta)
            [arquivo] = simulacao.glob("contexto-*.md")
            contexto = arquivo.read_text(encoding="utf-8")
            self.assertRegex(contexto, r"\A# Contexto: .+\n\n> Atualizado em .+ Quantidade: \d+/10\. Profundidade: \d+/10\.\n")
            self.assertIn(f"Quantidade: {nota}/10.", contexto)
            self.assertIn("\n## Resumo\n", contexto)
            self.assertNotIn("[fonte:", contexto)
            # Todo número dos fatos precisa ter chegado ao contexto.
            for _, fato in quantidade.ler_itens(documento):
                for numero in re.findall(r"\d[\d.]*\d|\d", quantidade.FONTE.sub("", fato)):
                    self.assertIn(numero, contexto, fato)

    def test_dados_que_nao_podem_vazar(self):
        for arquivo in (AQUI / "simulacoes" / "ate-alta").glob("*.md"):
            if arquivo.name != "README.md":
                self.assertNotIn("4471", arquivo.read_text(encoding="utf-8"))
        antigo = AQUI / "simulacoes" / "contexto-antigo-e-chega"
        self.assertNotIn("Davi", (antigo / "contexto-tcc-hortas.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
