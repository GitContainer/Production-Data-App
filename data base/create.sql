CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    origin VARCHAR NOT NULL,
    destination VARCHAR NOT NULL,
    duration INTEGER NOT NULL
);
SELECT * FROM flights;
INSERT INTO flights
    (origin, destination, duration)
    VALUES ('Lima', 'New York', 455);
SELECT origin, destination FROM flights;
SELECT * FROM flights WHERE origin = 'New York';