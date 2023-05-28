from tkinter import messagebox
from database_utils import calcular_soma_valores

# Função para exibir o pop-up
def calc_pop():
    messagebox.showinfo("Calculando...", "Calculo Realizado com sucesso...")
def gravar_pop():
    messagebox.showinfo("Enviando", "Dados inseridos com sucesso")
def valor_pop():
    messagebox.showinfo("Enviando", "Valor Inválido")
def inserir_pop():
    messagebox.showinfo("Enviando", "Erro ao inserir dado")
def numero_repetido_pop():
    messagebox.showinfo("Enviando", "Já existe um cadastro com esse CPF")
def numero_invalido_pop():
    messagebox.showinfo("Enviando", "CPF Inválido")


