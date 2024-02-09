from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDTextButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import (MDList, ThreeLineListItem, 
                             ThreeLineAvatarIconListItem, TwoLineAvatarIconListItem, IconLeftWidget,
                             IconRightWidget, OneLineAvatarIconListItem, OneLineListItem
                             )
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout 
from kivymd.uix.label import MDIcon
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.widget import *
from kivy.uix.widget import Widget

import json
from datetime import datetime
import os

# Importando Classe externa:
from listaitens import ListaItens


# Telas do app:
class HomePage(MDScreen):
    pass

class AddaComprar(MDScreen):
    pass

class AjustesPage(MDScreen):
    pass

class ResumoCompra(MDScreen):
    pass

class AdicionarItens(MDScreen):
    pass
   
class ListaPrincipal(MDScreen):
    pass

class ListasSalvas(MDScreen):
    pass

class ItensSalvos(MDScreen):
    pass

class ComprasSalvas(MDScreen):
    pass

class ItensSalvosCompras(MDScreen):
    pass

class FinalizarCompra(MDScreen):
    pass

class FinalizarLista(MDScreen):
    pass

class AddDaListaParaCompra(MDScreen):
    pass

class Example(MDApp):
    # Diálogo para adicionar o valor e confirmar a quantidade real:
    dialog = None
    # Diálogo para sair da lista salva e ir para o carrinho:
    dialogo = None
    # Diálogo para cancelar o uso da lista que redirecionará para compra:
    dialoga = None


    def build(self):
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.theme_style = "Light"

        '''['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 
        'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 
        'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray'''

        self.lista_itens = ListaItens()
        return Builder.load_file("main.kv")


    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela
    

    def on_release_callback(self):
        self.mudar_tela("adicionaritens")


    def add_item(self):
        # Nome do item(produto):
        nome = self.root.ids.adicionaritens.ids.nome_input.text

        # Preço do item(produto):
        ## Para transformar o preço:
        preco_texto_sem_formatar = self.root.ids.adicionaritens.ids.preco_input.text
        
        if preco_texto_sem_formatar == preco_texto_sem_formatar.replace(".", ".").replace(",", "."):
            preco_texto = self.root.ids.adicionaritens.ids.preco_input.text
        else:
            preco_texto = self.root.ids.adicionaritens.ids.preco_input.text.replace(",", ".")

        # Quantidade do item(produto):
        quantidade_texto = self.root.ids.adicionaritens.ids.quantidade_input.text

        # Processo de validação dos dados de entrada:
        ## Verificando entradas vazias:
        if nome == "" or preco_texto == "" or quantidade_texto == "":
            return  # Se entradas vazias, não faça nada
        
        ## Verificando se os valores são maiores ou iguas a zero:
        ### Para o preço:
        try:
            preco = float(preco_texto)
            if preco <= 0:
                return  # Se o preço for 0 ou negativa, não faça nada    
        except ValueError:
            return  # Se o preço não puder ser convertida para um número inteiro, não faça nada
        
        ### Para a quantidade:
        try:
            quantidade = int(quantidade_texto) 
            if quantidade <= 0:
                return  # Se a quantidade for 0 ou negativa, não faça nada 
        except ValueError:
            return  # Se a quantidade não puder ser convertida para um número inteiro, não faça nada

        # Calculando o total por item
        total_item = preco * quantidade

        # Definindo os valores na classe Item
        item = {"nome": f"{nome}", "preco": f"{preco:.2f}", "quantidade": f"{quantidade}", "total_item": f"{total_item}"}
        self.lista_itens.adicionar_item(item)

        self.tudo = self.lista_itens.obter_itens() 

        # Gerando widgets com os itens da lista:
        for item in reversed(self.tudo):
            #Definindo propriedades do MDListItem
            self.lista_nova = ThreeLineAvatarIconListItem(
                                                            # IconLeftWidget(
                                                            # #icon="plus", on_release = lambda x, i=item_index: self.adicionar_quantidade_item(i, 1)
                                                            #     ),
                                                            IconRightWidget(
                                                            icon="delete", on_release = lambda x, i=item: self.removendo_item(i)),
                                                            text=f"{item['nome']}", 
                                                            secondary_text= f"Preço: R$ {item['preco']}",
                                                            tertiary_text= f"Quantidade: {item['quantidade']}",
                                                            )
        # Adicionando o widget:                                                             
        self.root.ids.listaprincipal.ids.scroll.add_widget(self.lista_nova)

        # limpa as celulas:
        self.root.ids.adicionaritens.ids.nome_input.text = ""
        self.root.ids.adicionaritens.ids.preco_input.text = ""
        self.root.ids.adicionaritens.ids.quantidade_input.text = ""    
        
        # Atualizando o valor total, enquanto é adiconado o produto:
        self.atualizar_total()


    def atualizar_total(self):
        total = sum(float(item["total_item"]) for item in self.lista_itens.obter_itens())
        self.root.ids.adicionaritens.ids.total_parcial.text = f"Total: R$ {total:.2f}"
        self.root.ids.listaprincipal.ids.total_parcial.text = f"Total: \nR$ {total:.2f}"


    def removendo_item(self, item_apagado):
        self.lista_itens.remover_item(item_apagado)
        self.atualizar_lista()
        self.atualizar_total()


    def compra_nao_salva(self):
        # Limpando a lista para a próxima que for criada:
        self.lista_itens.limpar_itens()

        # limpa as celulas:
        self.root.ids.adicionaritens.ids.nome_input.text = ""
        self.root.ids.adicionaritens.ids.preco_input.text = ""
        self.root.ids.adicionaritens.ids.quantidade_input.text = ""

        # Indo para tela inicial: 
        self.mudar_tela("homepage")


    def resultado_finalizar_compra(self):
        self.mudar_tela("comprassalvas")


    def atualizar_lista(self):
        # LImpando a tela para a nova entrada de widgets:
        scroll = self.root.ids.listaprincipal.ids.scroll
        scroll.clear_widgets()

        # Gerando widgets com os itens da lista:
        for item in reversed(self.lista_itens.obter_itens()):
            lista_nova = ThreeLineAvatarIconListItem(
                # IconLeftWidget(
                #     #icon="plus", on_release = lambda x, i=item_index: self.adicionar_quantidade_item(i, 1)
                # ),
                IconRightWidget(
                    icon="delete", on_release=lambda x, i=item: self.removendo_item(i)
                    ),
                    text=f"{item['nome']}",
                    secondary_text=f"Preço: R$ {item['preco']}",
                    tertiary_text=f"Quantidade: {item['quantidade']}",
            )
            scroll.add_widget(lista_nova)
        self.mudar_tela("listaprincipal")
        

    def vizualizar_item(self):
        # Atualizando a lista, para a entrada de itens corretos:
        self.atualizar_lista()
        # Visualizando a lista:
        self.mudar_tela("listaprincipal")



# PARA ITENS A COMPRAR, lista que será feita antes do ato da compra:     
    def add_item_a_comprar(self):
        # Definindo a origem dos dados de entrada (nome e quantidade):
        nome = self.root.ids.addacomprar.ids.nome_input_a_comprar.text
        quantidade_texto = self.root.ids.addacomprar.ids.quantidade_input_a_comprar.text

        # Processo de validação dos dados de entrada:
        ## Verificando entradas vazias:
        if nome == "" or quantidade_texto =="":
            return
        
        ## Verificando se os valores são maiores ou iguas a zero:
        ### Para a quantidade:
        try:
            quantidade = int(quantidade_texto)
            if quantidade <= 0:
                return  # Se a quantidade for 0 ou negativa, não faça nada
        except ValueError:
            return  # Se a quantidade não puder ser convertida para um número inteiro, não faça nada

        # Definindo os valores na classe Item:
        item = {"nome": f"{nome}", "quantidade": f"{quantidade}"}
        
        # Adicionando os itens na lista:
        self.lista_itens.adicionar_item_a_comprar(item)

        # A lista com itens adicionados:
        self.tudo_a_comprar = self.lista_itens.obter_itens_a_comprar()

        # Gerando widgets com os itens da lista:
        for item in reversed(self.tudo_a_comprar):  
            self.lista_nova_a_comprar = TwoLineAvatarIconListItem(
                IconRightWidget(
                    icon="delete", on_release=lambda x, i=item: self.removendo_item_a_comprar(i)
                    ),
                    text=f"{item['nome']}",
                    secondary_text=f"Quantidade: {item['quantidade']}"
            )
        # Adicionando o widget:
        self.root.ids.resumocompra.ids.scroll_a_comprar.add_widget(self.lista_nova_a_comprar)

        # LImpando as células:
        self.root.ids.addacomprar.ids.nome_input_a_comprar.text = ""
        self.root.ids.addacomprar.ids.quantidade_input_a_comprar.text = ""


    def removendo_item_a_comprar(self, item_apagado):
        # Removendo item da lista feita antes do ato da compra:
        self.lista_itens.remover_item_a_comprar(item_apagado)
        # Atualizando a lista, agora sem o item:
        self.atualizar_lista_a_comprar()


    def atualizar_lista_a_comprar(self):
        # LImpando a tela para a nova entrada de widgets:
        scroll_a_comprar = self.root.ids.resumocompra.ids.scroll_a_comprar
        scroll_a_comprar.clear_widgets()

        # Gerando widgets com os itens da lista de COMPRAS já realizadas:
        for item in reversed(self.tudo_a_comprar):
            lista_nova_a_comprar = TwoLineAvatarIconListItem(
                IconRightWidget(
                    icon="delete", on_release=lambda x, i=item: self.removendo_item_a_comprar(i)
                    ),
                    text=f"{item['nome']}",
                    secondary_text=f"Quantidade: {item['quantidade']}",
            )

            # Adicionando o widget:
            scroll_a_comprar.add_widget(lista_nova_a_comprar)
        
        # Mudando para a tela com a lista de COMPRAS já realizadas:
        self.mudar_tela("resumocompra")


    def vizualizar_item_a_comprar(self):
        # Visualizando a lista:
        ## Atualizando:
        self.atualizar_lista_a_comprar()
        
        ## Mudando para a tela com a lista de COMPRAS já realizadas:
        self.mudar_tela("resumocompra")


    def lista_nao_salva(self):
        # Limpando Lista que não foi salva, para a compra:
        self.lista_itens.limpar_itens_a_comprar()
        # Redirecionando para a página inicial:
        self.mudar_tela("homepage")

#=====================================================================================
    def salvar_compra(self):
        # Se não houver nenhum item, retornar à página inicial:
        if not self.lista_itens.obter_itens():
            return self.mudar_tela("homepage")

        # Especificando a data da compra, com a biblioteca datetime, (dia/mês/ano e horas:minutos:segundos):
        data_hora_atual_sem_formatacao = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        hora_formatada = data_hora_atual_sem_formatacao[-8:].replace(":", "-")

        # Substituir a parte da hora na string original:
        data_hora_atual = data_hora_atual_sem_formatacao[:-8] + hora_formatada

        # Retornando a lista de itens COMPRA, que será salva:
        compra_a_salvar = self.lista_itens.obter_itens()

        # Constrói o nome do arquivo com a data e hora(nome_data_hora):
        nome_compra = f"compras/Compra_{data_hora_atual}.json"

        # Usando a biblioteca OS para salvar a lista COMPRA:
        ## Determinando o caminho e nome do arquivo:
        os.makedirs(os.path.dirname(nome_compra), exist_ok=True)
        ## Salvando a COMPRA, em formato .json:
        with open(nome_compra, 'w') as arquivo:
            json.dump(compra_a_salvar, arquivo)
        
        # Limpando a lista itens, que já foram salvos, liberando o espaço para salvar outras COMPRAS:
        self.lista_itens.limpar_itens()
        # Retornando para a página inicial:
        self.mudar_tela("homepage")
            

    def apagar_item_na_pasta_compra (self, item):
        # Localizando a pasta em que foi salva a compra:
        caminho_do_arquivo = f"compras/{item}"

        # Verificando a existência da COMPRA salva:
        if os.path.exists(caminho_do_arquivo):
            # Exclua o arquivo COMPRA:
            os.remove(caminho_do_arquivo)

        # Chamando a função para recarregar a página com as COMPRAS:
        self.compra_na_screen()


    def compra_na_screen(self):
        # Garantindo que a lista com nomes e compras esteja vazias antes de iniciar o função:
        self.lista_itens.limpar_compra()
        self.lista_itens.limpar_compra_nomes()
        
        # Localizando as COMPRAS Na pasta em que foi salva:
        caminho_pasta = "compras/"
        os.makedirs(os.path.dirname(caminho_pasta), exist_ok=True)

        # loop para encontrar todas as pastas:
        for nome_arquivo in os.listdir(caminho_pasta):
            caminho_pasta_completo = os.path.join(caminho_pasta, nome_arquivo)
            
            # adicionando a lista da COMPRA:
            self.lista_itens.adicionar_compra_nomes(nome_arquivo)
            
            # Carregando os itens COMPRA existentes na pasta:
            if os.path.isfile(caminho_pasta_completo):
                try:
                    with open(caminho_pasta_completo, 'r') as arquivo:
                        itens_carregados = json.load(arquivo)

                        # Adicionando a lista:
                        self.lista_itens.adicionar_compra(itens_carregados)
                        
                except FileNotFoundError:
                    pass  # Se o arquivo não existe, apenas continue com uma lista vazia

        # Retornando os nomes e compras salvas:
        todas_as_compras = self.lista_itens.obter_compra()
        todos_os_nomes = self.lista_itens.obter_compra_nomes()

        # Limpando os widgets da tela, antes de adicionar:
        scroll_compras = self.root.ids.comprassalvas.ids.scroll_compras
        scroll_compras.clear_widgets()

        # Para NOME e COMPRA, gerar nova lista com as compras salvas:
        for lista_compra, nome_compra in zip(reversed(todas_as_compras), reversed(todos_os_nomes)):
            
            # Convertendo data e hora que será exibida apenas em tela:
            hora = nome_compra.split("_")[-1]
            hora_tela = hora.replace("-", ":").split(".")[0]
            data = nome_compra.split("_")[1]  # Divide a string pelo "_" e pega a segunda parte
            data_formatada = data.replace("-", "/").replace("_", " ")

            # Calculando o total da compra:
            total_compra = sum(float(item["total_item"]) for item in lista_compra)

            lista_da_compra = ThreeLineAvatarIconListItem(
                IconLeftWidget(
                    icon="format-list-bulleted", on_release=lambda x, i=lista_compra: self.carregar_compras(i)
                    ),
                IconRightWidget(
                    icon="delete", on_release=lambda x, i=nome_compra: self.apagar_item_na_pasta_compra(i)
                    ),
                    text=f"Compra {data_formatada}",
                    secondary_text=f"Horário: {hora_tela}",
                    tertiary_text=f"Valor: R${total_compra:.2f}"
            )

            # Adicionando o widget:
            self.root.ids.comprassalvas.ids.scroll_compras.add_widget(lista_da_compra)
            
            # Redirecionando para tela de compras Salvas:
            self.mudar_tela("comprassalvas")
    

    def carregar_compras(self, compra):   
        # Limpando a tela, para carregar novos widgets:   
        scroll_compras_salvas = self.root.ids.itenssalvoscompras.ids.scroll_itens_compras
        scroll_compras_salvas.clear_widgets()

        # Inicializando com um total 0 das compras, para armazenar o TOTAL da compra, após o loop:
        total_compras = 0  

        # Carregando os itens da compra e valor por item:
        for item in compra:
            nome = item["nome"]
            preco = item["preco"]
            quantidade = item["quantidade"]
            total_item = item["total_item"]

            # Somando o valor de cada item e adicionando ao TOTAL:
            total_compras += float(total_item)
            # Gerando widget:
            compra_nova_salva = ThreeLineAvatarIconListItem(
                                                            text=nome, 
                                                            secondary_text= f"Preço: {preco}",
                                                            tertiary_text= f"Quantidade: {quantidade}",
                                                            )
            # Adicionando o widget:
            self.root.ids.itenssalvoscompras.ids.scroll_itens_compras.add_widget(compra_nova_salva)
        
        # Atualizando e redirecionando a lista de itens da COMPRA salva:   
        self.atualizar_total_compras_salvas(total_compras)
        self.mudar_tela("itenssalvoscompras")
        

    def atualizar_total_compras_salvas(self, total):
        # Total da compra adicionado a um card, na lista de itens salvos:
        self.root.ids.itenssalvoscompras.ids.total_parcial_compras.text = f"Total: \nR$ {total:.2f}"



# Salvando as LISTAS, para posteriormente comprar:
## Métodos adicionados para salvar e carregar a lista:
    def salvar_lista(self):
        # Verificando a extistencia de itens na lista:
        if not self.lista_itens.obter_itens_a_comprar():
            return self.mudar_tela("homepage")

        # Especificando a data da compra, com a biblioteca datetime, (dia/mês/ano e horas:minutos:segundos):
        data_hora_atual_sem_formatacao = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        hora_formatada = data_hora_atual_sem_formatacao[-8:].replace(":", "-")

        # Substituir a parte da hora na string original:
        self.data_hora_atual = data_hora_atual_sem_formatacao[:-8] + hora_formatada

        # Retornando a lista:
        lista_a_salvar = self.lista_itens.obter_itens_a_comprar()

        # Constrói o nome do arquivo com a data e hora:
        self.nome_lista = f"listas/Lista_{self.data_hora_atual}.json"

        # Salavando a LISTA:
        os.makedirs(os.path.dirname(self.nome_lista), exist_ok=True)
        with open(self.nome_lista, 'w') as arquivo:
            json.dump(lista_a_salvar, arquivo)
  
    
        # Limpando a LISTA para as proximas entradas e retornando a página inicial:    
        self.lista_itens.limpar_itens_a_comprar()
        self.mudar_tela("homepage")


    def apagar_item_na_pasta_lista (self, item):
        # Localizando o caminho das listas salavas na pasta:
        caminho_do_arquivo = f"listas/{item}"

        # Verificando a existência e removendo:
        if os.path.exists(caminho_do_arquivo):
            # Excluindo o arquivo:
            os.remove(caminho_do_arquivo)

        # Recarregando a lista, sem a lista apagada:
        self.lista_na_screen()


    def lista_na_screen(self):
        # Garantir que a lista esteja limpa antes de entrar com os dados:
        self.lista_itens.limpar_lista_nomes()

        # Determinando o caminho das listas:
        caminho_pasta = "listas/"
        os.makedirs(os.path.dirname(caminho_pasta), exist_ok=True)

        # Carregando as LISTAS salvas:
        for nome_arquivo in os.listdir(caminho_pasta):
            caminho_pasta_completo = os.path.join(caminho_pasta, nome_arquivo)
            
            # Carregando os nomes das LISTAS:
            self.lista_itens.adicionar_lista_nomes(nome_arquivo)

            # Carregando as LISTAS:
            if os.path.isfile(caminho_pasta_completo):
                try:
                    with open(caminho_pasta_completo, 'r') as arquivo:
                        itens_carregados = json.load(arquivo)

                        # Carregando cada LISTA:
                        self.lista_itens.adicionar_lista(itens_carregados)
                        
                except FileNotFoundError:
                    pass  # Se o arquivo não existe, apenas continue com uma lista vazia

        # Retornando Listas Salvas pela função OBTER:
        todas_listas = self.lista_itens.obter_lista()
        todos_os_nomes = self.lista_itens.obter_lista_nomes()

        # Limpando os widgets da tela:
        scroll_listas_salvos = self.root.ids.listassalvas.ids.scroll_listas
        scroll_listas_salvos.clear_widgets()

        # Gerando um loop para adicionar o nome e os itens contidos:   
        for lista, nome_lista in zip(reversed(todas_listas), reversed(todos_os_nomes)):
            
            # Convertendo data e hora que será exibida apenas em tela:
            hora = nome_lista.split("_")[-1]
            hora_tela = hora.replace("-", ":").split(".")[0]
            data = nome_lista.split("_")[1]  # Divide a string pelo "_" e pega a segunda parte
            data_formatada = data.replace("-", "/").replace("_", " ")
            
            
            # Criando a LISTA E EXIBINDO OS ITENS:
            lista_da_lista = OneLineAvatarIconListItem(
                IconLeftWidget(
                    icon="format-list-bulleted", on_release=lambda x, itens=lista: self.carregar_itens_lista_base(itens)
                    ),
                IconRightWidget(
                    icon="delete", on_release=lambda x, i=nome_lista: self.apagar_item_na_pasta_lista(i)
                    ),
                    text=f"Lista {data_formatada} {hora_tela}"
            )
            
            # Adicionando o Widget de listas na tela:
            self.root.ids.listassalvas.ids.scroll_listas.add_widget(lista_da_lista)  
            
        # Exibindo a tela:
        self.mudar_tela("listassalvas")


    def carregar_itens_lista_base(self,lista_base):
        # Loop para carregar os itens da lista:
        for item in lista_base:
            nome_pa = item["nome"]
            quantidade_pa = item["quantidade"]

            item_novo = {"nome": f"{nome_pa}", "quantidade": f"{quantidade_pa}"}

            # adicionando item em uma nova lista temporária, para que seja feita a compra:
            self.lista_itens.adicionar_item_pa(item_novo)
        
        # Chamando a função carregar itens para a compra:
        self.carregar_itens()


    def carregar_itens(self): 
        # Limpando os widgets da tela:     
        scroll_itens_salvos = self.root.ids.itenssalvos.ids.scroll_itens_salvos
        scroll_itens_salvos.clear_widgets()

        # Loop para carregar os itens da lista temporária:
        for item in self.lista_itens.obter_itens_pa():
            nome = item["nome"]
            quantidade = item["quantidade"]

            self.lista_nova_salva = ThreeLineAvatarIconListItem(
                IconRightWidget(
                    icon="plus", on_release=lambda x, i=item: self.dialogo_quantidade(i)
                    ),
                    text=nome,
                    secondary_text=f"Quantidade: {quantidade}",        
            )

            # Adicionando o widget:
            self.root.ids.itenssalvos.ids.scroll_itens_salvos.add_widget(self.lista_nova_salva)

        # Redirecionando para a lista de itens:
        self.mudar_tela("itenssalvos")   


    def dialogo_quantidade(self, item):
        # Determinando o item da lista:
        self.item_atual = item 
        
        # Especificando os itens:
        self.novo_nome = item["nome"]
        nova_quantidade = item["quantidade"]
    
        # Diálogo para adicionar o item na compra:
        if not self.dialog:
            self.dialog = MDDialog(
                content_cls = DialogContent(),
                type="custom",
                size_hint=(None, None),
                size=(dp(280), dp(180)),                
                background_color=(0.5, 0.5, 0.5, 1),  
                auto_dismiss=False,  # Define se o diálogo pode ser fechado clicando fora dele
                
                buttons=[
                    MDFlatButton(
                        text="CANCELAR",
                        theme_text_color="Custom",
                        text_color="black",
                        on_release=self.dismiss_dialog, 
                    ),
                    MDFlatButton(
                        text="ADICIONAR",
                        theme_text_color="Custom",
                        text_color="black",
                        on_release=self.process_text,
                    ),
                ],
            )

        # Adicionando o texto principal do diálogo:
        self.dialog.title = (
        f"[size=20]Nome: [color=#3366FF][b]{self.novo_nome.upper()}.[/b][/color][/size]\n"
        f"[size=20]Quantidade prevista: [color=#3366FF][b]{nova_quantidade}[/b][/color][/size]\n"
        f"[size=20]Adicionar produto ao carrinho?[/size]"
        )

        # Abrindo o diálogo de adiconar o item e confirmar a quantidade:
        self.dialog.open()


    def process_text(self, *args):
        # Obtendo o nome do item, fornecido pelo usuário:
        nome = self.novo_nome

        # Preço do item(produto), fornecido pelo usuário:
        ## Para transformar o preço:
        preco_texto_sem_formatar = self.dialog.content_cls.text_field1.text
        if preco_texto_sem_formatar == preco_texto_sem_formatar.replace(".", ".").replace(",", "."):
            preco_texto = self.dialog.content_cls.text_field1.text
        else:
            preco_texto = self.dialog.content_cls.text_field1.text.replace(",", ".")

        quantidade_texto = self.dialog.content_cls.text_field2.text  

        # Processo de validação dos dados de entrada:
        ## Verificando entradas vazias:
        if nome == "" or preco_texto == "" or quantidade_texto == "":
            return
        
        ## Verificando se os valores são maiores ou iguas a zero:
        ### Para o preço:
        try:
            preco = float(preco_texto)
            if preco <= 0:
                return  # Se a quantidade for 0 ou negativa, não faça nada      
        except ValueError:
            return  # Se a quantidade não puder ser convertida para um número inteiro, não faça nada  

        ### Para a quantidade:
        try:
            quantidade = int(quantidade_texto) 
            if quantidade <= 0:
                return  # Se a quantidade for 0 ou negativa, não faça nada  
        except ValueError:
            return  # Se a quantidade não puder ser convertida para um número inteiro, não faça nada  

        # Calculando o total para este item:
        total_item = preco * quantidade

        # Definindo os valores na classe Item:
        pa_item = {"nome": f"{nome}", "preco": f"{preco:.2f}", "quantidade": f"{quantidade}", "total_item": f"{total_item}"}
        
        # Adicionando a lista pricinpal, para a compra:
        self.lista_itens.adicionar_item(pa_item)

        # Retornando a lista:
        self.tudo = self.lista_itens.obter_itens()

        # Loop para retornar a lista no ato da compra:
        for item in self.tudo:
            self.lista_nova = ThreeLineAvatarIconListItem(
                                                            IconRightWidget(
                                                            icon="delete", on_release = lambda x, i=item: self.removendo_item(i)),
                                                            text=f"{item['nome']}", 
                                                            secondary_text= f"Preço: R$ {item['preco']}",
                                                            tertiary_text= f"Quantidade: {item['quantidade']}",
                                                            )
            
        # Adicionando widget:                                                          
        self.root.ids.listaprincipal.ids.scroll.add_widget(self.lista_nova)

        # Atualizando o valor total, enquanto é adiconado o produto:
        self.atualizar_total()
        
        # Remover o item e atualizar:
        self.lista_itens.remover_item_pa(self.item_atual)
        self.carregar_itens()

        # Limpando a celulas do diálogo:
        self.dialog.content_cls.text_field1.text = ""
        self.dialog.content_cls.text_field2.text = ""
        
        # Fechando o diálogo:
        self.dialog.dismiss()


    def dismiss_dialog(self, *args):
        # Limpando a celulas do diálogo:
        self.dialog.content_cls.text_field1.text = ""
        self.dialog.content_cls.text_field2.text = ""

        # Fechando o diálogo sem processar o texto:
        self.dialog.dismiss()


    def dialogo_ir_para_carrinho(self):
        # Verificando:
        if not self.dialogo:
            self.dialogo = MDDialog(
                type="custom",
                size_hint=(None, None),
                size=(dp(300), dp(150)), 
                background_color=(0.5, 0.5, 0.5, 1),
                auto_dismiss=False,  # Define se o diálogo pode ser fechado clicando fora dele

                buttons=[
                    MDFlatButton(
                        text="CANCELAR",
                        theme_text_color="Custom",
                        text_color="black",
                        on_release=self.dismiss_dialog_dois, 
                    ),
                    MDFlatButton(
                        text="CONFIRMAR",
                        theme_text_color="Custom",
                        text_color="black",
                        on_release=self.process_text_dois,
                    ),
                ],
            )

        # Adicionando o texto principal do diálogo:
        self.dialogo.title = (
        f"[size=21]Deseja ir para o [color=#3366FF][b]carrinho[/b][/color]?[/size]\n"
        f'[size=18]Caso confirme, a operação [color=#3366FF][b]NÃO[/b][/color] poderá ser desfeita. Porém, caso queira adicionar outro item, a mudança poderá ser feita pela campo de "adicionar itens".[/size]\n'
        )

        # Fechando o diálogo:
        self.dialogo.open()


    def dismiss_dialog_dois(self, *args):
        # Fechando o diálogo sem processar o texto:
        self.dialogo.dismiss()


    def process_text_dois(self, *args):
        # Limapndo a lista temorária, para não duplicar itens:
        self.lista_itens.limpar_itens_pa()
        
        # Carregando os itens da compra:
        self.vizualizar_item()
        
        # Fechando o diálogo:
        self.dialogo.dismiss()

    
    def dialogo_cancelar(self):
        # Saindo da lista e deixando de criar a lista no mercado:
        if not self.dialoga:
            self.dialoga = MDDialog(
                type="custom",
                size_hint=(None, None),
                size=(dp(300), dp(100)),  
                background_color=(0.5, 0.5, 0.5, 1),              
                auto_dismiss=False,  # Define se o diálogo pode ser fechado clicando fora dele
                
                buttons=[
                    MDFlatButton(
                        text="CANCELAR",
                        theme_text_color="Custom",
                        text_color="black",
                        on_release=self.dismiss_dialog_cancelar, 
                    ),
                    MDFlatButton(
                        text="CONFIRMAR",
                        theme_text_color="Custom",
                        text_color="black",
                        on_release=self.process_text_cancelar,
                    ),
                ],
            )

        # Adicionando o texto principal do diálogo:
        self.dialoga.title = (
        f"[size=20]Deseja cancelar [color=#3366FF][b]CANCELAR[/b][/color]?[/size]"
        )

        # Fechando o diálogo:
        self.dialoga.open()


    def dismiss_dialog_cancelar(self, *args):
        # Fechando o diálogo sem processar o texto:
        self.dialoga.dismiss()


    def process_text_cancelar(self, *args):
        # Limapndo a lista temorária, para não duplicar itens:
        self.lista_itens.limpar_itens_pa()
        
        # Limpando a lista de itens, para evitar duplicação:
        self.lista_itens.limpar_itens()
        
        # Fechando o diálogo:
        self.dialoga.dismiss()
        
        # Redirecioando para as listas salvas:
        self.mudar_tela("listassalvas")
    

# Classe de Entrada texto, do diálogo, para adicionar o valor e confirmar a quantidade real no ato da compra: 
class DialogContent(MDBoxLayout):
    # Configurando o texto:
    text_field1 = ObjectProperty(None)
    text_field2 = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Propriedades do MDBoxLayout, que será inserido no diálogo:
        self.orientation = "vertical"  
        self.size_hint= (None, None)  
        self.width = Window.width * 1  
        self.height = Window.height * 0.20
        
        # Criando dois widgets MDTextField:
        self.text_field1 = MDTextField(
                                        # Texto a ser digitado:
                                        hint_text="Digite o valor",
                                        text_color_normal= "black",
                                        text_color_focus="black",
                                        # Definindo as cores das linhas do cabeçalho
                                        line_color_normal= "green",
                                        line_color_focus= "FF8400",
                                        # Texto no cabeçalho
                                        hint_text_color_normal= "grey",
                                        hint_text_color_focus= "green",
                                        # Estilo do cabeçalho:
                                        mode= "rectangle",
                                        # Texto de ajuda do cabeçalho:
                                        helper_text= "Ex.: R$ 15,00",
                                        helper_text_color_normal= "green",
                                        helper_text_color_focus= "green",
                                        # Tamanho:
                                        size_hint= (0.65, 0.09),
                                       )
        
        self.text_field2 = MDTextField(
                                        hint_text="Digite a quantidade real",
                                        text_color_normal= "black",
                                        text_color_focus="black",
                                        # Definindo as cores das linhas do cabeçalho
                                        line_color_normal= "green",
                                        line_color_focus= "FF8400",
                                        # Texto no cabeçalho
                                        hint_text_color_normal= "grey",
                                        hint_text_color_focus= "green",
                                        # Estilo do cabeçalho:
                                        mode= "rectangle",
                                        # Texto de ajuda do cabeçalho:
                                        helper_text= "Ex.: 10 unidades",
                                        helper_text_color_normal= "green",
                                        helper_text_color_focus= "green",
                                        # Tamanho:
                                        size_hint= (0.65, 0.09),
                                        ) 

        # Adicionando os widgets ao layout:
        self.add_widget(self.text_field1)
        self.add_widget(Widget(size_hint_y=None, height=dp(18)))
        self.add_widget(self.text_field2)

Example().run()


