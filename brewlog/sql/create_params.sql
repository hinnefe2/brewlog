CREATE TABLE params(
    id SERIAL PRIMARY KEY,
    brew_id INT,
    param_type VARCHAR (50),
    value VARCHAR (100)
);
