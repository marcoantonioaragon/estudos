import math

class ANOVABase:
    """
    Classe base para implementação de testes ANOVA.

    Esta classe contém métodos comuns para cálculos de ANOVA, como cálculo de médias,
    somas de quadrados e graus de liberdade. Ela serve como base para as classes
    ANOVA tradicional e ANOVA de Welch.

    Atributos:
        grupos (tuple): Tuplas contendo (média, tamanho da amostra, desvio padrão) de cada grupo.
        numero_grupos (int): Número de grupos.
        numero_total_observacoes (int): Número total de observações.

    Métodos:
        calcular_media_geral(): Calcula a média geral (grand mean) com base nas médias e tamanhos das amostras.
        calcular_soma_quadrados_dentro_grupos(): Calcula a soma dos quadrados dentro dos grupos.
        calcular_graus_liberdade(): Calcula os graus de liberdade entre grupos e dentro dos grupos.
        calcular_valor_p(valor_f, graus_liberdade_entre, graus_liberdade_dentro): Calcula o valor p usando a CDF da distribuição F.
        interpretar_resultado(valor_p, alpha): Interpreta o resultado do teste ANOVA com base no valor p.

    Definições:
        - ANOVA: Análise de Variância, um teste estatístico para comparar médias de grupos.
        - Soma dos Quadrados Entre Grupos: Mede a variabilidade entre as médias dos grupos.
        - Soma dos Quadrados Dentro dos Grupos: Mede a variabilidade dentro de cada grupo.
        - Valor F: Razão entre a variância entre grupos e a variância dentro dos grupos.
        - Valor p: Probabilidade de observar um valor F tão extremo quanto o calculado, assumindo que a hipótese nula é verdadeira.

    Limitações:
        1. Depende de estatísticas agregadas (média, tamanho da amostra e desvio padrão) para cada grupo.
        2. O cálculo do valor p é uma aproximação numérica e pode não ser tão preciso quanto métodos analíticos.
        3. Não inclui testes post-hoc (como Tukey) para identificar quais grupos diferem entre si.
        4. A precisão do valor p depende do número de passos na integração numérica.

    Referências:
        - Fisher, R. A. (1925). Statistical Methods for Research Workers. Edinburgh: Oliver and Boyd.
        - Montgomery, D. C. (2017). Design and Analysis of Experiments. Wiley.
        - Wikipedia. (2023). Analysis of Variance (ANOVA). Disponível em: https://en.wikipedia.org/wiki/Analysis_of_variance.
    """

    def __init__(self, *grupos):
        """
        Inicializa a classe com as estatísticas agregadas dos grupos.

        :param grupos: Tuplas contendo (média, tamanho da amostra, desvio padrão) de cada grupo.
        """
        self.grupos = grupos
        self.numero_grupos = len(grupos)  # Número de grupos
        self.numero_total_observacoes = sum(tamanho for (_, tamanho, _) in grupos)  # Número total de observações

    def calcular_media_geral(self):
        """
        Calcula a média geral (grand mean) com base nas médias e tamanhos das amostras.

        :return: Média geral.
        """
        soma_ponderada = sum(media * tamanho for (media, tamanho, _) in self.grupos)
        return soma_ponderada / self.numero_total_observacoes

    def calcular_soma_quadrados_dentro_grupos(self):
        """
        Calcula a soma dos quadrados dentro dos grupos.

        :return: Soma dos quadrados dentro dos grupos.
        """
        soma_quadrados_dentro = sum((tamanho - 1) * (desvio ** 2) for (_, tamanho, desvio) in self.grupos)
        return soma_quadrados_dentro

    def calcular_graus_liberdade(self):
        """
        Calcula os graus de liberdade entre grupos e dentro dos grupos.

        :return: Graus de liberdade entre grupos e dentro dos grupos.
        """
        graus_liberdade_entre = self.numero_grupos - 1
        graus_liberdade_dentro = self.numero_total_observacoes - self.numero_grupos
        return graus_liberdade_entre, graus_liberdade_dentro

    def calcular_valor_p(self, valor_f, graus_liberdade_entre, graus_liberdade_dentro):
        """
        Calcula o valor p usando a CDF da distribuição F com integração numérica.

        :param valor_f: Valor F calculado.
        :param graus_liberdade_entre: Graus de liberdade entre grupos.
        :param graus_liberdade_dentro: Graus de liberdade dentro dos grupos.
        :return: Valor p.
        """
        def funcao_beta(a, b):
            """Calcula a função beta usando a função gamma."""
            def gamma(x):
                """Calcula a função gamma usando a aproximação de Lanczos."""
                if x == 1:
                    return 1
                elif x == 0.5:
                    return math.sqrt(math.pi)
                else:
                    return math.exp(math.lgamma(x))
            return gamma(a) * gamma(b) / gamma(a + b)

        def pdf_f(x, d1, d2):
            """Calcula a função de densidade de probabilidade (PDF) da distribuição F."""
            if x <= 0:
                return 0
            numerador = math.sqrt((d1 * x) ** d1 * d2 ** d2 / ((d1 * x + d2) ** (d1 + d2)))
            denominador = x * funcao_beta(d1 / 2, d2 / 2)
            return numerador / denominador

        def cdf_f(x, d1, d2, passos=1000):
            """Calcula a função de distribuição acumulada (CDF) da distribuição F usando integração numérica."""
            if x <= 0:
                return 0
            # Integração numérica usando o método do trapézio
            h = x / passos
            integral = 0
            for i in range(passos):
                x0 = i * h
                x1 = (i + 1) * h
                y0 = pdf_f(x0, d1, d2)
                y1 = pdf_f(x1, d1, d2)
                integral += (y0 + y1) * h / 2
            return integral

        return 1 - cdf_f(valor_f, graus_liberdade_entre, graus_liberdade_dentro)

    def interpretar_resultado(self, valor_p, alpha):
        """
        Interpreta o resultado do teste ANOVA com base no valor p.

        :param valor_p: Valor p calculado.
        :param alpha: Nível de significância.
        :return: Uma string indicando se há diferenças significativas entre os grupos.
        """
        if valor_p < alpha:
            return "Há diferenças significativas entre os grupos (rejeitamos a hipótese nula)."
        else:
            return "Não há diferenças significativas entre os grupos (não rejeitamos a hipótese nula)."


class ANOVA(ANOVABase):
    """
    Classe para realizar o teste ANOVA tradicional com base em estatísticas agregadas.

    O teste ANOVA é utilizado para comparar as médias de três ou mais grupos, determinando se há
    diferenças estatisticamente significativas entre eles. Esta implementação utiliza apenas
    estatísticas agregadas (média, tamanho da amostra e desvio padrão) e não depende de bibliotecas
    externas, exceto as built-in do Python.

    Métodos:
        calcular_soma_quadrados_entre_grupos(media_geral): Calcula a soma dos quadrados entre grupos.
        realizar_teste(alpha=0.05): Realiza o teste ANOVA e retorna um dicionário com resultados detalhados.

    Exemplo de uso:
        >>> grupo1 = (24.8, 5, math.sqrt(5.2))
        >>> grupo2 = (30.0, 5, math.sqrt(2.5))
        >>> grupo3 = (22.0, 5, math.sqrt(2.5))
        >>> anova_teste = ANOVA(grupo1, grupo2, grupo3)
        >>> resultados = anova_teste.realizar_teste(alpha=0.01)
        >>> print(resultados)

    Referências:
        - Fisher, R. A. (1925). Statistical Methods for Research Workers. Edinburgh: Oliver and Boyd.
        - Montgomery, D. C. (2017). Design and Analysis of Experiments. Wiley.
        - Wikipedia. (2023). Analysis of Variance (ANOVA). Disponível em: https://en.wikipedia.org/wiki/Analysis_of_variance.
    """

    def calcular_soma_quadrados_entre_grupos(self, media_geral):
        """
        Calcula a soma dos quadrados entre grupos.

        :param media_geral: Média geral.
        :return: Soma dos quadrados entre grupos.
        """
        soma_quadrados_entre = sum(tamanho * (media - media_geral) ** 2 for (media, tamanho, _) in self.grupos)
        return soma_quadrados_entre

    def realizar_teste(self, alpha=0.05):
        """
        Realiza o teste ANOVA e retorna um dicionário com resultados detalhados.

        :param alpha: Nível de significância (padrão é 0.05).
        :return: Dicionário com resultados detalhados.
        """
        # Passo 1: Calcular a média geral
        media_geral = self.calcular_media_geral()

        # Passo 2: Calcular soma dos quadrados entre grupos e dentro dos grupos
        soma_quadrados_entre = self.calcular_soma_quadrados_entre_grupos(media_geral)
        soma_quadrados_dentro = self.calcular_soma_quadrados_dentro_grupos()

        # Passo 3: Calcular graus de liberdade
        graus_liberdade_entre, graus_liberdade_dentro = self.calcular_graus_liberdade()

        # Passo 4: Calcular o valor F
        valor_f = soma_quadrados_entre / graus_liberdade_entre / (soma_quadrados_dentro / graus_liberdade_dentro)

        # Passo 5: Calcular o valor p
        valor_p = self.calcular_valor_p(valor_f, graus_liberdade_entre, graus_liberdade_dentro)

        # Passo 6: Interpretar o resultado
        resultado = self.interpretar_resultado(valor_p, alpha)

        # Retornar um dicionário com todas as informações
        return {
            "media_geral": media_geral,
            "soma_quadrados_entre_grupos": soma_quadrados_entre,
            "soma_quadrados_dentro_grupos": soma_quadrados_dentro,
            "graus_liberdade_entre_grupos": graus_liberdade_entre,
            "graus_liberdade_dentro_grupos": graus_liberdade_dentro,
            "valor_f": valor_f,
            "valor_p": valor_p,
            "alpha": alpha,
            "resultado": resultado
        }


class ANOVAWelch(ANOVABase):
    """
    Classe para realizar o teste ANOVA de Welch com base em estatísticas agregadas.

    O teste ANOVA de Welch é uma variação do teste ANOVA que não assume homogeneidade das variâncias
    entre os grupos. Ele é mais robusto quando as variâncias dos grupos são diferentes.

    Métodos:
        calcular_pesos(): Calcula os pesos de cada grupo, que são inversamente proporcionais à variância.
        calcular_media_ponderada(pesos): Calcula a média ponderada das médias dos grupos.
        calcular_soma_quadrados_entre_grupos_welch(pesos, media_ponderada): Calcula a soma dos quadrados entre grupos.
        calcular_graus_liberdade_ajustados(pesos): Calcula os graus de liberdade ajustados.
        realizar_teste(alpha=0.05): Realiza o teste ANOVA de Welch e retorna um dicionário com resultados detalhados.

    Exemplo de uso:
        >>> grupo1 = (24.8, 5, math.sqrt(5.2))
        >>> grupo2 = (30.0, 5, math.sqrt(2.5))
        >>> grupo3 = (22.0, 5, math.sqrt(2.5))
        >>> anova_welch_teste = ANOVAWelch(grupo1, grupo2, grupo3)
        >>> resultados = anova_welch_teste.realizar_teste(alpha=0.01)
        >>> print(resultados)

    Referências:
        - Welch, B. L. (1951). On the comparison of several mean values: An alternative approach. Biometrika.
        - Wikipedia. (2023). Welch's ANOVA. Disponível em: https://en.wikipedia.org/wiki/Welch%27s_ANOVA.
    """

    def calcular_pesos(self):
        """
        Calcula os pesos de cada grupo, que são inversamente proporcionais à variância.

        :return: Lista de pesos para cada grupo.
        """
        pesos = [tamanho / (desvio ** 2) for (_, tamanho, desvio) in self.grupos]
        return pesos

    def calcular_media_ponderada(self, pesos):
        """
        Calcula a média ponderada das médias dos grupos.

        :param pesos: Lista de pesos para cada grupo.
        :return: Média ponderada.
        """
        soma_ponderada = sum(peso * media for (media, _, _), peso in zip(self.grupos, pesos))
        soma_pesos = sum(pesos)
        return soma_ponderada / soma_pesos

    def calcular_soma_quadrados_entre_grupos_welch(self, pesos, media_ponderada):
        """
        Calcula a soma dos quadrados entre grupos para a ANOVA de Welch.

        :param pesos: Lista de pesos para cada grupo.
        :param media_ponderada: Média ponderada.
        :return: Soma dos quadrados entre grupos.
        """
        soma_quadrados_entre = sum(peso * (media - media_ponderada) ** 2 for (media, _, _), peso in zip(self.grupos, pesos))
        return soma_quadrados_entre

    def calcular_graus_liberdade_ajustados(self, pesos):
        """
        Calcula os graus de liberdade ajustados para a ANOVA de Welch.

        :param pesos: Lista de pesos para cada grupo.
        :return: Graus de liberdade ajustados.
        """
        soma_pesos = sum(pesos)
        soma_pesos_quadrados = sum(peso ** 2 for peso in pesos)
        graus_liberdade_ajustados = (soma_pesos ** 2) / (soma_pesos_quadrados - (soma_pesos_quadrados / self.numero_grupos))
        return graus_liberdade_ajustados

    def realizar_teste(self, alpha=0.05):
        """
        Realiza o teste ANOVA de Welch e retorna um dicionário com resultados detalhados.

        :param alpha: Nível de significância (padrão é 0.05).
        :return: Dicionário com resultados detalhados.
        """
        # Passo 1: Calcular os pesos
        pesos = self.calcular_pesos()

        # Passo 2: Calcular a média ponderada
        media_ponderada = self.calcular_media_ponderada(pesos)

        # Passo 3: Calcular soma dos quadrados entre grupos
        soma_quadrados_entre = self.calcular_soma_quadrados_entre_grupos_welch(pesos, media_ponderada)

        # Passo 4: Calcular graus de liberdade ajustados
        graus_liberdade_ajustados = self.calcular_graus_liberdade_ajustados(pesos)

        # Passo 5: Calcular o valor F de Welch
        valor_f = soma_quadrados_entre / (self.numero_grupos - 1)

        # Passo 6: Calcular o valor p
        valor_p = self.calcular_valor_p(valor_f, self.numero_grupos - 1, graus_liberdade_ajustados)

        # Passo 7: Interpretar o resultado
        resultado = self.interpretar_resultado(valor_p, alpha)

        # Retornar um dicionário com todas as informações
        return {
            "media_ponderada": media_ponderada,
            "soma_quadrados_entre_grupos": soma_quadrados_entre,
            "graus_liberdade_ajustados": graus_liberdade_ajustados,
            "valor_f": valor_f,
            "valor_p": valor_p,
            "alpha": alpha,
            "resultado": resultado
        }