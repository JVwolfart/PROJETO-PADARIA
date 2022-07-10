from PyQt5 import QtWidgets
from PyQt5.QtCore import QVariant 
import banco
import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import funcoes
from datetime import date
from classes import  Cliente, Produto, Usuarios, Funcionario


data_atual = date.today()


#FUNÇÕES PARA TELA LOGIN
def fazer_login():
    usuario = login.InputUsuario.text().upper()
    senha = login.InputSenha.text()
    usuario_banco = banco.buscar_usuario(usuario)
    if usuario != "ROOT":
        usuario1.banco_para_modelo(usuario_banco)
    if usuario == 'ROOT' and senha == 'manager':
        login.close()
        abrir_cria_usuario()
        manut_usuarios.BtnOrdenar.setVisible(False)
        manut_usuarios.BtnOrdenarID.setVisible(False)
    else:
        if len(usuario_banco) == 0:
            QMessageBox.about(login, 'ERRO', 'Usuário inexistente no banco')
        if senha != usuario1.senha:
            QMessageBox.about(login, 'ERRO', 'Senha não confere')
        else:
            #usuario1.banco_para_modelo(usuario_banco)
            permi = banco.busca_permissoes(usuario)
            manut_usuarios.BtnOrdenar.setVisible(False)
            manut_usuarios.BtnOrdenarID.setVisible(False)
            #VENDAS

            vendas.BtnCadFuncionario.setVisible(usuario_banco[0][6])
            vendas.BtnCadClientes.setVisible(usuario_banco[0][3])
            vendas.BtnCadProdutos.setVisible(usuario_banco[0][3])
            vendas.BtnNVenda.setVisible(usuario_banco[0][3])
            vendas.BtnRoot.setVisible(usuario_banco[0][6])
            if usuario_banco[0][6]:
                vendas.lbl_root.setVisible(False)
            

            #FUNCIONÁRIOS
            cad_func.BtnInserir.setVisible(usuario_banco[0][6])
            manut_func.BtnAlterar.setVisible(usuario_banco[0][4])
            manut_func.BtnDesligar.setVisible(usuario_banco[0][6])
            manut_func.BtnReativar.setVisible(usuario_banco[0][6])
            ##############

            #CLIENTES
            cad_cliente.BtnInserir.setVisible(usuario_banco[0][3])
            manut_cliente.BtnAlterar.setVisible(usuario_banco[0][4])
            manut_cliente.BtnDesligar.setVisible(usuario_banco[0][5])
            manut_cliente.BtnReativar.setVisible(usuario_banco[0][6])
            #####################

            #PRODUTOS
            cad_produtos.BtnInserir.setVisible(usuario_banco[0][3])
            manut_produtos.BtnAlterar.setVisible(usuario_banco[0][4])
            manut_produtos.BtnDesligar.setVisible(usuario_banco[0][5])
            manut_produtos.BtnReativar.setVisible(usuario_banco[0][6])
            ###############

            #NOTA FISCAL
            manut_nf.BtnInserir.setVisible(usuario_banco[0][3])
            manut_nf.BtnCalcularNf.setVisible(usuario_banco[0][3])
            manut_nf.BtnCancelarNf.setVisible(usuario_banco[0][5])
            manut_item.BtnAlterar.setVisible(usuario_banco[0][4])
            manut_item.BtnExcluir.setVisible(usuario_banco[0][5])
            
            ###############
            login.close()
            vendas.lbl_ola.setText(f'Seja bem vindo usuário {usuario1.nome}')
            vendas.lbl_id_user.setText(f'{usuario1.id}')
            vendas.show()
            QMessageBox.about(vendas, 'BOAS VINDAS', f'Bem vindo usuário {usuario1.nome}, você possui as seguintes permissões: {permi}')
            banco.cria_tabelas()
            carrega_tabelas()

def abrir_cria_usuario():
    login.close()
    cad_usuario.CbCriar.setVisible(False)
    cad_usuario.CbEditar.setVisible(False)
    cad_usuario.CbExcluir.setVisible(False)
    cad_usuario.CbRoot.setVisible(False)
    cad_usuario.show()    


##############################

#FUNÇÕES PARA CRIAÇÃO DE USUÁRIOS

def abrir_tela_login():
    cad_usuario.close()
    vendas.close()
    login.InputUsuario.setText('')
    login.InputSenha.setText('')
    login.show()

def criar_novo_usuario():
    usuario = cad_usuario.InputUsuario.text().upper().strip()
    senha = cad_usuario.InputSenha.text()
    confirma = cad_usuario.InputConfirmar.text()
    criar = cad_usuario.CbCriar.isChecked()
    editar = cad_usuario.CbEditar.isChecked()
    excluir = cad_usuario.CbExcluir.isChecked()
    usuario_banco = banco.buscar_usuario(usuario)
    if len(usuario) < 5 or len(senha) < 5:
        QMessageBox.about(cad_usuario, 'ERRO', 'usuário e senha devem ter pelo menos 5 caractéres')
    elif senha != confirma:
        QMessageBox.about(cad_usuario, 'ERRO', 'Senha e confirmação são diferentes')
    elif len(usuario_banco) != 0:
        QMessageBox.about(cad_usuario, 'ERRO', 'Usuário já existe no sistema')
    else:
        banco.novo_usuario(usuario, senha, criar, editar, excluir)
        QMessageBox.about(cad_usuario, 'USUÁRIO CRIADO', f'Usuário {usuario} criado com sucesso!')
        cad_usuario.InputUsuario.setText('')
        cad_usuario.InputSenha.setText('')
        cad_usuario.InputConfirmar.setText('')
        cad_usuario.CbCriar.setChecked(False)
        cad_usuario.CbEditar.setChecked(False)
        cad_usuario.CbExcluir.setChecked(False)
        novo_usuario = banco.buscar_usuario(usuario)
        id_usuario = str(novo_usuario[0][0])
################################

#MANUTENÇÃO DE USUÁRIOS

def carrega_usuarios():
    usuarios = banco.buscar_todos_usuarios()
    row = 0
    tabela = manut_usuarios.TabelaUsuarios
    tabela.setRowCount(len(usuarios))
    tabela.setColumnWidth(0, 50)
    tabela.setColumnWidth(1, 350)
    tabela.setColumnWidth(2, 100)
    tabela.setColumnWidth(3, 100)
    tabela.setColumnWidth(4, 100)
    tabela.setColumnWidth(5, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    for c in usuarios:
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        if c[3] == 1:
            tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'SIM'))
        else:
            tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'NÃO'))
        if c[4] == 1:
            tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'SIM'))
        else:
            tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'NÃO'))
        if c[5] == 1:
            tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'SIM'))
        else:
            tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'NÃO'))
        if c[6] == 1:
            tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'SIM'))
        else:
            tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'NÃO'))            
        row += 1
    manut_usuarios.show()
    

def pega_usuario():
    linha = manut_usuarios.TabelaUsuarios.currentRow()
    nome = manut_usuarios.TabelaUsuarios.item(linha, 1).text()
    criar = manut_usuarios.TabelaUsuarios.item(linha, 2).text()
    editar = manut_usuarios.TabelaUsuarios.item(linha, 3).text()
    excluir = manut_usuarios.TabelaUsuarios.item(linha, 4).text()
    root = manut_usuarios.TabelaUsuarios.item(linha, 5).text()
    permissoes.InputUsuario.setText(nome)
    if criar == 'SIM':
        permissoes.CbCriar.setChecked(True)
    else:
        permissoes.CbCriar.setChecked(False)
    
    if editar == 'SIM':
        permissoes.CbEditar.setChecked(True)
    else:
        permissoes.CbEditar.setChecked(False)

    if excluir == 'SIM':
        permissoes.CbExcluir.setChecked(True)
    else:
        permissoes.CbExcluir.setChecked(False)
    
    if root == 'SIM':
        permissoes.CbRoot.setChecked(True)
    else:
        permissoes.CbRoot.setChecked(False)
    
    permissoes.show()

def carrega_usuario_asc():
    usuarios = banco.buscar_todos_usuarios_asc()
    row = 0
    tabela = manut_usuarios.TabelaUsuarios
    tabela.setRowCount(len(usuarios))
    tabela.setColumnWidth(0, 50)
    tabela.setColumnWidth(1, 350)
    tabela.setColumnWidth(2, 100)
    tabela.setColumnWidth(3, 100)
    tabela.setColumnWidth(4, 100)
    tabela.setColumnWidth(5, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    for c in usuarios:
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        if c[3] == 1:
            tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'SIM'))
        else:
            tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'NÃO'))
        if c[4] == 1:
            tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'SIM'))
        else:
            tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'NÃO'))
        if c[5] == 1:
            tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'SIM'))
        else:
            tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'NÃO'))
        if c[6] == 1:
            tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'SIM'))
        else:
            tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'NÃO'))            
        row += 1
    manut_usuarios.show()

def teste():
    print('Cheguei aqui')
    

def setar_permissoes():
    nome = permissoes.InputUsuario.text()
    criar = permissoes.CbCriar.isChecked()
    editar = permissoes.CbEditar.isChecked()
    excluir = permissoes.CbExcluir.isChecked()
    root = permissoes.CbRoot.isChecked()
    banco.alterar_permissoes(nome, criar, editar, excluir, root)
    QMessageBox.about(permissoes, 'PERMISSÕES ALTERADAS', f'Permissões do usuário {nome} alteradas com sucesso')
    carrega_usuarios()
    permissoes.close()


###########################

#FUNÇÕES PARA FUNCIONARIOS

def inserir_funcionario():
    funcionario.matricula = cad_func.InputMatricula.text().strip()
    funcionario.nome= cad_func.InputNome.text().title().strip()
    funcionario.funcao = cad_func.InputFuncao.text().title().strip()
    funcionario.id = None
    if funcionario.matricula == "" or funcionario.nome == ""  or funcionario.funcao=="":
        QMessageBox.about(cad_func, 'ERRO', f'Nenhum campo pode ficar sem preenchimento')
    else:
        existe = banco.busca_func_matricula(funcionario.matricula)
        if len(existe) != 0:
            QMessageBox.about(cad_func, 'ERRO', f'Já existe funcionário cadastrado com esta Matricula, verifique!!!')
        else:
            banco.inserir_funcionario(funcionario.nome, funcionario.funcao, funcionario.matricula)
            QMessageBox.about(cad_func, 'Funcionário Inserido', f'Funcionário {funcionario.nome} Inserido com sucesso')
            cad_func.InputMatricula.setText("")
            cad_func.InputNome.setText("")
            cad_func.InputFuncao.setText("")
            carrega_funcionario()
            cad_func.close()

def carrega_funcionario():
    vendas.tabWidget.setCurrentIndex(0)
    func = banco.busca_todos_funcionarios()
    row = 0
    tabela = vendas.TabelaFunc
    tabela.setRowCount(len(func))
    tabela.setColumnWidth(0, 30)
    tabela.setColumnWidth(1, 150)
    tabela.setColumnWidth(2, 350)
    tabela.setColumnWidth(3, 250)
    tabela.setColumnWidth(4, 150)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    for c in func:
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[3]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{c[4]}'))
        row += 1
      
    vendas.show()

def pega_func():
    linha = vendas.TabelaFunc.currentRow()
    id_func = int(vendas.TabelaFunc.item(linha, 0).text())
    matricula = vendas.TabelaFunc.item(linha, 1).text()
    nome = vendas.TabelaFunc.item(linha, 2).text()
    cargo = vendas.TabelaFunc.item(linha, 3).text()
    status = vendas.TabelaFunc.item(linha, 4).text()
    if status == 'Desligado' and usuario1.root == False:
        QMessageBox.about(vendas, 'ERRO', f'Funcionário já está desligado, solicite ao root para reativa-lo')
    else:
        manut_func.InputId.setValue(id_func)
        manut_func.InputMatricula.setText(matricula)
        manut_func.InputNome.setText(nome)
        manut_func.InputFuncao.setText(cargo)
        manut_func.show()

def altera_func():
    id_func = manut_func.InputId.value()
    matricula = manut_func.InputMatricula.text()
    nome = manut_func.InputNome.text().title().strip()
    cargo = manut_func.InputFuncao.text().title().strip()
    if nome == '' or cargo == '':
        QMessageBox.about(manut_func, 'ERRO', f'Nenhum campo pode ficar sem preenchimento')
    else:
        banco.alterar_funcionario(id_func, nome, cargo)
        QMessageBox.about(manut_func, 'FUNCIONÁRIO ALTERADO', f'Funcionário {nome} de matricula {matricula} alterado com sucesso')
        manut_func.close()
        carrega_tabelas()

def desliga_func():
    id_func = manut_func.InputId.value()
    matricula = manut_func.InputMatricula.text()
    nome = manut_func.InputNome.text().title()
    cargo = manut_func.InputFuncao.text().title()
    men = QMessageBox.question(manut_func, 'DESLIGAR FUNCIONÁRIO', f'ATENÇÃO, deseja realmente desligar o funcionário {nome}, com matricula {matricula} e cargo {cargo}?', QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
    if men == QMessageBox.Ok:
        banco.desligar_funcionario(id_func)
        QMessageBox.about(manut_item, 'FUNCIONÁRIO DESLIGADO', f'Funcionário {nome} desligado com sucesso')
        carrega_tabelas()
        manut_func.close()
    else:
        return

def reativa_func():
    id_func = manut_func.InputId.value()
    matricula = manut_func.InputMatricula.text()
    nome = manut_func.InputNome.text().title()
    cargo = manut_func.InputFuncao.text().title()
    men = QMessageBox.question(manut_func, 'REATIVAR FUNCIONÁRIO', f'ATENÇÃO, deseja realmente reativar o funcionário {nome}, com matricula {matricula} e cargo {cargo}?', QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
    if men == QMessageBox.Ok:
        banco.reativar_funcionario(id_func)
        QMessageBox.about(manut_item, 'FUNCIONÁRIO REATIVADO', f'Funcionário {nome} reativado com sucesso')
        carrega_tabelas()
        manut_func.close()
    else:
        return

################   

#FUNÇÕES PARA CLIENTES

def inserir_cliente():
    
    cliente.nome= cad_cliente.InputNome.text().title().strip()
    cliente.id = None
    if cliente.nome == "":
        QMessageBox.about(cad_cliente, 'ERRO', f'Nenhum campo pode ficar sem preenchimento')
    else:
        existe = banco.busca_cliente_nome(cliente.nome)
        if len(existe) != 0:
            QMessageBox.about(cad_cliente, 'ERRO', f'Já existe cliente cadastrado com esse nome, verifique!!!')
        else:
            banco.inserir_cliente(cliente.nome)
            QMessageBox.about(cad_cliente, 'Cliente Inserido', f'Cliente {cliente.nome} Inserido com sucesso')
            cad_cliente.InputNome.setText("")
            carrega_clientes()
            cad_cliente.close()

def carrega_clientes():
    vendas.tabWidget.setCurrentIndex(1)
    clientes = banco.busca_todos_clientes()
    row = 0
    tabela = vendas.TabelaClientes
    tabela.setRowCount(len(clientes))
    tabela.setColumnWidth(0, 50)
    tabela.setColumnWidth(1, 500)
    tabela.setColumnWidth(2, 150)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    for c in clientes:
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        row += 1
      
    vendas.show()

def pega_cliente():
    linha = vendas.TabelaClientes.currentRow()
    id_cliente = int(vendas.TabelaClientes.item(linha, 0).text())
    nome = vendas.TabelaClientes.item(linha, 1).text()
    status = vendas.TabelaClientes.item(linha, 2).text()
    if status == 'Desligado' and usuario1.root == False:
        QMessageBox.about(vendas, 'ERRO', f'Cliente já está desligado, solicite ao root para reativa-lo')
    else:
        manut_cliente.InputId.setValue(id_cliente)
        manut_cliente.InputNome.setText(nome)
        manut_cliente.show()

def altera_cliente():
    id_cliente = manut_cliente.InputId.value()
    nome = manut_cliente.InputNome.text().title().strip()
    if nome == '':
        QMessageBox.about(manut_cliente, 'ERRO', f'Nenhum campo pode ficar sem preenchimento')
    else:
        banco.alterar_cliente(id_cliente, nome)
        QMessageBox.about(manut_func, 'CLIENTE ALTERADO', f'Cliente {nome} alterado com sucesso')
        manut_cliente.close()
        carrega_tabelas()
        vendas.tabWidget.setCurrentIndex(1)

def desliga_cliente():
    id_cliente = manut_cliente.InputId.value()
    nome = manut_cliente.InputNome.text().title()
    if id_cliente == 1:
        QMessageBox.about(manut_cliente, 'ERRO', f'O cliente {nome} não pode ser desligado')
    else:
        men = QMessageBox.question(manut_cliente, 'DESLIGAR CLIENTE', f'ATENÇÃO, deseja realmente desligar o cliente {nome}?', QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if men == QMessageBox.Ok:
            banco.desligar_cliente(id_cliente)
            QMessageBox.about(manut_cliente, 'CLIENTE DESLIGADO', f'Cliente {nome} desligado com sucesso')
            carrega_tabelas()
            carrega_clientes()
            manut_cliente.close()
        else:
            return

def reativa_cliente():
    id_cliente = manut_cliente.InputId.value()
    nome = manut_cliente.InputNome.text().title()
    if id_cliente == 1:
        QMessageBox.about(manut_cliente, 'ERRO', f'O cliente {nome} não pode ser desligado')
    else:
        men = QMessageBox.question(manut_cliente, 'REATIVAR CLIENTE', f'ATENÇÃO, deseja realmente reativar o cliente {nome}?', QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if men == QMessageBox.Ok:
            banco.reativar_cliente(id_cliente)
            QMessageBox.about(manut_cliente, 'CLIENTE REATIVADO', f'Cliente {nome} reativado com sucesso')
            carrega_tabelas()
            carrega_clientes()
            manut_cliente.close()
        else:
            return
#########################

#FUNÇÕES PARA PRODUTOS

def inserir_produto():
    
    produto.nome = cad_produtos.InputNome.text().title().strip()
    produto.valor= cad_produtos.InputValor.value()
    produto.codigo = None
    if produto.nome == "" or produto.valor == 0:
        QMessageBox.about(cad_produtos, 'ERRO', f'Nenhum campo pode ficar sem preenchimento e o valor do produto não pode ser Zero')
    else:
        existe = banco.busca_produto_nome(produto.nome)
        if len(existe) != 0:
            QMessageBox.about(cad_produtos, 'ERRO', f'Já existe produto cadastrado com esse nome, verifique!!!')
        else:
            banco.inserir_produto(produto.nome, produto.valor)
            QMessageBox.about(cad_produtos, 'Produto Inserido', f'Produto {produto.nome} Inserido com sucesso')
            cad_produtos.InputNome.setText("")
            cad_produtos.InputValor.setValue(0)
            carrega_produtos()
            cad_produtos.close()

def carrega_produtos():
    vendas.tabWidget.setCurrentIndex(2)
    produtos = banco.busca_todos_produtos()
    row = 0
    tabela = vendas.TabelaProd
    tabela.setRowCount(len(produtos))
    tabela.setColumnWidth(0, 100)
    tabela.setColumnWidth(1, 400)
    tabela.setColumnWidth(2, 100)
    tabela.setColumnWidth(3, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    for c in produtos:
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'R$ {c[2]:.2f}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[3]}'))
        row += 1
      
    vendas.show()

def pega_produto():
    linha = vendas.TabelaProd.currentRow()
    codigo = int(vendas.TabelaProd.item(linha, 0).text())
    descricao = vendas.TabelaProd.item(linha, 1).text()
    valor = vendas.TabelaProd.item(linha, 2).text()
    valor = valor.replace('R$ ', '')
    valor = float(valor)
    status = vendas.TabelaProd.item(linha, 3).text()
    if status == 'Desligado' and usuario1.root == False:
        QMessageBox.about(vendas, 'ERRO', f'Produto já está desligado, solicite ao root para reativa-lo')
    else:
        manut_produtos.InputCodigo.setValue(codigo)
        manut_produtos.InputNome.setText(descricao)
        manut_produtos.InputValor.setValue(valor)
        manut_produtos.show()

def altera_produto():
    codigo = manut_produtos.InputCodigo.value()
    descricao = manut_produtos.InputNome.text().title().strip()
    preco = manut_produtos.InputValor.value()
    if descricao == '' or preco == 0:
        QMessageBox.about(manut_produtos, 'ERRO', f'Nenhum campo pode ficar sem preenchimento e o preço não pode ser Zero')
    else:
        banco.alterar_produto(codigo, descricao, preco)
        QMessageBox.about(manut_produtos, 'PRODUTO ALTERADO', f'Produto {descricao} alterado com sucesso')
        manut_produtos.close()
        carrega_tabelas()
        carrega_produtos()

def desliga_produto():
    codigo = manut_produtos.InputCodigo.value()
    descricao = manut_produtos.InputNome.text().title()
    men = QMessageBox.question(manut_produtos, 'DESLIGAR PRODUTO', f'ATENÇÃO, deseja realmente desligar o produto {descricao}?', QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
    if men == QMessageBox.Ok:
        banco.desligar_produto(codigo)
        QMessageBox.about(manut_produtos, 'PRODUTO DESLIGADO', f'Produto {descricao} desligado com sucesso')
        carrega_tabelas()
        carrega_produtos()
        manut_produtos.close()
    else:
        return

def reativa_produto():
    codigo = manut_produtos.InputCodigo.value()
    descricao = manut_produtos.InputNome.text().title()
    men = QMessageBox.question(manut_produtos, 'REATIVAR PRODUTO', f'ATENÇÃO, deseja realmente reativar o produto {descricao}?', QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
    if men == QMessageBox.Ok:
        banco.reativar_produto(codigo)
        QMessageBox.about(manut_produtos, 'PRODUTO REATIVADO', f'Produto {descricao} reativado com sucesso')
        carrega_tabelas()
        carrega_produtos()
        manut_produtos.close()
    else:
        return

#################

#FUNÇÕES NF

def emitir_nf():
    nf.comboClientes.clear()
    nf.comboVendedor.clear()
    nf.comboProdutos.clear()
    nf.tabWidget.setCurrentIndex(0)
    clientes = banco.busca_todos_clientes_combo_ativos()
    vendedor = banco.busca_todos_funcionarios_combo_ativos()
    for c in clientes:
        nf.comboClientes.addItem(f"{c[1]}", QVariant(c[0]))
    for v in vendedor:
        nf.comboVendedor.addItem(f'{v[1]}        MATRÍCULA->{v[3]}', QVariant(v[0]))
    carrega_notas()
    nf.NumeroNf.setValue(0)
    nf.show()

def informa_itens():
    nf.tabWidget.setCurrentIndex(1)
    produtos = banco.busca_todos_produtos_ativos()
    for p in produtos:
        nf.comboProdutos.addItem(f"{p[1]}", QVariant(p[0]))
    carrega_notas()
    nf.show()

def busca_preco():
    id_produto = nf.comboProdutos.currentData()
    preco_produto = banco.buscar_preco_id(id_produto)
    preco = float(preco_produto[0][0])
    nf.InputPreco.setValue(preco)

def busca_preco_manut():
    id_produto = manut_nf.comboProdutos.currentData()
    preco_produto = banco.buscar_preco_id(id_produto)
    preco = float(preco_produto[0][0])
    manut_nf.InputPreco.setValue(preco)

def busca_ultima_nota():
    num = banco.proxima_nf()
    proxima_nota = num[0]
    return proxima_nota

def gerar_nf():
    nf.tabWidget.setCurrentIndex(1)
    id_cliente = nf.comboClientes.currentData()
    id_vendedor = nf.comboVendedor.currentData()
    banco.gravar_nf(id_cliente, id_vendedor)
    carrega_itens()

    num_nf = busca_ultima_nota()
    nf.NumeroNf.setValue(num_nf)
    carrega_notas()
    informa_itens()
    habilitar_botao()

def inserir_item():
    num_nf = nf.NumeroNf.value()
    codigo = int(nf.comboProdutos.currentData())
    qtde = nf.InputQuantidade.value()
    preco = nf.InputPreco.value()
    if qtde == 0 or preco == 0:
        QMessageBox.about(nf, 'ERRO', f'Quantidade ou valor inválido, verifique!!!')
    else:
        banco.inserir_itens_nf(num_nf, codigo, qtde, preco)
        nf.InputQuantidade.setValue(0)
        carrega_itens()

def inserir_item_manut():
    num_nf = manut_nf.NumeroNf.value()
    codigo = int(manut_nf.comboProdutos.currentData())
    qtde = manut_nf.InputQuantidade.value()
    preco = manut_nf.InputPreco.value()
    if qtde == 0 or preco == 0:
        QMessageBox.about(manut_nf, 'ERRO', f'Quantidade ou valor inválido, verifique!!!')
    else:
        banco.inserir_itens_nf(num_nf, codigo, qtde, preco)
        manut_nf.InputQuantidade.setValue(0)
        carrega_itens_manut()

def calcular_nf():
    num_nf = nf.NumeroNf.value()
    total = banco.calcula_total_nf(num_nf)
    if total[0][0] == None:
        QMessageBox.about(nf, 'ERRO', f'Nota fiscal não pode ser gerada pois não foi incluido nenhum item')
    else:
        total_nf = float(total[0][0])
        banco.atualizar_nf(num_nf, total_nf)
        carrega_tabelas()
        vendas.tabWidget.setCurrentIndex(3)
        nf.NumeroNf.setValue(0)
        nf.close()

def calcular_nf_manut():
    num_nf = manut_nf.NumeroNf.value()
    total = banco.calcula_total_nf(num_nf)
    if total[0][0] == None:
        QMessageBox.about(manut_nf, 'ERRO', f'Nota fiscal não pode ser gerada pois não foi incluido nenhum item')
    else:
        total_nf = float(total[0][0])
        banco.atualizar_nf(num_nf, total_nf)
        carrega_tabelas()
        vendas.tabWidget.setCurrentIndex(3)
        manut_nf.NumeroNf.setValue(0)
        manut_nf.close()

def habilitar_botao():
    if nf.NumeroNf.value() == 0:
        nf.BtnInserir.setVisible(False)
        nf.BtnCalcularNf.setVisible(False)
    else:
        nf.BtnInserir.setVisible(True)
        nf.BtnCalcularNf.setVisible(True)

def carrega_notas():
    vendas.tabWidget.setCurrentIndex(3)
    todas = vendas.RbTodas.isChecked()
    pendentes = vendas.RbPendentes.isChecked()
    emitidas = vendas.RbEmitidas.isChecked()
    canceladas = vendas.RbCanceladas.isChecked()
    if todas:
        notas = banco.busca_todas_notas()
    elif pendentes:
        notas = banco.busca_todas_notas_status('Pendente')
    elif emitidas:
        notas = banco.busca_todas_notas_status('Emitida')
    else:
        notas = banco.busca_todas_notas_status('Cancelada')
    row = 0
    tabela = vendas.TabelaNfs
    tabela.setRowCount(len(notas))
    tabela.setColumnWidth(0, 70)
    tabela.setColumnWidth(1, 130)
    tabela.setColumnWidth(2, 130)
    tabela.setColumnWidth(3, 200)
    tabela.setColumnWidth(4, 200)
    tabela.setColumnWidth(5, 200)
    tabela.setColumnWidth(6, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total_notas = 0
    for c in notas:
        total_notas += c[5]
        data = funcoes.banco_data(c[1])
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{data}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[4]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[3]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'R$ {c[5]:.2f}'))
        tabela.setItem(row, 6, QtWidgets.QTableWidgetItem(f'{c[6]}'))
        row += 1
    vendas.lbl_total.setText(f'Total das notas selecionadas: R$ {total_notas:.2f}')
    vendas.show()

def carrega_notas_data():
    vendas.tabWidget.setCurrentIndex(3)
    data = nf_data.InputData.text()
    data = funcoes.data_banco(data)
    todas = nf_data.RbTodas.isChecked()
    pendentes = nf_data.RbPendentes.isChecked()
    emitidas = nf_data.RbEmitidas.isChecked()
    canceladas = nf_data.RbCanceladas.isChecked()
    if todas:
        notas = banco.buscar_nf_data(data)
    elif pendentes:
        notas = banco.busca_nf_data_status(data, 'Pendente')
    elif emitidas:
        notas = banco.busca_nf_data_status(data ,'Emitida')
    else:
        notas = banco.busca_nf_data_status(data, 'Cancelada')
    row = 0
    tabela = vendas.TabelaNfs
    tabela.setRowCount(len(notas))
    tabela.setColumnWidth(0, 70)
    tabela.setColumnWidth(1, 130)
    tabela.setColumnWidth(2, 130)
    tabela.setColumnWidth(3, 200)
    tabela.setColumnWidth(4, 200)
    tabela.setColumnWidth(5, 200)
    tabela.setColumnWidth(6, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total_notas = 0
    for c in notas:
        total_notas += c[5]
        data = funcoes.banco_data(c[1])
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{data}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[4]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[3]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'R$ {c[5]:.2f}'))
        tabela.setItem(row, 6, QtWidgets.QTableWidgetItem(f'{c[6]}'))
        row += 1
    vendas.lbl_total.setText(f'Total das notas selecionadas: R$ {total_notas:.2f}')
    nf_data.close()  
    vendas.show()

def carrega_notas_cliente():
    vendas.tabWidget.setCurrentIndex(3)
    id_cliente = nf_cliente.comboClientes.currentData()
    todas = nf_cliente.RbTodas.isChecked()
    pendentes = nf_cliente.RbPendentes.isChecked()
    emitidas = nf_cliente.RbEmitidas.isChecked()
    canceladas = nf_cliente.RbCanceladas.isChecked()
    if todas:
        notas = banco.buscar_nf_cliente(id_cliente)
    elif pendentes:
        notas = banco.buscar_nf_cliente_status(id_cliente, 'Pendente')
    elif emitidas:
        notas = banco.buscar_nf_cliente_status(id_cliente ,'Emitida')
    else:
        notas = banco.buscar_nf_cliente_status(id_cliente, 'Cancelada')
    row = 0
    tabela = vendas.TabelaNfs
    tabela.setRowCount(len(notas))
    tabela.setColumnWidth(0, 70)
    tabela.setColumnWidth(1, 130)
    tabela.setColumnWidth(2, 130)
    tabela.setColumnWidth(3, 200)
    tabela.setColumnWidth(4, 200)
    tabela.setColumnWidth(5, 200)
    tabela.setColumnWidth(6, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total_notas = 0
    for c in notas:
        total_notas += c[5]
        data = funcoes.banco_data(c[1])
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{data}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[4]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[3]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'R$ {c[5]:.2f}'))
        tabela.setItem(row, 6, QtWidgets.QTableWidgetItem(f'{c[6]}'))
        row += 1
    vendas.lbl_total.setText(f'Total das notas selecionadas: R$ {total_notas:.2f}')
    nf_cliente.close()  
    vendas.show()

def carrega_notas_func():
    vendas.tabWidget.setCurrentIndex(3)
    id_func = nf_func.comboFunc.currentData()
    todas = nf_func.RbTodas.isChecked()
    pendentes = nf_func.RbPendentes.isChecked()
    emitidas = nf_func.RbEmitidas.isChecked()
    canceladas = nf_func.RbCanceladas.isChecked()
    if todas:
        notas = banco.buscar_nf_func(id_func)
    elif pendentes:
        notas = banco.buscar_nf_func_status(id_func, 'Pendente')
    elif emitidas:
        notas = banco.buscar_nf_func_status(id_func ,'Emitida')
    else:
        notas = banco.buscar_nf_func_status(id_func, 'Cancelada')
    row = 0
    tabela = vendas.TabelaNfs
    tabela.setRowCount(len(notas))
    tabela.setColumnWidth(0, 70)
    tabela.setColumnWidth(1, 130)
    tabela.setColumnWidth(2, 130)
    tabela.setColumnWidth(3, 200)
    tabela.setColumnWidth(4, 200)
    tabela.setColumnWidth(5, 200)
    tabela.setColumnWidth(6, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total_notas = 0
    for c in notas:
        data = funcoes.banco_data(c[1])
        total_notas += c[5]
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{data}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[4]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[3]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'R$ {c[5]:.2f}'))
        tabela.setItem(row, 6, QtWidgets.QTableWidgetItem(f'{c[6]}'))
        row += 1
    vendas.lbl_total.setText(f'Total das notas selecionadas: R$ {total_notas:.2f}')
    nf_func.close()  
    vendas.show()

def carrega_itens():
    nf.tabWidget.setCurrentIndex(1)
    num_nf = nf.NumeroNf.value()
    itens = banco.buscar_itens_nf(num_nf)
    row = 0
    tabela = nf.TabelaItensNf
    tabela.setRowCount(len(itens))
    tabela.setColumnWidth(0, 40)
    tabela.setColumnWidth(1, 80)
    tabela.setColumnWidth(2, 80)
    tabela.setColumnWidth(3, 300)
    tabela.setColumnWidth(4, 100)
    tabela.setColumnWidth(5, 120)
    tabela.setColumnWidth(6, 200)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total_notas = 0
    for c in itens:
        total_notas += c[5]
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[8]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{c[3]}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'R$ {c[4]:.2f}'))
        tabela.setItem(row, 6, QtWidgets.QTableWidgetItem(f'R$ {c[5]:.2f}'))
        row += 1
    nf.lbl_total.setText(f'Total dos itens da nota: R$ {total_notas:.2f}')

def carrega_itens_manut():
    num_nf = manut_nf.NumeroNf.value()
    itens = banco.buscar_itens_nf(num_nf)
    row = 0
    tabela = manut_nf.TabelaItensNf
    tabela.setRowCount(len(itens))
    tabela.setColumnWidth(0, 40)
    tabela.setColumnWidth(1, 80)
    tabela.setColumnWidth(2, 80)
    tabela.setColumnWidth(3, 300)
    tabela.setColumnWidth(4, 100)
    tabela.setColumnWidth(5, 120)
    tabela.setColumnWidth(6, 200)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total_notas = 0
    for c in itens:
        total_notas += c[5]
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[8]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{c[3]}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'R$ {c[4]:.2f}'))
        tabela.setItem(row, 6, QtWidgets.QTableWidgetItem(f'R$ {c[5]:.2f}'))
        row += 1
    manut_nf.lbl_total.setText(f'Total dos itens da nota: R$ {total_notas:.2f}')

def pega_nota():
    manut_nf.comboProdutos.clear()
    linha = vendas.TabelaNfs.currentRow()
    num_nf = int(vendas.TabelaNfs.item(linha, 0).text())
    status = vendas.TabelaNfs.item(linha, 6).text()
    manut_nf.InputStatus.setText(status)
    manut_nf.NumeroNf.setValue(num_nf)
    if status == 'Pendente':
        produtos = banco.busca_todos_produtos_ativos()
        for p in produtos:
            manut_nf.comboProdutos.addItem(f"{p[1]}", QVariant(p[0]))
        manut_nf.BtnInserir.setVisible(True)
        manut_nf.BtnCalcularNf.setVisible(True)
    else:
        manut_nf.BtnInserir.setVisible(False)
        manut_nf.BtnCalcularNf.setVisible(False)
    carrega_itens_manut()
    manut_nf.show()

def pega_item():
    linha = nf.TabelaItensNf.currentRow()
    num_nf = int(nf.TabelaItensNf.item(linha, 1).text())
    id_item = int(nf.TabelaItensNf.item(linha, 0).text())
    item = nf.TabelaItensNf.item(linha, 3).text()
    preco = nf.TabelaItensNf.item(linha, 5).text()
    preco = preco.replace('R$ ', '')
    preco = float(preco)
    qtde = float(nf.TabelaItensNf.item(linha, 4).text()) 
    manut_item.NumeroNf.setValue(num_nf)
    manut_item.InputQuantidade.setValue(qtde)
    manut_item.IdItem.setValue(id_item)
    manut_item.InputPreco.setValue(preco)
    manut_item.InputProduto.setText(item)
    manut_item.show()

def pega_item_manut():
    linha = manut_nf.TabelaItensNf.currentRow()
    num_nf = int(manut_nf.TabelaItensNf.item(linha, 1).text())
    id_item = int(manut_nf.TabelaItensNf.item(linha, 0).text())
    item = manut_nf.TabelaItensNf.item(linha, 3).text()
    preco = manut_nf.TabelaItensNf.item(linha, 5).text()
    preco = preco.replace('R$ ', '')
    preco = float(preco)
    qtde = float(manut_nf.TabelaItensNf.item(linha, 4).text()) 
    status = manut_nf.InputStatus.text()
    manut_item.NumeroNf.setValue(num_nf)
    manut_item.InputQuantidade.setValue(qtde)
    manut_item.IdItem.setValue(id_item)
    manut_item.InputPreco.setValue(preco)
    manut_item.InputProduto.setText(item)
    if status == 'Pendente':
        manut_item.BtnAlterar.setVisible(True)
        manut_item.BtnExcluir.setVisible(True)
    else:
        manut_item.BtnAlterar.setVisible(False)
        manut_item.BtnExcluir.setVisible(False)
    manut_item.show()

def cancelar_nf():
    num_nf = manut_nf.NumeroNf.value()
    banco.cancelar_nf(num_nf)
    banco.excluir_itens_nf(num_nf)
    banco.atualizar_nf_cancelamento(num_nf, 0)
    carrega_notas()
    manut_nf.close()
    
def excluir_item():
    id = manut_item.IdItem.value()
    item = manut_item.InputProduto.text()
    men = QMessageBox.question(manut_item, 'EXCLUSÃO DE ITEM', f'ATENÇÃO, deseja excluir o item {item}?', QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
    if men == QMessageBox.Ok:
        banco.excluir_item_nf(id)
        QMessageBox.about(manut_item, 'ITEM EXCLUIDO', f'item {item} excluido com sucesso')
        carrega_itens_manut()
        carrega_itens()
        manut_item.close()
    else:
        return
        
def altera_item():
    id = manut_item.IdItem.value()
    qtde = manut_item.InputQuantidade.value()
    preco = manut_item.InputPreco.value()
    if qtde == 0 or preco == 0:
        QMessageBox.about(manut_item, 'ERRO', f'Quantidade ou valor inválido, verifique!!!')
    else:
        banco.alterar_itens_nf(qtde, preco, id)
        QMessageBox.about(manut_item, 'PRODUTO ALTERADO', f'Item alterado com sucesso')
        manut_item.close()
        carrega_itens_manut()
        carrega_itens()

def cliente_nf_combo():
    nf_cliente.comboClientes.clear()
    clientes = banco.busca_todos_clientes_combo()
    for c in clientes:
        nf_cliente.comboClientes.addItem(f"{c[1]}", QVariant(c[0]))
    nf_cliente.show()

def vendedor_nf_combo():
    nf_func.comboFunc.clear()
    vendedor = banco.busca_todos_funcionarios_combo()
    for v in vendedor:
        nf_func.comboFunc.addItem(f'{v[1]}        MATRÍCULA->{v[3]}', QVariant(v[0]))
    nf_func.show()

######################



#ESTATÍSTICAS


def setar_periodo():
    data_inicial = analise.dataInicial.date()
    data_final = analise.dataFinal.date()
    ok = funcoes.inicial_maior_final(data_inicial, data_final)
    if not ok:
        QMessageBox.about(analise, 'ERRO', 'Data inicial precisa ser menor ou igual a data final')
    else:
        carrega_ranking_produtos()
        carrega_ranking_clientes()
        carrega_ranking_funcionarios()
        analise.tabWidget.setCurrentIndex(1)

def carrega_ranking_produtos():
    data_inicial = funcoes.data_banco(analise.dataInicial.text())
    data_final = funcoes.data_banco(analise.dataFinal.text())
    row = 0
    tabela = analise.TabelaProd
    produtos = banco.vendas_por_item_ranking_desc_datas(data_inicial, data_final)
    tabela.setRowCount(len(produtos))
    tabela.setColumnWidth(0, 250)
    tabela.setColumnWidth(1, 80)
    tabela.setColumnWidth(2, 300)
    tabela.setColumnWidth(3, 100)
    tabela.setColumnWidth(4, 100)
    tabela.setColumnWidth(5, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total = 0
    for c in produtos:
        total += c[3]
        preco_medio = c[3]/c[2]
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'   {row+1}° colocado no ranking'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'R$ {c[3]:.2f}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'R$ {preco_medio:.2f}'))
        row += 1
    analise.lbl_total_Produto.setText(f'Total do período: R$ {total:.2f}')

def carrega_ranking_clientes():
    data_inicial = funcoes.data_banco(analise.dataInicial.text())
    data_final = funcoes.data_banco(analise.dataFinal.text())
    row = 0
    tabela = analise.TabelaClientes
    clientes = banco.vendas_por_cliente_ranking_desc_datas(data_inicial, data_final)
    tabela.setRowCount(len(clientes))
    tabela.setColumnWidth(0, 250)
    tabela.setColumnWidth(1, 80)
    tabela.setColumnWidth(2, 300)
    tabela.setColumnWidth(3, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total = 0
    for c in clientes:
        total += c[2]
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'   {row+1}° colocado no ranking'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'R$ {c[2]:.2f}'))
        row += 1
    analise.lbl_total_Cliente.setText(f'Total do período: R$ {total:.2f}')

def carrega_ranking_funcionarios():
    data_inicial = funcoes.data_banco(analise.dataInicial.text())
    data_final = funcoes.data_banco(analise.dataFinal.text())
    row = 0
    tabela = analise.Tabelafunc
    funcionarios = banco.vendas_por_funcionario_ranking_desc_data(data_inicial, data_final)
    tabela.setRowCount(len(funcionarios))
    tabela.setColumnWidth(0, 250)
    tabela.setColumnWidth(1, 80)
    tabela.setColumnWidth(2, 150)
    tabela.setColumnWidth(3, 300)
    tabela.setColumnWidth(4, 150)
    tabela.setColumnWidth(5, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total = 0
    for c in funcionarios:
        total += c[3]
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'   {row+1}° colocado no ranking'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'R$ {c[3]:.2f}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'{c[4]}'))
        row += 1
    analise.lbl_total_func.setText(f'Total do período: R$ {total:.2f}')


def rodar():
    analise.tabWidget.setCurrentIndex(0)
    analise.show()


####################

def carrega_tabelas():
    carrega_funcionario()
    carrega_clientes()
    carrega_produtos()
    carrega_notas()
    carrega_funcionario()
    vendas.show()

#TELAS

if __name__ == '__main__':

    usuario1 = Usuarios()
    

    qt = QtWidgets.QApplication(sys.argv)
    login = uic.loadUi('tela_login.ui')
    cad_usuario = uic.loadUi('tela_cadastro.ui')
    manut_usuarios = uic.loadUi('manutencao_usuarios.ui')
    permissoes = uic.loadUi('permissoes_usuarios.ui')
    vendas = uic.loadUi('vendas.ui')
    cad_func = uic.loadUi('cad_func.ui')
    cad_cliente = uic.loadUi('cad_cliente.ui')
    cad_produtos = uic.loadUi('cad_produtos.ui')
    nf = uic.loadUi('emissao_nf.ui')
    manut_nf = uic.loadUi('manut_nf.ui')
    manut_item = uic.loadUi('manut_item_nf.ui')
    nf_data = uic.loadUi('nf_por_data.ui')
    nf_func = uic.loadUi('nf_por_func.ui')
    nf_cliente = uic.loadUi('nf_por_cliente.ui')
    manut_func = uic.loadUi('manut_func.ui')
    manut_cliente = uic.loadUi('manut_cliente.ui')
    manut_produtos = uic.loadUi('manut_produtos.ui')
    analise = uic.loadUi('estatisticas.ui')
    #VENDAS

    vendas.BtnCadFuncionario.clicked.connect(cad_func.show)
    vendas.BtnCadClientes.clicked.connect(cad_cliente.show)
    vendas.BtnCadProdutos.clicked.connect(cad_produtos.show)
    vendas.BtnNVenda.clicked.connect(emitir_nf)
    vendas.TabelaNfs.doubleClicked.connect(pega_nota)
    vendas.RbCanceladas.clicked.connect(carrega_notas)
    vendas.RbEmitidas.clicked.connect(carrega_notas)
    vendas.RbPendentes.clicked.connect(carrega_notas)
    vendas.RbTodas.clicked.connect(carrega_notas)
    vendas.RbData.clicked.connect(nf_data.show)
    vendas.RbCliente.clicked.connect(cliente_nf_combo)
    vendas.RbFunc.clicked.connect(vendedor_nf_combo)
    vendas.BtnRoot.clicked.connect(abrir_cria_usuario)
    vendas.BtnEstatisiticas.clicked.connect(rodar)
    nf_data.BtnConfirmar.clicked.connect(carrega_notas_data)
    nf_data.InputData.setDate(data_atual)
    nf_cliente.BtnConfirmar.clicked.connect(carrega_notas_cliente)
    nf_func.BtnConfirmar.clicked.connect(carrega_notas_func)
    ############


    #FUNCIONÁRIOS
    funcionario = Funcionario()
    vendas.TabelaFunc.doubleClicked.connect(pega_func)
    cad_func.BtnInserir.clicked.connect(inserir_funcionario)
    manut_func.BtnAlterar.clicked.connect(altera_func)
    manut_func.BtnSair.clicked.connect(manut_func.close)
    manut_func.BtnDesligar.clicked.connect(desliga_func)
    manut_func.BtnReativar.clicked.connect(reativa_func)
    ##############

    #CLIENTES
    cliente = Cliente()
    vendas.TabelaClientes.doubleClicked.connect(pega_cliente)
    cad_cliente.BtnInserir.clicked.connect(inserir_cliente)
    manut_cliente.BtnAlterar.clicked.connect(altera_cliente)
    manut_cliente.BtnSair.clicked.connect(manut_cliente.close)
    manut_cliente.BtnDesligar.clicked.connect(desliga_cliente)
    manut_cliente.BtnReativar.clicked.connect(reativa_cliente)
    #####################

    #PRODUTOS
    produto = Produto()
    vendas.TabelaProd.doubleClicked.connect(pega_produto)
    cad_produtos.BtnInserir.clicked.connect(inserir_produto)
    manut_produtos.BtnAlterar.clicked.connect(altera_produto)
    manut_produtos.BtnSair.clicked.connect(manut_produtos.close)
    manut_produtos.BtnDesligar.clicked.connect(desliga_produto)
    manut_produtos.BtnReativar.clicked.connect(reativa_produto)
    ###############

    #NOTA FISCAL

    nf.tabWidget.currentChanged.connect(habilitar_botao)
    nf.BtnGerarNf.clicked.connect(gerar_nf)
    nf.comboProdutos.currentTextChanged.connect(busca_preco)
    nf.BtnInserir.clicked.connect(inserir_item)
    nf.BtnCalcularNf.clicked.connect(calcular_nf)
    nf.TabelaItensNf.doubleClicked.connect(pega_item)
    manut_nf.comboProdutos.currentTextChanged.connect(busca_preco_manut)
    manut_nf.BtnInserir.clicked.connect(inserir_item_manut)
    manut_nf.BtnCalcularNf.clicked.connect(calcular_nf_manut)
    manut_nf.BtnCancelarNf.clicked.connect(cancelar_nf)
    manut_nf.TabelaItensNf.doubleClicked.connect(pega_item_manut)
    manut_item.BtnSair.clicked.connect(manut_item.close)
    manut_item.BtnAlterar.clicked.connect(altera_item)
    manut_item.BtnExcluir.clicked.connect(excluir_item)
    
    ###############

    #USUÁRIOS



    login.BtnEntrar.clicked.connect(fazer_login)
    cad_usuario.BtnCadastrar.clicked.connect(criar_novo_usuario)
    cad_usuario.BtnLogin.clicked.connect(abrir_tela_login)
    cad_usuario.BtnPermissao.clicked.connect(carrega_usuarios)
    manut_usuarios.BtnVoltar.clicked.connect(manut_usuarios.close)
    manut_usuarios.BtnOrdenar.clicked.connect(carrega_usuario_asc)
    manut_usuarios.BtnOrdenarID.clicked.connect(carrega_usuarios)
    manut_usuarios.TabelaUsuarios.doubleClicked.connect(pega_usuario)
    manut_usuarios.TabelaUsuarios.setSortingEnabled(True)
    tabela = manut_usuarios.TabelaUsuarios
    permissoes.BtnCancelar.clicked.connect(permissoes.close)
    permissoes.BtnSetar.clicked.connect(setar_permissoes)

    ##############

    #ESTATÍSTICAS

    
    analise.dataInicial.setDate(data_atual)
    analise.dataFinal.setDate(data_atual)
    analise.BtnConfirmar.clicked.connect(setar_periodo)


    ##################

    banco.cria_tabelas()
    login.show()
    qt.exec_()