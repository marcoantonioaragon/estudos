import math

class TesteQuiQuadradoProporcoes:
    """
    Classe para realizar o teste qui-quadrado para proporções no contexto de teste A/B com N grupos.

    O teste qui-quadrado compara as proporções de sucesso entre N grupos para verificar
    se há diferenças estatisticamente significativas. Esta implementação utiliza taxas de conversão
    já calculadas (valores entre 0 e 1) e tamanhos de amostra.

    Atributos:
        n_grupos (list): Lista de tamanhos das amostras dos grupos.
        taxas_conversao (list): Lista de taxas de conversão dos grupos (valores entre 0 e 1).

    Métodos:
        calcular_estatistica_qui_quadrado(): Calcula a estatística qui-quadrado.
        calcular_graus_liberdade(): Calcula os graus de liberdade.
        calcular_valor_p(qui_quadrado): Calcula o valor p.
        realizar_teste(alpha=0.05): Realiza o teste e retorna um dicionário com resultados detalhados.

    Exemplo de uso:
        >>> n_grupos = [1000, 1000]  # Tamanhos das amostras dos grupos
        >>> taxas_conversao = [0.2, 0.25]  # Taxas de conversão dos grupos
        >>> teste = TesteQuiQuadradoProporcoes(n_grupos, taxas_conversao)
        >>> resultados = teste.realizar_teste(alpha=0.05)
        >>> print(resultados)

    Definições:
        - Teste Qui-Quadrado: Um teste estatístico usado para comparar proporções entre grupos.
        - Taxa de Conversão: Proporção de sucessos em um grupo (valor entre 0 e 1).
        - Valor p: Probabilidade de observar um valor tão extremo quanto o calculado, assumindo que a hipótese nula é verdadeira.
        - Graus de Liberdade: Número de grupos menos 1.

    Limitações:
        1. Depende de taxas de conversão e tamanhos de amostra já calculados.
        2. O cálculo do valor p é uma aproximação numérica e pode não ser tão preciso quanto métodos analíticos.

    Referências:
        - Fisher, R. A. (1925). Statistical Methods for Research Workers. Edinburgh: Oliver and Boyd.
        - Montgomery, D. C. (2017). Design and Analysis of Experiments. Wiley.
        - Wikipedia. (2023). Chi-squared test. Disponível em: https://en.wikipedia.org/wiki/Chi-squared_test.
    """

    def __init__(self, n_grupos, taxas_conversao):
        """
        Inicializa a classe com as estatísticas agregadas dos grupos.

        :param n_grupos: Lista de tamanhos das amostras dos grupos.
        :param taxas_conversao: Lista de taxas de conversão dos grupos (valores entre 0 e 1).
        """
        self.n_grupos = n_grupos
        self.taxas_conversao = taxas_conversao
        self.num_grupos = len(n_grupos)  # Número de grupos

    def calcular_estatistica_qui_quadrado(self):
        """
        Calcula a estatística qui-quadrado para proporções.

        :return: Valor da estatística qui-quadrado.
        """
        # Proporção combinada (sob a hipótese nula)
        p_combinada = sum(taxa * n for taxa, n in zip(self.taxas_conversao, self.n_grupos)) / sum(self.n_grupos)

        # Cálculo da estatística qui-quadrado
        qui_quadrado = 0
        for taxa, n in zip(self.taxas_conversao, self.n_grupos):
            qui_quadrado += ((taxa - p_combinada) ** 2 / p_combinada) * n
        return qui_quadrado

    def calcular_graus_liberdade(self):
        """
        Calcula os graus de liberdade do teste.

        :return: Graus de liberdade.
        """
        return self.num_grupos - 1  # Graus de liberdade = número de grupos - 1

    def calcular_valor_p(self, qui_quadrado):
        """
        Calcula o valor p usando a CDF da distribuição qui-quadrado.

        :param qui_quadrado: Valor da estatística qui-quadrado.
        :return: Valor p.
        """
        def funcao_gamma(x):
            """Calcula a função gamma usando a aproximação de Lanczos."""
            if x == 1:
                return 1
            elif x == 0.5:
                return math.sqrt(math.pi)
            else:
                return math.exp(math.lgamma(x))

        def pdf_qui_quadrado(x, k):
            """Calcula a função de densidade de probabilidade (PDF) da distribuição qui-quadrado."""
            if x <= 0:
                return 0
            numerador = x ** (k / 2 - 1) * math.exp(-x / 2)
            denominador = (2 ** (k / 2)) * funcao_gamma(k / 2)
            return numerador / denominador

        def cdf_qui_quadrado(x, k, passos=1000):
            """Calcula a função de distribuição acumulada (CDF) da distribuição qui-quadrado usando integração numérica."""
            if x <= 0:
                return 0
            # Integração numérica usando o método do trapézio
            h = x / passos
            integral = 0
            for i in range(passos):
                x0 = i * h
                x1 = (i + 1) * h
                y0 = pdf_qui_quadrado(x0, k)
                y1 = pdf_qui_quadrado(x1, k)
                integral += (y0 + y1) * h / 2
            return integral

        # Cálculo do valor p
        valor_p = 1 - cdf_qui_quadrado(qui_quadrado, self.calcular_graus_liberdade())
        return valor_p

    def interpretar_resultado(self, valor_p, alpha):
        """
        Interpreta o resultado do teste qui-quadrado com base no valor p.

        :param valor_p: Valor p calculado.
        :param alpha: Nível de significância.
        :return: Uma string indicando se há diferenças significativas.
        """
        if valor_p < alpha:
            return "Há diferenças significativas entre as proporções (rejeitamos a hipótese nula)."
        else:
            return "Não há diferenças significativas entre as proporções (não rejeitamos a hipótese nula)."

    def realizar_teste(self, alpha=0.05):
        """
        Realiza o teste qui-quadrado e retorna um dicionário com resultados detalhados.

        :param alpha: Nível de significância (padrão é 0.05).
        :return: Dicionário com resultados detalhados.
        """
        # Passo 1: Calcular a estatística qui-quadrado
        qui_quadrado = self.calcular_estatistica_qui_quadrado()

        # Passo 2: Calcular o valor p
        valor_p = self.calcular_valor_p(qui_quadrado)

        # Passo 3: Interpretar o resultado
        resultado = self.interpretar_resultado(valor_p, alpha)

        # Retornar um dicionário com todas as informações
        return {
            "estatistica_qui_quadrado": qui_quadrado,
            "graus_liberdade": self.calcular_graus_liberdade(),
            "valor_p": valor_p,
            "alpha": alpha,
            "resultado": resultado
        }