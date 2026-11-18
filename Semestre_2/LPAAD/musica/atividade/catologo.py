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
        if self.verifiquando_duplicata(musica):
            print(f"A música '{musica.nome}' já está no catálogo. Não será adicionada novamente.")
            return False
        self.musicas.append(musica)
        self.reproduzidas[musica.nome] = 0
        self.musica_atual = musica 
        self.adicionar_favorito(musica)
        return True

    def adicionar_favorito(self, musica):
        if musica.favorito:
            self.favoritos.append(musica)

    def verifiquando_duplicata(self, musica):
        for m in self.musicas:
            if m.nome == musica.nome and m.cantor == musica.cantor and m.genero == musica.genero and m.duracao == musica.duracao and m.ano == musica.ano:
                return True
        return False