import subprocess
import sys
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SCRIPT = AQUI.parent.parent / "skills" / "quanto-voce-sabe" / "scripts" / "quantidade.py"
sys.path.insert(0, str(SCRIPT.parent))
import quantidade


def documento(*temas, palavras=2):
    """Cria um documento com a quantidade de fatos pedida em cada tema."""
    linhas = ["# Assunto", "", "## Fatos"]
    for t, total in enumerate(temas):
        linhas += ["", f"### Tema {t}"]
        for f in range(total):
            linhas.append(f"- fato{t}x{f}" + " palavra" * (palavras - 1) + " [fonte: conversa]")
    return "\n".join(linhas)


class TestQuantidade(unittest.TestCase):
    def test_vazio(self):
        for texto in ("", "## Fatos\n", "## Fatos\n\n### Tema vazio\n"):
            self.assertEqual(quantidade.medir(texto)["nota"], 0)

    def test_limites_de_fatos(self):
        # (último valor da faixa, pontos); um fato a mais sobe um ponto.
        for maximo, pontos in ((0, 0), (2, 1), (5, 2), (10, 3), (20, 4), (35, 5), (55, 6)):
            self.assertEqual(quantidade.medir(documento(maximo))["nota"], pontos)
            self.assertEqual(quantidade.medir(documento(maximo + 1))["nota"], pontos + 1)

    def test_limites_de_temas(self):
        for temas, pontos in ((1, 0), (2, 1), (4, 1), (5, 2)):
            self.assertEqual(quantidade.pontos(temas, quantidade.LIMITES_TEMAS), pontos)

    def test_tema_com_um_fato_nao_pontua(self):
        self.assertEqual(quantidade.medir(documento(1, 1, 1))["temas"], 0)

    def test_limite_de_palavras(self):
        self.assertEqual(quantidade.medir(documento(1, palavras=299))["nota"], 1)
        self.assertEqual(quantidade.medir(documento(1, palavras=300))["nota"], 2)

    def test_exemplos_acordados(self):
        self.assertEqual(quantidade.medir(documento(3, 2))["nota"], 3)
        self.assertEqual(quantidade.medir(documento(4, 4, 4, 3))["nota"], 5)
        self.assertEqual(quantidade.medir(documento(5, 5, 5, 5, 5, palavras=13))["nota"], 8)

    def test_nota_maxima(self):
        self.assertEqual(quantidade.medir(documento(*[20] * 5, palavras=4))["nota"], 10)

    def test_repetidos(self):
        texto = documento(1) + "\n- FATO0X0  palavra. [fonte: memória]"
        medida = quantidade.medir(texto)
        self.assertEqual((medida["fatos"], medida["repetidos"]), (1, 1))

    def test_inferencias_e_conflitos_nao_contam(self):
        texto = documento(2) + (
            "\n\n## Inferências\n\n### Tema\n- inferência [fonte: conversa]"
            "\n\n## Conflitos\n- conflito [fonte: conversa]"
        )
        self.assertEqual(quantidade.medir(texto)["fatos"], 2)

    def test_item_sem_fonte_nao_conta(self):
        medida = quantidade.medir("## Fatos\n### Tema\n- sem fonte\n- vazia [fonte: ]")
        self.assertEqual((medida["fatos"], medida["sem_fonte"]), (0, 2))

    def test_fonte_nao_entra_nas_palavras(self):
        medida = quantidade.medir("## Fatos\n### Tema\n- duas palavras [fonte: texto longo da fonte]")
        self.assertEqual(medida["palavras"], 2)

    def test_item_em_varias_linhas(self):
        medida = quantidade.medir("## Fatos\n### Tema\n- começo\n  e fim [fonte: conversa]")
        self.assertEqual((medida["fatos"], medida["palavras"]), (1, 3))

    def test_niveis(self):
        for nota, nome in ((0, "baixa"), (3, "baixa"), (4, "média"), (6, "média"), (7, "alta"), (10, "alta")):
            self.assertEqual(quantidade.nivel(nota), nome)

    def rodar(self, *args, entrada=""):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *args], input=entrada.encode(), capture_output=True
        )

    def test_linha_de_comando(self):
        resultado = self.rodar("-", entrada=documento(4, 4, 4, 3))
        self.assertEqual(resultado.returncode, 0)
        self.assertIn("Quantidade: média (5/10)", resultado.stdout.decode())

    def test_documento_sem_secao_fatos(self):
        self.assertNotEqual(self.rodar("-", entrada="# Só título").returncode, 0)

    def test_simulacoes(self):
        for pasta, saida in (
            ("muito-contexto", "Quantidade: alta (7/10)"),
            ("pouco-contexto", "Quantidade: baixa (2/10)"),
            ("sem-contexto", "Quantidade: baixa (0/10)"),
        ):
            resultado = self.rodar(str(AQUI / "simulacoes" / pasta / "documento.md"))
            self.assertIn(saida, resultado.stdout.decode(), pasta)


if __name__ == "__main__":
    unittest.main()
