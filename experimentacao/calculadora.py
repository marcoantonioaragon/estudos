import math
import scipy.stats as stats
from typing import List, Optional


class CalculadoraAmostralABn:
    """
    Classe avançada para cálculo de tamanho amostral em testes ABn com suporte a:
    - Alocação desigual entre variantes
    - Correções para múltiplas comparações (Bonferroni/Sidak)
    - Métricas numéricas e categóricas
    - Testes unilaterais e bilaterais

    Atributos:
        num_variantes (int): Número total de variantes (controle + variações)
        alfa (float): Nível de significância (default=0.05)
        beta (float): Probabilidade de erro tipo II (default=0.2)
        mde (float): Efeito mínimo detectável (em proporção)
        sentido (str): "unilateral" ou "bilateral"
        tipo_metrica (str): "numerica" ou "categorica"
        desvio_padrao (Optional[float]): Desvio padrão (apenas para métricas numéricas)
        baseline (float): Valor base da métrica
        correcao_multipla (str): "nenhuma", "bonferroni" ou "sidak"
        proporcoes (Optional[List[float]]): Proporções de alocação para cada variante
    """

    def __init__(self,
                 num_variantes: int = 2,
                 alfa: float = 0.05,
                 beta: float = 0.2,
                 mde: float = 0.1,
                 sentido: str = "unilateral",
                 tipo_metrica: str = "numerica",
                 desvio_padrao: Optional[float] = None,
                 baseline: Optional[float] = None,
                 correcao_multipla: str = "nenhuma",
                 proporcoes: Optional[List[float]] = None):
        """
        Inicializa a calculadora com os parâmetros do teste.

        Args:
            proporcoes: Lista com as proporções de alocação para cada variante.
                       Deve somar 1.0. Ex: [0.5, 0.3, 0.2] para 3 variantes.
                       Se None, usa alocação igualitária.
        """
        self.num_variantes = num_variantes
        self.alfa = alfa
        self.beta = beta
        self.mde = mde
        self.sentido = sentido
        self.tipo_metrica = tipo_metrica
        self.desvio_padrao = desvio_padrao
        self.baseline = baseline
        self.correcao_multipla = correcao_multipla
        self.proporcoes = proporcoes
        self.resultado = None

        self._validar_parametros()
        self._processar_proporcoes()

    def _validar_parametros(self):
        """Valida todos os parâmetros de entrada."""
        if self.num_variantes < 2:
            raise ValueError("Número de variantes deve ser ≥ 2")

        if self.tipo_metrica not in ["numerica", "categorica"]:
            raise ValueError(
                "Tipo de métrica deve ser 'numerica' ou 'categorica'")

        if self.sentido not in ["unilateral", "bilateral"]:
            raise ValueError(
                "Sentido do teste deve ser 'unilateral' ou 'bilateral'")

        if self.correcao_multipla not in ["nenhuma", "bonferroni", "sidak"]:
            raise ValueError(
                "Correção múltipla deve ser 'nenhuma', 'bonferroni' ou 'sidak'")

        if self.tipo_metrica == "numerica" and self.desvio_padrao is None:
            raise ValueError(
                "Para métricas numéricas, desvio_padrao é necessário")

        if self.baseline is None:
            raise ValueError(
                "Baseline é necessário para ambos tipos de métrica")

        if self.proporcoes and len(self.proporcoes) != self.num_variantes:
            raise ValueError(
                f"proporcoes deve ter {self.num_variantes} elementos")

    def _processar_proporcoes(self):
        """Processa as proporções de alocação ou define padrão como igualitário."""
        if self.proporcoes is not None:
            if not math.isclose(sum(self.proporcoes), 1.0, rel_tol=1e-9):
                raise ValueError("A soma das proporções deve ser 1.0")
            # Normaliza para garantir soma exata = 1
            self.proporcoes = [p/sum(self.proporcoes) for p in self.proporcoes]
        else:
            # Alocação igualitária padrão
            self.proporcoes = [1/self.num_variantes] * self.num_variantes

    def _aplicar_correcao_multipla(self):
        """Aplica correção para múltiplas comparações."""
        self.alfa_original = self.alfa
        self.num_comparacoes = self.num_variantes - 1

        if self.correcao_multipla == "bonferroni":
            self.alfa_ajustado = self.alfa / self.num_comparacoes
        elif self.correcao_multipla == "sidak":
            self.alfa_ajustado = 1 - \
                (1 - self.alfa) ** (1/self.num_comparacoes)
        else:
            self.alfa_ajustado = self.alfa

    def _calcular_valores_criticos(self):
        """Calcula os valores críticos da distribuição normal."""
        if self.sentido == "bilateral":
            self.z_alfa = stats.norm.ppf(1 - self.alfa_ajustado/2)
        else:
            self.z_alfa = stats.norm.ppf(1 - self.alfa_ajustado)

        self.z_beta = stats.norm.ppf(1 - self.beta)

    def _calcular_numerico(self):
        """Calcula tamanho amostral para métricas numéricas."""
        variancia = self.desvio_padrao ** 2
        efeito = self.mde * self.baseline
        n_minimo = (variancia + variancia) * \
            (self.z_alfa + self.z_beta)**2 / (efeito**2)
        return n_minimo

    def _calcular_categorico(self):
        """Calcula tamanho amostral para métricas categóricas."""
        p1 = self.baseline
        p2 = p1 * (1 + self.mde)
        p_medio = (p1 + p2) / 2
        n_minimo = (
            (self.z_alfa * math.sqrt(2 * p_medio * (1 - p_medio)) +
             self.z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2)))
        )**2 / (p1 - p2)**2
        return n_minimo

    def calcular(self) -> dict:
        """
        Executa o cálculo do tamanho amostral considerando alocação desigual.

        Returns:
            dict: Resultados com tamanhos amostrais totais e por grupo, poder, etc.
        """
        # Passo 1: Aplicar correções e calcular valores críticos
        self._aplicar_correcao_multipla()
        self._calcular_valores_criticos()

        # Passo 2: Calcular tamanho mínimo para o grupo de controle
        if self.tipo_metrica == "numerica":
            n_minimo_controle = self._calcular_numerico()
        else:
            n_minimo_controle = self._calcular_categorico()

        n_minimo_controle = math.ceil(n_minimo_controle)

        # Passo 3: Calcular tamanhos para alocação desigual
        proporcao_controle = self.proporcoes[0]
        n_total = math.ceil(n_minimo_controle / proporcao_controle)

        tamanhos_grupos = []
        for proporcao in self.proporcoes:
            tamanho_grupo = math.ceil(n_total * proporcao)
            tamanhos_grupos.append(tamanho_grupo)

        # Ajuste final para garantir que a soma esteja correta
        diferenca = sum(tamanhos_grupos) - n_total
        if diferenca != 0:
            tamanhos_grupos[-1] -= diferenca

        # Passo 4: Armazenar resultados
        self.resultado = {
            "tamanho_amostral_total": n_total,
            "tamanho_por_grupo": tamanhos_grupos,
            "proporcoes": self.proporcoes,
            "poder_estatistico": 1 - self.beta,
            "alfa_original": self.alfa_original,
            "alfa_ajustado": self.alfa_ajustado if self.correcao_multipla != "nenhuma" else None,
            "correcao_aplicada": self.correcao_multipla,
            "num_comparacoes": self.num_comparacoes,
            "mde": self.mde,
            "baseline": self.baseline,
            "tipo_metrica": self.tipo_metrica
        }

        return self.resultado

    def formatar_resultado(self) -> str:
        """
        Formata os resultados de forma legível para impressão.

        Returns:
            str: Resultados formatados com detalhes do cálculo
        """
        if not self.resultado:
            return "Nenhum cálculo foi executado ainda. Use o método calcular()."

        output = []
        output.append("\n=== RESULTADO DO CÁLCULO AMOSTRAL ===")
        output.append(f"Configuração do Teste:")
        output.append(f"- Tipo de métrica: {self.tipo_metrica.upper()}")
        output.append(f"- Baseline: {self.baseline}")
        output.append(f"- MDE: {self.mde*100:.1f}%")
        output.append(
            f"- Poder estatístico (1-β): {self.resultado['poder_estatistico']*100:.1f}%")

        output.append("\nTamanhos Amostrais:")
        output.append(f"- Total: {self.resultado['tamanho_amostral_total']}")

        for i, (tamanho, proporcao) in enumerate(zip(self.resultado['tamanho_por_grupo'],
                                                     self.resultado['proporcoes'])):
            grupo = "controle" if i == 0 else f"variação {i}"
            output.append(f"  - {grupo}: {tamanho} ({proporcao*100:.1f}%)")

        if self.resultado['correcao_aplicada'] != "nenhuma":
            output.append("\nCorreção para Múltiplas Comparações:")
            output.append(
                f"- Método: {self.resultado['correcao_aplicada'].capitalize()}")
            output.append(f"- α original: {self.resultado['alfa_original']}")
            output.append(
                f"- α ajustado: {self.resultado['alfa_ajustado']:.6f}")
            output.append(
                f"- Número de comparações: {self.resultado['num_comparacoes']}")

        return "\n".join(output)
