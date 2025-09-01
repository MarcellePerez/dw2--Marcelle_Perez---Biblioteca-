from datetime import datetime
from models import Base, Livro
from database import engine, SessionLocal
import json

# Criar as tabelas
Base.metadata.create_all(bind=engine)

# Dados de exemplo para livros
livros = [
    {
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "ano": 1899,
        "genero": "Romance",
        "isbn": "9788535914660",
        "status": "disponível"
    },
    {
        "titulo": "O Pequeno Príncipe",
        "autor": "Antoine de Saint-Exupéry",
        "ano": 1943,
        "genero": "Literatura Infantil",
        "isbn": "9788574068398",
        "status": "disponível"
    },
    {
        "titulo": "1984",
        "autor": "George Orwell",
        "ano": 1949,
        "genero": "Ficção Científica",
        "isbn": "9788535914849",
        "status": "disponível"
    },
    # Adicionar mais 17 livros aqui...
]

def seed_database():
    db = SessionLocal()
    try:
        # Limpar dados existentes
        db.query(Livro).delete()
        
        # Inserir novos dados
        for livro_data in livros:
            livro = Livro(**livro_data)
            db.add(livro)
        
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
