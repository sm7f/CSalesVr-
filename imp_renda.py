from tkinter import *  
from pymongo import MongoClient

# ------------------------------- Janela ----------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------
janela = Tk()  
janela.resizable(width=False, height=False)  
janela.geometry('400x200')  
janela.title('Calcula Venda VR e VA')  

# --------------------------------------------------------------------------------------------------------------------------
# ------------------------------- Informação -------------------------------------------------------------------------------

v_1 = Label (janela, text="Valor Pago")
v_1.place(x=1, y=50)  # Posição
v_1.grid(row=2, column=0, sticky="nsew")  

v_2 = Label(janela,text='Valor Recebido')  
v_2.place(x=100, y=102)  # Posição
v_2.grid(row=2, column=1, sticky="nsew")  

label1 = Label(janela, text="Valor Bruto")
label2 = Label(janela, text="Porcentagem")
# --------------------------------------------------------------------------------------------------------------------------
# ------------------------------- Display -----------------------------------------------------------------------------------

caixa1 = Entry(janela)  # Display 1
caixa1.place(x=50, y=70)  # Posição
caixa1.grid(row=1, column=0, sticky="nsew")

caixa2 = Entry(janela, text='5%')  # Display 2
caixa2.place(x=200, y=70)  # Posição
caixa2.grid(row=1, column=1, sticky="nsew")

nome_ = Entry(janela)  # Display 1
nome_.place(x=50, y=70)  # Posição
nome_.grid(row=5, column=0, sticky="nsew")  

sobre_n = Entry(janela)  # Display 2
sobre_n.place(x=200, y=70)  # Posição
sobre_n.grid(row=5, column=1, sticky="nsew")
 
nome_t = Label(janela, text='Nome Cliente')  # Display 1
nome_t.place(x=50, y=70)  # Posição
nome_t.grid(row=4, column=0, sticky="nsew")  

sobre_nt = Label(janela, text='Sobrenome')  # Display 2
sobre_nt.place(x=200, y=70)  # Posição
sobre_nt.grid(row=4, column=1, sticky="nsew") 

# ------------------------------- Resultados -------------------------------------------------------------------------------

vlr_receber = Label (janela, text="-------------")
vlr_receber.place(x=1, y=50)  # Posição
vlr_receber.grid(row=3, column=0, sticky="nsew") 

calc = Label(janela,text='-------------')  
calc.place(x=100, y=102)  # Posição
calc.grid(row=3, column=1, sticky="nsew")  

# --------------------------------------------------------------------------------------------------------------------------
# ------------------------------- Configuração ----------------------------------------------------------------------------------

# Configurando o gerenciamento de geometria "grid"
janela.grid_columnconfigure(0, weight=1)  
janela.grid_columnconfigure(1, weight=1)  

label1.grid(row=0, column=0, sticky="nsew")  
label2.grid(row=0, column=1, sticky="nsew") 

# ------------------------------- Multiplicação ------------------------------------------------------------------------
def bt_Mt(vlr_receber, calc):
    try:
        n1 = float(caixa1.get())
        n2 = float(caixa2.get())
        valor = n1 * (n2 / 100)
        calc['text'] = n1 - valor
        vlr_receber['text'] = n1 - float(calc['text'])
        return valor, float(calc['text'])
    except ValueError:
        calc['text'] = 'Digite um valor'
        vlr_receber['text'] = 'Digite um valor'
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

        n3 = nome_.get()
        n4 = sobre_n.get()

        # Obter os valores de 'valor pago' e 'valor recebido' usando a função bt_Mt()
        valor_pago, valor_recebido = bt_Mt(vlr_receber, calc)  # Passando os argumentos corretos

        if valor_pago is not None and valor_recebido is not None:
            # Criar um documento com os dados
            documento = {
                'nome': n3,
                'sobrenome': n4,
                'valor pago': valor_pago,
                'valor recebido': valor_recebido
            }

            # Inserir o documento na coleção
            resultado = colecao.insert_one(documento)

            if resultado.inserted_id:
                print('Documento inserido com sucesso')
            else:
                print('Erro ao inserir o documento')
        else:
            print('Valor inválido')

    except Exception as e:
        print('Erro durante a conexão ou operação:', e)

# ----------------------------- Botões -----------------------------------------------------------------------------------
# atribuindo função aos botões

btMt = Button(janela, text='Calc', font='bold', width=4, command=lambda: bt_Mt(vlr_receber, calc))
btMt.place(x=190, y=170)

btn_cliente = Button(janela, text='Salva', font='bold', width=4, command=lambda: cd_cliente(vlr_receber, calc))
btn_cliente.place(x=235, y=170)


janela.mainloop()