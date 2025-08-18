# Sistema de Biblioteca - Relatório Técnico

## Descrição do Projeto
Este projeto é um sistema de gerenciamento de biblioteca que permite o controle de livros, usuários e empréstimos. O sistema foi desenvolvido utilizando uma arquitetura cliente-servidor, com frontend em HTML, CSS e JavaScript puro, e backend em Python com FastAPI.

## Tecnologias Utilizadas

### Frontend
- HTML5
- CSS3 (Flexbox e Grid para layouts responsivos)
- JavaScript ES6+ (sem frameworks)

### Backend
- Python 3.8+
- FastAPI (framework web)
- SQLite (banco de dados)
- Pydantic (validação de dados)
- CORS middleware (para permitir requisições do frontend)

## Estrutura do Projeto
```
biblioteca/
├── backend/
│   └── main.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
└── index.html
```

## Funcionalidades

### 1. Gerenciamento de Livros
- Adicionar novo livro (título, autor, ISBN)
- Listar todos os livros
- Excluir livro

### 2. Gerenciamento de Usuários
- Cadastrar novo usuário (nome, email)
- Listar todos os usuários
- Excluir usuário

### 3. Gerenciamento de Empréstimos
- Registrar empréstimo de livro
- Listar empréstimos ativos
- Registrar devolução

## API Endpoints

### Livros
- GET /api/livros - Lista todos os livros
- POST /api/livros - Adiciona um novo livro
- DELETE /api/livros/{id} - Remove um livro

### Usuários
- GET /api/usuarios - Lista todos os usuários
- POST /api/usuarios - Adiciona um novo usuário
- DELETE /api/usuarios/{id} - Remove um usuário

### Empréstimos
- GET /api/emprestimos - Lista todos os empréstimos ativos
- POST /api/emprestimos - Registra um novo empréstimo
- PUT /api/emprestimos/{id} - Atualiza um empréstimo (devolução)

## Interface do Usuário
A interface foi desenvolvida com foco na usabilidade e responsividade, utilizando:
- Layout responsivo com Flexbox e Grid
- Navegação por abas
- Formulários intuitivos
- Feedback visual das ações
- Design minimalista e funcional

## Banco de Dados
O sistema utiliza SQLite como banco de dados, com as seguintes tabelas:
- livros (id, titulo, autor, isbn)
- usuarios (id, nome, email)
- emprestimos (id, livro_id, usuario_id, data_emprestimo, devolvido)

## Como Executar o Projeto

1. Instalar as dependências do Python:
```bash
pip install fastapi uvicorn
```

2. Iniciar o servidor backend:
```bash
cd backend
python main.py
```

3. Abrir o arquivo index.html em um navegador web ou usar um servidor local.

## Segurança e Validações
- Validação de dados no frontend e backend
- Verificação de disponibilidade de livros
- Prevenção de duplicatas de ISBN e email
- Proteção contra SQL injection usando parametrização

## Melhorias Futuras
- Implementação de autenticação de usuários
- Sistema de reserva de livros
- Histórico de empréstimos
- Notificações de atraso
- Busca e filtros avançados
- Relatórios e estatísticas

## Conclusão
O sistema atende aos requisitos básicos de um sistema de biblioteca, oferecendo uma interface intuitiva e funcionalidades essenciais para o gerenciamento de livros, usuários e empréstimos.
