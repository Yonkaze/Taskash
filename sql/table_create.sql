DROP TABLE IF EXISTS User;

CREATE TABLE User(
    username varchar(20) PRIMARY KEY,
    password varchar(256)
);
