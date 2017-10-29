CREATE TABLE scores(
    id SERIAL PRIMARY KEY,
    brew_id INT,
    score_type VARCHAR (50),
    value INT
);
