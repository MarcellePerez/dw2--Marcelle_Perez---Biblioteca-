from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime
from pathlib import Path

app = FastAPI(title="Sistema de Biblioteca API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend via file:// ou http://localhost
    allow_credentials=False,  # não usamos cookies/credenciais
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = str((BASE_DIR / "biblioteca.db").resolve())

# Modelos Pydantic
class LivroBase(BaseModel):
    titulo: str
    autor: str
    ano: int
    genero: Optional[str] = None
    isbn: Optional[str] = None
    status: str = "disponível"
    data_emprestimo: Optional[str] = None
    # campo de capa removido da API

class Livro(LivroBase):
    id: int

# Funções de banco de dados
def get_db():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
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
    """)
    # tabela pode possuir coluna antiga 'capa_url'; ignoramos
    conn.commit()
    conn.close()

init_db()

# Rotas da API

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.get("/livros", response_model=List[Livro])
def listar_livros(search: Optional[str] = None, genero: Optional[str] = None, ano: Optional[int] = None, status: Optional[str] = None):
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT id, titulo, autor, ano, genero, isbn, status, data_emprestimo FROM livros WHERE 1=1"
    params = []
    if search:
        query += " AND (titulo LIKE ? OR autor LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    if genero:
        query += " AND genero = ?"
        params.append(genero)
    if ano:
        query += " AND ano = ?"
        params.append(ano)
    if status:
        query += " AND status = ?"
        params.append(status)
    cursor.execute(query, params)
    livros = [Livro(**dict(row)) for row in cursor.fetchall()]
    conn.close()
    return livros

@app.post("/livros", response_model=Livro)
def criar_livro(livro: LivroBase):
    if livro.ano < 1900 or livro.ano > datetime.now().year:
        raise HTTPException(status_code=422, detail="Ano inválido.")
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO livros (titulo, autor, ano, genero, isbn, status, data_emprestimo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (livro.titulo, livro.autor, livro.ano, livro.genero, livro.isbn, livro.status, livro.data_emprestimo))
        conn.commit()
        livro_id = cursor.lastrowid
        cursor.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
        novo_livro = Livro(**dict(cursor.fetchone()))
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Título já existe.")
    conn.close()
    return novo_livro

@app.put("/livros/{id}", response_model=Livro)
def atualizar_livro(id: int, livro: LivroBase):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    cursor.execute("""
        UPDATE livros SET titulo=?, autor=?, ano=?, genero=?, isbn=?, status=?, data_emprestimo=?
        WHERE id=?
    """, (livro.titulo, livro.autor, livro.ano, livro.genero, livro.isbn, livro.status, livro.data_emprestimo, id))
    conn.commit()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    livro_atualizado = Livro(**dict(cursor.fetchone()))
    conn.close()
    return livro_atualizado

@app.delete("/livros/{id}")
def deletar_livro(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"detail": "Livro excluído com sucesso."}

@app.post("/livros/{id}/emprestar", response_model=Livro)
def emprestar_livro(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    livro = cursor.fetchone()
    if not livro:
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    if livro["status"] == "emprestado":
        conn.close()
        raise HTTPException(status_code=400, detail="Livro já está emprestado.")
    data_emprestimo = datetime.utcnow().isoformat()
    cursor.execute("UPDATE livros SET status='emprestado', data_emprestimo=? WHERE id=?", (data_emprestimo, id))
    conn.commit()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    livro_atualizado = Livro(**dict(cursor.fetchone()))
    conn.close()
    return livro_atualizado

@app.post("/livros/{id}/devolver", response_model=Livro)
def devolver_livro(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    livro = cursor.fetchone()
    if not livro:
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    if livro["status"] == "disponível":
        conn.close()
        raise HTTPException(status_code=400, detail="Livro já está disponível.")
    cursor.execute("UPDATE livros SET status='disponível', data_emprestimo=NULL WHERE id=?", (id,))
    conn.commit()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    livro_atualizado = Livro(**dict(cursor.fetchone()))
    conn.close()
    return livro_atualizado