# Testes de Normalidade em Python

Este projeto implementa uma classe em Python para realizar testes de normalidade em conjuntos de dados. Ele inclui três testes estatísticos:
1. **Shapiro-Wilk** (com aproximação de Royston para amostras grandes).
2. **Anderson-Darling**.
3. **Kolmogorov-Smirnov**.

Além disso, o projeto utiliza um **ensemble** para combinar os resultados dos testes e decidir se os dados são normais com base em uma regra de maioria.

---

## Introdução

O teste de normalidade é uma etapa crucial em muitas análises estatísticas, pois muitas técnicas (como testes paramétricos) assumem que os dados seguem uma distribuição normal. Este projeto implementa três testes de normalidade comuns e combina seus resultados em um **ensemble** para aumentar a confiabilidade da decisão.

---

## Instalação e Requisitos

### Requisitos
- Python 3.8 ou superior.
- Bibliotecas padrão do Python: `random`, `math`.

### Instalação
Este projeto não requer instalação de bibliotecas externas. Basta copiar o código para o seu ambiente Python.

---

## Uso da Classe `TesteNormalidade`

A classe `TesteNormalidade` é o núcleo do projeto. Ela permite gerar dados normalmente distribuídos e realizar testes de normalidade.

### Exemplo Básico

```python
# Exemplo básico de uso
from teste_normalidade import TesteNormalidade

# Definindo parâmetros
media = 0.0455
desvio_padrao = 1
tamanho_amostra = 1000

# Criando uma instância da classe
teste = TesteNormalidade(media, desvio_padrao, tamanho_amostra)

# Realizando o ensemble de testes
resultados = teste.ensemble_normalidade(alpha=0.05)

# Exibindo os resultados
print("Resultados detalhados:")
print(resultados)
```
### Exemplo com Alpha Personalizado

```python
# Exemplo com alpha personalizado
resultados = teste.ensemble_normalidade(alpha=0.01)  # Alpha = 0.01
print("Resultados com alpha = 0.01:")
print(resultados)
```
---

## Métodos da Classe

### Método `ensemble_normalidade`
Realiza os três testes de normalidade e combina os resultados em um ensemble.

### Parâmetros
`alpha` (float, opcional): Nível de significância. Padrão é 0.05.

### Retorno
Um dicionário contendo:
- Estatísticas e p-valores de cada teste.
- Decisão de normalidade de cada teste.
- Decisão final do ensemble.

### Exemplo de saída

```python
{
    "tamanho_amostra": 1000,
    "alpha": 0.05,
    "shapiro_wilk": {
        "aplicavel": True,
        "estatistica": 0.987,
        "p_valor": 0.456,
        "normal": True,
    },
    "anderson_darling": {
        "estatistica": 0.123,
        "normal": True,
    },
    "kolmogorov_smirnov": {
        "estatistica": 0.045,
        "normal": True,
    },
    "decisao_final": "Os dados são considerados normais (ensemble)."
}
```

### Métodos Individuais de Teste
#### realizar_teste_shapiro(alpha=0.05):
- Realiza o teste de Shapiro-Wilk.
- Retorna a estatística W e o p-valor.

#### realizar_teste_anderson_darling(alpha=0.05):

Realiza o teste de Anderson-Darling.
Retorna a estatística A² e a decisão de normalidade.

#### realizar_teste_kolmogorov_smirnov(alpha=0.05):
- Realiza o teste de Kolmogorov-Smirnov.
- Retorna a estatística D e a decisão de normalidade.

---

## Limitações e Considerações

### 1. Aproximação de Royston:

- Funciona bem para amostras até 5000 observações.
- Para amostras maiores, o teste de Shapiro-Wilk não é aplicável.

### 2. Valores Críticos Simplificados:

- Os valores críticos dos testes de Anderson-Darling e Kolmogorov-Smirnov são simplificados e podem não ser precisos para todos os casos.

### 3. Desempenho:

- Para amostras muito grandes (n > 100000), o desempenho pode ser afetado devido à complexidade dos cálculos.

---

## Exemplo Completo de Uso

Aqui está um exemplo completo de uso da classe `TesteNormalidade`:

```python
from teste_normalidade import TesteNormalidade

# Definindo parâmetros
media = 0.0455
desvio_padrao = 1
tamanho_amostra = 1000

# Criando uma instância da classe
teste = TesteNormalidade(media, desvio_padrao, tamanho_amostra)

# Realizando o ensemble de testes
resultados = teste.ensemble_normalidade(alpha=0.01)

# Exibindo os resultados
print("Resultados detalhados:")
print(f"Tamanho da amostra: {resultados['tamanho_amostra']}")
print(f"Nível de significância (alpha): {resultados['alpha']}")
print("\nTeste de Shapiro-Wilk:")
print(f"Aplicável: {resultados['shapiro_wilk']['aplicavel']}")
if resultados["shapiro_wilk"]["aplicavel"]:
    print(f"Estatística W: {resultados['shapiro_wilk']['estatistica']}")
    print(f"P-valor: {resultados['shapiro_wilk']['p_valor']}")
print(f"Normal: {resultados['shapiro_wilk']['normal']}")
print("\nTeste de Anderson-Darling:")
print(f"Estatística A²: {resultados['anderson_darling']['estatistica']}")
print(f"Normal: {resultados['anderson_darling']['normal']}")
print("\nTeste de Kolmogorov-Smirnov:")
print(f"Estatística D: {resultados['kolmogorov_smirnov']['estatistica']}")
print(f"Normal: {resultados['kolmogorov_smirnov']['normal']}")
print("\nDecisão final:")
print(resultados["decisao_final"])
```

---


## Referências e Fundamentação Teórica

### Teste de Shapiro-Wilk
- **Objetivo:** Verificar se uma amostra segue uma distribuição normal.
- **Referência:** Shapiro, S. S., & Wilk, M. B. (1965). An analysis of variance test for normality (complete samples). Biometrika, 52(3-4), 591-611.

### Teste de Anderson-Darling
- **Objetivo:** Comparar a distribuição empírica dos dados com uma distribuição teórica (normal).
- **Referência:** Anderson, T. W., & Darling, D. A. (1954). A test of goodness of fit. Journal of the American Statistical Association, 49(268), 765-769.

### Teste de Kolmogorov-Smirnov
- **Objetivo:** Testar se uma amostra segue uma distribuição específica.
- **Referência:** Kolmogorov, A. N. (1933). Sulla determinazione empirica di una legge di distribuzione. Giornale dell'Istituto Italiano degli Attuari, 4, 83-91.

### Aproximação de Royston
- **Objetivo:** Estender o teste de Shapiro-Wilk para amostras grandes.
- **Referência:** Royston, P. (1992). Approximating the Shapiro-Wilk W-test for non-normality. Statistics and Computing, 2(3), 117-119.