-- CREATE TABLE flights (
--     id SERIAL PRIMARY KEY,
--     origin VARCHAR NOT NULL,
--     destination VARCHAR NOT NULL,
--     duration INTEGER NOT NULL
-- );
-- SELECT * FROM flights;
-- INSERT INTO flights
--     (origin, destination, duration)
--     VALUES ('Shangai', 'Istanbul', 735);
-- SELECT origin, destination FROM flights;
-- SELECT * FROM flights WHERE origin = 'New York';
-- SELECT AVG(duration) FROM flights 
--     WHERE destination = 'New York';
-- UPDATE flights
--     SET duration = 430
--     WHERE origin = 'Lima'
--     AND destination = 'New York';
-- DELETE FROM flights
--     WHERE destination = 'Istanbul';
-- CREATE EXTENSION pgcrypto;
insert into users
    (name, email, password)
    values ('Julio Sánchez', 'julio.sanchez@armasel.com', crypt('Autom2018', gen_salt('bf', 8)));
SELECT email FROM users
    WHERE email='julio.sanchez@armasel.com' 
    AND password = crypt('Autom2018', password);
drop table users;

update users set name = 'Braulio Gonzalez' where id = 2;
UPDATE machines
    SET start_hour = '10:30:00'
    WHERE id = 'MG320';

INSERT INTO production 
    (date, shift, machine, start_hour, stop_time, stops, hits)
    VALUES ('19/01/2019', 1, 'Schlatter 5', '9:30:05', '3:20:15', 50, 549);

delete from production where id >= 1;

-- ALTER TABLE production ALTER COLUMN date TYPE VARCHAR;
select * from machines; 
select * from production; 
select * from products;