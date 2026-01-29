async function clicar(botao) {
    // Expecting id and name parameters now; if caller passed only name, keep compatibility
    let botaoNome = botao;
    let botaoId = null;
    if (arguments.length === 2) {
        botaoId = arguments[0];
        botaoNome = arguments[1];
    }

    const btn = botaoId ? document.querySelector(`button[data-id="${botaoId}"]`) : null;
    if (btn) btn.disabled = true;

    try {
        const response = await fetch('/clicar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ botao: botaoNome })
        });
        const data = await response.json();
        const resultado = document.getElementById('resultado');

        // Add animation class
        resultado.classList.remove('fade-in');
        void resultado.offsetWidth; // trigger reflow
        resultado.classList.add('fade-in');

        resultado.innerHTML = `
            <div class="result-card">
                <div class="result-item"><span>Botão:</span> <strong>${data.botao}</strong></div>
                <div class="result-item"><span>Clique do dia:</span> <strong>${data.sequencial}</strong></div>
                <div class="result-item"><span>Data:</span> <strong>${data.data}</strong></div>
                <div class="result-item"><span>Hora:</span> <strong>${data.hora}</strong></div>
            </div>
        `;

        // Atualiza área de contadores (abaixo dos botões)
        const counts = document.getElementById('counts');
        if (counts) {
            counts.innerHTML = `Registro adicionado: <strong>${data.botao}</strong> — Clique do dia: <strong>${data.sequencial}</strong>`;
        }
        // atualizar contagens detalhadas
        fetchStats();
    } catch (err) {
        alert('Erro ao registrar clique. Tente novamente.');
        console.error(err);
    } finally {
        if (btn) setTimeout(() => btn.disabled = false, 500);
    }
}

// Alternar modo claro/escuro
// Alternar modo claro/escuro com persistência
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('themeToggle') || document.getElementById('toggleMode');
    const saved = localStorage.getItem('theme');
    if (saved === 'light') {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
    }
    if (btn) {
        btn.textContent = document.body.classList.contains('dark-mode') ? 'Modo Claro' : 'Modo Escuro';
        btn.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            document.body.classList.toggle('light-mode');
            const novo = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
            localStorage.setItem('theme', novo);
            btn.textContent = document.body.classList.contains('dark-mode') ? 'Modo Claro' : 'Modo Escuro';
        });
    }

    // fetch and apply stats
    fetchStats();
    // attach scroll buttons if present
    const toTop = document.getElementById('toTopBtn');
    const toBottom = document.getElementById('toBottomBtn');
    if (toTop) toTop.addEventListener('click', scrollToTop);
    if (toBottom) toBottom.addEventListener('click', scrollToBottom);
    // Admin: bind add/update/delete buttons if present
    const addBtn = document.getElementById('add-button');
    if (addBtn) addBtn.addEventListener('click', addButton);
    document.querySelectorAll('.btn-update').forEach(b => b.addEventListener('click', () => updateButton(b.dataset.id)));
    document.querySelectorAll('.btn-delete').forEach(b => b.addEventListener('click', () => deleteButton(b.dataset.id)));
});

async function fetchStats() {
    try {
        const res = await fetch('/stats');
        const dados = await res.json();
        const counts = document.getElementById('counts');
        if (counts) {
            // construir lista simples de contadores por botão
            counts.innerHTML = dados.map(b => `
                <div class="count-item"><strong>${b.nome}</strong>: Hoje ${b.hoje} — Total ${b.total}</div>
            `).join('');
        }
        dados.forEach(b => {
            const btn = document.querySelector(`button[data-id="${b.id}"]`);
            if (btn) btn.title = `${b.nome} — Hoje: ${b.hoje} / Total: ${b.total}`;
        });
    } catch (e) {
        console.error('Falha ao buscar estatísticas', e);
    }
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToBottom() {
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
}

// Admin: funções para adicionar/atualizar/remover botões
async function updateButton(id) {
    try {
        const nome = document.getElementById(`name-${id}`).value;
        if (!nome || !nome.trim()) return alert('Informe um nome válido');
        const res = await fetch('/admin/update_button', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ id: id, nome: nome })
        });
        if (res.ok) {
            alert('Nome do botão atualizado!');
            location.reload();
        } else {
            const txt = await res.text();
            console.error('updateButton error', txt);
            alert('Falha ao atualizar o botão');
        }
    } catch (e) {
        console.error(e);
        alert('Erro ao atualizar botão');
    }
}

async function addButton() {
    try {
        const el = document.getElementById('new-button-name');
        if (!el) return alert('Campo de nome não encontrado');
        const nome = el.value.trim();
        if (!nome) return alert('Informe um nome válido');
        const res = await fetch('/admin/add_button', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ nome: nome })
        });
        if (res.ok) {
            alert('Botão adicionado');
            location.reload();
        } else {
            console.error('addButton failed', await res.text());
            alert('Falha ao adicionar botão');
        }
    } catch (e) {
        console.error(e);
        alert('Erro ao adicionar botão');
    }
}

async function deleteButton(id) {
    try {
        if (!confirm('Remover este botão?')) return;
        const res = await fetch('/admin/delete_button', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ id: id })
        });
        if (res.ok) {
            alert('Botão removido');
            location.reload();
        } else {
            console.error('deleteButton failed', await res.text());
            alert('Falha ao remover botão');
        }
    } catch (e) {
        console.error(e);
        alert('Erro ao remover botão');
    }
}
