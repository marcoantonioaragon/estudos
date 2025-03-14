import random
from math import sqrt, log, cos, pi, sin, exp

class TesteNormalidade:
    def __init__(self, media, desvio_padrao, tamanho_amostra):
        """
        Inicializa a classe com valores agregados para gerar os dados.
        
        Parâmetros:
        - media (float): Média da distribuição normal.
        - desvio_padrao (float): Desvio padrão da distribuição normal.
        - tamanho_amostra (int): Tamanho da amostra a ser gerada.
        """
        self.media = media
        self.desvio_padrao = desvio_padrao
        self.tamanho_amostra = tamanho_amostra
        self.dados = self._gerar_dados()

    def _gerar_dados(self):
        """
        Gera uma amostra de dados normalmente distribuídos usando o método Box-Muller.
        
        Retorna:
        - list: Lista com os dados gerados.
        """
        dados = []
        for _ in range(self.tamanho_amostra // 2):
            # Gera dois números aleatórios uniformes entre 0 e 1
            u1 = random.random()
            u2 = random.random()
            
            # Aplica a transformação Box-Muller
            z0 = sqrt(-2.0 * log(u1)) * cos(2.0 * pi * u2)
            z1 = sqrt(-2.0 * log(u1)) * sin(2.0 * pi * u2)
            
            # Ajusta para a média e desvio padrão desejados
            x0 = self.media + z0 * self.desvio_padrao
            x1 = self.media + z1 * self.desvio_padrao
            
            dados.extend([x0, x1])
        
        # Se o tamanho da amostra for ímpar, remove o último elemento
        if self.tamanho_amostra % 2 != 0:
            dados.pop()
        
        return dados

    def _calcular_estatistica_shapiro(self, dados):
        """
        Calcula a estatística W do teste de Shapiro-Wilk.
        """
        n = len(dados)
        if n < 3 or n > 5000:
            raise ValueError("O teste de Shapiro-Wilk requer entre 3 e 5000 observações.")
        
        dados_ordenados = sorted(dados)
        media = sum(dados_ordenados) / n
        soma_quadrados = sum((x - media) ** 2 for x in dados_ordenados)
        
        # Coeficientes aproximados (simplificação)
        a = [1.0 / sqrt(n) for _ in range(n)]
        
        # Calcula o numerador da estatística W
        numerador = sum(a[i] * (dados_ordenados[n - i - 1] - dados_ordenados[i]) for i in range(len(a))) ** 2
        
        # Calcula a estatística W
        W = numerador / soma_quadrados
        return W

    def _aproximacao_royston(self, W, n):
        """
        Aplica a aproximação de Royston para calcular o p-valor do teste de Shapiro-Wilk.
        """
        # Verifica se o tamanho da amostra é suportado
        if n > 5000:
            raise ValueError("A aproximação de Royston não suporta amostras maiores que 5000.")
        
        # Parâmetros da transformação de Royston
        if n <= 11:
            gamma = 0.459 * n - 2.273
            mu = 0.544 * n - 1.382
            sigma = exp(0.026 * n - 0.434)
        else:
            gamma = 0.459 * n - 4.9
            mu = 0.544 * n - 5.38
            sigma = exp(0.026 * n - 0.434)
        
        # Transformação de Royston
        z = (log(1 - W) - mu) / sigma
        p_valor = 1 - self._funcao_distribuicao_normal(z)
        return p_valor

    def _calcular_estatistica_anderson_darling(self, dados):
        """
        Calcula a estatística do teste de Anderson-Darling.
        """
        n = len(dados)
        dados_ordenados = sorted(dados)
        media = sum(dados_ordenados) / n
        desvio = sqrt(sum((x - media) ** 2 for x in dados_ordenados) / n)
        
        # Calcula a estatística A²
        A2 = -n
        for i in range(n):
            xi = (dados_ordenados[i] - media) / desvio
            cdf = self._funcao_distribuicao_normal(xi)
            A2 -= (2 * i + 1) * (log(cdf) + log(1 - cdf)) / n
        return A2

    def _calcular_estatistica_kolmogorov_smirnov(self, dados):
        """
        Calcula a estatística do teste de Kolmogorov-Smirnov.
        """
        n = len(dados)
        dados_ordenados = sorted(dados)
        media = sum(dados_ordenados) / n
        desvio = sqrt(sum((x - media) ** 2 for x in dados_ordenados) / n)
        
        # Calcula a estatística D
        D = 0
        for i in range(n):
            xi = (dados_ordenados[i] - media) / desvio
            cdf_teorico = self._funcao_distribuicao_normal(xi)
            cdf_empirico = (i + 1) / n
            D = max(D, abs(cdf_empirico - cdf_teorico))
        return D

    def _funcao_distribuicao_normal(self, x):
        """
        Calcula a função de distribuição acumulada (CDF) da distribuição normal padrão.
        """
        return (1.0 + self._funcao_erf(x / sqrt(2.0))) / 2.0

    def _funcao_erf(self, x):
        """
        Aproximação da função erro (erf) para a distribuição normal.
        """
        # Aproximação polinomial
        a1 =  0.254829592
        a2 = -0.284496736
        a3 =  1.421413741
        a4 = -1.453152027
        a5 =  1.061405429
        p  =  0.3275911

        t = 1.0 / (1.0 + p * abs(x))
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * exp(-x * x)
        return -y if x < 0 else y

    def realizar_teste_shapiro(self, alpha=0.05):
        """
        Realiza o teste de Shapiro-Wilk com a aproximação de Royston.
        
        Parâmetros:
        - alpha (float): Nível de significância (padrão é 0.05).
        
        Retorna:
        - W (float): Estatística do teste de Shapiro-Wilk.
        - p_valor (float): P-valor aproximado usando a transformação de Royston.
        """
        if self.tamanho_amostra > 5000:
            return None, None  # Não aplicável para amostras grandes
        W = self._calcular_estatistica_shapiro(self.dados)
        p_valor = self._aproximacao_royston(W, self.tamanho_amostra)
        return W, p_valor

    def realizar_teste_anderson_darling(self, alpha=0.05):
        """
        Realiza o teste de Anderson-Darling.
        
        Parâmetros:
        - alpha (float): Nível de significância (padrão é 0.05).
        
        Retorna:
        - estatistica (float): Estatística do teste de Anderson-Darling.
        - normal (bool): Indica se os dados são normais com base no teste.
        """
        estatistica = self._calcular_estatistica_anderson_darling(self.dados)
        # Valor crítico simplificado para alpha = 0.05
        valor_critico = 0.75  # Exemplo simplificado
        normal = estatistica < valor_critico
        return estatistica, normal

    def realizar_teste_kolmogorov_smirnov(self, alpha=0.05):
        """
        Realiza o teste de Kolmogorov-Smirnov.
        
        Parâmetros:
        - alpha (float): Nível de significância (padrão é 0.05).
        
        Retorna:
        - estatistica (float): Estatística do teste de Kolmogorov-Smirnov.
        - normal (bool): Indica se os dados são normais com base no teste.
        """
        estatistica = self._calcular_estatistica_kolmogorov_smirnov(self.dados)
        # Valor crítico simplificado para alpha = 0.05
        valor_critico = 0.05  # Exemplo simplificado
        normal = estatistica < valor_critico
        return estatistica, normal

    def ensemble_normalidade(self, alpha=0.05):
        """
        Realiza os três testes de normalidade e decide se os dados são normais com base em um ensemble.
        
        Parâmetros:
        - alpha (float): Nível de significância (padrão é 0.05).
        
        Retorna:
        - dict: Um dicionário contendo os resultados detalhados de cada teste e a decisão final.
        """
        resultados = {
            "tamanho_amostra": self.tamanho_amostra,
            "alpha": alpha,
            "shapiro_wilk": {
                "aplicavel": self.tamanho_amostra <= 5000,
                "estatistica": None,
                "p_valor": None,
                "normal": False,
            },
            "anderson_darling": {
                "estatistica": None,
                "normal": False,
            },
            "kolmogorov_smirnov": {
                "estatistica": None,
                "normal": False,
            },
            "decisao_final": None,
        }

        # Realiza o teste de Shapiro-Wilk (se aplicável)
        if resultados["shapiro_wilk"]["aplicavel"]:
            shapiro_w, shapiro_p = self.realizar_teste_shapiro(alpha)
            resultados["shapiro_wilk"]["estatistica"] = shapiro_w
            resultados["shapiro_wilk"]["p_valor"] = shapiro_p
            resultados["shapiro_wilk"]["normal"] = shapiro_p > alpha

        # Realiza o teste de Anderson-Darling
        anderson_a2, anderson_normal = self.realizar_teste_anderson_darling(alpha)
        resultados["anderson_darling"]["estatistica"] = anderson_a2
        resultados["anderson_darling"]["normal"] = anderson_normal

        # Realiza o teste de Kolmogorov-Smirnov
        kolmogorov_d, kolmogorov_normal = self.realizar_teste_kolmogorov_smirnov(alpha)
        resultados["kolmogorov_smirnov"]["estatistica"] = kolmogorov_d
        resultados["kolmogorov_smirnov"]["normal"] = kolmogorov_normal

        # Conta quantos testes indicam normalidade
        if resultados["shapiro_wilk"]["aplicavel"]:
            # Se Shapiro-Wilk for aplicável, precisamos de pelo menos 2 testes normais
            contagem = sum([
                resultados["shapiro_wilk"]["normal"],
                resultados["anderson_darling"]["normal"],
                resultados["kolmogorov_smirnov"]["normal"],
            ])
            decisao_final = contagem >= 2
        else:
            # Se Shapiro-Wilk não for aplicável, precisamos de pelo menos 1 teste normal
            contagem = sum([
                resultados["anderson_darling"]["normal"],
                resultados["kolmogorov_smirnov"]["normal"],
            ])
            decisao_final = contagem >= 1

        # Decide com base no ensemble
        if decisao_final:
            resultados["decisao_final"] = "Os dados são considerados normais (ensemble)."
        else:
            resultados["decisao_final"] = "Os dados não são considerados normais (ensemble)."

        return resultados