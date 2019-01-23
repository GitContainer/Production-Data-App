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
    SET start_hour = '12:30:00',
        stop_time = '00:30:15',
        stops = 5,
        velocity = 79,
        hits = 225
    WHERE id = '5S07';

INSERT INTO production 
    (date, shift, machine, start_hour, stop_time, stops, hits)
    VALUES ('19/01/2019', 1, 'Schlatter 1', '8:50:05', '8:40:15', 40, 629);

delete from production where id >= 1;

-- ALTER TABLE production ALTER COLUMN date TYPE VARCHAR;
select * from machines; 
select * from production; 
select * from products;
SELECT pg_reload_conf();

UPDATE machines
    SET hits = 0,
        velocity = 0,
        stops = 0,
        stop_time = '00:00:00',
        start_hour = null

SELECT * FROM pg_stat_activity;
