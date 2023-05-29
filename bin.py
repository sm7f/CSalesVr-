from tkinter import *
from tkinter import messagebox
from pydantic import FilePath  
from pymongo import MongoClient
from component_pop_up import gravar_pop,valor_pop,inserir_pop,numero_invalido_pop,numero_repetido_pop
from database_utils import calcular_soma_valores
from graficos import mostragrafico
from datetime import datetime
import pdfkit
import os
import subprocess
import webbrowser
from component_function import open_html_file, create_table,create_table








# ------------------------------- Janela ----------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------
janela = Tk()  
janela.resizable(width=False, height=False)  
janela.geometry('600x350')  
janela.title('CSalesVr 1.0.1')  
janela.configure(bg='dim gray')

# --------------------------------------------------------------------------------------------------------------------------
# ------------------------------- Informação -------------------------------------------------------------------------------

v_1 = Label (janela, text="Valor Pago", bd=1, relief='solid', padx=5, pady=5)
v_1.place(x=1, y=50)  # Posição
v_1.grid(row=2, column=0, sticky="nsew")  

v_2 = Label(janela,text='Valor Recebido', bd=1, relief='solid', padx=5, pady=5)  
v_2.place(x=100, y=102)  # Posição
v_2.grid(row=2, column=1, sticky="nsew")  

label1 = Label(janela, text="Valor Bruto", bd=1, relief='solid', padx=5, pady=5)
label2 = Label(janela, text="Porcentagem", bd=1, relief='solid', padx=5, pady=5)

nome_t = Label(janela, text='Nome Cliente', bd=1, relief='solid', padx=5, pady=5)
nome_t.place(x=50, y=70)  # Posição
nome_t.grid(row=5, column=0, sticky="nsew")
  
numero_t = Label(janela, text='Número', bd=1, relief='solid', padx=5, pady=5)
numero_t.place(x=50, y=70)  # Posição
numero_t.grid(row=7, column=0, sticky="nsew")  

space = Label(janela, text='    ',bg='dim gray') 
space.place(x=200, y=70)  # Posição
space.grid(row=4, column=0, sticky="nsew") 

space = Label(janela, text='    ',bg='dim gray') 
space.place(x=200, y=70)  # Posição
space.grid(row=4, column=1, sticky="nsew") 
# --------------------------------------------------------------------------------------------------------------------------
# ------------------------------- Display -----------------------------------------------------------------------------------

caixa1 = Entry(janela, justify="center")  # Display 1
caixa1.place(x=50, y=70)  # Posição
caixa1.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)

caixa2 = Entry(janela, justify="center")  # Display 1
caixa2.place(x=200, y=70)  # Posição
caixa2.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)



numero_ = Entry(janela, justify="center")  # Display 2
numero_.grid(row=9, column=0, sticky="nsew", padx=1, pady=1)

nome_ = Entry(janela, justify="center")  # Display 2
nome_.place(x=50, y=70)  # Posição
nome_.grid(row=6, column=0, sticky="nsew", padx=1, pady=1)  

 
# ------------------------------- Resultados -------------------------------------------------------------------------------

vlr_receber = Label (janela, text="-------------", bd=1, relief='solid')
vlr_receber.place(x=1, y=50)  # Posição
vlr_receber.grid(row=3, column=0, sticky="nsew") 

calc = Label(janela,text='-------------', bd=1, relief='solid')  
calc.place(x=100, y=102)  # Posição
calc.grid(row=3, column=1, sticky="nsew")


# --------------------------------------------------------------------------------------------------------------------------
# ------------------------------- Configuração ----------------------------------------------------------------------------------

# Configurando o gerenciamento de geometria "grid"
# Ajustando a largura das colunas
janela.grid_columnconfigure(0, minsize=150, pad=10)
janela.grid_columnconfigure(1, minsize=150, pad=10)
janela.grid_columnconfigure(2, minsize=150, pad=10)
janela.grid_columnconfigure(3, minsize=150, pad=10)
janela.grid_columnconfigure(4, minsize=150, pad=10)
janela.grid_columnconfigure(5, minsize=150, pad=10)
janela.grid_columnconfigure(6, minsize=150, pad=10)
janela.grid_columnconfigure(7, minsize=150, pad=10)

label1.grid(row=0, column=0, sticky="nsew")  
label2.grid(row=0, column=1, sticky="nsew") 

# ------------------------------- Calc --------------------------------------------------------------------------------------
def bt_Mt(vlr_receber, calc):
    try:
        n1 = float(caixa1.get())
        n2 = float(caixa2.get())
        valor = n1 * (n2 / 100)
        calc_value = "${:.2f}".format(n1 - valor)
        calc['text'] = calc_value
        vlr_receber_value = "${:.2f}".format(valor)
        vlr_receber['text'] = vlr_receber_value
        return valor, float(calc_value[1:])
        
    
    except ValueError:
        calc['text'] = valor_pop()
        vlr_receber['text'] = valor_pop()
        return None, None
    
    


# ------------------------------- Cadastra Cliente -------------------------------------------------------------------------       
def vender():
    # Chamar a função cd_cliente
    documento = cd_cliente(vlr_receber, calc)

    # Chamar a função gerar_html
    html = gerar_html(documento)

    # Salvar o comprovante em formato HTML
    file_path = 'Comprovante/operacao.html'
    gerar_html_file(html, file_path)

def cd_cliente(vlr_receber, calc):
    try:
        # Conectar ao banco de dados
        client = MongoClient('mongodb://localhost:27017/')  # Insira o host e a porta do MongoDB

        # Selecionar o banco de dados
        db = client['DataBase']  # Insira o nome do banco de dados

        # Selecionar a coleção
        colecao = db['DataBase']  # Insira o nome da coleção

        vendas_collection = db["Vendas"]

        nro = numero_.get()
        n3 = nome_.get()
        

        data_hora_atual = datetime.now()

        # Verificar se o número já está em uso
        if colecao.find_one({'numero': nro}):
            # Número já existe na coleção
            numero_repetido_pop()
            return

        # Verificar o comprimento do número
        if len(nro) != 11:
            # Número inválido
            numero_invalido_pop()
            return

        # Obter os valores de 'valor pago' e 'valor recebido' usando a função bt_Mt()
        valor_pago, valor_recebido = bt_Mt(vlr_receber, calc)  # Passando os argumentos

        if valor_pago is not None and valor_recebido is not None:
            # Criar um documento com os dados
            documento = {
                'numero': nro,
                'nome': n3,
                'valor pago': valor_pago,
                'valor recebido': valor_recebido,
                'data e hora': data_hora_atual
            }

            # Inserir o documento na coleção
            resultado = colecao.insert_one(documento)
            resultado = vendas_collection.insert_one(documento)

            if resultado.inserted_id:
                gravar_pop()
                gerar_html_and_confirm(documento)
            else:
                inserir_pop()
        else:
            valor_pop()

        return documento

    except Exception as e:
        print('Erro durante a conexão ou operação:', e)


def gerar_html(documento):
    campos_necessarios = ['numero', 'nome', 'valor pago', 'valor recebido', 'data e hora']
    if not all(campo in documento for campo in campos_necessarios):
        print("Documento inválido. Campos necessários ausentes.")
        return None

    html = '''
    <html>
    <head>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                text-align: left;
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <h2>Detalhes da Operação</h2>
        <table>
            <tr>
                <th>CPF</th>
                <th>Nome</th>
                <th>Valor Pago</th>
                <th>Valor Recebido</th>
                <th>Data e Hora</th>
            </tr>
            <tr>
                <td>{0}</td>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>
                <td>{4}</td>
            </tr>
        </table>
        <button onclick="window.print()">Imprimir</button> <!-- Botão para imprimir -->
    </body>
    </html>
    '''.format(documento['numero'], documento['nome'], documento['valor pago'],
               documento['valor recebido'], documento['data e hora'])

    return html



def gerar_html_file(html, file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    print(f"Diretório do arquivo: {directory}")  # Exibe o diretório do arquivo

    with open(file_path, 'w') as file:
        file.write(html)
    print(f"Comprovante salvo em {file_path}")


def gerar_html_and_confirm(documento):
    directory = 'Comprovante'  # Diretório onde o arquivo será salvo
    cpf = documento['numero']  # CPF do cliente
    data_hora = documento['data e hora'].strftime("%Y-%m-%d_%H-%M-%S")  # Data e hora da operação
    file_name = f'operacao_{cpf}_{data_hora}.html'  # Nome do arquivo com CPF e data/hora
    file_path = os.path.join(directory, file_name)

    html = gerar_html(documento)
    gerar_html_file(html, file_path)

    # Exibir caixa de diálogo para confirmar a geração do arquivo HTML
    result = messagebox.askquestion("Confirmação", "Deseja imprimir o comprovante ?")
    if result == 'yes':
        return open_html_file()
    


# ------------------------------- Atualizar -------------------------------------------------------------------------

def atualizar_cliente(vlr_receber, calc):
    try:
        # Conectar ao banco de dados
        client = MongoClient('mongodb://localhost:27017/')  # Insira o host e a porta do MongoDB

        # Selecionar o banco de dados
        db = client['DataBase']  # Insira o nome do banco de dados

        # Selecionar as coleções
        colecao_clientes = db['DataBase']  # Insira o nome da coleção de clientes
        colecao_registros = db['Registros']  # Insira o nome da coleção de registros

        nro = numero_.get()
        n3 = nome_.get()

        data_hora_atual = datetime.now()

        # Consultar o valor atual do campo 'valor pago' do cliente
        cliente = colecao_clientes.find_one({'numero': nro})
        valor_pago_atual = cliente.get('valor pago', 0)

        # Obter os valores de 'valor pago' e 'valor recebido' usando a função bt_Mt()
        valor_pago, valor_recebido = bt_Mt(vlr_receber, calc)  # Passando os argumentos

        if valor_pago is not None and valor_recebido is not None:
            # Somar o novo valor pago ao valor atual
            novo_valor_pago = valor_pago_atual + valor_pago

            # Criar o dicionário com os campos a serem atualizados no cliente
            update_fields_cliente = {
                'valor pago': novo_valor_pago,
                'valor recebido': valor_recebido,
                'data e hora': data_hora_atual
            }

            # Verificar se o campo 'nome' não está em branco antes de incluí-lo no dicionário de atualização do cliente
            if n3.strip():
                update_fields_cliente['nome'] = n3

            # Atualizar os dados do cliente no banco de dados
            resultado = colecao_clientes.update_one(
                {'numero': nro},
                {'$set': update_fields_cliente}
            )

            if resultado.modified_count > 0:
                # Criar o documento de registro
                registro = {
                    'valor pago': valor_pago,
                    'valor recebido': valor_recebido,
                    'data e hora': data_hora_atual,
                    'cliente': cliente['_id']  # Incluir a referência ao cliente correspondente
                }

                # Inserir o registro na coleção de registros
                colecao_registros.insert_one(registro)

                # Calcular o valor total do valor pago
                pipeline_pago = [
                    {'$group': {'_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$data e hora'}}, 'total_pago': {'$sum': '$valor pago'}}},
                    {'$group': {'_id': None, 'total_valor_pago': {'$sum': '$total_pago'}}}
                ]
                total_valor_pago = colecao_registros.aggregate(pipeline_pago).next()['total_valor_pago']

                # Atualizar o valor total de valor recebido e valor pago no registro
                colecao_registros.update_many({}, {'$set': {'total_valor_pago': total_valor_pago}})

                gravar_pop()
            else:
                inserir_pop()
        else:
            valor_pop()
    except Exception as e:
        # Lidar com exceção (opcional)
        print('Ocorreu um erro:', str(e))


btn_cliente = Button(janela, text='Vender', width=2, bd=1, relief='solid', command=vender)
btn_cliente.place(x=235, y=170)
btn_cliente.grid(row=5, column=3, sticky="nsew")



# ----------------------------- Botões -----------------------------------------------------------------------------------
# atribuindo função aos botões

btMt = Button(janela, text='Calcular', bd=1, relief='solid', width=2, command=lambda: bt_Mt(vlr_receber, calc))
btMt.place(x=190, y=170)
btMt.grid(row=0, column=2, sticky="nsew")

btn_cliente = Button(janela, text='Total Vendas', width=2, bd=1, relief='solid', command=lambda: calcular_soma_valores(['valor pago']))
btn_cliente.place(x=235, y=170)
btn_cliente.grid(row=0, column=3, sticky="nsew")


btn_relatorio = Button(janela, text='Relatório', width=2, bd=1, relief='solid', command=mostragrafico)
btn_relatorio.place(x=235, y=170)
btn_relatorio.grid(row=1, column=3, sticky="nsew")

btn_atualizar = Button(janela, text='Nova Venda', width=2, bd=1, relief='solid', command=lambda: atualizar_cliente(vlr_receber, calc))
btn_atualizar.place(x=280, y=170)
btn_atualizar.grid(row=6, column=3, sticky="nsew")

btn_atualizar = Button(janela, text='Comprovante', width=2, bd=1, relief='solid', command=lambda:open_html_file())
btn_atualizar.place(x=280, y=170)
btn_atualizar.grid(row=2, column=2, sticky="nsew")

btn_cliente = Button(janela, text='Vendas Realizadas', width=2, bd=1, relief='solid', command=lambda: create_table())
btn_cliente.place(x=235, y=170)
btn_cliente.grid(row=2, column=3, sticky="nsew")

# Botão Limpar
def limpar_info():
    
    caixa1.delete(0, END)
    caixa2.delete(0, END)
    nome_.delete(0, END)
    numero_.delete(0, END)
    vlr_receber['text'] = '-------------'
    calc['text'] = '-------------'


btn_limpar = Button(janela, text='Limpar', width=10, bd=1, relief='solid' ,command=limpar_info)
btn_limpar.place(x=200, y=170)
btn_limpar.grid(row=1, column=2, sticky="nsew")


janela.mainloop()
