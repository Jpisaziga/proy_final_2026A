CREATE TABLE IF NOT EXISTS candidatos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS votos (
    codigo VARCHAR(50) PRIMARY KEY,
    candidato_id INT REFERENCES candidatos(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO candidatos (nombre) VALUES
    ('Candidato 01'),
    ('Candidato 02'),
    ('Candidato 03');