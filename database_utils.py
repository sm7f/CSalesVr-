from pymongo import MongoClient
from tkinter import messagebox

def valor_somado(soma_valores):
    messagebox.showinfo("Visualizando", "Vendas Realizadas: " + str(soma_valores))


def calcular_soma_valores(campos):
    try:
        # Conectar ao banco de dados
        client = MongoClient('mongodb://localhost:27017/')  # Insira o host e a porta do MongoDB

        # Selecionar o banco de dados
        db = client['DataBase']  # Insira o nome do banco de dados

        # Selecionar a coleção
        colecao = db['DataBase']  # Insira o nome da coleção

        # Inicializar a variável para armazenar a soma dos valores
        soma_valores = 0

        # Percorrer todos os documentos da coleção
        for documento in colecao.find():
            for campo in campos:
                valor = documento[campo]
                soma_valores += valor

        # Exibir a soma dos valores
        valor_somado("${:.2f}".format(soma_valores))

    except Exception as e:
        print('Erro durante a conexão ou operação:', e)
