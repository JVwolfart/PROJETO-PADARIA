from PyQt5 import QtWidgets
import banco
import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
#import funcoes
import datetime
from classes import Usuarios
from funcoes import banco_data, data_banco, data_banco1, inicial_maior_final


data_atual = datetime.date.today()
ano_atual = data_atual.year

def setar_periodo():
    data_inicial = analise.dataInicial.date()
    data_final = analise.dataFinal.date()
    ok = inicial_maior_final(data_inicial, data_final)
    if not ok:
        QMessageBox.about(analise, 'ERRO', 'Data inicial precisa ser menor ou igual a data final')
    else:
        carrega_ranking_produtos()
        carrega_ranking_clientes()
        carrega_ranking_funcionarios()
        analise.tabWidget.setCurrentIndex(1)

def carrega_ranking_produtos():
    data_inicial = data_banco(analise.dataInicial.text())
    data_final = data_banco(analise.dataFinal.text())
    row = 0
    tabela = analise.TabelaProd
    produtos = banco.vendas_por_item_ranking_desc_datas(data_inicial, data_final)
    tabela.setRowCount(len(produtos))
    tabela.setColumnWidth(0, 200)
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
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{row+1}° no ranking'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'R$ {c[3]:.2f}'))
        tabela.setItem(row, 5, QtWidgets.QTableWidgetItem(f'R$ {preco_medio:.2f}'))
        row += 1
    analise.lbl_total_Produto.setText(f'Total do período: R$ {total:.2f}')

def carrega_ranking_clientes():
    data_inicial = data_banco(analise.dataInicial.text())
    data_final = data_banco(analise.dataFinal.text())
    row = 0
    tabela = analise.TabelaClientes
    clientes = banco.vendas_por_cliente_ranking_desc_datas(data_inicial, data_final)
    tabela.setRowCount(len(clientes))
    tabela.setColumnWidth(0, 200)
    tabela.setColumnWidth(1, 80)
    tabela.setColumnWidth(2, 300)
    tabela.setColumnWidth(3, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total = 0
    for c in clientes:
        total += c[2]
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{row+1}° no ranking'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'R$ {c[2]:.2f}'))
        row += 1
    analise.lbl_total_Cliente.setText(f'Total do período: R$ {total:.2f}')

def carrega_ranking_funcionarios():
    data_inicial = data_banco(analise.dataInicial.text())
    data_final = data_banco(analise.dataFinal.text())
    row = 0
    tabela = analise.Tabelafunc
    funcionarios = banco.vendas_por_funcionario_ranking_desc_data(data_inicial, data_final)
    tabela.setRowCount(len(funcionarios))
    tabela.setColumnWidth(0, 200)
    tabela.setColumnWidth(1, 80)
    tabela.setColumnWidth(2, 150)
    tabela.setColumnWidth(3, 300)
    tabela.setColumnWidth(4, 100)
    tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    total = 0
    for c in funcionarios:
        total += c[3]
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{row+1}° no ranking'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{c[0]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{c[1]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{c[2]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'R$ {c[3]:.2f}'))
        row += 1
    analise.lbl_total_func.setText(f'Total do período: R$ {total:.2f}')


def rodar():
    analise.tabWidget.setCurrentIndex(0)
    analise.show()


usuario1 = Usuarios()

qt = QtWidgets.QApplication(sys.argv)
analise = uic.loadUi('estatisticas.ui')


analise.dataInicial.setDate(data_atual)
analise.dataFinal.setDate(data_atual)
analise.BtnConfirmar.clicked.connect(setar_periodo)

if __name__ == '__main__':
    
    rodar()
    qt.exec_()