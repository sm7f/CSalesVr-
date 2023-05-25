from tkinter import *
import matplotlib.pyplot as plt
from database_utils import valor_somado

# Resto do seu código...

# ----------------------------- Botões -----------------------------------------------------------------------------------

# Adicionar um novo botão para exibir o gráfico
def mostrar_grafico():
    # Dados de exemplo
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    vendas = valor_somado()

    # Criar o gráfico de barras
    plt.bar(meses, vendas)

    # Definir os rótulos dos eixos
    plt.xlabel('Meses')
    plt.ylabel('Vendas')

    # Definir o título do gráfico
    plt.title('Vendas Mensais')

    # Exibir o gráfico
    plt.show()

