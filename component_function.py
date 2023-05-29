import os
import webbrowser
import subprocess
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from datetime import datetime
import tkinter.messagebox as messagebox



def open_html_file():
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Diretório do script atual
    file_path = os.path.join(script_dir, 'Comprovante/operacao.html')  # Caminho completo para o arquivo HTML

    # Configura o Brave como navegador padrão
    webbrowser.register('brave', None, webbrowser.BackgroundBrowser('C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'))

    # Abre o arquivo HTML no navegador padrão (que será o Brave)
    webbrowser.get('brave').open(file_path)


    webbrowser.open(file_path)




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

    # Função de callback para gerar o comprovante
    def gerar_comprovante(event):
        item = table.selection()
        if item:
            item_values = table.item(item)['values']
            documento = {
                'numero': item_values[0],
                'nome': item_values[1],
                'valor pago': item_values[2],
                'valor recebido': item_values[3],
                'data e hora': datetime.strptime(item_values[4], '%Y-%m-%d %H:%M:%S')
            }
        confirmar = messagebox.askyesno("Confirmação", "Deseja gerar o comprovante?")  # Caixa de diálogo de confirmação
        if confirmar:
            file_name = f'comprovante_{documento["numero"]}_{documento["data e hora"].strftime("%Y-%m-%d_%H-%M-%S")}.html'
            directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Comprovante')
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_path = os.path.join(directory, file_name)
            comprovante_html = open_html_file()
            with open(file_path, 'w') as file:
                file.write(comprovante_html)
        else:
            print("Operação cancelada.")

    # Associar a função de callback ao evento de clique na linha
    table.bind('<ButtonRelease-1>', gerar_comprovante)

    # Exibir a tabela
    table.pack()

   

    root.mainloop()





