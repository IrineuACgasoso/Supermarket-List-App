// ─────────────────────────────────────────
// AJAX — Lista de compras
// ─────────────────────────────────────────

export function adicionarItem(nomeProduto, botao) {
    const card       = botao.closest('.produto-card');
    const qtdInput   = card.querySelector('.qtd-input');
    const quantidade = parseInt(qtdInput.value) || 1;
    const form       = new FormData();
    form.append('produto', nomeProduto);
    form.append('quantidade', quantidade);

    fetch('/api/adicionar', { method: 'POST', body: form })
        .then(r => r.json())
        .then(lista => { renderizarLista(lista); qtdInput.value = 1; })
        .catch(err => console.error('Erro ao adicionar:', err));
}

export function removerItem(nome) {
    fetch('/api/remover/' + encodeURIComponent(nome))
        .then(r => r.json())
        .then(lista => renderizarLista(lista))
        .catch(err => console.error('Erro ao remover:', err));
}

export function renderizarLista(lista) {
    const container = document.getElementById('listaCompras');
    container.innerHTML = '';

    if (lista.length === 0) {
        container.innerHTML =
            '<p style="text-align:center;color:#888;font-style:italic;">A lista está vazia! 🎉</p>';
        return;
    }

    lista.forEach(item => {
        const div = document.createElement('div');
        div.className = 'item-lista';
        div.innerHTML = `
            <span><strong>${item.quantidade}x</strong> ${item.nome}</span>
            <button class="btn-remover"
                    onclick="window.removerItem('${item.nome.replace(/'/g, "\\'")}')">
                Remover
            </button>
        `;
        container.appendChild(div);
    });
}