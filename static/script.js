async function clicar(botao) {
    const response = await fetch('/clicar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ botao })
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
}

// Alternar modo claro/escuro
document.getElementById('toggleMode').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
    
    const btn = document.getElementById('toggleMode');
    btn.textContent = document.body.classList.contains('dark-mode') ? 'Modo Claro' : 'Modo Escuro';
});
