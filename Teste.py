import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from datetime import datetime

def create_table():
    root = tk.Tk()
    root.title("Vendas")

    # Criar Treeview
    table = ttk.Treeview(root)

    # Definir as colunas da tabela
    table['columns'] = ('numero', 'nome', 'valor pago', 'valor recebido', 'data e hora')

    # Formatar as colunas
    table.column('#0', width=0, stretch=tk.NO)  # Coluna vazia para indentação
    table.column('numero', anchor=tk.CENTER, width=80)
    table.column('nome', anchor=tk.W, width=150)
    table.column('valor pago', anchor=tk.CENTER, width=100)
    table.column('valor recebido', anchor=tk.CENTER, width=120)
    table.column('data e hora', anchor=tk.CENTER, width=150)

    # Cabeçalho das colunas
    table.heading('#0', text='', anchor=tk.W)
    table.heading('numero', text='CPF', anchor=tk.CENTER)
    table.heading('nome', text='Nome', anchor=tk.W)
    table.heading('valor pago', text='Valor Pago', anchor=tk.CENTER)
    table.heading('valor recebido', text='Valor Recebido', anchor=tk.CENTER)
    table.heading('data e hora', text='Data e Hora', anchor=tk.CENTER)

    try:
        # Conectar-se ao banco de dados MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['DataBase']  # Insira o nome do banco de dados
        vendas_collection = db['Vendas']  # Insira o nome da coleção

        # Consultar todas as vendas
        vendas = vendas_collection.find()

        # Adicionar linhas à tabela com base nos dados de vendas
        for venda in vendas:
            table.insert('', tk.END, text='',
                         values=(
                             venda['numero'],
                             venda['nome'],
                             venda['valor pago'],
                             venda['valor recebido'],
                             venda['data e hora'].strftime('%Y-%m-%d %H:%M:%S')
                         ))

    except Exception as e:
        print('Erro durante a conexão ou operação:', e)

    # Exibir a tabela
    table.pack()

    root.mainloop()

# Chame a função para criar a tabela
create_table()
