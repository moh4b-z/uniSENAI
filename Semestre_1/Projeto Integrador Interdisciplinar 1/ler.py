import os
import pandas as pd

def mapear_estrutura_csv(caminho_da_pasta, arquivo_saida="relatorio_colunas.txt"):
    # Verifica se a pasta existe
    if not os.path.exists(caminho_da_pasta):
        print(f"Erro: A pasta '{caminho_da_pasta}' não foi encontrada.")
        return

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE ESTRUTURA DE TABELAS (CSV)\n")
        f.write("=" * 60 + "\n\n")

        # Percorre todos os arquivos da pasta
        arquivos = [a for a in os.listdir(caminho_da_pasta) if a.endswith('.csv')]
        
        if not arquivos:
            f.write("Nenhum arquivo .csv encontrado na pasta informada.\n")
        
        for arquivo in arquivos:
            caminho_completo = os.path.join(caminho_da_pasta, arquivo)
            
            try:
                # Lemos as primeiras 10 linhas para que o pandas possa inferir os tipos corretamente
                df = pd.read_csv(caminho_completo, nrows=10)
                
                f.write(f"TABELA: {arquivo}\n")
                f.write("-" * 40 + "\n")
                
                # df.dtypes retorna uma série com Nome da Coluna e o Tipo de Dado
                for coluna, tipo in df.dtypes.items():
                    f.write(f"  - {coluna:<25} | Tipo: {tipo}\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
                print(f"Processado: {arquivo}")

            except Exception as e:
                f.write(f"ERRO AO PROCESSAR {arquivo}: {e}\n\n")

    print(f"\nConcluído! O relatório foi salvo em: {arquivo_saida}")

# CONFIGURAÇÃO:
# 1. Coloque o caminho da sua pasta aqui
# 2. Execute o script
caminho_pasta = "./Banco_de_Dados_PII3_AWS" 
mapear_estrutura_csv(caminho_pasta)