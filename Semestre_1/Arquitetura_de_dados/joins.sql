
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