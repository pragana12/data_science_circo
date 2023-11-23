import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector



# Função para explorar Gurupi em mais detalhes
def explorar_cidade_outlier(df, cidade_outlier):
    cidade_detalhada = df[df['CIDADE'] == cidade_outlier]
    print(f"\nDetalhes da Cidade Outlier ({cidade_outlier}):")
    print(cidade_detalhada)


# Função para identificar outliers em outras variáveis
def identificar_outliers(df, variavel):
    plt.figure(figsize=(8, 6))
    sns.boxplot(df[variavel])
    plt.title(f'Boxplot para Identificação de Outliers em {variavel}')
    plt.show()

    limite_superior = df[variavel].quantile(0.75) + 1.5 * (df[variavel].quantile(0.75) - df[variavel].quantile(0.25))
    outliers = df[df[variavel] > limite_superior]
    print(f'\nCidades com {variavel.lower()} considerado outlier:')
    print(outliers)

# Carregar dados do banco de dados
try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dados_circo"
    )

except mysql.connector.Error as err:
    print(f"Erro na conexão ao banco de dados: {err}")


query = "SELECT * FROM dados_circo"
df_circo = pd.read_sql(query, conexao)



# Realizar análises ( as cidades estão enumeradas de 1 á 12 conforme Banco de dados)
#explorar_cidade_outlier(df_circo, '3')


identificar_outliers(df_circo, 'LUCRO')
identificar_outliers(df_circo, 'PIB')
identificar_outliers(df_circo, 'SALARIO_MEDIO')
identificar_outliers(df_circo, 'DIAS_DE_EVENTO')
identificar_outliers(df_circo, 'HABITANTES')

# Fechar a conexão com o banco de dados
conexao.close()