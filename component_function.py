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



from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk, messagebox

class ProductDatabase:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    def register_product(self, product):
        if self.db:
            collection = self.db['products']
            result = collection.insert_one(product)
            return result.inserted_id
        else:
            raise Exception("Database not connected")

from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk, messagebox

class ProductDatabase:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    def register_product(self, product):
        if self.db is not None:
            collection = self.db['products']
            result = collection.insert_one(product)
            return result.inserted_id
        else:
            raise Exception("Database not connected")

def cd_produo(): 
    root = tk.Tk()
    root.title("Vendas")

    # Criar Treeview
    table = ttk.Treeview(root)

    # Definir as colunas da tabela
    table['columns'] = ('numero', 'nome', 'valor compra', 'valor venda', 'estoque')

    # Formatar as colunas
    table.column('#0', width=0, stretch=tk.NO)  # Coluna vazia para indentação
    table.column('numero', anchor=tk.CENTER, width=80)
    table.column('nome', anchor=tk.W, width=150)
    table.column('valor compra', anchor=tk.CENTER, width=100)
    table.column('valor venda', anchor=tk.CENTER, width=120)
    table.column('estoque', anchor=tk.CENTER, width=100)

    # Cabeçalho das colunas
    table.heading('#0', text='', anchor=tk.W)
    table.heading('numero', text='Número', anchor=tk.CENTER)
    table.heading('nome', text='Nome', anchor=tk.W)
    table.heading('valor compra', text='Valor Compra', anchor=tk.CENTER)
    table.heading('valor venda', text='Valor Venda', anchor=tk.CENTER)
    table.heading('estoque', text='Estoque', anchor=tk.CENTER)

    try:
        # Conectar-se ao banco de dados MongoDB
        db = ProductDatabase('localhost', 27017, 'DataBase')
        db.connect()
        products_collection = db.db['Products']  # Insira o nome da coleção

        # Consultar todos os produtos
        products = products_collection.find()

        # Adicionar linhas à tabela com base nos dados dos produtos
        for product in products:
            table.insert('', tk.END, text='',
                         values=(
                             product['numero'],
                             product['nome'],
                             product['valor compra'],
                             product['valor venda'],
                             product['estoque']
                         ))

    except Exception as e:
        print('Erro durante a conexão ou operação:', e)

    # Função de callback para cadastrar um novo produto
    def cadastrar_produto():
        def salvar_produto():
            product = {
                'numero': numero_entry.get(),
                'nome': nome_entry.get(),
                'valor compra': float(valor_compra_entry.get()),
                'valor venda': float(valor_venda_entry.get()),
                'estoque': int(estoque_entry.get())
            }

            inserted_id = db.register_product(product)
            print(f"Produto cadastrado com o ID: {inserted_id}")

            # Atualizar a tabela exibindo o novo produto
            table.insert('', tk.END, text='',
                         values=(
                             product['numero'],
                             product['nome'],
                             product['valor compra'],
                             product['valor venda'],
                             product['estoque']
                         ))

            # Fechar a janela de cadastro
            cadastro_window.destroy()

        # Criar uma nova janela para o cadastro
        cadastro_window = tk.Toplevel(root)
        cadastro_window.title("Cadastrar Produto")

        # Criar e posicionar os widgets na janela de cadastro
        numero_label = tk.Label(cadastro_window, text="Número:")
        numero_label.grid(row=0, column=0, sticky=tk.W)
        numero_entry = tk.Entry(cadastro_window)
        numero_entry.grid(row=0, column=1)

        nome_label = tk.Label(cadastro_window, text="Nome:")
        nome_label.grid(row=1, column=0, sticky=tk.W)
        nome_entry = tk.Entry(cadastro_window)
        nome_entry.grid(row=1, column=1)

        valor_compra_label = tk.Label(cadastro_window, text="Valor Compra:")
        valor_compra_label.grid(row=2, column=0, sticky=tk.W)
        valor_compra_entry = tk.Entry(cadastro_window)
        valor_compra_entry.grid(row=2, column=1)

        valor_venda_label = tk.Label(cadastro_window, text="Valor Venda:")
        valor_venda_label.grid(row=3, column=0, sticky=tk.W)
        valor_venda_entry = tk.Entry(cadastro_window)
        valor_venda_entry.grid(row=3, column=1)

        estoque_label = tk.Label(cadastro_window, text="Estoque:")
        estoque_label.grid(row=4, column=0, sticky=tk.W)
        estoque_entry = tk.Entry(cadastro_window)
        estoque_entry.grid(row=4, column=1)

        salvar_button = tk.Button(cadastro_window, text="Salvar", command=salvar_produto)
        salvar_button.grid(row=5, column=0, columnspan=2)

    # Botão para cadastrar um novo produto
    cadastrar_button = tk.Button(root, text="Cadastrar Produto", command=cadastrar_produto)
    cadastrar_button.pack()

    # Exibir a tabela
    table.pack()

    root.mainloop()








