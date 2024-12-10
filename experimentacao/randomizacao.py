import pandas as pd
import random
import numpy as np
# import boto3


class RandomizacaoBatch:
    def __init__(self, id_experimento):
        self.id_experimento = id_experimento

    def executa_randomizacao(self, dados, coluna_id):
        """
        Executa a randomização de uma base.

        Args:
            dados (pd.DataFrame): DataFrame com os dados.
            coluna_id (str): Nome da coluna a ser randomizada.

        Returns:
            pd.DataFrame: DataFrame com a coluna 'variante' adicionada.
        """

        # Cria a coluna 'variante' com valores aleatórios 'A' ou 'B'
        dados['variante'] = [random.choice(['A', 'B'])
                             for _ in range(len(dados))]

        return dados

    def executa_randomizacao_estratificada(self, dados, coluna_id, coluna_categorias):
        """
        Executa a randomização estratificada de uma base que tenha categorias.

        Args:
            dados (pd.DataFrame): DataFrame com os dados.
            coluna_id (str): Nome da coluna a ser randomizada.
            coluna_categorias (str): Nome da coluna com as categorias para estratificação.

        Returns:
            pd.DataFrame: DataFrame com a coluna 'variante' adicionada.
        """

        # Agrupa os dados por categoria e cria uma lista de DataFrames para cada estrato
        estratos = dict(list(dados.groupby(coluna_categorias)))

        # Randomiza os dados dentro de cada estrato
        for categoria, estrato in estratos.items():
            estrato['variante'] = [random.choice(
                ['A', 'B']) for _ in range(len(estrato))]
            estratos[categoria] = estrato

        # Concatena os estratos para formar o DataFrame final
        dados = pd.concat(estratos.values(), ignore_index=True)

        return dados

    def enviar_para_datamesh(self, dados):
        """
        Envia o DataFrame para o Data Mesh via Glue Job.

        Args:
            df (pd.DataFrame): DataFrame a ser enviado.
        """

        # # Configurações do Glue Job (substitua pelos seus valores)
        # glue = boto3.client('glue')
        # job_name = 'seu_glue_job'
        # input_path = 's3://seu-bucket/input.parquet'
        # output_path = 's3://seu-bucket/output.parquet'

        # # Cria um Job no Glue para processar o DataFrame
        # response = glue.start_job_run(
        #     JobName=job_name,
        #     Arguments={
        #         '--input_path': input_path,
        #         '--output_path': output_path,
        #         '--experiment_id': str(self.id_experimento)
        #     }
        # )

        # print(f"Job iniciado com JobRunId: {response['JobRunId']}")
        print(f"Job iniciado com JobRunId: response JobID")
