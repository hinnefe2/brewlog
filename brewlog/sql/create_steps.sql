CREATE TABLE steps(
    id SERIAL PRIMARY KEY,
    brew_id INT,
    step_type VARCHAR (50),
    value VARCHAR (10)
);
