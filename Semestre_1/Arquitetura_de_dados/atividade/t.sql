SELECT
  b.nome AS build_nome,
  FLOOR(m.Host_Death_Time / 20) * 20 AS tempo_intervalo,
  AVG(m.Health_Pct) AS media_vida_pct,
  COUNT(*) AS quantidade_lutas,
  STDDEV(m.Health_Pct) AS desvio_vida
FROM
  malenia_normalizado m
JOIN
  tabela_builds_referencia b ON m.Host_Build = b.id_build
WHERE
  m.Host_Death_Time IS NOT NULL
  AND m.Health_Pct IS NOT NULL
GROUP BY
  b.nome,
  tempo_intervalo
ORDER BY
  tempo_intervalo,
  media_vida_pct;