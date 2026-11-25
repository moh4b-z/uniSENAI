class Musica:
    def __init__(self, nome, cantor, genero, duracao, ano): 
        #=========================================================================================#

        self._nome = self._validae_string(nome, "nome")
        self._cantor = self._validae_string(cantor, "cantor")
        self._genero = self._validae_string(genero, "genero")
        self._duracao = self._validae_int(duracao, "duração")
        self._ano = self._validae_int(ano, "ano")
        
        # Atributos de controle
        self.reproducoes = 0 # int, conta as reproduções iniciadas.
        self.tocando = False # bool, indica se a música está tocando.
        self.favorito = False
    #=========================================================================================#
    @staticmethod
    def _validae_string(valor, nome_atributo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"O atributo {nome_atributo} deve ser um texto não vazio.")
        return valor.strip()
    @staticmethod
    def _validae_int(valor, nome_atributo):
        if type(valor) is not int or valor <= 0:
            raise ValueError(f"O atributo {nome_atributo} deve ser um número inteiro positivo.")
        return valor
    # Propriedades de leitura (@property)
    @property
    def nome(self):
        return self._nome

    @property
    def cantor(self):
        return self._cantor

    @property
    def genero(self):
        return self._genero

    @property
    def duracao(self):
        return self._duracao
    
    @property
    def ano(self):
        return self._ano
    
    #=========================================================================================#
    # Representação textual do objeto (__str__)
    def __str__(self):
        minutos = self.duracao // 60
        segundos = self.duracao % 60
        return (f"{self._nome} - {self._cantor} ({self._genero}) - {minutos:02d}:{segundos:02d}")
    #=========================================================================================#
    
    #=========================================================================================#
    # Métodos de exibição de atributos   
    def mostrar_nome(self):
        print(f"Nome da música: {self._nome}.")    
        
    def mostrar_cantor(self):
        print(f"Cantor(a): {self._cantor}.")
        
    def mostrar_genero(self):
        print(f"Gênero musical: {self._genero}.")
    
    def mostrar_duracao(self):
        print(f"Duração: {self._duracao} segundos.")
    
    def mostrar_ano(self):
        print(f"Ano de lançamento: {self._ano}.")
        
    # Método para mostrar todas as informações
    def mostrar_detalhe(self):
        self.mostrar_nome()
        self.mostrar_cantor()
        self.mostrar_genero()
        self.mostrar_duracao()
        self.mostrar_ano()
        print(f"Favorito: {'Sim' if self.favorito else 'Não'}")
        print(f"Tocando: {'Sim' if self.tocando else 'Não'}")
        print(f"Reproduções: {self.reproducoes}")
    #=========================================================================================#    

    def reproduzir(self):

        # Verifica se a música NÃO está tocando.
        if self.tocando == False:
            self.tocando = True # modifica o atributo.
            self.reproducoes += 1 # incrementa o contador de reproduções.
            print(f"Reproduzindo a música: {self._nome}.")

        else:
            print(f"A música {self._nome} já está sendo reproduzida.") # Se já estiver tocando, não inicia outra reprodução.
    
    
    # Método que pausa a reprodução da música.        
    def pausar(self):
         # Verifica se a música está tocando.
        if self.tocando == True:
            self.tocando = False
            print(f"A reprodução da música {self._nome} foi pausada.")

        else:
            print("Nenhuma música está sendo reproduzida.") # Não altera o estado se a música já estiver parada.


    def favoritar(self):
        if self.favorito == False:
            self.favorito = True
            print(f"A música : {self._nome} foi adicionada aos favoritos!")
        else:
            print(f"A música : {self._nome} já está nos favoritos!")

    def defavoritar(self):
            if self.favorito == True:
                self.favorito = False
                print(f"A música : {self._nome} foi removida dos favoritos!")
            else:
                print(f"A música : {self._nome} não está nos favoritos!")

    #=========================================================================================#
    
    #=========================================================================================#
    # Métodos de Alterações
    
    def alterar_nome(self, novo_nome):
        self._nome = self._validae_string(novo_nome, "nome")
        print(f"Nome atualizado para: {self._nome}")

    def alterar_cantor(self, novo_cantor):
        self._cantor = self._validae_string(novo_cantor, "cantor")
        print(f"Cantor(a) atualizado(a) para: {self._cantor}")

    def alterar_genero(self, novo_genero):
        self._genero = self._validae_string(novo_genero, "gênero")
        print(f"Gênero atualizado para: {self._genero}")  

    def alterar_duracao(self, nova_duracao):
        self._duracao = self._validae_int(nova_duracao, "duração")
        print(f"Duração atualizada para: {self._duracao} segundos.")  

    def alterar_ano(self, novo_ano):
        self._ano = self._validae_int(novo_ano, "ano")
        print(f"Ano de lançamento atualizado para: {self._ano}") 
    #=========================================================================================#       

    def _normalizar(texto):
        return texto.strip().lower()

    def verificar_duplicidade(self, musica):
        if not  isinstance(musica, Musica):
            raise ValueError("O objeto adicionado deve ser uma instância da classe Musica.")

        for cadastrada in self.musicas:
            if(
                self._normalizar(cadastrada.nome) == self._normalizar(musica.nome) and
                self._normalizar(cadastrada.cantor) == self._normalizar(musica.cantor) and
                self._normalizar(cadastrada.genero) == self._normalizar(musica.genero) and
                (cadastrada.ano) == (musica.ano)
            ):
                return True
        return False