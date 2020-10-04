CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE,
    password VARCHAR NOT NULL,
    email VARCHAR NOT NULL
);

CREATE TABLE books (
isbn VARCHAR UNIQUE,
title VARCHAR NOT NULL,
author VARCHAR NOT NULL,
year INTEGER 
);
CREATE TABLE user_books (
	user_id INTEGER REFERENCES users(id),
	u_books VARCHAR REFERENCES books(isbn)
);
CREATE TABLE reviews (
	user_id INTEGER REFERENCES users(id),
	u_books VARCHAR REFERENCES books(isbn),
	comment VARCHAR

);