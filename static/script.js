async function clicar(botao) {
    const response = await fetch('/clicar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ botao })
    });

    const data = await response.json();
    const resultado = document.getElementById('resultado');
    resultado.innerHTML = `
        Botão: <strong>${data.botao}</strong><br>
        Clique do dia: <strong>${data.sequencial}</strong><br>
        Data: <strong>${data.data}</strong><br>
        Hora: <strong>${data.hora}</strong>
    `;
}

// Alternar modo claro/escuro
document.getElementById('toggleMode').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
});
