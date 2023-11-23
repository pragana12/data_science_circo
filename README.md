# Introdução

Este projeto de Análise e Previsão de Dados, foi elaborado para entender as dificuldades do Circo em ter suas metas de Lucro alcançadas durante sua turner. 

Este repositório contém scripts Python voltados para análise exploratória, correlação, regressão linear e identificação de outliers em dados relacionados a performances circenses. Esses scripts são projetados para fornecer insights valiosos e previsões relevantes com base em dados específicos do circo no ano de 2023.

Foi utilizado o banco de dados MySQL dos detalhes do faturamento do circo em relação as cidades por onde passou, mas no repositorio contém além do backup do banco SQL, também possui os dados em excel.


O banco de dados foi tratado, de forma remover strings (Transformando todos os dados em dados númericos) e adicionando informações extras como PIB das cidades e numero de Habitantes.


# Conteúdo do Repositório

1. Script previsao_lucro.py

Realiza a previsão de lucro utilizando um modelo de regressão linear.
Conecta-se a um banco de dados MySQL para obter dados de treinamento.
Permite a entrada de novos dados para previsão de lucro e lucro de estreia.

2. Script analise_outliers.py

Explora detalhes de uma cidade específica do circo.
Identifica outliers em diversas variáveis, incluindo lucro, PIB, salário médio, dias de evento e número de habitantes.

3. Script analise_correlacao_regressao.py

Realiza análises estatísticas, como correlação entre variáveis e regressão linear múltipla.
Exibe visualizações, incluindo gráfico de dispersão, histograma de lucro e gráfico comparativo por cidade.


# Como Utilizar

Para utilizar esses scripts, siga as instruções abaixo:

## Configuração do Ambiente:

1. Certifique-se de ter Python instalado no seu ambiente.

2. Instale as bibliotecas necessárias executando pip install -r requirements.txt.

## Configuração do Banco de Dados:

1. Certifique-se de ter um banco de dados MySQL configurado com os dados do circo.

## Execução dos Scripts:

1. Execute os scripts utilizando um ambiente Python."


## Primeiro começamos com a indentificação de Outliers

# identificacao_outliers.py

"""
Script de Identificação de Outliers

Este script realiza a identificação de outliers em diferentes variáveis do conjunto de dados do circo.

Principais Funcionalidades:
1. Exploração detalhada de uma cidade específica (opcional).
2. Identificação de outliers em variáveis como LUCRO, PIB, SALARIO_MEDIO, DIAS_DE_EVENTO e HABITANTES.

"""

# Importando bibliotecas necessárias

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import mysql.connector

# Função para explorar detalhes de uma cidade específica (opcional)

    def explorar_cidade_outlier(df, cidade_outlier):
    """
    Explora detalhes de uma cidade específica.

    Args:
    - df: DataFrame do Pandas contendo os dados do circo.
    - cidade_outlier (str): Nome da cidade a ser explorada.

    """
    cidade_detalhada = df[df['CIDADE'] == cidade_outlier]
    print(f"\nDetalhes da Cidade Outlier ({cidade_outlier}):")
    print(cidade_detalhada)

# Função para identificar outliers em uma variável específica

    def identificar_outliers(df, variavel):
    """
    Identifica outliers em uma variável específica e exibe informações relevantes.

    Args:
    - df: DataFrame do Pandas contendo os dados do circo.
    - variavel (str): Nome da variável para identificação de outliers.

    """
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

# Realizar análises de identificação de outliers

    query = "SELECT * FROM dados_circo"
    df_circo = pd.read_sql(query, conexao)

# Explorar detalhes de uma cidade específica (opcional)

    explorar_cidade_outlier(df_circo, '3')  # 3 é equivalente a 3ª cidade do banco de dados.

# Identificar outliers em diferentes variáveis

    identificar_outliers(df_circo, 'LUCRO')
    identificar_outliers(df_circo, 'PIB')
    identificar_outliers(df_circo, 'SALARIO_MEDIO')
    identificar_outliers(df_circo, 'DIAS_DE_EVENTO')
    identificar_outliers(df_circo, 'HABITANTES')

# Fechar a conexão com o banco de dados

    conexao.close()


## Após indentificar os Outliers, fazemos uma análise exploratória para identificar a natureza dos dados, como a correlação dos dados e ter uma visão geral do negócio.

# analise_correlacao_regressao_outlier.py

"""
Script de Análise de Correlação, Regressão Linear e Identificação de Outliers

Este script realiza análises de correlação entre variáveis, regressão linear e identificação de outliers no conjunto de dados do circo.

Principais Funcionalidades:
1. Obtém dados do banco de dados MySQL.
2. Realiza análise de correlação entre variáveis.
3. Exibe gráficos e estatísticas descritivas para análise visual.
4. Realiza análise de regressão linear.
5. Identifica cidades com lucro considerado outlier.

"""

# Importando bibliotecas necessárias

    import pandas as pd
    import matplotlib.pyplot as plt
    import mysql.connector
    import seaborn as sns
    import statsmodels.api as sm

# Função para obter dados do banco de dados

    def obter_dados_do_banco():
        """
        Obtém os dados do banco de dados MySQL.

        Returns:
        - df: DataFrame do Pandas contendo os dados do circo

        """
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dados_circo"
        )

        query = "SELECT * FROM dados_circo"
        df = pd.read_sql(query, conexao)
        conexao.close()
        return df

# Função para análise de correlação

    def analise_correlacao():
        """
        Realiza análise de correlação entre variáveis.

        """
        dados = obter_dados_do_banco()
        
        df = dados

        correlacao = df[['LUCRO', 'PIB']].corr()
        print(correlacao)

        # Criar e Exibir o mapa de calor
        correlacao_total = df.corr()
        sns.heatmap(correlacao_total, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Mapa de Calor da Correlação entre Variáveis')
        plt.show()

# Função para análise de regressão

    def analise_regressao():
        """
        Realiza análise de regressão linear.

        """
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

# Função para análise geral com gráficos

    def analises_geral():
        """
        Realiza análises gerais com gráficos.

        """
        df = obter_dados_do_banco()
        
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


# Executar as análises
    analise_correlacao()
    analises_geral()
    analise_regressao()


## Agora com uma Análise bem feita, podemos identificar os Outliers e os dados que mais influenciam no Lucro do circo pra preparar o banco de dados para ser utilizado nas técnicas de machine learning e tentar prevê o resultado do circo na próxima cidade


# previsao_lucro.py

"""
Script de Previsão de Lucro

Este script realiza a previsão de lucro com base em um modelo de regressão linear treinado usando dados do circo.

Principais Funcionalidades:
1. Conectar ao banco de dados MySQL.
2. Carregar dados do banco de dados.
3. Treinar um modelo de regressão linear.
4. Solicitar novos dados para previsão.
5. Realizar previsão de LUCRO e LUCRO_ESTREIA com base nos novos dados.
6. Exibir as previsões.

"""

# Importando bibliotecas necessárias

    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import mysql.connector

# Conectar ao banco de dados MySQL

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dados_circo"
        )
    except mysql.connector.Error as err:
        print(f"Erro na conexão ao banco de dados: {err}")

# Carregar dados do banco de dados

    query = "SELECT * FROM dados_circo"
    df_treinamento = pd.read_sql(query, conexao)

# Selecionar as colunas relevantes para treinamento

    colunas_treinamento = ['HABITANTES', 'PIB']
    X = df_treinamento[colunas_treinamento]

# Selecionar as colunas alvo para previsão

    y = df_treinamento[['LUCRO', 'LUCRO_ESTREIA']]

# Dividir os dados em conjuntos de treinamento e teste

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo de regressão linear

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

# Solicitar novos dados para previsão

    novo_habitantes = float(input('Informe o número de habitantes: '))
    novo_pib = float(input('Informe o PIB: '))

# Prever LUCRO e LUCRO_ESTREIA com base nos novos dados

    nova_previsao = modelo.predict([[novo_habitantes, novo_pib]])

    previsao_lucro = nova_previsao[0][0]
    previsao_lucro_estreia = nova_previsao[0][1]

# Exibir as previsões

    print(f'\nPrevisão de LUCRO: R${previsao_lucro:.2f}')
    print(f'Previsão de LUCRO ESTREIA: %{previsao_lucro_estreia:.2f}')

# Fechar a conexão com o banco de dados

    conexao.close()


# Conclusão

Estes scripts foram desenvolvidos para fornecer ferramentas analíticas avançadas e previsões relevantes para dados relacionados ao circo. Espero que esses recursos sejam úteis para análises aprofundadas e tomada de decisões informadas.

Agradeço por explorar este repositório e espero que essas ferramentas proporcionem uma experiência enriquecedora na análise de dados. 

Se houver dúvidas ou sugestões, sinta-se à vontade para entrar em contato.

Divirta-se explorando os dados.
