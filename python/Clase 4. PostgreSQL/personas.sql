CREATE TABLE personas
(
    id_persona SERIAL,
    nombre VARCHAR,
    apellido VARCHAR,
    email VARCHAR
);

SELECT * FROM public.persona
ORDER BY id_persona ASC;

INSERT INTO public.persona
("Juan", "Perez", "jperez@gmail.com"),
("Carla", "Gomez", "cgomez@gmail.com");