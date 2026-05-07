import csv
import os

def normalizar_builds_malenia():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    arquivo_entrada = os.path.join(diretorio_atual, 'malenia.csv')
    arquivo_builds_ref = os.path.join(diretorio_atual, 'tabela_builds_referencia.csv')
    arquivo_malenia_final = os.path.join(diretorio_atual, 'malenia_normalizado.csv')

    # 1. Definição da Tabela de Referência (O "Dicionário" de builds)
    builds_data = [
        {"id_build": 1, "nome": "RAW_MELEE", "descricao": "A build based on dealing normal damage with a melee weapon..."},
        {"id_build": 2, "nome": "RAW_CAST", "descricao": "Casters build to deal damage based on their casting type..."},
        {"id_build": 3, "nome": "PROC_MELEE", "descricao": "Melee fighters built specifically to cause a status effect..."},
        {"id_build": 4, "nome": "PROC_CAST", "descricao": "Casters built specifically to cause a status effect..."},
        {"id_build": 5, "nome": "HYBRID", "descricao": "A mix of the above with no clear activity pointing..."}
    ]

    # Criar um mapa para busca rápida: {"RAW_MELEE": 1, ...}
    mapa_builds = {b["nome"]: b["id_build"] for b in builds_data}

    # 2. Criar o arquivo de referência (Tabela de Builds)
    with open(arquivo_builds_ref, mode='w', encoding='utf-8', newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=["id_build", "nome", "descricao"])
        escritor.writeheader()
        escritor.writerows(builds_data)

    # 3. Ler o malenia.csv e gerar a nova versão com IDs
    try:
        with open(arquivo_entrada, mode='r', encoding='utf-8-sig') as f_in:
            leitor = csv.DictReader(f_in)
            campos_originais = leitor.fieldnames
            
            # Criamos a nova lista de colunas: id_registro + originais (com builds alteradas)
            # Vamos manter os nomes Host_Build e Phantom_Build, mas agora eles guardam números
            campos_saida = ['id_registro'] + campos_originais

            with open(arquivo_malenia_final, mode='w', encoding='utf-8', newline='') as f_out:
                escritor_final = csv.DictWriter(f_out, fieldnames=campos_saida)
                escritor_final.writeheader()

                id_registro = 1
                for linha in leitor:
                    # Substitui o nome da build pelo ID numérico
                    nome_host = linha['Host_Build'].strip()
                    nome_phantom = linha['Phantom_Build'].strip()

                    # Se a build não for encontrada ou estiver vazia, deixamos vazio ou 0
                    linha['Host_Build'] = mapa_builds.get(nome_host, "")
                    linha['Phantom_Build'] = mapa_builds.get(nome_phantom, "")
                    
                    # Adiciona o ID da linha (PK)
                    nova_linha = {'id_registro': id_registro}
                    nova_linha.update(linha)
                    
                    escritor_final.writerow(nova_linha)
                    id_registro += 1

        print("\n✅ NORMALIZAÇÃO CONCLUÍDA!")
        print(f"1. Criada: 'tabela_builds_referencia.csv' (Contém os nomes e as descrições)")
        print(f"2. Criada: 'malenia_normalizado.csv' (As colunas de build agora contêm apenas IDs de 1 a 5)")
        
    except Exception as e:
        print(f"Erro ao processar: {e}")

# Rodar a função
normalizar_builds_malenia()