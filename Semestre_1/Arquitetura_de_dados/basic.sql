-- Apagar o banco de dados caso ele já exista 
drop database if exists universidade;

-- Criar banco de dados
create database universidade; 

-- Selecionar o banco para uso 
use universidade;

-- Criar tabela alunos 
create table alunos(
	id int auto_increment primary key,
    nome varchar(100) not null,
    curso varchar(100) not null,
    idade int
);

-- Inserir registros na tabela 
insert into alunos(nome, curso, idade)
values('Ana', 'Ciencia de dados', 21);

insert into alunos(nome, curso, idade)
values('Carlos', 'Engenharia', 23);

insert into alunos(nome, curso, idade)
values('Maria', 'ADS', 20);

insert into alunos(nome, curso, idade)
values('João', 'ADS', 25);

-- Visualizar todos os registros 
select * from alunos;

-- Visualizar apenas a coluna do nome 
select nome from alunos;

-- Visualizar nome e curso 
select nome, curso from alunos;

-- Filtrar alunos maiores de 21 anos
select * from alunos where idade >= 21;

-- Filtrar alunos no curso ADS
select * from alunos where curso = 'ADS';

-- Filtrar alunos com idade entre 21 e 23 anos 
select * from alunos where idade between 21 and 23;

-- Outra forma defiltrar intervalo
select * from alunos where idade >= 21 and idade <=23;

-- Ordenar alunos pela idade 
select * from alunos order by idade;

-- Ordenar aluno pela idade (maior para menor)
select * from alunos order by idade desc;



insert into alunos(nome, curso, idade)
values
('Fernanda', 'ADS', 22),
('Pedro', 'Engenheria', 24),
('Juliana', 'Ciencia de Dados', 24),
('Rafael', 'ADS', 21),
('Camila', 'Engenheria', 24),
('Bruno', 'Ciencia de Dados', 25),
('Larissa', 'ADS', 20),
('Patricia', 'ADS', 24),
('Daniel', 'Engenheria', 26),
('Marcos', 'Ciencia de Dados', 21);


-- Verificar como ficou a tabela
SET SQL_SAFE_UPDATES = 0;
update alunos
set idade = 22
where nome = 'Ana';
SET SQL_SAFE_UPDATES = 1;

SET SQL_SAFE_UPDATES = 0;
update alunos
set curso = 'Ciencia de Dados'
where nome = 'João';


update alunos
set idade = idade + 1
where curso = 'ADS';
SET SQL_SAFE_UPDATES = 1;

SET SQL_SAFE_UPDATES = 0;
delete from alunos where idade < 21; 
SET SQL_SAFE_UPDATES = 1;

select *
from alunos
order by id;



select count(*) as total_alunos
from alunos;



select curso, max(idade) as maior_idade
from alunos
group by curso;

select curso, sum(idade) as soma_idade
from alunos
group by curso;

select curso, min(idade) as menor_idade
from alunos
group by curso;



select curso, count(*) as quantidade
from alunos
group by curso
order by quantidade DESC;

select curso, count(*) as quantidade
from alunos
group by curso
order by quantidade DESC;


select curso, count(*) as quantidade
from alunos
group by curso
order by curso ASC;

select curso, sum(idade) as suma_idades
from alunos
group by curso
having soma_idades > 40;

select curso, count(*) as quantidade
from alunos
group by curso
having quantidade > 2;

select curso, count(*) as quantidade
from alunos
where idade >= 22
group by curso
having quantidade > 2;

select curso, count(*) as quantidade
from alunos
where idade >= 21
group by curso
order by quantidade DESC;


select curso, count(*) as quantidade
from alunos
group by curso
having quantidade >= 2
order by curso;


select idade, count(*) as quantidade
from alunos
group by idade
order by idade desc;


select curso, 
	count(*) as quantidade,
     sum(idade) as suma_idades,
     max(idade) as maior_idade,
     min(idade) as menor_idade,
     AVG(idade) as media_idade
from alunos
group by curso
order by curso ASC;


select curso, AVG(idade) as media_idade
from alunos
group by curso
order by media_idade desc;

