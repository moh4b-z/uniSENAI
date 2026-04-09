CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nome_categoria VARCHAR(255) NOT NULL
);

CREATE TABLE leitores (
    id_leitor INT PRIMARY KEY AUTO_INCREMENT,
    nome_leitor VARCHAR(255) NOT NULL
);

CREATE TABLE livros (
    id_livro INT PRIMARY KEY AUTO_INCREMENT,
    nome_livro VARCHAR(255) NOT NULL,
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE emprestimos (
    id_leitor INT,
    id_livro INT,
    PRIMARY KEY (id_leitor, id_livro),
    FOREIGN KEY (id_leitor) REFERENCES leitores(id_leitor),
    FOREIGN KEY (id_livro) REFERENCES livros(id_livro)
);


INSERT INTO categorias (nome_categoria) 
VALUES 
('Romance'), 
('Tecnologia'), 
('História'), 
('Ciência'),
('Filosofia'),
('Biografia'),
('Arte'),
('Psicologia')
;

INSERT INTO livros (nome_livro, id_categoria) 
VALUES 
('Orgulho e Preconceito', 1), 
('Dom Casmurro', 1), 
('SQL para Iniciantes', 2), 
('Python na Prática', 2), 
('História do Brasil', 3), 
('Física Básica', 4), 
('O Pequeno Príncipe', NULL), 
('Steve Jobs', 6), 
('História da Arte', 7), 
('Inteligência Emocional', NULL);


INSERT INTO leitores (nome_leitor) 
VALUES
    ('Ana'),
    ('Bruno'),
    ('Carla'),
    ('Diego'),
    ('Elisa'),
    ('Felipe'),
    ('Gabriela'),
    ('Henrique'),
    ('Isabela');

INSERT INTO emprestimos (id_leitor, id_livro)
VALUES
    (1, 1),
    (1, 3),
    (2, 2),
    (2, 4),
    (3, 3),
    (4, 5),
    (5, 6),
    (3, 8),
    (4, 2),
    (5, 3),
    (7, 9);

/*1- Lista - Mostrar apenas livros que possuem categoria*/

SELECT nome_livro, nome_categoria
FROM livros left join categorias c on livros.id_categoria = c.id_categoria
WHERE nome_categoria IS NOT NULL;

/*2- Lista - Mostrar todos os livros*/

SELECT nome_livro, nome_categoria
FROM livros left join categorias c on livros.id_categoria = c.id_categoria;

/*3- Lista - Mesmo categorias sem livros devem aparecer*/

SELECT nome_livro, nome_categoria
FROM livros right join categorias c on livros.id_categoria = c.id_categoria;

/*4- Explique com suas palavras a diferença entre:*/
/* 
    LEFT JOIN: Mostra todos os registros da tabela à esquerda que você está consultando
    e os registros correspondentes da tabela à "direita". 
*/
/* 
    INNER JOIN: Mostra apenas os registros que têm correspondência em ambas as tabelas. 
*/

/*5- Lista - Mostrar quem pegou qual livro.*/

SELECT l.nome_leitor, li.nome_livro
FROM leitores l
JOIN emprestimos e ON l.id_leitor = e.id_leitor
JOIN livros li ON e.id_livro = li.id_livro;

/*6- Lista - Mostrar apenas leitores que possuem empréstimos.*/

SELECT DISTINCT l.nome_leitor
FROM leitores l
JOIN emprestimos e ON l.id_leitor = e.id_leitor;

/*7- Lista - leitores que não pegaram nenhum livro.*/

SELECT l.nome_leitor
FROM leitores l
LEFT JOIN emprestimos e ON l.id_leitor = e.id_leitor
WHERE e.id_leitor IS NULL;

/*8- Lista - Mostrar os livros que não foram emprestados.*/

SELECT li.nome_livro
FROM livros li
LEFT JOIN emprestimos e ON li.id_livro = e.id_livro
WHERE e.id_livro IS NULL;

/*9- Lista - categorias que não possuem livros.*/

SELECT c.nome_categoria
FROM categorias c
LEFT JOIN livros l ON c.id_categoria = l.id_categoria
WHERE l.id_categoria IS NULL;

/* 10- Monte uma consulta que mostre.
- todos os leitores
- nome do livro
- categoria do livro
Mesmo que o leitor não tenha feito empréstimo
*/

SELECT l.nome_leitor, li.nome_livro, c.nome_categoria
FROM leitores l
LEFT JOIN emprestimos e ON l.id_leitor = e.id_leitor
LEFT JOIN livros li ON e.id_livro = li.id_livro
LEFT JOIN categorias c ON li.id_categoria = c.id_categoria;

/* 
    11.Diagrama do banco de dados
Usando o recurso Reverse Engineer no MySQL Workbench, gere o diagrama
das tabelas do banco de dados e identifique:
• as chaves primárias;
• as chaves estrangeiras;
• os relacionamentos entre as tabelas.
*/


/*
12.Desafio extra
Explique por que a tabela emprestimos representa um relacionamento muitospara-muitos (N:N) entre leitores e livros.
*/
/*
    É porque um leitor pode pegar vários livros emprestados e um livro pode 
    ser emprestado para vários leitores ao longo do tempo.
*/