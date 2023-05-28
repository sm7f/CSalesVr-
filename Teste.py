import pdfkit
from pymongo import MongoClient
from datetime import datetime

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

def cd_cliente(vlr_receber, calc):
    try:
        # Conectar ao banco de dados
        client = MongoClient('mongodb://localhost:27017/')  # Insira o host e a porta do MongoDB

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

                # Gerar PDF da operação
                gerar_pdf(documento)

            else:
                inserir_pop()
        else:
            valor_pop()

    except Exception as e:
        print('Erro durante a conexão ou operação:', e)


btn_cliente = Button(janela, text='Vender', width=2, bd=1, relief='solid', command=lambda: cd_cliente(vlr_receber, calc))
btn_cliente.place(x=235, y=170)
btn_cliente.grid(row=5, column=3, sticky="nsew")
