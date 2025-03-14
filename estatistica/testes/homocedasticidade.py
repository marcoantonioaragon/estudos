from math import log

class TesteHomocedasticidade:
    """
    Classe para testar homocedasticidade (igualdade de variâncias) entre grupos utilizando os testes de Bartlett e Levene.
    A classe recebe valores agregados dos grupos, como variância, tamanho da amostra, média e normalidade, e decide
    automaticamente qual teste utilizar com base nas características dos dados.

    Métodos:
    - _calcular_estatistica_bartlett: Calcula a estatística do teste de Bartlett.
    - _calcular_estatistica_levene: Calcula a estatística do teste de Levene.
    - _verificar_normalidade_grupos: Verifica se todos os grupos são normais.
    - realizar_teste: Realiza o teste de homocedasticidade e retorna resultados detalhados.

    Limitações:
    - Os valores críticos para os testes de Bartlett e Levene são simplificados e podem não ser precisos para todos os cenários.
    - A classe depende de valores agregados (variância, média, tamanho da amostra etc.) para funcionar.
    - Se a normalidade dos grupos não for fornecida, a classe não pode decidir qual teste utilizar.

    Referências:
    - Bartlett, M. S. (1937). Properties of Sufficiency and Statistical Tests. *Proceedings of the Royal Statistical Society*, 160, 268-282.
    - Levene, H. (1960). Robust Tests for Equality of Variances. *Contributions to Probability and Statistics*, 278-292.
    """

    def __init__(self, grupos_agregados):
        """
        Inicializa a classe com valores agregados dos grupos para testar homocedasticidade.
        
        Parâmetros:
        - grupos_agregados (list of dicts): Lista contendo dicionários com valores agregados de cada grupo.
            Cada dicionário deve conter:
            - "variancia" (float): Variância do grupo.
            - "tamanho" (int): Tamanho da amostra do grupo.
            - "media" (float, opcional): Média do grupo (necessária para Levene).
            - "normal" (bool, opcional): Indica se o grupo é normal (necessário para escolha do teste).
        """
        self.grupos_agregados = grupos_agregados

    def _calcular_estatistica_bartlett(self):
        """
        Calcula a estatística do teste de Bartlett.
        
        Retorno:
        - float: Estatística do teste de Bartlett.
        """
        # Número total de observações
        N = sum(grupo["tamanho"] for grupo in self.grupos_agregados)
        # Número de grupos
        k = len(self.grupos_agregados)
        
        # Variâncias e tamanhos dos grupos
        variancias = [grupo["variancia"] for grupo in self.grupos_agregados]
        tamanhos = [grupo["tamanho"] for grupo in self.grupos_agregados]
        
        # Variância combinada
        S2_p = sum((tamanhos[i] - 1) * variancias[i] for i in range(k)) / (N - k)
        
        # Numerador e denominador da estatística
        numerador = (N - k) * log(S2_p) - sum((tamanhos[i] - 1) * log(variancias[i]) for i in range(k))
        denominador = 1 + (1 / (3 * (k - 1))) * (sum(1 / (tamanhos[i] - 1) for i in range(k)) - 1 / (N - k))
        
        # Estatística de Bartlett
        B = numerador / denominador
        return B

    def _calcular_estatistica_levene(self):
        """
        Calcula a estatística do teste de Levene.
        
        Retorno:
        - float: Estatística do teste de Levene.
        """
        # Desvios absolutos em relação à média de cada grupo
        desvios = []
        for grupo in self.grupos_agregados:
            if "media" not in grupo:
                raise ValueError("A média do grupo é necessária para o teste de Levene.")
            desvios.append(grupo["variancia"])  # Usamos a variância como proxy para desvios absolutos
        
        # Média global dos desvios
        media_global = sum(desvios[i] * self.grupos_agregados[i]["tamanho"] for i in range(len(desvios))) / sum(grupo["tamanho"] for grupo in self.grupos_agregados)
        
        # Variância entre grupos
        variancia_entre = sum(self.grupos_agregados[i]["tamanho"] * (desvios[i] - media_global) ** 2 for i in range(len(desvios))) / (len(self.grupos_agregados) - 1)
        
        # Variância dentro dos grupos
        variancia_dentro = sum((self.grupos_agregados[i]["tamanho"] - 1) * desvios[i] for i in range(len(desvios))) / (sum(grupo["tamanho"] for grupo in self.grupos_agregados) - len(self.grupos_agregados))
        
        # Estatística de Levene
        W = variancia_entre / variancia_dentro
        return W

    def _verificar_normalidade_grupos(self):
        """
        Verifica se todos os grupos são normais.
        
        Retorno:
        - bool: True se todos os grupos forem normais, False caso contrário.
        """
        for grupo in self.grupos_agregados:
            if "normal" not in grupo:
                raise ValueError("A normalidade do grupo deve ser fornecida ou calculada.")
            if not grupo["normal"]:
                return False
        return True

    def realizar_teste(self, alpha=0.05):
        """
        Realiza o teste de homocedasticidade (Bartlett ou Levene) com base nas características dos grupos.
        
        Parâmetros:
        - alpha (float): Nível de significância (padrão é 0.05).
        
        Retorno:
        - dict: Resultados detalhados do teste, incluindo:
            - "teste_utilizado" (str): Nome do teste utilizado ("Bartlett" ou "Levene").
            - "estatistica" (float): Valor da estatística calculada.
            - "valor_critico" (float): Valor crítico utilizado para a decisão.
            - "alpha" (float): Nível de significância utilizado.
            - "homocedastico" (bool): Indica se os dados são homocedásticos.
            - "mensagem" (str): Mensagem descritiva sobre o resultado.
        """
        resultados = {
            "teste_utilizado": None,
            "estatistica": None,
            "valor_critico": None,
            "alpha": alpha,
            "homocedastico": None,
            "mensagem": None,
        }

        # Verifica se todos os grupos são normais
        todos_normais = self._verificar_normalidade_grupos()

        # Escolhe o teste com base na normalidade dos grupos
        if todos_normais:
            resultados["teste_utilizado"] = "Bartlett"
            estatistica = self._calcular_estatistica_bartlett()
            valor_critico = 3.841  # Valor crítico aproximado para alpha = 0.05
        else:
            resultados["teste_utilizado"] = "Levene"
            estatistica = self._calcular_estatistica_levene()
            valor_critico = 2.5  # Valor crítico aproximado para alpha = 0.05

        resultados["estatistica"] = estatistica
        resultados["valor_critico"] = valor_critico
        resultados["homocedastico"] = estatistica < valor_critico

        # Mensagem descritiva
        if resultados["homocedastico"]:
            resultados["mensagem"] = f"Os dados são homocedásticos ao nível de significância {alpha}."
        else:
            resultados["mensagem"] = f"Os dados não são homocedásticos ao nível de significância {alpha}."

        return resultados