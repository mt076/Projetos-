import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import random
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
random.seed(SEED)

print("\nCarregando os Dados")

df = pd.read_csv("C:/Users/conta/OneDrive/Desktop\Projetos-/Projetos Python/Projetos Python para Dados Financeiros/p3_prev_acoes/dataset.csv")

eps = df['eps'].values.reshape(-1, 1)

def cria_dataset(data, look_back = 1):
    X, Y = [], []

    for i in range(len(data) - look_back):

        a = data[i:(i + look_back), 0]
        X.append(a)
        Y.append(data[i + look_back, 0])

    return np.array(X), np.array(Y)

indice = int(len(eps) * 0.8)
dados_treino, dados_teste = eps[0:indice, :], eps[indice:len(eps), :]

scaler = MinMaxScaler(feature_range = (0, 1))

dados_treino_norm = scaler.fit_transform(dados_treino)
dados_teste_norm = scaler.transform(dados_teste)

look_back = 1
X_treino, y_treino = cria_dataset(dados_treino_norm, look_back)
X_teste, y_teste = cria_dataset(dados_teste_norm, look_back)

X_treino = np.reshape(X_treino, (X_treino.shape[0], X_treino.shape[1], 1))
X_teste = np.reshape(X_teste, (X_teste.shape[0], X_teste.shape[1], 1))

modelo = tf.keras.models.Sequential([tf.keras.layers.LSTM(50, input_shape = (look_back, 1)),
                                     tf.keras.layers.Dense(1)])

modelo.compile(optimizer = 'adam', loss = 'mean_squared_error')

print("\nTreinando o Modelo")

try:
    modelo.fit(X_treino, y_treino, epochs = 50, batch_size = 1, verbose = 1)
except KeyboardInterrupt:
    print("Treinamento interrompido pelo usuário.")

try:
    previsao_treino = modelo.predict(X_treino)
    previsao_teste = modelo.predict(X_teste)
except KeyboardInterrupt:
    print("Previsões interrompidas pelo usuário.")
    exit()

previsao_treino = scaler.inverse_transform(previsao_treino)
y_treino_rescaled = scaler.inverse_transform([y_treino])
previsao_teste = scaler.inverse_transform(previsao_teste)
y_teste_rescaled = scaler.inverse_transform([y_teste])

train_score = np.sqrt(mean_squared_error(y_treino_rescaled[0], previsao_treino[:, 0]))
print(f"\nRMSE Treinamento: {train_score:.2f}")

test_score = np.sqrt(mean_squared_error(y_teste_rescaled[0], previsao_teste[:, 0]))
print(f"RMSE Teste: {test_score:.2f}")

original_train_data_index = df['ano'][look_back:look_back + len(y_treino_rescaled[0])]
original_test_data_index = df['ano'][len(y_treino_rescaled[0]) + 2 * look_back:len(y_treino_rescaled[0]) + 2 * look_back + len(y_teste_rescaled[0])]

predicted_train_data_index = df['ano'][look_back:look_back + len(previsao_treino)]
predicted_test_data_index = df['ano'][len(y_treino_rescaled[0]) + 2 * look_back:len(y_treino_rescaled[0]) + 2 * look_back+len(previsao_teste)]

plt.figure(figsize=(15, 6))
plt.plot(original_train_data_index, y_treino_rescaled[0], label="Dados de Treino Originais", color="blue", linestyle='-')
plt.plot(predicted_train_data_index, previsao_treino[:, 0], label="Previsões em Treino", color="green", linestyle='--')
plt.plot(original_test_data_index, y_teste_rescaled[0], label="Dados de Teste Originais", color="black", linestyle='-')
plt.plot(predicted_test_data_index, previsao_teste[:, 0], label="Previsões em Teste", color="red", linestyle='--')
plt.title("EPS Real vs. EPS Previsto com IA")
plt.xlabel("Ano")
plt.ylabel("EPS")
plt.legend()
plt.grid(True)
plt.show()

last_data = dados_teste_norm[-look_back:]
last_data = np.reshape(last_data, (1, look_back, 1))


lista_previsoes = []

for _ in range(2):  

    prediction = modelo.predict(last_data)

    lista_previsoes.append(prediction[0, 0])

    last_data = np.roll(last_data, shift = -1)
    last_data[0, look_back - 1, 0] = prediction

lista_previsoes_rescaled = scaler.inverse_transform(np.array(lista_previsoes).reshape(-1, 1))

print(f"\nPrevisão do EPS Para 2024: {lista_previsoes_rescaled[0, 0]:.2f}")
print(f"Previsão do EPS Para 2025: {lista_previsoes_rescaled[1, 0]:.2f}")

print("Fim do Projeto! - Matheus dos Anjos")


