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
    const btn = document.getElementById('toggleMode');
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
            localStorage.setItem('theme', novo === 'dark' ? 'dark' : 'light');
            btn.textContent = document.body.classList.contains('dark-mode') ? 'Modo Claro' : 'Modo Escuro';
        });
    }

    // fetch and apply stats
    fetchStats();
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
