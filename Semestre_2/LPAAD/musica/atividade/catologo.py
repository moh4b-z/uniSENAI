from musica import Musica

class Catalogo:
    def __init__(self):
        self.musicas = []
        self.musica_atual = None
        self.favoritos = []
        self.reproduzidas = {}

    def adicionar_musica(self, musica):
        if not isinstance(musica, Musica):
            raise ValueError("O objeto adicionado deve ser uma instância da classe Musica.")
        if self.verificar_duplicidade(musica):
            print(f"A música '{musica.nome}' já está no catálogo. Não será adicionada novamente.")
            return False
        self.musicas.append(musica)
        self.reproduzidas[musica.nome] = 0
        self.musica_atual = musica 
        self.adicionar_favorito(musica)
        return True
    
    def remover_musica(self, musica):
        if musica not in self.musicas:
            return False
        if self.musica_atual is musica:
            self.musica_atual = None

        if self.favoritos is musica:
            self.favoritos.remove(musica)

        self.reproduzidas.pop(musica, None)
        self.musicas.remove(musica)
        return True

    def reproduzir(self, musica):
        if musica not in self.musicas:
            print(f"A música '{musica.nome}' não está no catálogo.")
            return False
        if self.musica_atual is musica:
            print(f"A música '{musica.nome}' já está sendo reproduzida.")
            return False
        self.musica_atual = musica
        self.reproduzidas[musica.nome] += 1
        print(f"Reproduzindo: {musica.nome} - {musica.cantor}")
        return True
    
    def pausar(self):
        if self.musica_atual is None:
            print(f"Nenhuma música está sendo reproduzida.")
            return False
        print(f"Pausando: {self.musica_atual.nome}")
        self.musica_atual = None
        return True
        

    def adicionar_favorito(self, musica):
        if musica not in self.musicas:
            print(f"A música '{musica.nome}' não está no catálogo. Não pode ser adicionada aos favoritos.")
            return False

        self.favoritos.append(musica)

    def remover_favorito(self, musica):
        if musica in self.favoritos:
            self.favoritos.remove(musica)
            musica.defavoritar()
            print(f"A música '{musica.nome}' foi removida dos favoritos.")
        else:
            print(f"A música '{musica.nome}' não está nos favoritos.") 

    @staticmethod
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

    def listar_musicas(self):
        for musica in self.musicas:
            print(musica)

    def filtra_por_nome(self, termo):
        termo = self._normalizar(termo)

        return [musica for musica in self.musicas 
                    if termo in self._normalizar(musica.nome)]

    def filtra_por_cantor(self, termo):
        termo = self._normalizar(termo)

        return [musica for musica in self.musicas 
                    if termo in self._normalizar(musica.cantor)]

    def filtra_por_genero(self, termo):
        termo = self._normalizar(termo)

        return [musica for musica in self.musicas 
                    if termo in self._normalizar(musica.genero)]
    
    def filtra_por_ano(self, ano):
        return [musica for musica in self.musicas if musica.ano == ano]

    def filtra_por_duracao(self, min, max):
        segundos_min = min * 60
        segundos_max = max * 60

        return [musica for musica in self.musicas 
                if segundos_min <= musica.duracao <= segundos_max]