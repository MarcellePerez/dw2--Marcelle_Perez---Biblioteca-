// Seleção de elementos do DOM
const sections = {
    livros: document.getElementById('livrosSection'),
    usuarios: document.getElementById('usuariosSection'),
    emprestimos: document.getElementById('emprestimosSection')
};

const forms = {
    livro: document.getElementById('livroForm'),
    usuario: document.getElementById('usuarioForm'),
    emprestimo: document.getElementById('emprestimoForm')
};

const lists = {
    livros: document.getElementById('livrosList'),
    usuarios: document.getElementById('usuariosList'),
    emprestimos: document.getElementById('emprestimosList')
};

// Funções de navegação
document.getElementById('livrosLink').addEventListener('click', () => showSection('livros'));
document.getElementById('usuariosLink').addEventListener('click', () => showSection('usuarios'));
document.getElementById('emprestimosLink').addEventListener('click', () => showSection('emprestimos'));

function showSection(sectionName) {
    Object.keys(sections).forEach(key => {
        sections[key].classList.add('hidden');
    });
    sections[sectionName].classList.remove('hidden');
}

// Funções para interação com a API
async function fetchAPI(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`http://localhost:8000/api/${endpoint}`, options);
        if (!response.ok) throw new Error('Erro na requisição');
        return await response.json();
    } catch (error) {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao processar sua requisição');
    }
}

// Gerenciamento de Livros
forms.livro.addEventListener('submit', async (e) => {
    e.preventDefault();
    const livro = {
        titulo: document.getElementById('titulo').value,
        autor: document.getElementById('autor').value,
        isbn: document.getElementById('isbn').value
    };
    
    await fetchAPI('livros', 'POST', livro);
    forms.livro.reset();
    await loadLivros();
});

async function loadLivros() {
    const livros = await fetchAPI('livros');
    lists.livros.innerHTML = '';
    
    livros.forEach(livro => {
        const div = document.createElement('div');
        div.className = 'item';
        div.innerHTML = `
            <h3>${livro.titulo}</h3>
            <p>Autor: ${livro.autor}</p>
            <p>ISBN: ${livro.isbn}</p>
            <button onclick="deleteLivro(${livro.id})">Excluir</button>
        `;
        lists.livros.appendChild(div);
    });
}

async function deleteLivro(id) {
    await fetchAPI(`livros/${id}`, 'DELETE');
    await loadLivros();
}

// Gerenciamento de Usuários
forms.usuario.addEventListener('submit', async (e) => {
    e.preventDefault();
    const usuario = {
        nome: document.getElementById('nome').value,
        email: document.getElementById('email').value
    };
    
    await fetchAPI('usuarios', 'POST', usuario);
    forms.usuario.reset();
    await loadUsuarios();
});

async function loadUsuarios() {
    const usuarios = await fetchAPI('usuarios');
    lists.usuarios.innerHTML = '';
    
    usuarios.forEach(usuario => {
        const div = document.createElement('div');
        div.className = 'item';
        div.innerHTML = `
            <h3>${usuario.nome}</h3>
            <p>Email: ${usuario.email}</p>
            <button onclick="deleteUsuario(${usuario.id})">Excluir</button>
        `;
        lists.usuarios.appendChild(div);
    });
}

async function deleteUsuario(id) {
    await fetchAPI(`usuarios/${id}`, 'DELETE');
    await loadUsuarios();
}

// Gerenciamento de Empréstimos
forms.emprestimo.addEventListener('submit', async (e) => {
    e.preventDefault();
    const emprestimo = {
        livro_id: document.getElementById('livroSelect').value,
        usuario_id: document.getElementById('usuarioSelect').value
    };
    
    await fetchAPI('emprestimos', 'POST', emprestimo);
    forms.emprestimo.reset();
    await loadEmprestimos();
});

async function loadEmprestimos() {
    const emprestimos = await fetchAPI('emprestimos');
    lists.emprestimos.innerHTML = '';
    
    emprestimos.forEach(emprestimo => {
        const div = document.createElement('div');
        div.className = 'item';
        div.innerHTML = `
            <h3>Empréstimo #${emprestimo.id}</h3>
            <p>Livro: ${emprestimo.livro.titulo}</p>
            <p>Usuário: ${emprestimo.usuario.nome}</p>
            <p>Data: ${new Date(emprestimo.data_emprestimo).toLocaleDateString()}</p>
            <button onclick="finalizarEmprestimo(${emprestimo.id})">Devolver</button>
        `;
        lists.emprestimos.appendChild(div);
    });
}

async function finalizarEmprestimo(id) {
    await fetchAPI(`emprestimos/${id}`, 'PUT', { devolvido: true });
    await loadEmprestimos();
}

// Inicialização
async function init() {
    await Promise.all([
        loadLivros(),
        loadUsuarios(),
        loadEmprestimos()
    ]);
}

init();
