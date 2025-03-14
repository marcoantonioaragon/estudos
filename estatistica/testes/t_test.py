import math


class TesteT:
    def __init__(self, media, desvio_padrao, tamanho, media_populacional):
        self.media = media
        self.desvio_padrao = desvio_padrao
        self.tamanho = tamanho
        self.media_populacional = media_populacional

    def calcular_estatistica_t(self):
        return (self.media - self.media_populacional) / (self.desvio_padrao / math.sqrt(self.tamanho))

    def calcular_valor_p(self, t):
        def cdf_t(x, graus_liberdade):
            # Implementação da CDF da distribuição t
            pass
        graus_liberdade = self.tamanho - 1
        return 2 * (1 - cdf_t(abs(t), graus_liberdade))

    def realizar_teste(self, alpha=0.05):
        t = self.calcular_estatistica_t()
        valor_p = self.calcular_valor_p(t)
        resultado = "Há diferenças significativas (rejeitamos a hipótese nula)." if valor_p < alpha else "Não há diferenças significativas (não rejeitamos a hipótese nula)."
        return {
            "teste_utilizado": "Teste T",
            "estatistica": t,
            "valor_p": valor_p,
            "alpha": alpha,
            "resultado": resultado
        }