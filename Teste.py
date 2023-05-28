import tkinter as tk
from tkinter import messagebox

def on_option_selected(option):
    messagebox.showinfo("Opção selecionada", f"Você selecionou: {option}")

# Função de callback para o botão "Selecione uma opção"
def on_button_click():
    selected_option = var.get()
    if selected_option:
        on_option_selected(selected_option)
    else:
        messagebox.showwarning("Opção não selecionada", "Selecione uma opção antes de prosseguir.")

# Criação da janela principal
root = tk.Tk()
root.title("Botão com opções")

# Variável de controle para a opção selecionada
var = tk.StringVar(root)

# Opções do menu suspenso
options = ["Opção 1", "Opção 2", "Opção 3"]

# Definição do menu suspenso
option_menu = tk.OptionMenu(root, var, *options)
option_menu.pack(pady=10)

# Botão "Selecione uma opção"
button = tk.Button(root, text="Selecione uma opção", command=on_button_click)
button.pack(pady=10)

# Execução do loop principal do tkinter
root.mainloop()
