from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(90), nullable=False)
    autor = Column(String(90), nullable=False)
    ano = Column(Integer, nullable=False)
    genero = Column(String(50))
    isbn = Column(String(13), unique=True)
    status = Column(Enum('disponível', 'emprestado', name='status_enum'), nullable=False)
    data_emprestimo = Column(Date)
