import datetime
import pandas as pd
import streamlit as st
import yfinance as yf
from ta.momentum import date
from ta.volatility import BollingerBands
from ta.trend import MACD, EMAIndicator, SMAIndicator
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

st.title("Web App com Inteligência Artificial para Análise e Previsão de Preços de Criptomoedas em Tempo Real")

st.sidebar.header("Análise de Criptoativos")
st.sidebar.info("Matheus dos Anjos")
st.sidebar.info("Github: https://github.com/mt076/Projetos-")

#Espaço em branco para ajuste de tamanho
st.sidebar.markdown("&#8203;" * 100)

def selecione_pagina():

    option = st.sidebar.selectbox('Selecione o Que Deseja Fazer', ['Vizualizar Gráficos', 'Visualizar Tabela', 'Fazer Previsões'])

    if option == 'Vizualizar Gráficos':
        indicadores_tecnicos()

    elif option == 'Vizualizar Tabela de Dados':
        imprime_tabela()

    else:
        previsoes()

@st.cache_resource

def donwload_dados(ticker, start_date, end_date):
    dados = yf.donwload(ticker, start = start_date, end = end_date, progress = False)
    return dados

option = st.sidebar.selectbox("Selecione a Criptomoeda:", ['Bitcoin-USD', 'Ethereum-USD', 'Solana-USD', 'Chainlink-USD'])

option = option.upper()

print(option)

num_pontos_dados = st.sidebar.number_input('Número de Registros Para Treinar o Modelo', value = 3000)

today = datetime.date.today()

data_padrao = today - datetime.timedelta(days = num_pontos_dados)

start_date = st.sidebar.date_input('Selecione Uma Data Inicial', value = data_padrao)
end_date = st.sidebar.date_input('Selecione Uma Data Final', today)

if option=='BITCOIN-USD':
    st.sidebar.sucess('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (start_date, end_date))
    stock = "BTC-USD"
elif option=='ETHEREUM-USD':
    st.sidebar.sucess('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (start_date, end_date))
    stock = "ETH-USD"
elif option=='SOLANA-USD':
    st.sidebar.sucess('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (start_date, end_date))
    stock = "SOL-USD"
elif option=='CHAINLINK-USD':
    st.sidebar.sucess('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (start_date, end_date))
    stock = "LINK-USD"

df = donwload_dados(stock, start_date, end_date)

def indicadores_tecnicos():

    st.header('Indicadores Técnicos')

    option = st.radio('Selecione Um Indicador Técnico Para Vizualizar', ['Preço de Fechamento',
                                                                         'BollingerBands',
                                                                         'Moving Average Convergence Divergence (MACD)',
                                                                         'Relative Strength Indicator (RSI)',
                                                                         'Simple Moving Average (SMA)',
                                                                         'Exponential Moving Average (EMA)'])
indicador_bb = BollingerBands(df.Close)
df_bb = df
df_bb['bb_maximo'] = indicador_bb.bollinger_hband()
df_bb['bb_minimo'] = indicador_bb.bollinger_lband()
df_bb = df_bb[['Close', 'bb_maximo', 'bb_minimo']]

macd = MACD(df.Close).macd()
rsi = RSIIndicator(df.Close).rsi()
sma = SMAIndicator(df.Close, window=14).sma_indicator()
ema = EMAIndicator(df.Close).ema_indicator()

if option == 'Preço de Fechamento':
    st.write('Preço de Fechamento')
    st.line_chart(df.Close)
elif option == 'BollingerBands':
    st.write('BollingerBands')
    st.line_chart(df_bb)
elif option == 'Moving Average Convergence Divergence (MACD)':
    st.write('Moving Average Convergence Divergence (MACD)')
    
    #Se necessário, instale: pip install PyQt5
    import matplotlib.pyplot as plt
    df['MACD'] = macd_object.macd()
    df['Signal_Line'] = macd_object.macd_signal()
    df['MACD_Diff'] = macd_object.macd_diff()

    plt.figure(figsize=(14,7))

    plt.subplot(2, 1, 1)
    plt.plot(df['Close'], label='Close Price')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(df['MACD'], label='MACD', color='blue')
    plt.plot(df['Signal_Line'], label='Sinal', color='magenta')
    plt.bar(df.index, df['macd_Diff'], label='Histograma', color='black', alpha=0.8)
    st.pyplot(plt)

elif option == 'Relative Strength Indicator (RSI)':
    st.write('Relative Strength Indicator (RSI)')
    st.line_chart(rsi)
elif option == 'Simple Moving Average (SMA)':   
    st.write('Simple Moving Average (SMA)')
    st.line_chart(sma)
else:
    st.write('Exponential Moving Average (EMA)')
    st.line_chart(ema)

def imprime_tabela():
    st.header('Tabela de Criptomoedas')
    st.dataframe(df.tail(10))

def previsoes():
    num = st.number_input('Fazer a Previsão de Quantos Dias no Futuro?', value=1, min_value=1, max_value=30)
    num = int(num)

    if st.button('Previsão') and num > 0:
        inteligencia_artificial(num)
    elif num <= 0:
        st.error('Por favor, insira um número de dias maior que 0 para previsão.')
    
def inteligencia_artificial(num):

    df1 = df[['Close']].copy()

    df1['preds'] = df1.Close.shift(-num)

    x = df.drop(['preds'], axis=1).values
    y = df.preds.values[:-num]

    x_train, x_test, y_train, y_test = train_test_split(x[:-num], y, test_size = .2, random_state = 7)
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaler = scaler.transform(x_test)

    modelo = LinearRegression().fit(x_train_scaled, y_train)

    preds = modelo.predict(x_test_scaled)

    st.text(f'Previsão com Acurácia de: {r2_score(y_test, preds)}')

    x_forecast = df1.drop(['preds'], axis=1).values[-num:]
    x_forecast_scaled = scaler.transform(x_forecast)
    forecast_pred = modelo.predict(x_forecast_scaled)

    day = 1
    for i in forecast_pred:
        st.text(f'Previsão do Preço de Fechamento no Dia {day} é: {i}')
        day += 1

st.caption('Desenvolvido por Matheus dos Anjos com Base na Aula da Data Science Academy')

if __name__ == '__main__':
    selecione_pagina()