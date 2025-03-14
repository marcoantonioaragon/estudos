from .testes.normalidade import TesteNormalidade
from .testes.homocedasticidade import TesteHomocedasticidade
from .testes.anova import ANOVA, ANOVAWelch
from .testes.mann_whitney import TesteMannWhitney
from .testes.qui import TesteQuiQuadradoProporcoes
from .testes.z_test import TesteZ
from .testes.t_test import TesteT


class MotorEstatistico:
    """
    Classe responsável por escolher e realizar o teste estatístico apropriado com base nas características dos dados.
    """

    def __init__(self, grupos):
        """
        Inicializa o motor estatístico com os grupos de dados.

        :param grupos: Lista de dicionários contendo as estatísticas agregadas de cada grupo.
            Cada dicionário deve conter:
            - "media" (float): Média do grupo.
            - "tamanho" (int): Tamanho da amostra.
            - "desvio_padrao" (float): Desvio padrão do grupo.
            - "dados" (list, opcional): Dados brutos do grupo (necessário para teste de normalidade).
            - "soma_postos" (float, opcional): Soma dos postos do grupo (necessário para Mann-Whitney).
            - "taxa_conversao" (float, opcional): Taxa de conversão do grupo (necessário para Qui-Quadrado).
        """
        self.grupos = grupos
        self.num_grupos = len(grupos)
        self._verificar_normalidade()

    def _verificar_normalidade(self):
        """
        Verifica a normalidade dos grupos usando o teste de Shapiro-Wilk.
        Atualiza o campo "normal" em cada grupo com base no resultado do teste.
        """
        for grupo in self.grupos:
            if "dados" not in grupo:
                raise ValueError(
                    "Os dados brutos do grupo são necessários para verificar a normalidade.")
            teste_normalidade = TesteNormalidade(
                media=grupo["media"],
                desvio_padrao=grupo["desvio_padrao"],
                tamanho_amostra=grupo["tamanho"]
            )
            resultados = teste_normalidade.ensemble_normalidade()
            grupo["normal"] = resultados[
                "decisao_final"] == "Os dados são considerados normais (ensemble)."

    def _verificar_homocedasticidade(self):
        """
        Verifica se os grupos são homocedásticos (variâncias iguais).

        :return: True se os grupos forem homocedásticos, False caso contrário.
        """
        teste_homocedasticidade = TesteHomocedasticidade(self.grupos)
        resultados = teste_homocedasticidade.realizar_teste()
        return resultados["homocedastico"]

    def _escolher_teste(self):
        """
        Escolhe o teste estatístico apropriado com base nas características dos dados.

        :return: Nome do teste a ser utilizado.
        """
        todos_normais = all(grupo["normal"] for grupo in self.grupos)
        homocedastico = self._verificar_homocedasticidade()

        if self.num_grupos == 1:
            # Teste Z ou T para uma amostra
            if todos_normais:
                return "Teste Z" if self.grupos[0]["tamanho"] > 30 else "Teste T"
            else:
                return "Teste de Wilcoxon"  # Não implementado aqui, mas seria uma opção

        elif self.num_grupos == 2:
            # Teste T, Mann-Whitney, etc.
            if todos_normais:
                if homocedastico:
                    return "Teste T para duas amostras"
                else:
                    return "Teste T de Welch"
            else:
                return "Teste de Mann-Whitney"

        else:
            # ANOVA, ANOVA de Welch, etc.
            if todos_normais:
                if homocedastico:
                    return "ANOVA"
                else:
                    return "ANOVA de Welch"
            else:
                return "Teste de Kruskal-Wallis"  # Não implementado aqui, mas seria uma opção

    def realizar_teste(self, alpha=0.05):
        """
        Realiza o teste estatístico apropriado e retorna os resultados.

        :param alpha: Nível de significância (padrão é 0.05).
        :return: Dicionário com os resultados do teste.
        """
        teste_escolhido = self._escolher_teste()

        if teste_escolhido == "Teste Z":
            teste = TesteZ(
                media=self.grupos[0]["media"],
                desvio_padrao=self.grupos[0]["desvio_padrao"],
                tamanho=self.grupos[0]["tamanho"],
                media_populacional=0  # Valor padrão, pode ser ajustado
            )
        elif teste_escolhido == "Teste T":
            teste = TesteT(
                media=self.grupos[0]["media"],
                desvio_padrao=self.grupos[0]["desvio_padrao"],
                tamanho=self.grupos[0]["tamanho"],
                media_populacional=0  # Valor padrão, pode ser ajustado
            )
        elif teste_escolhido == "Teste T para duas amostras":
            # Implementar lógica para duas amostras
            pass
        elif teste_escolhido == "Teste T de Welch":
            # Implementar lógica para Welch
            pass
        elif teste_escolhido == "Teste de Mann-Whitney":
            if "soma_postos" not in self.grupos[0] or "soma_postos" not in self.grupos[1]:
                raise ValueError(
                    "A soma dos postos é necessária para o teste de Mann-Whitney.")
            teste = TesteMannWhitney(
                tamanho_amostra_grupo_a=self.grupos[0]["tamanho"],
                tamanho_amostra_grupo_b=self.grupos[1]["tamanho"],
                soma_postos_grupo_a=self.grupos[0]["soma_postos"],
                soma_postos_grupo_b=self.grupos[1]["soma_postos"]
            )
        elif teste_escolhido == "ANOVA":
            teste = ANOVA(
                (self.grupos[0]["media"], self.grupos[0]
                 ["tamanho"], self.grupos[0]["desvio_padrao"]),
                (self.grupos[1]["media"], self.grupos[1]
                 ["tamanho"], self.grupos[1]["desvio_padrao"]),
                # Adicionar mais grupos conforme necessário
            )
        elif teste_escolhido == "ANOVA de Welch":
            teste = ANOVAWelch(
                (self.grupos[0]["media"], self.grupos[0]
                 ["tamanho"], self.grupos[0]["desvio_padrao"]),
                (self.grupos[1]["media"], self.grupos[1]
                 ["tamanho"], self.grupos[1]["desvio_padrao"]),
                # Adicionar mais grupos conforme necessário
            )
        elif teste_escolhido == "Teste Qui-Quadrado":
            if "taxa_conversao" not in self.grupos[0] or "taxa_conversao" not in self.grupos[1]:
                raise ValueError(
                    "A taxa de conversão é necessária para o teste Qui-Quadrado.")
            teste = TesteQuiQuadradoProporcoes(
                n_grupos=[grupo["tamanho"] for grupo in self.grupos],
                taxas_conversao=[grupo["taxa_conversao"]
                                 for grupo in self.grupos]
            )
        else:
            raise ValueError(f"Teste {teste_escolhido} não implementado.")

        # Realiza o teste e retorna os resultados
        return teste.realizar_teste(alpha=alpha)
