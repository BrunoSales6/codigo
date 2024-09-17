import sqlite3  # importa sqlite
from PyQt5.QtWidgets import *  # importa todos os widgets
from PyQt5.QtGui import *  # importa todos os recursos gráficos
import sys  # importa algumas variavies
import os 
from os import path  # importa o módulo pathpara manipular caminho de arquivos
from PyQt5.uic import loadUiType  # classe que carrega um arquivo de extensão .ui
def resource_path(relative_path): #função do py-to-exe
    '''GET absolute path to resource, works for dev and for PyInstaller'''
    base_path=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,relative_path)

# Carregando Interface e criando uma classe a parti dela
FORM_CLASS, _ = loadUiType(resource_path("GUI.ui"))
# O caracter '_' faz com que a seguunda classe cirada pelo loadUiType seja ignorada. 
# A primeira classe contém todos os widgets e layouts definidos no Qt Designer.
# A segunda classe é apenas uma classe Qt que serve commo base para interface.


# Classe Main que define tudo da interface.
# A class Main herda tudo da FORM_CLASS e da QMainWindow.
#A QMainWindow tem todos os elemetos básicos de uma interface.
class Main(QMainWindow, FORM_CLASS):
    def __init__(self):
        super(Main, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.NAVEGAR()
        self.NAVEGAR_SERVICO()

    def Handel_Buttons(self):  # Trnasmite os sinais dos botões da interface para os slots
        self.atualizar.clicked.connect(self.GET_DATA)
        self.atualizar2.clicked.connect(self.GET_DATA2)
        self.procura_botao.clicked.connect(self.PROCURAR)
        self.verificar_inventario.clicked.connect(self.VERIFICAR)
        self.update_btn.clicked.connect(self.UPDATE)
        self.update_btn_servico.clicked.connect(self.UPDATE_SERVICO)
        self.delete_btn.clicked.connect(self.DELETAR)
        self.delete_btn_servico.clicked.connect(self.DELETAR_SERVICO)
        self.add_btn.clicked.connect(self.ADICIONAR)
        self.add_btn_servico.clicked.connect(self.ADICIONAR_SERVICO)
        self.next_btn.clicked.connect(self.PROXIMO)
        self.next_btn_servico.clicked.connect(self.PROXIMO_servico)
        self.previous_btn.clicked.connect(self.ANTERIOR)
        self.previous_btn_servico.clicked.connect(self.ANTERIOR_SERVICO)
        self.first_btn.clicked.connect(self.PRIMEIRO)
        self.first_btn_servico.clicked.connect(self.PRIMEIRO_SERVICO)
        self.last_btn.clicked.connect(self.ULTIMO)
        self.last_btn_servico.clicked.connect(self.ULTIMO_SERVICO)
        self.fechar.clicked.connect(self.Fechar)

    # Se conecta com o SQL lite database e adiciona as informações da batabase na interface de inventário.
    def GET_DATA(self):
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand = '''SELECT * from peças_carro'''
        result = cursor.execute(comand)
        self.tabela.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabela.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabela.setItem(row_number, column_number,
                                    QTableWidgetItem(str(data)))
    

        # Mostra quantas peças diferentes tem no sistema e quantas referências únicad tem na database
        cursor2 = db.cursor()
        cursor3 = db.cursor()
        pecas_diferentes = '''SELECT COUNT(DISTINCT Peça) from peças_carro'''
        ref = '''SELECT COUNT (DISTINCT Referência) from peças_carro '''

        result_pecas_diferentes = cursor2.execute(pecas_diferentes)
        result_ref = cursor3.execute(ref)

        self.lbl_ref.setText(str(result_ref.fetchone()[0]))
        self.lbl_peca.setText(str(result_pecas_diferentes.fetchone()[0]))

        # Mostra a peça mais cara e a mais barata com suas respectivas referências

        cursor4 = db.cursor()
        cursor5 = db.cursor()

        min_valor = '''SELECT MIN(Preço), Referência from peças_carro'''
        max_valor = '''SELECT MAX(Preço), Referência from peças_carro'''

        result_min_valor = cursor4.execute(min_valor)
        result_max_valor = cursor5.execute(max_valor)

        r1 = result_min_valor.fetchone()
        r2 = result_max_valor.fetchone()

        self.lbl_menor.setText(str(r1[0]))
        self.lbl_maior.setText(str(r2[0]))
        self.lbl_ref_menor.setText(str(r1[1]))
        self.lbl_ref_maior.setText(str(r2[1]))

    # Se conecta com o SQL lite database e adiciona as informações da batabase na interface de inventário.
    def GET_DATA2(self):
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        comand = '''SELECT * from servicos'''
        result = cursor.execute(comand)
        self.tabela_2.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabela_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabela_2.setItem(row_number, column_number,
                                    QTableWidgetItem(str(data)))

    def PROCURAR(self):  # Mostra na interface o filtro de bsuca
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        filtro = int(self.numero_botao.text())
        comand = '''SELECT * from peças_carro WHERE Quantidade<=?'''
        result = cursor.execute(comand, [filtro])
        self.tabela.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabela.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabela.setItem(row_number, column_number,
                                    QTableWidgetItem(str(data)))

    # Verifica os 3 itens em menor quantidade em estoque

    def VERIFICAR(self):
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand2 = '''SELECT Referência, Peça, Quantidade from peças_carro order by Quantidade asc LIMIT 3'''
        result = cursor.execute(comand2)
        self.tabela2.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tabela2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabela2.setItem(row_number, column_number,
                                     QTableWidgetItem(str(data)))

    def NAVEGAR(self):  # Essa função alimenta a interface na aba editar inventário
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand = '''SELECT * from peças_carro'''
        result = cursor.execute(comand)
        val = result.fetchone()
        self.id.setText(str(val[0]))
        self.ref.setText(str(val[1]))
        self.peca.setText(str(val[2]))
        self.quantidade.setValue(val[3])
        self.preco.setText(str(val[4]))
        self.marca.setText(str(val[5]))
    
    def NAVEGAR_SERVICO(self):  # Essa função alimenta a interface na aba editar serviço
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        comand = '''SELECT * from servicos'''
        result = cursor.execute(comand)
        val = result.fetchone()
        self.id_servico.setText(str(val[0]))
        self.nome_servico.setText(str(val[1]))
        self.ref_servico.setText(str(val[2]))
        self.precoServico.setText(str(val[3]))

    def UPDATE(self):  # Atualiza o banco de dados de peças
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        id_ = int(self.id.text())
        ref_ = self.ref.text()
        peca_ = self.peca.text()
        quantidade_ = str(self.quantidade.value())
        preco_ = self.preco.text()
        marca_ = self.marca.text()

        row = (ref_, peca_, quantidade_, preco_, marca_, id_)

        comand = '''UPDATE peças_carro SET Referência=?, Peça=?, Quantidade=?,Preço=?,Marca=? WHERE ID=? '''
        cursor.execute(comand, row)
        db.commit()
    
    def UPDATE_SERVICO(self):  # Atualiza o banco de dados de serviços
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        id_ = int(self.id_servico.text())
        ref_ = self.ref_servico.text()
        servico_ = self.nome_servico.text()
        preco_ = self.precoServico.text()
        row = (ref_,preco_,servico_, id_)

        comand = '''UPDATE servicos SET REF=?,PRECO=?,Servico=? WHERE ID=? '''
        cursor.execute(comand, row)
        db.commit()

    def DELETAR(self):  # Deleta do banco de dados
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        d = self.id.text()
        comand = '''DELETE from peças_carro WHERE ID=?'''
        cursor.execute(comand, d)
        db.commit()

    def DELETAR_SERVICO(self):  # Deleta do banco de dados
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        d = self.id_servico.text()
        comand = '''DELETE from servicos WHERE ID=?'''
        cursor.execute(comand, d)
        db.commit()

    def ADICIONAR(self):  # Adiciona no banco de dados de peças
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        ref_ = self.ref.text()
        peca_ = self.peca.text()
        quantidade_ = str(self.quantidade.value())
        preco_ = self.preco.text()
        marca_ = self.marca.text()

        row = (ref_, peca_, quantidade_, preco_, marca_)

        comand = '''INSERT INTO peças_carro (Referência, Peça, Quantidade,Preço,Marca) VALUES(?,?,?,?,?) '''
        cursor.execute(comand, row)
        db.commit()
    
    def ADICIONAR_SERVICO(self):  # Adiciona no banco de dados de serviços
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        ref_ = self.ref_servico.text()
        servico_ = self.nome_servico.text()
        preco_ = self.precoServico.text()
        row = (ref_, servico_, preco_)

        comand = '''INSERT INTO servicos (REF,Servico,PRECO) VALUES(?,?,?) '''
        cursor.execute(comand, row)
        db.commit()

    def PROXIMO(self):  # Move a exibição na interface de editar peças
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        id_atual = int(self.id.text())
        
        # Incrementa o id_atual até encontrar um ID válido
        while True:
            id_atual += 1
            comand = '''SELECT * from peças_carro WHERE ID=?'''
            result = cursor.execute(comand, (id_atual,))
            val = result.fetchone()
            if val is not None:
                self.id.setText(str(val[0]))
                self.ref.setText(str(val[1]))
                self.peca.setText(str(val[2]))
                self.quantidade.setValue(val[3])
                self.preco.setText(str(val[4]))
                self.marca.setText(str(val[5]))
                break
            else:
                # Se não encontrar um ID válido, verifica se é o último ID
                cursor.execute('''SELECT MAX(ID) from peças_carro''')
                max_id = cursor.fetchone()[0]
                if id_atual >= max_id:
                    print("Você está visualizando o último ID")
                    break
    
    def PROXIMO_servico(self):  # Move a exibição na interface de editar peças
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        id_atual = int(self.id_servico.text())
        # Incrementa o id_atual até encontrar um ID válido
        while True:
            id_atual += 1
            comand = '''SELECT * from servicos WHERE ID=?'''
            result = cursor.execute(comand, (id_atual,))
            val = result.fetchone()
            if val is not None:
                self.id_servico.setText(str(val[0]))
                self.nome_servico.setText(str(val[1]))
                self.ref_servico.setText(str(val[2]))
                self.precoServico.setText(str(val[3]))
                break
            else:
                # Se não encontrar um ID válido, verifica se é o último ID
                cursor.execute('''SELECT MAX(ID) from servicos''')
                max_id = cursor.fetchone()[0]
                if id_atual >= max_id:
                    print("Você está visualizando o último ID")
                    break

    def ANTERIOR(self):  # Move a exibição na interface de editar peças
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        id_atual = int(self.id.text())
        # Incrementa o id_atual até encontrar um ID válido
        while True:
            id_atual -= 1
            comand = '''SELECT * from peças_carro WHERE ID=?'''
            result = cursor.execute(comand, (id_atual,))
            val = result.fetchone()
            if val is not None:
                self.id.setText(str(val[0]))
                self.ref.setText(str(val[1]))
                self.peca.setText(str(val[2]))
                self.quantidade.setValue(val[3])
                self.preco.setText(str(val[4]))
                self.marca.setText(str(val[5]))
                break
            else:
                # Se não encontrar um ID válido, verifica se é o último ID
                cursor.execute('''SELECT MIN(ID) from peças_carro''')
                min_id = cursor.fetchone()[0]
                if id_atual <= min_id:
                    print("Você está visualizando o primeiro ID")
                    break
    
    def ANTERIOR_SERVICO(self):  # Move a exibição na interface de editar serviços
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        id_atual = int(self.id_servico.text())
        while True:
            id_atual -= 1
            comand = '''SELECT * from servicos WHERE ID=?'''
            result = cursor.execute(comand, (id_atual,))
            val = result.fetchone()
            if val is not None:
                self.id_servico.setText(str(val[0]))
                self.nome_servico.setText(str(val[1]))
                self.ref_servico.setText(str(val[2]))
                self.precoServico.setText(str(val[3]))
                break
            else:
                # Se não encontrar um ID válido, verifica se é o último ID
                cursor.execute('''SELECT MIN(ID) from servicos''')
                min_id = cursor.fetchone()[0]
                if id_atual <= min_id:
                    print("Você está visualizando o primeiro ID")
                    break

    def PRIMEIRO(self): #Move para o primeiro ID na tabela de editar peças
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand = '''SELECT * FROM peças_carro ORDER BY ID ASC LIMIT 1 '''
        result=cursor.execute(comand)
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.ref.setText(str(val[1]))
        self.peca.setText(str(val[2]))
        self.quantidade.setValue(val[3])
        self.preco.setText(str(val[4]))
        self.marca.setText(str(val[5]))

    def PRIMEIRO_SERVICO(self): #Move para o primeiro ID na tabela de editar serviços
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        comand = '''SELECT * FROM servicos ORDER BY ID ASC LIMIT 1 '''
        result=cursor.execute(comand)
        val=result.fetchone()
        self.id_servico.setText(str(val[0]))
        self.nome_servico.setText(str(val[1]))
        self.ref_servico.setText(str(val[2]))
        self.precoServico.setText(str(val[3]))


    def ULTIMO(self): #Move para o último ID na tabela de editar peças
        db = sqlite3.connect(resource_path("peças.db"))
        cursor = db.cursor()
        comand = '''SELECT * FROM peças_carro ORDER BY ID DESC LIMIT 1 '''
        result=cursor.execute(comand)
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.ref.setText(str(val[1]))
        self.peca.setText(str(val[2]))
        self.quantidade.setValue(val[3])
        self.preco.setText(str(val[4]))
        self.marca.setText(str(val[5]))
    
    def ULTIMO_SERVICO(self): #Move para o último ID na tabela de editar serviços
        db = sqlite3.connect(resource_path("servicos.db"))
        cursor = db.cursor()
        comand = '''SELECT * FROM servicos ORDER BY ID DESC LIMIT 1 '''
        result=cursor.execute(comand)
        val=result.fetchone()
        self.id_servico.setText(str(val[0]))
        self.nome_servico.setText(str(val[1]))
        self.ref_servico.setText(str(val[2]))
        self.precoServico.setText(str(val[3]))
    
    def Fechar(self):
        dbPeca=sqlite3.connect(resource_path("peças.db"))
        dbServico=sqlite3.connect(resource_path("servicos.db"))
        cursoServico=dbServico.cursor()
        cursoPeca=dbPeca.cursor()
        nome=self.nome_cliente.text()
        telefone=self.telefone_cliente.text()
        materiais=self.input_materiais.text()
        servico=self.servico.text()
        obs=self.btn_obs.text()
        soma_pecas=0
        soma_servicos=0
        total=0
        lista_servicos=[]
        lista_pecas=[]

        if not nome or not telefone or not materiais or not servico:
            print("Erro: Todos os campos devem ser preenchidos.")
            return

        materiais_processados=materiais.split(";")
        try:
            for material in materiais_processados:
                quantidade,ref=material.split(",")
                quantidade=int(quantidade.strip())
                ref=ref.strip()
                comand_Update='''UPDATE peças_carro SET Quantidade = Quantidade - ? WHERE Referência =?'''
                comand_Select='''SELECT Preço FROM peças_carro WHERE Referência=?'''
                comand_Select_materiais='''SELECT Peça FROM peças_carro WHERE Referência=?'''
                cursoPeca.execute(comand_Update,(quantidade, ref))
                cursoPeca.execute(comand_Select,(ref,))
                preco_peca=cursoPeca.fetchone()[0]
                cursoPeca.execute(comand_Select_materiais,(ref,))
                nome_peca=cursoPeca.fetchone()[0]
                lista_pecas.append(nome_peca)
                soma_pecas+=preco_peca*quantidade
                dbPeca.commit()
        except ValueError:
            print(f"Erro: Formato inválido para material '{material}'. Use 'quantidade,ref'.")
            return
        
        try:
            servico_processados=servico.split(";")
            for s in servico_processados:
                ref_servico=s.strip()
                comand_Select_Preco='''SELECT PRECO FROM servicos WHERE REF=?'''
                comand_Select_Servico='''SELECT Servico FROM servicos WHERE REF=?'''
                cursoServico.execute(comand_Select_Preco,(ref_servico,))
                preco_servico=cursoServico.fetchone()[0]
                cursoServico.execute(comand_Select_Servico,(ref_servico,))
                nome_servico=cursoServico.fetchone()[0]
                lista_servicos.append(nome_servico)
                soma_servicos+=preco_servico
        except ValueError:
            print(f"Erro: Referência de serviço inválida.")
            return
        total=soma_servicos+soma_pecas

        with open(f"{nome}.txt", "w") as file:
            file.write("                   STOCK CAR LTDA\n")
            file.write("CNPJ: 47.546.538/0001-60\n")
            file.write("Rua das Flores, 123, Bairro Centro, Juazeiro do Norte, CE\n")
            file.write("CEP: 63000-000\n")
            file.write("-------------------------------------------------------------\n")
            file.write(f"Nome: {nome}\n")
            file.write(f"Telefone: {telefone}\n")
            file.write("-------------------------------------------------------------\n")
            file.write("Serviços feitos:\n")
            for servico in lista_servicos:
                file.write(f"  - {servico}\n")
            file.write("-------------------------------------------------------------\n")
            file.write("Produtos usados:\n")
            for peca, quant in zip(lista_pecas, lista_quantidade):
                file.write(f"  - {peca}: {quant}\n")
            file.write("-------------------------------------------------------------\n")
            
            file.write(f"Total a pagar (R$): {total:.2f}\n")
            file.write("-------------------------------------------------------------\n")
            file.write("Observação:\n")
            file.write(obs + "\n")
            file.write("-------------------------------------------------------------\n")
        


        
        





def main():  # Esta função instância a classe Main e roda o app ela num loop.
    app = QApplication(sys.argv) #QApplication é a classe que gerencia a aplicação GUI. Ela precisa ser instanciada antes de qualquer widget Qt ser criado.
    window = Main() #cria a tela e carrega todos os elementos visuais.
    window.show() #deixa a tela visível.
    app.exec() #Entra no loop de eventos principal da aplicação, que é necessário para que a aplicação responda a eventos do usuário.


if __name__ == "__main__":  # garante que o script só rode no arquivo princiapl.
    main()
