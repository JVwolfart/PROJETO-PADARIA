import funcoes
for c in range(0,100):
    cpf = funcoes.gera_cpf()
    cpf_format = f'{cpf[0:3]}' + '.' + f"{cpf[3:6]}" + '.' +  f'{cpf[6:9]}' + '-' + f'{cpf[9:11]}'
    print(f'{c+1}° CPF gerado: {cpf_format}')
    print(f'Baseado no CPF {cpf}')