import pickle

valueB = float(input("Valor Bruto: "))
nome = (input("Nome: "))
mensagem1 = f"Seu nome {nome}"
print(mensagem1)

Tr = 0.05
result = valueB - (valueB * Tr)

mensagem = f"Calculando Imposto... {result}"
print (mensagem)
print("Cadastre-se")

Sbnome = (input("Sobrenome: "))
idade = int(input("Idade: "))
cpf = int(input("CPF: "))
rg = int(input("RG: "))

resposta = input('Deseja visualizar os dados? (S/N) ')

if resposta.upper() == 'S':
    # Se a resposta for 'S', exibir os dados
    print(mensagem1,Sbnome,"Idade: ",idade, "CPF: ",cpf, "RG: ",rg)
else:
    # Se a resposta for qualquer outra coisa, não fazer nada
    pass







