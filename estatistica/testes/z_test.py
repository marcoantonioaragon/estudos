import math

class TesteZ:
    def __init__(self, media, desvio_padrao, tamanho, media_populacional):
        self.media = media
        self.desvio_padrao = desvio_padrao
        self.tamanho = tamanho
        self.media_populacional = media_populacional

    def calcular_estatistica_z(self):
        return (self.media - self.media_populacional) / (self.desvio_padrao / math.sqrt(self.tamanho))

    def calcular_valor_p(self, z):
        def cdf_normal(x):
            return (1 + math.erf(x / math.sqrt(2))) / 2
        return 2 * (1 - cdf_normal(abs(z)))

    def realizar_teste(self, alpha=0.05):
        z = self.calcular_estatistica_z()
        valor_p = self.calcular_valor_p(z)
        resultado = "Há diferenças significativas (rejeitamos a hipótese nula)." if valor_p < alpha else "Não há diferenças significativas (não rejeitamos a hipótese nula)."
        return {
            "teste_utilizado": "Teste Z",
            "estatistica": z,
            "valor_p": valor_p,
            "alpha": alpha,
            "resultado": resultado
        }