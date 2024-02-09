class ListaItens:
    def __init__(self):
        self.itens = []
        self.itens_salvos = []
        self.itens_a_comprar = []
        self.listas_salvas = []
        self.listas_salvas_nomes = []
        self.compras_salvas = []
        self.compras_salvas_nomes = []
        self.pega_pa_pra_mim = []


# Lista em tempo real:
    def adicionar_item(self, item):
        self.itens.append(item)

    def obter_itens(self):
        return self.itens
    
    def remover_item(self, item):
        if item in self.itens:
            self.itens.remove(item)

    def limpar_itens(self):
        self.itens.clear()


# Para Items a comprar:           
    def adicionar_item_a_comprar(self, item):
        self.itens_a_comprar.append(item)

    def obter_itens_a_comprar(self):
        return self.itens_a_comprar
    
    def remover_item_a_comprar(self, item):
        if item in self.itens_a_comprar:
            self.itens_a_comprar.remove(item)

    def limpar_itens_a_comprar(self):
        self.itens_a_comprar.clear()


# Para salvar as listas na pasta:      
    def adicionar_lista(self, lista):
        self.listas_salvas.append(lista)

    def obter_lista(self):
        return self.listas_salvas
    
    def remover_lista(self, lista):
        if lista in self.listas_salvas:
            self.listas_salvas.remove(lista)

    
# Para salvar as listas na pasta - nommes:        
    def adicionar_lista_nomes(self, nome):
        self.listas_salvas_nomes.append(nome)

    def obter_lista_nomes(self):
        return self.listas_salvas_nomes
    
    def remover_lista_nomes(self, nome):
        if nome in self.listas_salvas_nomes:
            self.listas_salvas_nomes.remove(nome)

    def limpar_lista_nomes(self):
        self.listas_salvas_nomes.clear()


# Lista contendo COMPRAS:
    def adicionar_compra(self, nome):
        self.compras_salvas.append(nome)

    def obter_compra(self):
        return self.compras_salvas
    
    def remover_compra(self, nome):
        if nome in self.compras_salvas:
            self.compras_salvas.remove(nome)

    def limpar_compra(self):
        self.compras_salvas.clear()


# Lista de nome das compras:
    def adicionar_compra_nomes(self, nome):
        self.compras_salvas_nomes.append(nome)

    def obter_compra_nomes(self):
        return self.compras_salvas_nomes
    
    def remover_compra_nomes(self, nome):
        if nome in self.compras_salvas_nomes:
            self.compras_salvas_nomes.remove(nome)

    def limpar_compra_nomes(self):
        self.compras_salvas_nomes.clear()
    

# Para buscar e usar Itens salvos na pasta listas:  
    def adicionar_item_salvos(self, item):
        self.itens_salvos.append(item)

    def obter_itens_salvos(self):
        return self.itens_salvos
    
    def remover_item_salvos(self, item):
        if item in self.itens_salvos:
            self.itens_salvos.remove(item)


# Lista resulatante da lista salva:
    def adicionar_item_pa(self, item):
        self.pega_pa_pra_mim.append(item)

    def obter_itens_pa(self):
        return self.pega_pa_pra_mim
    
    def remover_item_pa(self, item):
        if item in self.pega_pa_pra_mim:
            self.pega_pa_pra_mim.remove(item)

    def limpar_itens_pa(self):
        self.pega_pa_pra_mim.clear()

