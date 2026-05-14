-- Análises SQL para as tabelas: malenia_normalizado, tabela_builds_referencia, phantoms
-- Assumindo que as tabelas foram importadas em um banco de dados (ex: SQLite, PostgreSQL)
-- As tabelas são:
-- malenia_normalizado: id_registro, Host_Death_Time, Host_Build, Level, Phase, Waterflow_Death, Health_Pct, Location, id_phantom
-- tabela_builds_referencia: id_build, nome, descricao
-- phantoms: id_phantom, Phantom_Count, Phantom_Build, Phantom_Death

-- 1. Correlação entre tempo de morte do host (Host_Death_Time) e porcentagem de vida do boss (Health_Pct)
-- Agrupar por faixas de tempo para ver média de vida restante
SELECT
    CASE
        WHEN Host_Death_Time < 100 THEN '< 100s'
        WHEN Host_Death_Time BETWEEN 100 AND 200 THEN '100-200s'
        WHEN Host_Death_Time BETWEEN 200 AND 300 THEN '200-300s'
        ELSE '> 300s'
    END AS faixa_tempo,
    AVG(Health_Pct) AS media_vida_pct,
    COUNT(*) AS quantidade
FROM malenia_normalizado
GROUP BY faixa_tempo
ORDER BY faixa_tempo;

-- 2. Análise se o uso de phantoms aumenta a chance de passar para a segunda fase (Phase = 2)
-- Comparar porcentagem de chegadas à Phase 2 com e sem phantoms
SELECT
    CASE WHEN id_phantom != '' THEN 'Com Phantom' ELSE 'Sem Phantom' END AS uso_phantom,
    Phase,
    COUNT(*) AS quantidade,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN id_phantom != '' THEN 'Com Phantom' ELSE 'Sem Phantom' END), 2) AS porcentagem
FROM malenia_normalizado
GROUP BY uso_phantom, Phase
ORDER BY uso_phantom, Phase;

-- 3. Correlação entre build do host e tempo de morte
-- Média de tempo por build
SELECT
    b.nome AS build_nome,
    AVG(m.Host_Death_Time) AS media_tempo_morte,
    COUNT(*) AS quantidade
FROM malenia_normalizado m
JOIN tabela_builds_referencia b ON m.Host_Build = b.id_build
GROUP BY b.nome
ORDER BY media_tempo_morte;

-- 4. Análise de phantoms: Contagem média de phantoms por build do phantom
SELECT
    b.nome AS phantom_build_nome,
    AVG(p.Phantom_Count) AS media_count,
    COUNT(*) AS quantidade
FROM phantoms p
JOIN tabela_builds_referencia b ON p.Phantom_Build = b.id_build
GROUP BY b.nome
ORDER BY media_count DESC;

-- 5. Localização e fase alcançada
-- Distribuição de fases por localização
SELECT
    Location,
    Phase,
    COUNT(*) AS quantidade
FROM malenia_normalizado
GROUP BY Location, Phase
ORDER BY Location, Phase;

-- 6. Correlação entre nível do jogador (Level) e porcentagem de vida restante
SELECT
    CASE
        WHEN Level < 130 THEN '< 130'
        WHEN Level BETWEEN 130 AND 150 THEN '130-150'
        WHEN Level BETWEEN 150 AND 170 THEN '150-170'
        ELSE '> 170'
    END AS faixa_level,
    AVG(Health_Pct) AS media_vida_pct,
    COUNT(*) AS quantidade
FROM malenia_normalizado
GROUP BY faixa_level
ORDER BY faixa_level;

-- 7. Análise de mortes de phantoms e sucesso na fase
-- Para registros com phantom, ver se morte do phantom afetou a fase
SELECT
    p.Phantom_Death,
    m.Phase,
    COUNT(*) AS quantidade
FROM malenia_normalizado m
JOIN phantoms p ON m.id_phantom = p.id_phantom
GROUP BY p.Phantom_Death, m.Phase
ORDER BY p.Phantom_Death, m.Phase;

-- 8. Builds mais comuns por fase
SELECT
    Phase,
    b.nome AS build_nome,
    COUNT(*) AS quantidade
FROM malenia_normalizado m
JOIN tabela_builds_referencia b ON m.Host_Build = b.id_build
GROUP BY Phase, b.nome
ORDER BY Phase, quantidade DESC;