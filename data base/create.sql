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
select * from users
CREATE EXTENSION pgcrypto;
insert into users
    (name, email, password)
    values ('Julio Sánchez', 'julio.sanchez@armasel.com', crypt('Autom2018', gen_salt('bf', 8)));
SELECT email FROM users
    WHERE email='julio.sanchez@armasel.com' 
    AND password = crypt('Autom2018', password);
drop table users;

UPDATE users
    SET password = '$2b$12$ahpKOVPh4ntwBX5UHmm2XeKUzJjCC5tBHwkeDSO6q2Potfv6agXFq'
    WHERE id = 1