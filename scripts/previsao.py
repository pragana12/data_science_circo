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
#novo_dias_evento = float(input('Informe o número de dias de evento: '))

# Prever LUCRO e LUCRO ESTREIA com base nos novos dados
nova_previsao = modelo.predict([[novo_habitantes, novo_pib]])

previsao_lucro = nova_previsao[0][0]
previsao_lucro_estreia = nova_previsao[0][1]


print(f'\nPrevisão de LUCRO: R${previsao_lucro:.2f}')
print(f'Previsão de LUCRO ESTREIA: %{previsao_lucro_estreia:.2f}')

# Fechar a conexão com o banco de dados
conexao.close()