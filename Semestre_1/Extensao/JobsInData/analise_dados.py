# ============================================================================
# ANÁLISE DE DADOS: Jobs and Salaries in Data Science
# ============================================================================

import pandas as pd
from pathlib import Path

# 1. Carregar os dados
# ============================================================================
print("=" * 80)
print("1. CARREGANDO DADOS")
print("=" * 80)

# usar o CSV que está no mesmo diretório do script (resolve sem condicionais)
base_dir = Path(__file__).resolve().parent
csv_path = base_dir / "jobs_in_data.csv"
print(f"Carregando CSV de: {csv_path}")
df = pd.read_csv(csv_path)
print("\nPrimeiras linhas:")
print(df.head())
print("\nÚltimas linhas:")
print(df.tail())

# 2. Verificar tipos de dados
# ============================================================================
print("\n" + "=" * 80)
print("2. INFORMAÇÕES SOBRE O DATAFRAME")
print("=" * 80)

print("\nTipos de dados:")
print(df.dtypes)

# 3. Verificar valores faltantes e duplicados
# ============================================================================
print("\n" + "=" * 80)
print("3. VERIFICAÇÃO DE QUALIDADE DOS DADOS")
print("=" * 80)

print("\nValores nulos por coluna:")
print(df.isnull().sum())

print("\nVerificando duplicatas:")
print(df.T.duplicated())

# 4. Estatísticas descritivas
# ============================================================================
print("\n" + "=" * 80)
print("4. ESTATÍSTICAS DESCRITIVAS")
print("=" * 80)

print(df.describe())

# 5. Traduzir colunas para Português
# ============================================================================
print("\n" + "=" * 80)
print("5. TRADUÇÃO DAS COLUNAS")
print("=" * 80)

novos_nomes = {
    "work_year": "ano_trabalho",
    "job_title": "cargo",
    "job_category": "categoria_cargo",
    "salary_currency": "moeda_salario",
    "salary": "salario",
    "salary_in_usd": "salario_dolar",
    "employee_residence": "residencia_funcionario",
    "experience_level": "nivel_experiencia",
    "employment_type": "tipo_contrato",
    "work_setting": "modelo_trabalho",
    "company_location": "localizacao_empresa",
    "company_size": "porte_empresa"
}

df_pt_br = df.rename(columns=novos_nomes)
print("\nColunas traduzidas:")
print(df_pt_br.columns.tolist())

# 6. Análise temporal (usando coluna de ano)
# ============================================================================
print("\n" + "=" * 80)
print("6. ANÁLISE TEMPORAL")
print("=" * 80)

# Converter ano para datetime
df_pt_br['ano_trabalho'] = pd.to_datetime(df_pt_br['ano_trabalho'], format='%Y')

print("\nIntervalo temporal dos dados:")
print(f"Início: {df_pt_br['ano_trabalho'].min()}")
print(f"Fim: {df_pt_br['ano_trabalho'].max()}")

# 7. Análise de salários
# ============================================================================
print("\n" + "=" * 80)
print("7. ANÁLISE DE SALÁRIOS")
print("=" * 80)

print("\nComparação: Salário Local vs Salário em USD")
print(df_pt_br[['salario', 'salario_dolar', 'moeda_salario']].head(10))

print("\nResumo de salários em USD:")
print(df_pt_br['salario_dolar'].describe())

# ============================================================================
print("\n" + "=" * 80)
print("ANÁLISE CONCLUÍDA")
print("=" * 80)

# ============================================================================
# 9. ANÁLISE DAS CATEGORIAS PROFISSIONAIS
# ============================================================================
print("\n" + "=" * 80)
print("9. ANÁLISE DAS CATEGORIAS PROFISSIONAIS")
print("=" * 80)

# Agrupar por categoria e contar (usa o DataFrame traduzido `df_pt_br`)
df_categoria = (
    df_pt_br.groupby('categoria_cargo')
    .size()
    .reset_index(name='quantidade')
    .sort_values(by='quantidade', ascending=False)
)

print("\nContagem por categoria:")
print(df_categoria)