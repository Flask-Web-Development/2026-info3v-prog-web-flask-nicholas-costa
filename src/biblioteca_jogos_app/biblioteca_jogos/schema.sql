DROP TABLE IF EXISTS jogo;
DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE jogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    plataforma TEXT NOT NULL,
    genero TEXT NOT NULL,
    status TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
);