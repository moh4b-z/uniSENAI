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
#normalizar_builds_malenia()

def normalizar_phantoms():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    arquivo_malenia = os.path.join(diretorio_atual, 'malenia_normalizado.csv')
    arquivo_phantoms = os.path.join(diretorio_atual, 'phantoms.csv')

    try:
        with open(arquivo_malenia, mode='r', encoding='utf-8') as f_in:
            leitor = csv.DictReader(f_in)
            campos = leitor.fieldnames
            
            # Novos campos para a tabela principal: remover colunas de phantom e adicionar id_phantom
            campos_main = [c for c in campos if c not in ['Phantom_Count', 'Phantom_Build', 'Phantom_Death']]
            campos_main.append('id_phantom')
            
            phantom_data = []
            main_data = []
            
            for linha in leitor:
                id_reg = linha['id_registro']
                phantom_count = linha.get('Phantom_Count', '').strip()
                
                if phantom_count:
                    phantom_data.append({
                        'id_phantom': id_reg,
                        'Phantom_Count': linha['Phantom_Count'],
                        'Phantom_Build': linha['Phantom_Build'],
                        'Phantom_Death': linha['Phantom_Death']
                    })
                    linha['id_phantom'] = id_reg
                else:
                    linha['id_phantom'] = ''
                
                # Remover as colunas de phantom da linha
                for c in ['Phantom_Count', 'Phantom_Build', 'Phantom_Death']:
                    linha.pop(c, None)
                
                main_data.append(linha)
        
        # Criar tabela de phantoms
        with open(arquivo_phantoms, mode='w', encoding='utf-8', newline='') as f:
            escritor = csv.DictWriter(f, fieldnames=['id_phantom', 'Phantom_Count', 'Phantom_Build', 'Phantom_Death'])
            escritor.writeheader()
            escritor.writerows(phantom_data)
        
        # Reescrever malenia_normalizado.csv
        with open(arquivo_malenia, mode='w', encoding='utf-8', newline='') as f:
            escritor = csv.DictWriter(f, fieldnames=campos_main)
            escritor.writeheader()
            escritor.writerows(main_data)
        
        print("\n✅ NORMALIZAÇÃO DE PHANTOMS CONCLUÍDA!")
        print(f"1. Criada: 'phantoms.csv' (Tabela de fantasmas)")
        print(f"2. Atualizada: 'malenia_normalizado.csv' (Removidas colunas de phantom, adicionado id_phantom)")
        
    except Exception as e:
        print(f"Erro ao processar phantoms: {e}")

# Rodar a nova função
normalizar_phantoms()


