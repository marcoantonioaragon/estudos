import math

class TesteMannWhitney:
    """
    Classe para realizar o teste de Mann-Whitney (Wilcoxon-Mann-Whitney) para duas amostras independentes.

    O teste de Mann-Whitney é um teste não paramétrico que compara as medianas de duas amostras para verificar
    se há diferenças estatisticamente significativas. Ele é adequado para dados que não seguem uma distribuição normal.

    Atributos:
        tamanho_amostra_grupo_a (int): Tamanho da amostra do grupo A.
        tamanho_amostra_grupo_b (int): Tamanho da amostra do grupo B.
        soma_postos_grupo_a (float): Soma dos postos do grupo A.
        soma_postos_grupo_b (float): Soma dos postos do grupo B.

    Métodos:
        calcular_estatistica_u(): Calcula a estatística U de Mann-Whitney.
        calcular_valor_p(u): Calcula o valor p usando a distribuição normal (aproximação numérica).
        realizar_teste(alpha=0.05): Realiza o teste e retorna um dicionário com resultados detalhados.

    Exemplo de uso:
        >>> tamanho_amostra_grupo_a = 20  # Tamanho da amostra do grupo A
        >>> tamanho_amostra_grupo_b = 25  # Tamanho da amostra do grupo B
        >>> soma_postos_grupo_a = 250  # Soma dos postos do grupo A
        >>> soma_postos_grupo_b = 300  # Soma dos postos do grupo B
        >>> teste = TesteMannWhitney(tamanho_amostra_grupo_a, tamanho_amostra_grupo_b, soma_postos_grupo_a, soma_postos_grupo_b)
        >>> resultados = teste.realizar_teste(alpha=0.05)
        >>> print(resultados)

    Definições:
        - Teste de Mann-Whitney: Um teste não paramétrico para comparar duas amostras independentes.
        - Estatística U: Medida usada para comparar as distribuições das duas amostras.
        - Valor p: Probabilidade de observar um valor tão extremo quanto o calculado, assumindo que a hipótese nula é verdadeira.

    Limitações:
        1. Aproximação normal é válida para amostras grandes (tamanho da amostra > 20).
        2. Para amostras pequenas, é recomendado usar tabelas exatas de Mann-Whitney.

    Referências:
        - Mann, H. B., & Whitney, D. R. (1947). On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other. Annals of Mathematical Statistics.
        - Wikipedia. (2023). Mann-Whitney U test. Disponível em: https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test.
    """

    def __init__(self, tamanho_amostra_grupo_a, tamanho_amostra_grupo_b, soma_postos_grupo_a, soma_postos_grupo_b):
        """
        Inicializa a classe com as estatísticas agregadas dos grupos.

        :param tamanho_amostra_grupo_a: Tamanho da amostra do grupo A.
        :param tamanho_amostra_grupo_b: Tamanho da amostra do grupo B.
        :param soma_postos_grupo_a: Soma dos postos do grupo A.
        :param soma_postos_grupo_b: Soma dos postos do grupo B.
        """
        self.tamanho_amostra_grupo_a = tamanho_amostra_grupo_a
        self.tamanho_amostra_grupo_b = tamanho_amostra_grupo_b
        self.soma_postos_grupo_a = soma_postos_grupo_a
        self.soma_postos_grupo_b = soma_postos_grupo_b

    def calcular_estatistica_u(self):
        """
        Calcula a estatística U de Mann-Whitney.

        :return: Valor da estatística U.
        """
        u_a = self.soma_postos_grupo_a - (self.tamanho_amostra_grupo_a * (self.tamanho_amostra_grupo_a + 1)) / 2
        u_b = self.soma_postos_grupo_b - (self.tamanho_amostra_grupo_b * (self.tamanho_amostra_grupo_b + 1)) / 2
        return min(u_a, u_b)  # Retorna o menor valor entre U_A e U_B

    def calcular_valor_p(self, u):
        """
        Calcula o valor p usando a distribuição normal (aproximação numérica).

        :param u: Valor da estatística U.
        :return: Valor p.
        """
        # Média e desvio padrão da distribuição de U sob a hipótese nula
        media_u = (self.tamanho_amostra_grupo_a * self.tamanho_amostra_grupo_b) / 2
        variancia_u = (self.tamanho_amostra_grupo_a * self.tamanho_amostra_grupo_b * 
                       (self.tamanho_amostra_grupo_a + self.tamanho_amostra_grupo_b + 1)) / 12
        desvio_padrao_u = math.sqrt(variancia_u)

        # Cálculo do Z-score
        z = (u - media_u) / desvio_padrao_u

        # Cálculo do valor p usando a CDF da distribuição normal (aproximação numérica)
        def cdf_normal(x):
            """Calcula a função de distribuição acumulada (CDF) da distribuição normal."""
            return (1 + math.erf(x / math.sqrt(2))) / 2

        valor_p = 2 * (1 - cdf_normal(abs(z)))  # Teste bilateral
        return valor_p

    def interpretar_resultado(self, valor_p, alpha):
        """
        Interpreta o resultado do teste de Mann-Whitney com base no valor p.

        :param valor_p: Valor p calculado.
        :param alpha: Nível de significância.
        :return: Uma string indicando se há diferenças significativas.
        """
        if valor_p < alpha:
            return "Há diferenças significativas entre as medianas (rejeitamos a hipótese nula)."
        else:
            return "Não há diferenças significativas entre as medianas (não rejeitamos a hipótese nula)."

    def realizar_teste(self, alpha=0.05):
        """
        Realiza o teste de Mann-Whitney e retorna um dicionário com resultados detalhados.

        :param alpha: Nível de significância (padrão é 0.05).
        :return: Dicionário com resultados detalhados.
        """
        # Passo 1: Calcular a estatística U
        u = self.calcular_estatistica_u()

        # Passo 2: Calcular o valor p
        valor_p = self.calcular_valor_p(u)

        # Passo 3: Interpretar o resultado
        resultado = self.interpretar_resultado(valor_p, alpha)

        # Retornar um dicionário com todas as informações
        return {
            "estatistica_u": u,
            "valor_p": valor_p,
            "alpha": alpha,
            "resultado": resultado
        }