"""
Seed de dados para a API usando o mesmo SQLite do app (sqlite3).
Cria a tabela se não existir e insere ~20 livros plausíveis.
"""

import sqlite3
from datetime import datetime

DATABASE_FILE = "biblioteca.db"

LIVROS = [
    {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "genero": "Romance", "isbn": "9788535914660", "status": "disponível"},
    {"titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "ano": 1943, "genero": "Infantil", "isbn": "9788574068398", "status": "disponível"},
    {"titulo": "1984", "autor": "George Orwell", "ano": 1949, "genero": "Ficção", "isbn": "9788535914849", "status": "disponível"},
    {"titulo": "Capitães da Areia", "autor": "Jorge Amado", "ano": 1937, "genero": "Romance", "isbn": "9788520932109", "status": "disponível"},
    {"titulo": "O Alquimista", "autor": "Paulo Coelho", "ano": 1988, "genero": "Ficção", "isbn": "9788576653721", "status": "disponível"},
    {"titulo": "Harry Potter e a Pedra Filosofal", "autor": "J.K. Rowling", "ano": 1997, "genero": "Fantasia", "isbn": "9788532511010", "status": "disponível"},
    {"titulo": "O Senhor dos Anéis: A Sociedade do Anel", "autor": "J.R.R. Tolkien", "ano": 1954, "genero": "Fantasia", "isbn": "9788595084737", "status": "disponível"},
    {"titulo": "O Hobbit", "autor": "J.R.R. Tolkien", "ano": 1937, "genero": "Fantasia", "isbn": "9788595084751", "status": "disponível"},
    {"titulo": "A Menina que Roubava Livros", "autor": "Markus Zusak", "ano": 2005, "genero": "Drama", "isbn": "9788598078177", "status": "disponível"},
    {"titulo": "A Culpa é das Estrelas", "autor": "John Green", "ano": 2012, "genero": "Romance", "isbn": "9788580572261", "status": "disponível"},
    {"titulo": "O Código Da Vinci", "autor": "Dan Brown", "ano": 2003, "genero": "Suspense", "isbn": "9788580411164", "status": "disponível"},
    {"titulo": "Moby Dick", "autor": "Herman Melville", "ano": 1851, "genero": "Aventura", "isbn": "9788581050041", "status": "disponível"},
    {"titulo": "Orgulho e Preconceito", "autor": "Jane Austen", "ano": 1813, "genero": "Romance", "isbn": "9788520935933", "status": "disponível"},
    {"titulo": "Drácula", "autor": "Bram Stoker", "ano": 1897, "genero": "Terror", "isbn": "9788576572008", "status": "disponível"},
    {"titulo": "Frankenstein", "autor": "Mary Shelley", "ano": 1818, "genero": "Terror", "isbn": "9788520931805", "status": "disponível"},
    {"titulo": "O Morro dos Ventos Uivantes", "autor": "Emily Brontë", "ano": 1847, "genero": "Romance", "isbn": "9788520932949", "status": "disponível"},
    {"titulo": "It: A Coisa", "autor": "Stephen King", "ano": 1986, "genero": "Terror", "isbn": "9788532512062", "status": "disponível"},
    {"titulo": "O Apanhador no Campo de Centeio", "autor": "J. D. Salinger", "ano": 1951, "genero": "Ficção", "isbn": "9780316769488", "status": "disponível"},
    {"titulo": "Memórias Póstumas de Brás Cubas", "autor": "Machado de Assis", "ano": 1881, "genero": "Romance", "isbn": "9788520932789", "status": "disponível"},
    {"titulo": "Vidas Secas", "autor": "Graciliano Ramos", "ano": 1938, "genero": "Romance", "isbn": "9788520933069", "status": "disponível"},
]

def init_table():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL UNIQUE,
            autor TEXT NOT NULL,
            ano INTEGER NOT NULL,
            genero TEXT,
            isbn TEXT,
            status TEXT NOT NULL DEFAULT 'disponível',
            data_emprestimo TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def seed():
    init_table()
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    # Limpa tabela para idempotência do seed
    c.execute("DELETE FROM livros")
    for l in LIVROS:
        c.execute(
            """
            INSERT OR IGNORE INTO livros (titulo, autor, ano, genero, isbn, status, data_emprestimo)
            VALUES (?, ?, ?, ?, ?, ?, NULL)
            """,
            (l["titulo"], l["autor"], l["ano"], l.get("genero"), l.get("isbn"), l.get("status", "disponível")),
        )
    conn.commit()
    conn.close()
    print("Seed concluído com sucesso (20 livros).")

if __name__ == "__main__":
    seed()
