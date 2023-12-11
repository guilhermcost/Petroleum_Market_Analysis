import streamlit as st
import pandas as pd
import plotly.express as px

oil_data = pd.read_csv('datasets/abril.csv', sep = ';', encoding= 'latin-1') # lendo os dados

## --------------------------------------------------------
## --------------- LIMPEZA DOS DADOS ----------------------
## --------------------------------------------------------

## Passo 1: Descarte da coluna "DATA DE NOTIFICAÇÃO DE DESCOBERTA", pois ela não será utilizada nesta análise
oil_data.drop(oil_data.columns[-1], axis = 1, inplace = True)

## Passo 2: Renomear colunas que possuem acentoes, espaços e cedilhas
oil_data.columns = ['Poco_ANP', 'Bloco', 'Bacia', 'Estado', 'Ambiente', 'Operador', 'Inicio', 'Conclusao', 'Notificacao']

#Passo 3: Remoção de linhas com dados completamente ausentes - Linha 1730 e 1731
oil_data.drop([1730, 1731], inplace = True)
oil_data.reset_index(drop=True, inplace= True)

#Passo 4: Substituindo valores ausentes por valor desconhecido
oil_data['Operador'].fillna('Desconhecido', inplace = True)

#Passo 5: Troca de tipos de Dados das colunas "Inicio" e "Conclusao" para Datetime

oil_data['Inicio'] = pd.to_datetime(oil_data['Inicio'], format = '%d/%m/%Y')
oil_data['Conclusao'] = pd.to_datetime(oil_data['Conclusao'], format = '%d/%m/%Y')

#Passo 6: Criação da linha apenas com o ano de início da exploração de cada poço
oil_data['Ano_Inicio'] = oil_data['Inicio'].dt.year

## --------------------------------------------------------
## ----------- FIM  DA LIMPEZA DOS DADOS ------------------
## --------------------------------------------------------

st.header("Análise da distribuição de poços de petróleo pelo Brasil de 1998 até Abril de 2023", divider = 'blue')


hist_button = st.checkbox('Exibir Gráficos') # criar um botão

if hist_button: # se o botão for clicado

    ## ------- GRÁFICO 1 ----------##

    # escrever uma mensagem
    st.write('**Gráfico 1: Número de Poços de Petróleo (Concluídos ou em Andamento) por Estado**')

    # criar um histograma
    fig = px.histogram(oil_data, x='Estado')

    # exibir um gráfico Plotly interativo
    st.plotly_chart(fig, use_container_width=True)

    ## ------- GRÁFICO 2 ----------##

    ## Agrupamento de dados por ano e contagem do número de poços por ano
    pocos_por_ano = oil_data.groupby('Ano_Inicio')['Poco_ANP'].count()

    # escrever uma mensagem
    st.write('**Gráfico 2: Número de Poços de Petróleo Iniciados por Ano**')

    # criar um gráfico de dispersão
    fig = px.scatter(x=pocos_por_ano.index, y=pocos_por_ano.values)

    # exibir um gráfico Plotly interativo
    st.plotly_chart(fig, use_container_width=True)