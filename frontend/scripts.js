// Funções utilitárias
function showModal(id) {
    document.getElementById(id).classList.remove('hidden');
    document.getElementById(id).focus();
}
function hideModal(id) {
    document.getElementById(id).classList.add('hidden');
}

// Estado global
const API_BASE = 'http://localhost:8000';
let livros = [];
let paginaAtual = 1;
const livrosPorPagina = 10;
let ordenacao = localStorage.getItem('ordenacao') || 'titulo';

// Fetch inicial
window.onload = () => {
    carregarLivros();
    document.getElementById('novoLivroBtn').addEventListener('click', () => showModal('modalNovoLivro'));
    document.getElementById('fecharModalNovoLivro').addEventListener('click', () => hideModal('modalNovoLivro'));
    document.getElementById('fecharModalEmprestimo').addEventListener('click', () => hideModal('modalEmprestimo'));
    document.getElementById('novoLivroForm').addEventListener('submit', salvarLivro);
    document.getElementById('filterForm').addEventListener('change', filtrarLivros);
    document.getElementById('searchInput').addEventListener('input', filtrarLivros);
    document.getElementById('clearFilters').addEventListener('click', limparFiltros);
    document.getElementById('exportCSV').addEventListener('click', exportarCSV);
    document.getElementById('exportJSON').addEventListener('click', exportarJSON);
    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key.toLowerCase() === 'n') showModal('modalNovoLivro');
    });
};

function carregarLivros() {
    fetch(`${API_BASE}/livros`)
        .then(res => res.json())
        .then(data => {
            livros = data;
            renderizarLivros();
        });
}

function renderizarLivros() {
    let lista = document.getElementById('livrosList');
    lista.innerHTML = '';
    let filtrados = aplicarFiltros(livros);
    filtrados = aplicarOrdenacao(filtrados);
    let paginados = filtrados.slice((paginaAtual - 1) * livrosPorPagina, paginaAtual * livrosPorPagina);

    paginados.forEach(livro => {
        let card = document.createElement('div');
        card.className = 'livro-card section';
        card.innerHTML = `
            <h3>${livro.titulo}</h3>
            <p><strong>Autor:</strong> ${livro.autor}</p>
            <p><strong>Ano:</strong> ${livro.ano}</p>
            <p><strong>Gênero:</strong> ${livro.genero || '-'}</p>
            <p><strong>Status:</strong> ${livro.status}</p>
            <button onclick="abrirEmprestimo(${livro.id})" ${livro.status === 'emprestado' ? 'disabled' : ''}>Emprestar</button>
            <button onclick="abrirDevolucao(${livro.id})" ${livro.status === 'disponível' ? 'disabled' : ''}>Devolver</button>
            <button onclick="editarLivro(${livro.id})">Editar</button>
            <button onclick="deletarLivro(${livro.id})">Excluir</button>
        `;
        lista.appendChild(card);
    });
    renderizarPaginacao(filtrados.length);
}

function renderizarPaginacao(total) {
    let pagDiv = document.getElementById('pagination');
    pagDiv.innerHTML = '';
    let totalPaginas = Math.ceil(total / livrosPorPagina);
    for (let i = 1; i <= totalPaginas; i++) {
        let btn = document.createElement('button');
        btn.textContent = i;
        btn.disabled = i === paginaAtual;
        btn.onclick = () => {
            paginaAtual = i;
            renderizarLivros();
        };
        pagDiv.appendChild(btn);
    }
}

function aplicarFiltros(arr) {
    let genero = document.getElementById('genero').value;
    let ano = document.getElementById('ano').value;
    let status = document.getElementById('status').value;
    let busca = document.getElementById('searchInput').value.toLowerCase();

    return arr.filter(livro => {
        let ok = true;
        if (genero && livro.genero !== genero) ok = false;
        if (ano && livro.ano != ano) ok = false;
        if (status && livro.status !== status) ok = false;
        if (busca && !(livro.titulo.toLowerCase().includes(busca) || livro.autor.toLowerCase().includes(busca))) ok = false;
        return ok;
    });
}

function aplicarOrdenacao(arr) {
    if (ordenacao === 'titulo') {
        return arr.sort((a, b) => a.titulo.localeCompare(b.titulo));
    } else if (ordenacao === 'ano') {
        return arr.sort((a, b) => a.ano - b.ano);
    }
    return arr;
}

function filtrarLivros() {
    paginaAtual = 1;
    renderizarLivros();
}

function limparFiltros() {
    document.getElementById('genero').value = '';
    document.getElementById('ano').value = '';
    document.getElementById('status').value = '';
    document.getElementById('searchInput').value = '';
    filtrarLivros();
}

function salvarLivro(e) {
    e.preventDefault();
    let form = e.target;
    let livro = {
        titulo: form.titulo.value.trim(),
        autor: form.autor.value.trim(),
        ano: parseInt(form.anoLivro.value),
        genero: form.generoLivro.value,
        isbn: form.isbn.value,
    status: form.statusLivro.value
    };
    if (livro.titulo.length < 3 || livro.titulo.length > 90) {
        alert('Título deve ter entre 3 e 90 caracteres.');
        return;
    }
    if (livros.some(l => l.titulo.toLowerCase() === livro.titulo.toLowerCase())) {
        alert('Já existe um livro com esse título.');
        return;
    }
    fetch(`${API_BASE}/livros`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(livro)
    })
    .then(res => {
        if (!res.ok) throw new Error('Erro ao salvar livro');
        return res.json();
    })
    .then(() => {
        hideModal('modalNovoLivro');
        carregarLivros();
    })
    .catch(() => alert('Erro ao salvar livro.'));
}

function editarLivro(id) {
    let livro = livros.find(l => l.id === id);
    if (!livro) return;
    showModal('modalNovoLivro');
    let form = document.getElementById('novoLivroForm');
    form.titulo.value = livro.titulo;
    form.autor.value = livro.autor;
    form.anoLivro.value = livro.ano;
    form.generoLivro.value = livro.genero;
    form.isbn.value = livro.isbn;
    form.statusLivro.value = livro.status;
    form.onsubmit = function(e) {
        e.preventDefault();
        livro.titulo = form.titulo.value.trim();
        livro.autor = form.autor.value.trim();
        livro.ano = parseInt(form.anoLivro.value);
        livro.genero = form.generoLivro.value;
        livro.isbn = form.isbn.value;
        livro.status = form.statusLivro.value;
    fetch(`${API_BASE}/livros/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(livro)
        })
        .then(res => {
            if (!res.ok) throw new Error('Erro ao editar livro');
            return res.json();
        })
        .then(() => {
            hideModal('modalNovoLivro');
            carregarLivros();
            form.onsubmit = salvarLivro;
        })
        .catch(() => alert('Erro ao editar livro.'));
    };
}

function deletarLivro(id) {
    if (!confirm('Deseja realmente excluir este livro?')) return;
    fetch(`${API_BASE}/livros/${id}`, { method: 'DELETE' })
        .then(res => {
            if (!res.ok) throw new Error('Erro ao excluir livro');
            carregarLivros();
        })
        .catch(() => alert('Erro ao excluir livro.'));
}

function abrirEmprestimo(id) {
    let livro = livros.find(l => l.id === id);
    if (!livro || livro.status === 'emprestado') return;
    showModal('modalEmprestimo');
    document.getElementById('livroIdEmprestimo').value = id;
    document.getElementById('emprestimoInfo').innerHTML = `
        <p><strong>${livro.titulo}</strong> por ${livro.autor}</p>
        <p>Status atual: ${livro.status}</p>
    `;
    document.getElementById('confirmarEmprestimoBtn').onclick = function(e) {
        e.preventDefault();
    fetch(`${API_BASE}/livros/${id}/emprestar`, { method: 'POST' })
            .then(res => {
                if (!res.ok) throw new Error('Erro ao emprestar');
                hideModal('modalEmprestimo');
                carregarLivros();
            })
            .catch(() => alert('Erro ao emprestar livro.'));
    };
}

function abrirDevolucao(id) {
    let livro = livros.find(l => l.id === id);
    if (!livro || livro.status === 'disponível') return;
    showModal('modalEmprestimo');
    document.getElementById('livroIdEmprestimo').value = id;
    document.getElementById('emprestimoInfo').innerHTML = `
        <p><strong>${livro.titulo}</strong> por ${livro.autor}</p>
        <p>Status atual: ${livro.status}</p>
    `;
    document.getElementById('confirmarEmprestimoBtn').onclick = function(e) {
        e.preventDefault();
    fetch(`${API_BASE}/livros/${id}/devolver`, { method: 'POST' })
            .then(res => {
                if (!res.ok) throw new Error('Erro ao devolver');
                hideModal('modalEmprestimo');
                carregarLivros();
            })
            .catch(() => alert('Erro ao devolver livro.'));
    };
}

// Exportação CSV/JSON
function exportarCSV() {
    let filtrados = aplicarFiltros(livros);
    let csv = 'Título,Autor,Ano,Gênero,Status\n' +
        filtrados.map(l => `"${l.titulo}","${l.autor}",${l.ano},"${l.genero}","${l.status}"`).join('\n');
    baixarArquivo('livros.csv', csv);
}

function exportarJSON() {
    let filtrados = aplicarFiltros(livros);
    baixarArquivo('livros.json', JSON.stringify(filtrados, null, 2));
}

function baixarArquivo(nome, conteudo) {
    let blob = new Blob([conteudo], { type: 'text/plain' });
    let a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = nome;
    a.click();
}

// Ordenação persistida
document.addEventListener('DOMContentLoaded', () => {
    let selectOrdenacao = document.createElement('select');
    selectOrdenacao.innerHTML = `
        <option value="titulo">Título</option>
        <option value="ano">Ano</option>
    `;
    selectOrdenacao.value = ordenacao;
    selectOrdenacao.onchange = function() {
        ordenacao = this.value;
        localStorage.setItem('ordenacao', ordenacao);
        renderizarLivros();
    };
    document.querySelector('.section > div').appendChild(selectOrdenacao);
});