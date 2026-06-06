import csv

caminho_csv = "dataset_produtos.csv"

# 1. CONFIGURAÇÃO DA TABELA HASH
TAMANHO_TABELA = 1230

# o array preenchido com sublistas vazias para tratar colisões (encadeamento separado)
tabela_hash = [None for _ in range(TAMANHO_TABELA)]


def funcao_hash(chave):
    hash_valor = 2166136261
    for caractere in str(chave):
        hash_valor ^= ord(caractere)
        hash_valor = (hash_valor * 16777619) & 0xFFFFFFFF
        
    return hash_valor % TAMANHO_TABELA


def gerar_chave_composta(id_produto, nome_produto, categoria, preco):
    """Cria uma chave única combinando ID, Nome, Categoria e Preço para evitar conflito de IDs iguais."""
    return f"{id_produto}_{nome_produto.lower().strip()}_{categoria.lower().strip()}_{preco}"


# 2. FUNÇÃO DE INSERÇÃO COM DEDUPLICAÇÃO
def inserir_com_deduplicacao_linear(tabela, chave, dados_produto):
    indice_original = funcao_hash(chave)
    tamanho = len(tabela)
    
    # Percorre a tabela a partir do índice original tentando encontrar uma vaga
    for i in range(tamanho):
        # O '% tamanho' garante que se chegar ao fim do array, ele volta para o começo (circular)
        indice_atual = (indice_original + i) % tamanho
        
        # CASO 1: A posição está vazia. Podemos inserir!
        if tabela[indice_atual] is None:
            tabela[indice_atual] = [chave, dados_produto]
            return True
            
        # CASO 2: Encontrou a mesma chave já cadastrada em algum lugar
        if tabela[indice_atual][0] == chave:
            # DEDUPLICAÇÃO: Verifica se os dados internos são 100% idênticos
            if tabela[indice_atual][1] == dados_produto:
                # Já existe exatamente o mesmo produto. Ignora (Deduplicou!)
                return False
            else:
                # Se a chave for igual mas os dados mudaram, atualiza o valor
                tabela[indice_atual][1] = dados_produto
                return True
                
    # Se o loop terminar e não retornar, significa que olhou todas as posições e o array está cheio
    print("Erro: A tabela hash está completamente cheia!")
    return False


# 3. FUNÇÃO DE BUSCA
def buscar_linear(tabela, id_produto, nome_produto):
    chave = gerar_chave_composta(id_produto, nome_produto)
    indice_original = funcao_hash(chave)
    tamanho = len(tabela)
    
    for i in range(tamanho):
        indice_atual = (indice_original + i) % tamanho
        
        # Se encontrar um espaço vazio (None), significa que o item nunca foi inserido
        if tabela[indice_atual] is None:
            return None
            
        # Se achar a chave correspondente, retorna o produto
        if tabela[indice_atual][0] == chave:
            return tabela[indice_atual][1]
            
    return None # Varreu a tabela inteira cheia e não achou


# 4. CARREGAR DATASET (.CSV) PARA A TABELA HASH
def carregar_dataset_csv(caminho_arquivo, tabela):
    print(f"Lendo o arquivo: {caminho_arquivo}...")
    contador_inseridos = 0
    contador_deduplicados = 0
    
    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        # Usamos o DictReader para ler as colunas pelo nome automaticamente
        leitor = csv.DictReader(arquivo)
        
        for linha in leitor:
            id_prod = linha['id_produto']
            nome_prod = linha['nome']
            categoria = linha['categoria']
            preco = linha['preco']
            # Criamos a chave composta
            chave = gerar_chave_composta(id_prod, nome_prod, categoria, preco)

            # Montamos o dicionário com o restante das informações convertidas
            dados_produto = {
                "id_produto": int(id_prod),
                "nome": nome_prod,
                "categoria": linha['categoria'],
                "preco": float(linha['preco'])
            }
            
            # Tenta inserir na tabela hash
            foi_inserido = inserir_com_deduplicacao_linear(tabela, chave, dados_produto)
            
            if foi_inserido:
                contador_inseridos += 1
            else:
                contador_deduplicados += 1
                
    print(f"Carga concluída! Itens únicos inseridos: {contador_inseridos} | Itens idênticos deduplicados: {contador_deduplicados}\n")


# Executando a carga do arquivo para a tabela hash
carregar_dataset_csv('dataset_produtos.csv', tabela_hash)

# 6. VISUALIZAÇÃO INTERNA DA TABELA HASH
print("\n--- ESTRUTURA INTERNA DA TABELA HASH (ARRAY DE ARRAYS) ---")
for i, posicao in enumerate(tabela_hash):
    print(f"Índice {i}: {posicao}")