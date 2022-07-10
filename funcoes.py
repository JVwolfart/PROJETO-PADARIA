from random import randint
from datetime import datetime


def valida_cpf(cpf_informado):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in cpf_informado if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


def gera_cpf():
    #  Gera os primeiros nove dígitos (e certifica-se de que não são todos iguais)
    while True:
        cpf = [randint(0, 9) for i in range(9)]
        if cpf != cpf[::-1]:
            break

    #  Gera os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        cpf.append(digit)

    #  Retorna o CPF como string
    result = ''.join(map(str, cpf))
    return result

#FORMATA DATA CONVENCIONAL PARA DATA DO BANCO
def data_banco(data):
    data_format = data[6:] + '-' + data[3:5] + '-' + data[0:2]
    return data_format

#FORMATA DATA DO BANCO PARA DATA CONVENCIONAL
def banco_data(data):
    data_format = data[8:] + '/' + data[5:7] + '/' + data[0:4]
    return data_format

#FORMATA DATA CONVENCIONAL PARA DATA DO BANCO
def data_banco1(data):
    data_format = data[6:] + '/' + data[3:5] + '/' + data[0:2]
    return data_format


def calcula_intervalo_dias(data_inicio, data_fim):
    inicio = analise.dataInicial.date()
    fim = analise.dataFinal.date()
    print(inicio)
    print(fim)
    
    if inicio< fim:
        print ("inicio é menor que fim")
    elif inicio == fim:
        print ("as datas são iguais")
    else:
        print ("inicio é maior que fim")
    dia_inicial= analise.dataInicial.text()
    dia_final= analise.dataFinal.text()
    di = data_banco1(dia_inicial)
    df = data_banco1(dia_final)
    print(dia_inicial)
    print(dia_final)
    print(di)
    print(df)

    date1 = int(datetime.strptime(dia_inicial, '%d/%m/%Y').strftime("%s"))
    date2 = int(datetime.strptime(dia_final, '%d/%m/%Y').strftime("%s"))

    difdate = date2 - date1
    difdate = difdate/60
    difdate = difdate/60
    difdate = difdate/24
    print (int(difdate))
    return int(difdate)

def inicial_maior_final(inicio, fim):
    if inicio <= fim:
        return True
    else:
        return False