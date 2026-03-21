import wbgapi as wb
import pandas as pd
from datetime import date


def salario_internacional_simples(nome_pais, salario_local, ano=date.today().year):
    """
        Retorna apenas o salário convertido para dólares internacionais (número).

        Parâmetros:
            nome_pais : str, Nome do país reconhecido pelo wbgapi.
            salario_local: float,vValor na moeda local.
            ano: int, opcional
    """
    print(f"salario_internacional_simples: país={nome_pais}, salario_local={salario_local}, ano={ano}")
    id_pais = wb.economy.coder(nome_pais)
    if not id_pais:
        raise ValueError(f"País '{nome_pais}' não encontrado.")

    # Sempre busca o fator PPC para o ano solicitado.
    fator_ppc = wb.data.fetch('PA.NUS.PPP', id_pais, time=ano)
    valor_fator = list(fator_ppc)[0]['value']
    print(f"salario_internacional_simples: id_pais={id_pais}, fator_ppc={valor_fator}")
    if valor_fator is None:
        raise ValueError("Dados de PPC não disponíveis para este ano/país.")

    # Retorna o salário convertido e também o fator usado (útil para cache)
    return [salario_local / valor_fator, valor_fator]


def taxa_media_inflacao(nome_pais, ano_inicio, ano_fim):
    """
        Retorna a taxa média anual de inflação em percentual (%), apenas o número.
        A média é calculada somando-se as taxas válidas e dividindo pelo
        número de observações (ignora NaNs).
    """
    print(f"taxa_media_inflacao: país={nome_pais}, ano_inicio={ano_inicio}, ano_fim={ano_fim}")
    id_pais = wb.economy.coder(nome_pais)
    if not id_pais:
        raise ValueError(f"País '{nome_pais}' não encontrado.")

    df = wb.data.DataFrame('FP.CPI.TOTL.ZG', id_pais, time=range(ano_inicio, ano_fim + 1))
    inflacoes = df.values.flatten()
    validas = [taxa for taxa in inflacoes if taxa == taxa]
    if not validas:
        raise ValueError("Não há dados de inflação para o intervalo fornecido.")
    taxa_media = sum(validas) / len(validas)
    print(f"taxa_media_inflacao: média calculada={taxa_media}")
    return taxa_media


def corrigir_valor_com_inflacao(valor_original, taxa_percentual):
    print(f"corrigir_valor_com_inflacao: valor_original={valor_original}, taxa_percentual={taxa_percentual}")
    """
        Parâmetros:
            valor_original é um float valor a ser corrigido.
            taxa_percentual é um  float taxa de inflação em percentual

        Retorna um float com o valor corrigido.
    """
    return valor_original * (1 + taxa_percentual / 100)


# ==== Funções de nível superior para processamento de DataFrames =====

def _inicializa_cache():
    """Cria as estruturas de cache usadas por ``calcula_salario_internacional``.

    O cache guarda duas coisas:
    * ``fatores_ppc``: mapeia (pais, ano) -> fator para evitar múltiplas chamadas à API
    * ``taxas_inflacao``: armazena inflação média calculada para um intervalo

    Retornamos um dicionário mutável para ser compartilhado entre invocações.
    """
    return {"fatores_ppc": {}, "taxas_inflacao": {}}


def _obtem_fator_ppc(nome_pais, ano, cache):
    key = (nome_pais, ano)
    if key in cache["fatores_ppc"]:
        return cache["fatores_ppc"][key]
    _, fator = salario_internacional_simples(nome_pais, 1.0, ano=ano)
    cache["fatores_ppc"][key] = fator
    return fator


def _obtem_taxa_media(nome_pais, ano_inicio, ano_fim, cache):
    key = (nome_pais, ano_inicio, ano_fim)
    if key in cache["taxas_inflacao"]:
        return cache["taxas_inflacao"][key]
    taxa = taxa_media_inflacao(nome_pais, ano_inicio, ano_fim)
    cache["taxas_inflacao"][key] = taxa
    return taxa


def calcula_salario_internacional(pais, salario_local, ano_trabalho, ano_atual=None, cache=None):
    """Retorna salário convertido para dólar internacional corrigido pela inflação.

    Essa função encapsula toda a lógica de cache usada no notebook, garantindo
    que chamadas à World Bank API sejam feitas o mínimo possível.  O parâmetro
    ``cache`` deve ser um dicionário retornado por ``_inicializa_cache``; se
    omitido, a função cria um cache temporário local (útil em chamadas unitárias).

    ``ano_atual`` será preenchido com o ano corrente se não for fornecido.

    Em caso de qualquer falha na obtenção de dados (API fora do ar, ano
    indisponível etc.) o retorno será ``None`` para permitir filtragem pelo
    chamador sem interromper o processamento em lote.
    """
    print(f"calcula_salario_internacional: pais={pais}, salario_local={salario_local}, ano_trabalho={ano_trabalho}, ano_atual={ano_atual}")
    try:
        if ano_atual is None:
            ano_atual = date.today().year
        if cache is None:
            cache = _inicializa_cache()

        nome_pais = pais
        # valores nulos são tratados como None
        if pd.isna(salario_local) or nome_pais is None or (isinstance(nome_pais, float) and pd.isna(nome_pais)):
            print("calcula_salario_internacional: entrada inválida; retornando None")
            return None

        ano = ano_trabalho.year if hasattr(ano_trabalho, "year") else int(ano_trabalho)

        anos_diff = ano_atual - ano
        if anos_diff <= 0:
            salario_corrigido = salario_local
        else:
            taxa_media = _obtem_taxa_media(nome_pais, ano, ano_atual, cache)
            # fórmula composta usando taxa média anual
            salario_corrigido = salario_local * (1 + taxa_media / 100) ** anos_diff

        fator = _obtem_fator_ppc(nome_pais, ano_atual, cache)
        salario_conv = salario_corrigido / fator
        return salario_conv
    except Exception:
        # qualquer problema gera None (simples e silencioso como no notebook)
        return None


def adicionar_coluna_internacional(df, pais_col='residencia_funcionario',
                                   local_col='localizacao_empresa',
                                   salario_col='salario', ano_col='ano_trabalho'):
    """Adiciona ao ``df`` uma coluna ``salario_internacional_atual``.

    A função calcula o valor para cada linha, reusando o cache global para
    evitar duplicação de chamadas.  Ela retorna o DataFrame modificado (mesmo
    objeto passado).
    """
    cache = _inicializa_cache()
    ano_atual = date.today().year

    print('Iniciando processo de conversão de salário internacional para cada linha.')

    # 1. Preparar dados: país final AND ano numérico
    paises = df[pais_col].fillna(df[local_col]) if pais_col in df and local_col in df else df[pais_col]
    anos = df[ano_col]
    if hasattr(anos.dtype, 'kind') and anos.dtype.kind in 'Mm':
        anos = anos.dt.year
    else:
        anos = anos.astype('Int64')

    # 2. Encontrar pares únicos para evitar recalcular causa de grandes datasets
    keys = list(zip(paises, anos.astype('Int64')))
    unique_keys = list(dict.fromkeys(keys))  # mantém ordem e remove duplicados

    multiplier_por_chave = {}
    for idx, (pais, ano_em) in enumerate(unique_keys):
        print(f"Precalculando chave {idx+1}/{len(unique_keys)}: pais={pais}, ano={ano_em}")
        if pd.isna(pais) or pd.isna(ano_em):
            multiplier_por_chave[(pais, ano_em)] = None
            print(f"  chave inválida, pula")
            continue

        # Faz o cálculo com salário 1.0 para obter o fator multiplicador em vez de repetir a lógica toda.
        resultado_base = calcula_salario_internacional(pais, 1.0, ano_em,
                                                     ano_atual=ano_atual, cache=cache)
        multiplier_por_chave[(pais, ano_em)] = resultado_base
        print(f"  resultado base para chave: {resultado_base}")

    # 3. Aplicar multiplicador por linha - rápido e sem novas chamadas API.
    resultado_lista = []
    for idx, (pais, salario_local, ano_em) in enumerate(zip(paises, df[salario_col], anos)):
        key = (pais, int(ano_em) if not pd.isna(ano_em) else ano_em)
        multiplicador = multiplier_por_chave.get(key)

        if multiplicador is None or pd.isna(salario_local):
            print(f"Linha {idx}: resultado None (sem base ou salário inválido)")
            resultado_lista.append(None)
        else:
            valor = salario_local * multiplicador
            print(f"Linha {idx}: calculado (salario_local={salario_local}) => {valor}")
            resultado_lista.append(valor)

    df['salario_internacional_atual'] = resultado_lista

    print('Processo de conversão finalizado, todas as linhas foram processadas.')
    return df
