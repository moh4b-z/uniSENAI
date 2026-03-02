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
    id_pais = wb.economy.coder(nome_pais)
    if not id_pais:
        raise ValueError(f"País '{nome_pais}' não encontrado.")

    fator_ppc = wb.data.fetch('PA.NUS.PPP', id_pais, time=ano)
    valor_fator = list(fator_ppc)[0]['value']
    if valor_fator is None:
        raise ValueError("Dados de PPC não disponíveis para este ano/país.")

    return salario_local / valor_fator


def taxa_media_inflacao(nome_pais, ano_inicio, ano_fim):
    """
        Retorna a taxa média anual de inflação em percentual (%), apenas o número.
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
    """
        Parâmetros:
            valor_original é um float valor a ser corrigido.
            taxa_percentual é um  float taxa de inflação em percentual

        Retorna um float com o valor corrigido.
    """
    return valor_original * (1 + taxa_percentual / 100)