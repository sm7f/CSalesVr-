from tkinter import *  
from pymongo import MongoClient
from component_pop_up import gravar_pop,valor_pop,inserir_pop
from database_utils import calcular_soma_valores
from graficos import mostrar_grafico
from datetime import datetime


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

sobre_nt = Label(janela, text='Sobrenome', bd=1, relief='solid', padx=5, pady=5) 
sobre_nt.place(x=200, y=70)  # Posição
sobre_nt.grid(row=5, column=1, sticky="nsew")
 
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

sobre_n = Entry(janela, justify="center")  # Display 2
sobre_n.place(x=200, y=70)  # Posição
sobre_n.grid(row=6, column=1, sticky="nsew", padx=1, pady=1)
 
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
def cd_cliente(vlr_receber, calc):
    try:
        # Conectar ao banco de dados
        client = MongoClient('mongodb://localhost:27017/', 27017)  # Insira o host e a porta do MongoDB

        # Selecionar o banco de dados
        db = client['DataBase']  # Insira o nome do banco de dados

        # Selecionar a coleção
        colecao = db['DataBase']  # Insira o nome da coleção

        nro = numero_.get()
        n3 = nome_.get()
        n4 = sobre_n.get()

        data_hora_atual = datetime.now()

        # Obter os valores de 'valor pago' e 'valor recebido' usando a função bt_Mt()
        valor_pago, valor_recebido = bt_Mt(vlr_receber, calc)  # Passando os argumentos

        if valor_pago is not None and valor_recebido is not None:
            # Criar um documento com os dados
            documento = {
                'numero': nro,
                'nome': n3,
                'sobrenome': n4,
                'valor pago': valor_pago,
                'valor recebido': valor_recebido,
                'data e hora': data_hora_atual

            }

            # Inserir o documento na coleção
            resultado = colecao.insert_one(documento)

            if resultado.inserted_id:
                gravar_pop()
            else:
                inserir_pop()
        else:
            valor_pop()

    except Exception as e:
        print('Erro durante a conexão ou operação:', e)

# ----------------------------- Botões -----------------------------------------------------------------------------------
# atribuindo função aos botões

btMt = Button(janela, text='Calcular', bd=1, relief='solid', width=2, command=lambda: bt_Mt(vlr_receber, calc))
btMt.place(x=190, y=170)
btMt.grid(row=0, column=2, sticky="nsew")


btn_cliente = Button(janela, text='Gravar', width=2, bd=1, relief='solid', command=lambda: cd_cliente(vlr_receber, calc))
btn_cliente.place(x=235, y=170)
btn_cliente.grid(row=5, column=3, sticky="nsew")

btn_cliente = Button(janela, text='Vendas Realizadas', width=2, bd=1, relief='solid', command=lambda: calcular_soma_valores(['valor pago']))
btn_cliente.place(x=235, y=170)
btn_cliente.grid(row=0, column=3, sticky="nsew")

btn_cliente = Button(janela, text='Relatório', width=2, bd=1, relief='solid', command= lambda: mostrar_grafico())
btn_cliente.place(x=235, y=170)
btn_cliente.grid(row=1, column=3, sticky="nsew")

# Botão Limpar
def limpar_info():
    
    caixa1.delete(0, END)
    caixa2.delete(0, END)
    nome_.delete(0, END)
    sobre_n.delete(0, END)
    numero_.delete(0, END)
    vlr_receber['text'] = '-------------'
    calc['text'] = '-------------'


btn_limpar = Button(janela, text='Limpar', width=10, bd=1, relief='solid' ,command=limpar_info)
btn_limpar.place(x=200, y=170)
btn_limpar.grid(row=5, column=2, sticky="nsew")


janela.mainloop()
