-- Inserción de Datos iniciales de Bookhub

-- Inserción de Datos em tabla "generos"
INSERT INTO generos (nombre, descripcion, created_by) 
VALUES 
	('Ciencia Ficcion', 'Historias basadas en logros cientificos o tecnologicos hipoteticos.', 'System'),
    ('Desarrollo Personal', 'Contenido enfocado en la mejora de habitos, productividad y crecimiento.', 'System'),
    ('Ficcion Filosofica', 'Novelas que exploran cuestiones profundas sobre la vida y el destino.', 'System');

-- Inserción de Datos em tabla "autores"
INSERT INTO autores (nombre, email, created_by) VALUES 
	('Frank Herbert', 'frank@herbert.com', 'Sistema'),
	('James Clear', 'james@clear.com', 'Sistema'),
	('Paulo Coelho', 'paulo@coelho.com', 'Sistema');

-- Inserción de Datos em tabla "libros"
INSERT INTO libros (nombre, autor, descripcion, fecha_publicacion, imagen_portada, created_by) 
VALUES 
	(
		'Dune', 
		1, 
		'En el desértico planeta Arrakis, el joven Paul Atreides se ve envuelto en una lucha por el control de la especia, la sustancia más valiosa del universo.', 
		'1965-08-01', 
		'https://images.cdn2.buscalibre.com/fit-in/660x660/0d/73/0d739e6e0e837d7637f97f9aad3639b4.jpg', 
		'System'
	),
	(
		'Habitos Atomicos', 
		2, 
		'Un sistema revolucionario para mejorar un 1% cada día, rompiendo malos hábitos y construyendo conductas positivas a través de pequeños cambios.', 
		'2018-10-16', 
		'https://images.cdn1.buscalibre.com/fit-in/660x660/a1/25/a125a01ee6e0e4ddaaf69799be4bfdb5.jpg', 
		'System'
	),
	(
		'El alquimista', 
		3, 
		'La historia de Santiago, un joven pastor andaluz que viaja desde su tierra natal hacia el desierto egipcio en busca de un tesoro oculto en las pirámides.', 
		'1988-01-01', 
		'https://images.cdn2.buscalibre.com/fit-in/660x660/26/62/26625e8981526ce8fd0e1595e609f455.jpg', 
		'System'
	);
    
-- Inserción de Datos em tabla intermedia "libros_generos"
INSERT INTO libros_generos (id_libro, id_genero, created_by) 
VALUES 
	(1, 1, 'System'),
    (2, 2, 'System'),
    (3, 3, 'System');
