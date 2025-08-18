from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3
import os

# Criação do aplicativo FastAPI
app = FastAPI(title="Sistema de Biblioteca API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class LivroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str

class Livro(LivroBase):
    id: int

class UsuarioBase(BaseModel):
    nome: str
    email: str

class Usuario(UsuarioBase):
    id: int

class EmprestimoBase(BaseModel):
    livro_id: int
    usuario_id: int

class Emprestimo(EmprestimoBase):
    id: int
    data_emprestimo: datetime
    devolvido: bool = False

# Configuração do banco de dados
DATABASE_FILE = "biblioteca.db"

def init_db():
    if not os.path.exists(DATABASE_FILE):
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        
        # Criar tabelas
        c.execute('''
            CREATE TABLE livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE
            )
        ''')
        
        c.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        
        c.execute('''
            CREATE TABLE emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_id INTEGER,
                usuario_id INTEGER,
                data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                devolvido BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (livro_id) REFERENCES livros (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conn.commit()
        conn.close()

# Inicializar o banco de dados
init_db()

# Rotas da API
@app.get("/api/livros", response_model=List[Livro])
async def get_livros():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM livros")
    livros = [{"id": row[0], "titulo": row[1], "autor": row[2], "isbn": row[3]} 
              for row in c.fetchall()]
    conn.close()
    return livros

@app.post("/api/livros", response_model=Livro)
async def create_livro(livro: LivroBase):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO livros (titulo, autor, isbn) VALUES (?, ?, ?)",
            (livro.titulo, livro.autor, livro.isbn)
        )
        livro_id = c.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="ISBN já existe")
    conn.close()
    return {**livro.dict(), "id": livro_id}

@app.delete("/api/livros/{livro_id}")
async def delete_livro(livro_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    conn.commit()
    conn.close()
    return {"detail": "Livro excluído com sucesso"}

@app.get("/api/usuarios", response_model=List[Usuario])
async def get_usuarios():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios")
    usuarios = [{"id": row[0], "nome": row[1], "email": row[2]} 
                for row in c.fetchall()]
    conn.close()
    return usuarios

@app.post("/api/usuarios", response_model=Usuario)
async def create_usuario(usuario: UsuarioBase):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
            (usuario.nome, usuario.email)
        )
        usuario_id = c.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email já existe")
    conn.close()
    return {**usuario.dict(), "id": usuario_id}

@app.delete("/api/usuarios/{usuario_id}")
async def delete_usuario(usuario_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    conn.commit()
    conn.close()
    return {"detail": "Usuário excluído com sucesso"}

@app.get("/api/emprestimos", response_model=List[dict])
async def get_emprestimos():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT e.*, l.titulo, l.autor, u.nome, u.email
        FROM emprestimos e
        JOIN livros l ON e.livro_id = l.id
        JOIN usuarios u ON e.usuario_id = u.id
        WHERE e.devolvido = 0
    """)
    emprestimos = []
    for row in c.fetchall():
        emprestimo = {
            "id": row[0],
            "livro_id": row[1],
            "usuario_id": row[2],
            "data_emprestimo": row[3],
            "devolvido": bool(row[4]),
            "livro": {"titulo": row[5], "autor": row[6]},
            "usuario": {"nome": row[7], "email": row[8]}
        }
        emprestimos.append(emprestimo)
    conn.close()
    return emprestimos

@app.post("/api/emprestimos", response_model=dict)
async def create_emprestimo(emprestimo: EmprestimoBase):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    # Verificar se o livro está disponível
    c.execute("""
        SELECT COUNT(*) FROM emprestimos 
        WHERE livro_id = ? AND devolvido = 0
    """, (emprestimo.livro_id,))
    
    if c.fetchone()[0] > 0:
        conn.close()
        raise HTTPException(status_code=400, detail="Livro já está emprestado")
    
    try:
        c.execute(
            "INSERT INTO emprestimos (livro_id, usuario_id) VALUES (?, ?)",
            (emprestimo.livro_id, emprestimo.usuario_id)
        )
        emprestimo_id = c.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Erro ao criar empréstimo")
    
    conn.close()
    return {**emprestimo.dict(), "id": emprestimo_id}

@app.put("/api/emprestimos/{emprestimo_id}")
async def update_emprestimo(emprestimo_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(
        "UPDATE emprestimos SET devolvido = 1 WHERE id = ?",
        (emprestimo_id,)
    )
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    conn.commit()
    conn.close()
    return {"detail": "Empréstimo atualizado com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
