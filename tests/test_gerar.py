import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import gerar


class TestGerar(unittest.TestCase):
    def setUp(self):
        temporario = tempfile.TemporaryDirectory()
        self.addCleanup(temporario.cleanup)
        self.addCleanup(setattr, gerar, "RAIZ", gerar.RAIZ)
        gerar.RAIZ = Path(temporario.name)
        (gerar.RAIZ / "LICENSE").write_text("MIT")
        self.skills = [self.criar_skill("alfa"), self.criar_skill("beta")]

    def criar_skill(self, nome, extra=""):
        skill = gerar.RAIZ / "skills" / nome
        (skill / "scripts" / "__pycache__").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {nome}\ndescription: Teste.\ndisable-model-invocation: true\n{extra}---\n\nCorpo de {nome}.\n",
            encoding="utf-8",
        )
        (skill / "scripts" / "util.py").write_text("print(1)\n")
        (skill / "scripts" / "__pycache__" / "util.pyc").write_bytes(b"x")
        return skill

    def test_zip_individual(self):
        destino = gerar.gerar_zip(self.skills[0])
        self.assertEqual(destino.name, "alfa.zip")
        with zipfile.ZipFile(destino) as pacote:
            self.assertEqual(sorted(pacote.namelist()), ["alfa/SKILL.md", "alfa/scripts/util.py"])
            skill_md = pacote.read("alfa/SKILL.md").decode()
        self.assertIn("name: alfa", skill_md)
        self.assertNotIn("disable-model-invocation", skill_md)

    def test_zip_unico(self):
        destino = gerar.gerar_zip_unico(self.skills)
        self.assertEqual(destino.name, "todas-as-skills.zip")
        raiz = "skills-para-qualquer-um"
        with zipfile.ZipFile(destino) as pacote:
            self.assertEqual(
                sorted(pacote.namelist()),
                [
                    f"{raiz}/.claude-plugin/plugin.json",
                    f"{raiz}/LICENSE",
                    f"{raiz}/skills/alfa/SKILL.md",
                    f"{raiz}/skills/alfa/scripts/util.py",
                    f"{raiz}/skills/beta/SKILL.md",
                    f"{raiz}/skills/beta/scripts/util.py",
                ],
            )
            self.assertEqual(json.loads(pacote.read(f"{raiz}/.claude-plugin/plugin.json"))["name"], raiz)
            for nome in ("alfa", "beta"):
                skill_md = pacote.read(f"{raiz}/skills/{nome}/SKILL.md").decode()
                self.assertNotIn("disable-model-invocation", skill_md)

    def test_prompt(self):
        prompt = gerar.gerar_prompt(self.skills[0]).read_text(encoding="utf-8")
        self.assertEqual(prompt, "Corpo de alfa.\n\nMinha ideia: [descreva aqui]\n")

    def test_prompt_com_entrada(self):
        skill = self.criar_skill("gama", "metadata:\n  autor: alguém\n  entrada: Assunto\n")
        prompt = gerar.gerar_prompt(skill).read_text(encoding="utf-8")
        self.assertTrue(prompt.endswith("\n\nAssunto: [descreva aqui]\n"))


if __name__ == "__main__":
    unittest.main()
