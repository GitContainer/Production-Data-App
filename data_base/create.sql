CREATE TABLE velocities (
    timestamp TIME PRIMARY KEY,
    mg320 SMALLINT NOT NULL DEFAULT 0,
    pg12 SMALLINT NOT NULL DEFAULT 0,
    evg SMALLINT NOT NULL DEFAULT 0,
    jager SMALLINT NOT NULL DEFAULT 0,
    schl1 SMALLINT NOT NULL DEFAULT 0,
    schl4 SMALLINT NOT NULL DEFAULT 0,
    schl5 SMALLINT NOT NULL DEFAULT 0,
    schl6 SMALLINT NOT NULL DEFAULT 0,
    schl7 SMALLINT NOT NULL DEFAULT 0
);
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
        hits = 245
    WHERE id = '5S07';

INSERT INTO production 
    (date, shift, machine, start_hour, stop_time, stops, hits)
    VALUES ('19/01/2019', 1, 'Schlatter 1', '8:50:05', '8:40:15', 40, 629);

delete from production where id >= 1;

-- ALTER TABLE production ALTER COLUMN date TYPE VARCHAR;
 
select * from production; 
select * from products;
select * from machines;
select * from users;
SELECT pg_reload_conf();

UPDATE machines
    SET hits = 0,
        velocity = 0,
        stops = 0,
        stop_time = '00:00:00',
        start_hour = null

-- ALTER TABLE machines
--     ADD COLUMN hour0 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour1 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour2 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour3 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour4 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour5 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour6 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour7 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour8 INTEGER NOT NULL DEFAULT 0,
--     ADD COLUMN hour9 INTEGER NOT NULL DEFAULT 0;

-- UPDATE machines 
--     SET hour0 = 3000, 
--         hour1 = 6500, 
--         hour2 = 9300, 
--         hour3 = 12600, 
--         hour4 = 15000, 
--         hour5 = 17000, 
--         hour6 = 21320, 
--         hour7 = 23200, 
--         hour8 = 25000,  
--         hour9 = 28856
--     WHERE id = 'MG320';

SELECT pg_terminate_backend(23156);

SELECT * FROM pg_stat_activity;

UPDATE machines 
    SET stop_time = '8:32:35',
        stops = 98,
        velocity = 97,
        hits = 500,
        hour0 = 500
    WHERE id = 'MG320'

INSERT INTO velocities 
    (timestamp, mg320, pg12, evg, jager, schl1, schl4, schl5, schl6, schl7)
    VALUES ('9:10:52', 40, 65, 77, 92, 86, 70, 80, 60, 0);

select * from velocities;
select * from machines;

DELETE FROM velocities WHERE 1 = 1;

delete from production where 1 = 1;

delete from users where name = 'Braulio González'
select * from users;

insert into machines
    (id, name, start_hour, stop_time, stops, velocity, hits, hour0, hour1, hour2, hour3, hour4, hour5, hour6, hour7, hour8, hour9)
    values ('SCHL7', 'Schlatter 7', '7:40:32', '00:5:45', 45, 101, 6500, 500, 750 , 1650, 3200, 3500, 4200, 5000, 5420, 5900, 6500);

insert into machines
    (id, name)
    values ('SCHL', 'Schlatter 5')

--ALTER TABLE machines ALTER COLUMN hour9 set DEFAULT 0
-- ALTER TABLE machines
--     ADD COLUMN last_stop TIME