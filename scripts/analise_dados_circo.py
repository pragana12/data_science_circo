# Analises de : Correlação, Regressão liner, Indentificar Outlier
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns



def obter_dados_do_banco():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dados_circo"
    )

    query = "SELECT * FROM dados_circo"
    df = pd.read_sql(query, conexao)
    #print(df)

    conexao.close()
    return df

def analise_correlacao():
    dados = obter_dados_do_banco()
    
    df = dados

    correlacao = df[['LUCRO', 'PIB']].corr()
    print(correlacao)

    # Criar e Exibir o mapa de calor
    correlacao_total = df.corr()
    sns.heatmap(correlacao_total, annot=True, cmap='coolwarm', fmt=".2f")
    plt.show()

def analise_regressao():
    dados = obter_dados_do_banco()

    # Variáveis independentes (X)
    X = dados[['HABITANTES', 'PIB', 'DIAS_DE_EVENTO']]

    # Adiciona constante para o termo independente na regressão
    X = sm.add_constant(X)

    # Variável dependente (y)
    y = dados['LUCRO']

    # Cria e ajusta o modelo de regressão
    modelo = sm.OLS(y, X).fit()

    # Exibe os resultados da regressão
    print(modelo.summary())


def analises_geral():

    df = obter_dados_do_banco()
    
    #--------------------------------------------------
    # Gráfico de dispersão com linha de regressão
    sns.lmplot(x='HABITANTES', y='LUCRO', data=df)
    plt.xlabel('HABITANTES')
    plt.ylabel('LUCRO')
    plt.title('Gráfico de Dispersão com Linha de Regressão')
    plt.show()

    # Histograma de lucro
    plt.hist(df['LUCRO'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Histograma de Lucro')
    plt.show()

    # Gráfico de barras comparativo por cidade
    sns.barplot(x='CIDADE', y='LUCRO', data=df, ci=None)
    plt.title('Comparação de Lucro por Cidade')
    plt.xticks(rotation=45)
    plt.show()

    # Visualização 3: Histograma
    plt.hist(df['HABITANTES'], bins='auto', alpha=0.7, rwidth=0.85)
    plt.xlabel('HABITANTES')
    plt.ylabel('Frequência')
    plt.title('Histograma de HABITANTES')
    plt.show()

    # Identificar cidades com lucro acima de 75% do IQR
    limite_superior = df['LUCRO'].quantile(0.75) + 1.5 * (df['LUCRO'].quantile(0.75) - df['LUCRO'].quantile(0.25))
    outliers = df[df['LUCRO'] > limite_superior]
    print('Cidades com lucro considerado outlier:')
    print(outliers)

    # Estatísticas descritivas
    desc_estatisticas = df.describe()
    print(desc_estatisticas)


analise_correlacao()
analises_geral()
analise_regressao()

