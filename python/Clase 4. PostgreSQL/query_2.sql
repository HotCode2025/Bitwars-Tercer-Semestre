-- SELECT * FROM persona WHERE id_persona IN (1, 2, 3);

-- Insertar registro
INSERT INTO 
    persona(nombre, apellido, email) 
VALUES 
    ('Susana', 'Lara', 'susanalara@gmail.com');

-- Actualizar registro
UPDATE 
	persona 
SET 
	nombre = 'Ivonne', 
	apellido = 'Esparza', 
	email = 'iesparza@gmail.com' 
WHERE 
	id_persona = 3

-- Borrar registro
DELETE FROM
    persona
WHERE
    id_persona = 3