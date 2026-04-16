
-- ================================
-- 1 - criar banco de dados
-- ================================

drop database if exists escola;
create database escola;
use escola;

-- ================================
-- 2 - criar tabela de cursos
-- ================================

create table cursos(
    id_curso int primary key auto_increment,
    nome_curso varchar(100) not null
);

-- ================================
-- 3 - inserir dados na tabela de cursos
-- ================================

insert into cursos (nome_curso) values
    ('ADS'),
    ('Engenharia'),
    ('Direito'),
    ('Medicina');

select * from cursos;

-- ================================
-- 4 - criar tabela de alunos
-- ================================
create table alunos(
    id_aluno int primary key auto_increment,
    nome_aluno varchar(100) not null,
    id_curso int,
    foreign key (id_curso) references cursos(id_curso)
);

-- ================================
-- 5 - inserir dados na tabela de alunos
-- ================================
insert into alunos (nome_aluno, id_curso) values
    ('João', 1),
    ('Maria', 2),
    ('Pedro', 3),
    ('Ana', 4),
    ('Lucas', 1),
    ('Carla', 2),
    ('Felipe', 3),
    ('Gabriela', null);
;
select * from alunos;

-- ================================
-- 6 - tabela de disciplinas
-- ================================

create table disciplinas(
    id_disciplina int primary key auto_increment,
    nome_disciplina varchar(100) not null
);

insert into disciplinas (nome_disciplina) values
    ('SQL'),
    ('Estatística'),
    ('Direito Civil'),
    ('Anatomia'),
    ('Programação'),
    ('Física'),
    ('Power BI');

select * from disciplinas;


-- ================================
-- 7 - tabela entre alunos e disciplinas (tabela de relacionamento)
-- ================================

create table alunos_disciplinas(
    id_aluno int,
    id_disciplina int,
    primary key (id_aluno, id_disciplina),
    foreign key (id_aluno) references alunos(id_aluno),
    foreign key (id_disciplina) references disciplinas(id_disciplina)
);

-- ================================
-- 8 - inserir dados na tabela de relacionamento
-- ================================

insert into alunos_disciplinas (id_aluno, id_disciplina) values
    (1, 1),
    (1, 5),
    (2, 2),
    (2, 6),
    (3, 3),
    (3, 4),
    (4, 4),
    (4, 7),
    (5, 1),
    (5, 5),
    (6, 2),
    (6, 6),
    (7, 3),
    (7, 4);


-- ================================
-- 9 - INER JOIN - mostrar os alunos e os cursos que estão matriculados
-- ================================


select 
a.id_aluno,
a.nome_aluno as aluno, 
c.nome_curso as curso
from alunos a
inner join cursos c
on a.id_curso = c.id_curso;


-- ===============================
-- 10 - LEFT JOIN - mostrar todos os alunos e os cursos que estão matriculados (incluir alunos sem curso)
-- ===============================

select 
a.id_aluno,
a.nome_aluno as aluno,
c.nome_curso as curso
from alunos a
left join cursos c
on a.id_curso = c.id_curso;

-- ===============================
-- 11 - RIGHT JOIN - mostrar todos os cursos e os alunos que estão matriculados (incluir cursos sem alunos)
-- ===============================

select
a.id_aluno,
a.nome_aluno as aluno,
c.nome_curso as curso
from alunos a
right join cursos c
on a.id_curso = c.id_curso;

-- ===============================
-- 12 - FULL OUTER JOIN - mostrar todos os alunos e todos os cursos, relacion
-- ===============================

select
a.id_aluno,
a.nome_aluno as aluno,
c.nome_curso as curso
from alunos a
full outer join cursos c
on a.id_curso = c.id_curso;


-- ===============================
-- 13 - mostrar os alunos e as disciplinas que estão cursando
-- ===============================

select
a.id_aluno,
a.nome_aluno as aluno,
d.nome_disciplina as disciplina
from alunos a
inner join alunos_disciplinas ad on a.id_aluno = ad.id_aluno
inner join disciplinas d on ad.id_disciplina = d.id_disciplina;



-- ===============================
-- 14 - mostrar os alunos e as disciplinas que estão cursando, incluindo os alunos que não estão cursando nenhuma disciplina
-- ===============================

select
a.id_aluno,
a.nome_aluno as aluno,
d.nome_disciplina as disciplina
from alunos a
left join alunos_disciplinas ad on a.id_aluno = ad.id_aluno
left join disciplinas d on ad.id_disciplina = d.id_disciplina;


-- ===============================
-- 15 - mostrar os alunos e as disciplinas que estão cursando, incluindo os alunos que não estão cursando nenhuma disciplina e as disciplinas que não estão sendo cursadas por nenhum aluno
-- ===============================

select
a.id_aluno,
a.nome_aluno as aluno,
d.nome_disciplina as disciplina
from alunos a
full outer join alunos_disciplinas ad on a.id_aluno = ad.id_aluno
full outer join disciplinas d on ad.id_disciplina = d.id_disciplina;


-- =================================
-- 16 - Mostrar as diciplinas sem os alunos
-- =================================

select
    d.id_disciplina,
    d.nome_disciplina as disciplina
from disciplinas d
left join alunos_disciplinas ad on d.id_disciplina = ad.id_disciplina
where ad.id_disciplina is null;


-- =================================
-- =================================
-- 1. DISTINCT
-- =================================
-- ================================

select distinct id_curso 
from alunos
where id_curso is not null;

-- =================================
-- 2. DISTINCT com JOIN
-- Mostrar os cursos que possuem alunos matriculados
-- =================================

select distinct c.nome_curso
from alunos a
inner join cursos c
on a.id_curso = c.id_curso;

-- =================================
-- 3. DISTINCT com mais de uma coluna
-- DISTINCT considera a combinação de todas as colunas para eliminar duplicatas
-- =================================

select distinct 
    id_curso,
    nome_aluno
from alunos
where id_curso is not null;

-- =================================
-- 4. ORDER BY com mais de uma coluna
-- =================================

select 
    nome_aluno,
    id_curso
from alunos
where id_curso is not null
order by id_curso ASC, nome_aluno ASC;

-- =================================
-- 5. LIMIT
-- Mostrar apenas os 3 primeiros alunos
-- =================================

select *
from alunos
limit 3;

-- =================================
-- 6. Order by + Limit
-- Mostrar os 3 primeiros alunos ordenados por nome
-- =================================

select *
from alunos
order by nome_aluno ASC
limit 3;

-- =================================
-- 7. Multiplas filtros com AND
-- Alunos do curso 1 e com id maior que 1
-- =================================
select *
from alunos
where id_curso = 1 and id_aluno > 1;

-- =================================
-- 8. Multiplas filtros com OR
-- Alunos do curso 1 ou do curso 2
-- =================================

select *
from alunos
where id_curso = 1 or id_curso = 2;

-- =================================
-- 9. AND + is not null
-- Alunos que tem curso e ele são do curso 2
-- =================================

select *
from alunos
where id_curso = 2 and id_curso is not null;

-- =================================
-- 10. OR + AND (Sem parênteses)
-- Alunos do curso 1 ou do curso 2 e com id maior que 2
-- =================================

select *
from alunos
where id_curso = 1 or id_curso = 2 and id_aluno > 2;

-- =================================
-- 11. OR + AND (Com parênteses)
-- Alunos do curso 1 ou do curso 2 e com id maior que 2
-- =================================

select *
from alunos
where (id_curso = 1 or id_curso = 2) and id_aluno > 2;

-- =================================
-- 12. CONSULTA completa com JOIN, WHERE, ORDER BY
-- =================================

select
a.id_aluno, a.nome_aluno as aluno,
c.nome_curso as curso
from alunos a
inner join cursos c on a.id_curso = c.id_curso;


-- ================================================
-- 13. Group by
-- Quantidade de alunos por curso
-- ================================================
select 
	c.nome_curso,
    count(a.id_aluno) as quantidade_alunos
from cursos c
left join alunos a 
on a.id_curso = c.id_curso
group by c.nome_curso; 

-- ================================================
-- 14. Having
-- Mostrar apenas cursos com mais de 1 aluno
-- ================================================
select 
	c.nome_curso,
    count(a.id_aluno) as quantidade_alunos
from cursos c
left join alunos a 
on a.id_curso = c.id_curso
group by c.nome_curso
having count(a.id_aluno) > 1;

-- ================================================
-- 15. Case when 
-- Classificar alunos conforme possuem ou não curso 
-- ================================================
select 
	nome_aluno,
    case 
		when id_curso is null then "Sem Curso"
        else "Com Curso"
	end as situacao
from alunos; 

-- ================================================
-- 16. Case when com mais de uma condição
-- Classificar alunos conforme o curso
-- ================================================
select 
	nome_aluno,
    case 
		when id_curso = 1 then "Curso ADS"
        when id_curso = 2 then "Curso Engenharia"
        when id_curso = 3 then "Curso Direito"
        when id_curso = 4 then "Curso Medicina"
        else "Sem Curso"
	end as classificacao
from alunos; 

-- ================================================
-- 17. Case when + Relatorio
-- Classificar cursos pela quantidade de alunos
-- ================================================
select 
	c.nome_curso,
    case 
		when count(a.id_aluno) >= 2 then "Turma Maior"
        when count(a.id_aluno) = 2 then "Turma Menor"
        else "Sem Alunos"
	end as situacao_turma
from cursos c
left join alunos a
	on c.id_curso = a.id_curso
group by c.nome_curso; 

 -- ================================================
-- 18. CTE
-- Funciona como uma consulta temporária
-- ================================================
with alunos_com_curso as(
	select 
    id_aluno, nome_aluno, id_curso
    from alunos
    where id_curso is not null
)
select * from alunos_com_curso;

-- ================================================
-- 19. CTE com JOIN
-- ================================================
with alunos_com_curso as(
	select 
    id_aluno, nome_aluno, id_curso
    from alunos
    where id_curso is not null
)
select 
a.nome_aluno as aluno,
c.nome_curso as curso
from alunos_com_curso ac
inner join cursos c
on ac.id_curso = c.id_curso;

-- ================================================
-- 20. CTE + gregação
-- Calcular total de alunos por curso e depois filtra
-- ================================================

with alunos_com_curso as(
    select 
        id_curso
        COUNT(id_aluno) as total
    from alunos
    where id_curso is not null
    group by id_curso
),
select *
from total_por_curso
where total > 1;

-- ================================================
-- 21. WINDOW functions - ROW_NUMBER
-- Gera uma numeração linha a linha
-- Sem agrupar os dados
-- vamos criar um ranking alfabetico geral
-- ================================================

select
    nome_aluno,
    row_number() over (order by nome_aluno ASC) as ranking_alfabetico
from alunos;

 