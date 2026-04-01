CREATE DATABASE Atividades;
USE Atividades;


create table funcionarios(
	id int auto_increment primary key,
    nome varchar(100),
    departamento  varchar(100),
    idade int,
    salario decimal(10,2)
);


insert into funcionarios(nome, departamento, idade, salario) values
    ('Ana', 'TI', 25, 5000.00),
    ('Bruno', 'RH', 30, 3200.00),
    ('Carla', 'Financeiro', 28, 4500.00),
    ('Eduarda', 'TI', 35, 5500.00),
    ('Elisa', 'Administrativo', 22, 2800.00),
    ('Felipe', 'Financeiro', 40, 4700.00),
    ('Gabriela', 'RH', 27, 3100.00),
    ('Henrique', 'TI', 32, 6000.00)
;

-- 3. Mostrar todos os funcionários
select * from funcionarios;

-- 4. Mostrar funcionários ordenados por salário (do maior para o menor)
select * from funcionarios order by salario desc;

SET SQL_SAFE_UPDATES = 0;

-- 5. Atualizar o salário da funcionária Gabriela para 3300.00
update funcionarios
set salario = 3300.00
where nome = 'Gabriela';

-- 6. Atualizar o departamento do funcionário Bruno para 'TI'
update funcionarios
set departamento = 'TI'
where nome = 'Bruno';


-- 7. Excluir o registro do funcionário Eduarda
delete from funcionarios where nome = 'Edurda';

-- 8. Contar o número total de funcionários
select count(*) from funcionarios;

-- 9. Contar o número de funcionários em cada departamento
select departamento, count(*) as total_funcionarios
from funcionarios
group by departamento;

-- 10.  Calcular a média salarial por departamento e ordenar do maior para o menor
select departamento, avg(salario) as media_salarial
from funcionarios
group by departamento
order by media_salarial desc;

-- 11. Calcular o total de salários pagos por departamento e ordenar do maior para o menor
select departamento, count(salario) as salario_total
from funcionarios
group by departamento
order by media_salarial desc;

-- 12. Calcular o total de funcionários, média salarial, maior salário, menor salário e total pago por departamento, ordenando pelo departamento com a maior média salarial
select departamento, count(*) as total_funcionarios, 
                    avg(salario) as media_salarial, 
                    max(salario) as maior_salario, 
                    min(salario) as menor_salario,
                    sum(salario) as total_pago
from funcionarios
group by departamento
order by media_salarial desc;


-- 13.  Selecionar os departamentos que possuem mais de 1 funcionário e mostrar o total de funcionários em cada um desses departamentos
select departamento, count(*) as total_funcionarios
from funcionarios
group by departamento
having total_funcionarios > 1;

-- 14. Mesma coisa que a 12, porém ordenando pelo departamento com o maior total pago
select departamento, count(*) as total_funcionarios, 
                    avg(salario) as media_salarial, 
                    max(salario) as maior_salario, 
                    min(salario) as menor_salario,
                    sum(salario) as total_pago
from funcionarios
group by departamento
order by total_pago desc;


/*
  Qual departamento parece ser o mais caro para a empresa? Justifiquesua resposta com base nos dados.

    O departamento de TI parece ser o mais caro para a empresa, 
    pois possui a maior média salarial e o maior total pago em salários. 
    Isso pode ser devido à natureza técnica dos cargos nesse departamento, 
    que geralmente exigem habilidades especializadas e, 
    portanto, são remunerados com salários mais altos. 
    Além disso, o departamento de TI tem um número significativo de funcionários, 
    o que contribui para o alto total pago em salários.
*/


/*
ATIVIDADE 2: VENDAS
*/

create table vendas(
    id int auto_increment primary key,
    produto varchar(100),
    categoria varchar(100),
    quantidade int,
    valor decimal(10,2)
);

INSERT INTO vendas (produto, categoria, quantidade, valor) VALUES
    ('Notebook', 'Eletronicos', 2, 3500.00),
    ('Mouse', 'Eletronicos', 5, 80.00),
    ('Mesa', 'Moveis', 1, 900.00),
    ('Cadeira', 'Moveis', 4, 450.00),
    ('Curso SQL', 'Educacao', 10, 200.00),
    ('Livro Python', 'Educacao', 6, 120.00),
    ('Monitor', 'Eletronicos', 3, 1200.00),
    ('Estante', 'Moveis', 2, 700.00)
;

-- 2. Mostrar todas as vendas
select * from vendas;

-- 3. Mostrar vendas ordenadas por valor (do maior para o menor)
select * from vendas order by valor desc;

-- 4. Atualizar o valor do produto 'Livro Python' em 25%
update vendas
set valor = valor * 1.25
where produto = 'Livro Python';

-- 5. Vender o produto 'Mesa' e excluir das vendas esse movel
update vendas
set quantidade = quantidade - 1
where produto = 'Mesa';

delete from vendas where produto = 'Mesa';

-- 6. Contar o número total de vendas
select count(*) from vendas;

-- 7. Contar o número de vendas em cada categoria
select categoria, count(*) as total_vendas
from vendas
group by categoria;


-- 8. Calcular a média de valor por categoria
select categoria, avg(valor) as media_valor
from vendas
group by categoria;

-- 9. Calcular o total de valor vendido por categoria e ordenar do maior para o menor
select categoria, sum(valor) as total_vendido
from vendas
group by categoria
order by total_vendido desc;

-- 10. Calcular o total de vendas, média de valor, maior valor, menor valor e total vendido por categoria, ordenando pela categoria com a maior média de valor
select categoria, count(*) as total_vendas,
                    avg(valor) as media_valor,
                    max(valor) as maior_valor,
                    min(valor) as menor_valor,
                    sum(valor) as total_vendido
from vendas
group by categoria
order by media_valor desc;

-- 11. Mostrando só categorias que possuem mais de 2 vendas.
select categoria, count(*) as total_vendas
from vendas
group by categoria
having total_vendas > 2;

-- 12. Ordene as categorias pelo valor total vendido (maior → menor).
select categoria, count(*) as total_vendido
from vendas
group by categoria
order by total_vendido desc;


/*
ATIVIDADE 3: IMPACTO NA ATIVIDADE 1
*/


-- 1. Atualize o salário do bruno para 4000.00
update funcionarios
set salario = 4000.00
where nome = 'Bruno';

-- 2. Exclua a funcionária Gabriela.
delete from funcionarios where nome = 'Gabriela';

-- 3. Execute novamente o relatório da Atividade 1 (Parte 6).
select departamento, count(*) as total_funcionarios, 
                    avg(salario) as media_salarial, 
                    max(salario) as maior_salario, 
                    min(salario) as menor_salario,
                    sum(salario) as total_pago
from funcionarios
group by departamento
order by media_salarial desc;

/*
4. Responda:
• O que mudou nos resultados?
    Teve um almento no salário do funcionário Bruno, o que aumentou a média salarial e o total pago no departamento de TI.
    Já a exclusão da funcionária Gabriela resultou na redução do número total de funcionários, e não existe mais ninguem no RH


• Qual operação teve maior impacto: UPDATE ou DELETE? Por quê?
    Depende do ponto de vista. O UPDATE teve um impacto significativo no departamento de TI, 
    aumentando a média salarial e o total pago, enquanto o DELETE teve um impacto mais direto no departamento de RH, 
    reduzindo o número total de funcionários a zero.
*/


SET SQL_SAFE_UPDATES = 1;


/*
Atividade 4 – Conceitual: WHERE vs HAVING
*/


/*

Indique qual cláusula deve ser utilizada (WHERE ou HAVING) e justifique:

1. Mostrar apenas alunos com idade maior que 21:
    O WHERE deve ser utilizada para filtrar os alunos com idade maior que 21.

2. Mostrar apenas cursos com mais de 2 alunos:
    Tem que ser HAVING deve ser utilizada para filtrar os cursos com mais de 2 alunos,
    pois está lidando com uma condição que envolve uma função de agregação (COUNT) e um agrupamento por curso.

3. Mostrar apenas funcionários do departamento TI:
    O WHERE deve ser utilizada para filtrar os funcionários do departamento TI.

4. Mostrar apenas departamentos com média salarial maior que 4000:
    O HAVING deve ser utilizada para filtrar os departamentos com média salarial maior que 4000,
    pois está lidando com uma condição que envolve uma função de agregação (AVG) e um agrupamento por departamento.

*/