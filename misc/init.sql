CREATE SCHEMA demodata;

CREATE TABLE public.formation (
	name varchar(50) NULL,
	room varchar(50) NULL
);

INSERT INTO public.formation
(name, room)
VALUES('formation1', 'salle1');