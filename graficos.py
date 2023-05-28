import matplotlib.pyplot as plt
from pymongo import MongoClient
from database_utils import valor_somado





def mostragrafico():
    try:
        # Conectar ao banco de dados MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['DataBase']
        colecao = db['DataBase']

        # Consultar os dados para o gráfico
        dados = colecao.find({}, {'nome': 1, 'valor pago': 1})

        # Extrair os valores para o gráfico
        nomes = []
        valores_pagos = []

        for documento in dados:
            nomes.append(documento['nome'])
            valores_pagos.append(documento['valor pago'])

        # Calcular o valor somado e o lucro total
        valor_somado = sum(valores_pagos)
        lucro_total = valor_somado   # Exemplo de cálculo de lucro (20% do valor somado)

        # Criar o gráfico de barras
        plt.figure()
        plt.bar(nomes, valores_pagos)
        plt.xlabel("Cliente")
        plt.ylabel("Valor Pago")
        plt.title("Vendas")

        # Adicionar os valores exatos dentro das barras
        for i in range(len(nomes)):
            valor_formatado = "${:.2f}".format(valores_pagos[i])
            plt.text(nomes[i], valores_pagos[i], valor_formatado, ha='center', va='bottom')

        # Adicionar o valor somado e o lucro total no gráfico
        plt.text(0.5, 0.9, f"Lucro Total: ${lucro_total:.2f}", ha='center', va='center', transform=plt.gca().transAxes)

        plt.show()

    except Exception as e:
        print('Erro durante a conexão ou operação:', e)
