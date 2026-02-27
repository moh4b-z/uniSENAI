import wbgapi as wb
import pandas as pd

def buscar_dados_economicos(nome_pais, ano_inicio, ano_fim):
    try:
        # 1. Identificar o código do país (ex: 'BRA')
        id_pais = wb.economy.coder(nome_pais)
        if not id_pais:
            return f"País '{nome_pais}' não encontrado."

        # 2. Mapeamento de indicadores
        # FP.CPI.TOTL.ZG = Inflação
        # PA.NUS.PPP = Fator PPC (Poder de Compra)
        mapa_indicadores = {
            'FP.CPI.TOTL.ZG': 'Inflacao_%', #variação percentual média anual
            'PA.NUS.PPP': 'PPC_Fator'
        }

        # 3. Buscar os dados
        # Usamos numericTime=True para garantir que os anos sejam números no cabeçalho
        df = wb.data.DataFrame(list(mapa_indicadores.keys()), id_pais, time=range(ano_inicio, ano_fim + 1))

        # 4. Renomear as linhas (índice) usando o nosso dicionário
        df.index = df.index.map(mapa_indicadores)

        # 5. Transpor o quadro para que os anos fiquem nas linhas (mais fácil de ler)
        df = df.T
        
        return df

    except Exception as e:
        return f"Erro ao buscar dados: {str(e)}"

# Chamada do código
print(f"--- Dados Econômicos ---")
resultado = buscar_dados_economicos("Brazil", 2015, 2023)
print(resultado)


def calcular_aumento_custo_vida(nome_pais, ano_inicio, ano_fim):
    try:
        # 1. Identificar o país
        id_pais = wb.economy.coder(nome_pais)
        if not id_pais:
            return f"País '{nome_pais}' não encontrado."

        # 2. Buscar inflação (FP.CPI.TOTL.ZG) para o período
        # Pegamos de ano_inicio até ano_fim
        df = wb.data.DataFrame('FP.CPI.TOTL.ZG', id_pais, time=range(ano_inicio, ano_fim + 1))
        
        # O Banco Mundial retorna a inflação em porcentagem (ex: 6.4 para 6.4%)
        # Precisamos converter para fator decimal (ex: 1.064)
        inflacoes = df.values.flatten()
        
        fator_acumulado = 1.0
        for taxa in inflacoes:
            if taxa == taxa: # Verifica se não é NaN (vazio)
                fator_acumulado *= (1 + (taxa / 100))
        
        # 3. Transformar o fator de volta para porcentagem de aumento total
        aumento_total_percentual = (fator_acumulado - 1) * 100
        
        print(f"--- Resultado para {nome_pais} ({ano_inicio} a {ano_fim}) ---")
        print(f"Aumento acumulado no custo de vida: {aumento_total_percentual:.2f}%")
        print(f"Isso significa que algo que custava R$ 100,00 em {ano_inicio}")
        print(f"passou a custar R$ {100 * fator_acumulado:.2f} em {ano_fim}.")
        
    except Exception as e:
        print(f"Erro ao calcular: {e}")

# Exemplo de uso:
calcular_aumento_custo_vida("Brazil", 2015, 2023)


def comparar_poder_compra(pais1, pais2, ano):
    try:
        paises = {wb.economy.coder(pais1): pais1, wb.economy.coder(pais2): pais2}
        codigos = list(paises.keys())
        
        # NY.GDP.PCAP.PP.CD = PIB per capita, PPC (Dólar Internacional)
        df = wb.data.DataFrame('NY.GDP.PCAP.PP.CD', codigos, time=ano)
        
        print(f"--- Comparação de Poder de Compra ({ano}) ---")
        for cod, nome in paises.items():
            valor = df.loc[cod].values[0]
            print(f"{nome}: Int$ {valor:,.2f}")
            
    except Exception as e:
        print(f"Erro: {e}")

# Comparando Brasil e Argentina em 2022
comparar_poder_compra("Brazil", "Argentina", 2022)


def converter_salario_para_ppc(nome_pais, salario_local, ano=2024):
    try:
        # 1. Obter o código do país
        id_pais = wb.economy.coder(nome_pais)
        
        # 2. Buscar o fator PPC para o ano desejado
        # O indicador PA.NUS.PPP retorna: Moeda Local por 1 Dólar Internacional
        fator_ppc = wb.data.fetch('PA.NUS.PPP', id_pais, time=ano)
        
        # Extrair o valor do gerador de dados
        valor_fator = list(fator_ppc)[0]['value']
        
        if valor_fator is None:
            return "Dados de PPC não disponíveis para este ano/país."

        # 3. Realizar a conversão
        salario_internacional = salario_local / valor_fator
        
        print(f"--- Conversão de Poder de Compra ({ano}) ---")
        print(f"País: {nome_pais}")
        print(f"Salário Local: {salario_local:,.2f}")
        print(f"Fator PPC: {valor_fator:.4f}")
        print(f"Salário em Dólares Internacionais: Int$ {salario_internacional:,.2f}")
        
    except Exception as e:
        print(f"Erro: {e}")

# Exemplo: Se você ganha R$ 5.000 no Brasil
converter_salario_para_ppc("Brazil", 5000, 2024)


# funções mais diretas pedidas pelo usuário ----------------------------------

def salario_internacional_simples(nome_pais, salario_local, ano=2024):
    """Retorna apenas o salário convertido para dólares internacionais (número).

    Parâmetros
    ----------
    nome_pais : str
        Nome do país reconhecido pelo wbgapi.
    salario_local : float
        Valor na moeda local.
    ano : int, opcional
        Ano para o fator PPC (default 2024).
    """
    # reutiliza parte da lógica de converter_salario_para_ppc sem impressão
    id_pais = wb.economy.coder(nome_pais)
    if not id_pais:
        raise ValueError(f"País '{nome_pais}' não encontrado.")

    fator_ppc = wb.data.fetch('PA.NUS.PPP', id_pais, time=ano)
    valor_fator = list(fator_ppc)[0]['value']
    if valor_fator is None:
        raise ValueError("Dados de PPC não disponíveis para este ano/país.")

    return salario_local / valor_fator


def taxa_media_inflacao(nome_pais, ano_inicio, ano_fim):
    """Retorna a taxa média anual de inflação (%), apenas o número.

    A média é calculada somando-se as taxas válidas e dividindo pelo
    número de observações (ignora NaNs).
    """
    id_pais = wb.economy.coder(nome_pais)
    if not id_pais:
        raise ValueError(f"País '{nome_pais}' não encontrado.")

    df = wb.data.DataFrame('FP.CPI.TOTL.ZG', id_pais, time=range(ano_inicio, ano_fim + 1))
    inflacoes = df.values.flatten()
    validas = [taxa for taxa in inflacoes if taxa == taxa]
    if not validas:
        raise ValueError("Não há dados de inflação para o intervalo fornecido.")
    return sum(validas) / len(validas)


def corrigir_valor_com_inflacao(valor_original, taxa_percentual):
    """Corrige um valor usando uma taxa percentual de inflação.

    Parâmetros
    ----------
    valor_original : float
        Valor a ser corrigido.
    taxa_percentual : float
        Taxa de inflação em percentual (ex: 5 para 5%).

    Retorna
    -------
    float
        Valor corrigido.
    """
    return valor_original * (1 + taxa_percentual / 100)

