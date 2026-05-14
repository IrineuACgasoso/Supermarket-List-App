// ─────────────────────────────────────────
// Modais — abrir, fechar, Escape, checkboxes
// ─────────────────────────────────────────

export function abrirModal(id) {
    document.getElementById(id).classList.add('aberto');
}

export function fecharModal(id) {
    document.getElementById(id).classList.remove('aberto');
}

export function iniciarFecharModalEsc() {
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape')
            ['modalEdicao', 'modalNovaCategoria', 'modalEditarCategoria']
                .forEach(id => fecharModal(id));
    });
}

export function iniciarFecharModalClicandoFora() {
    ['modalEdicao', 'modalNovaCategoria', 'modalEditarCategoria'].forEach(id => {
        document.getElementById(id).addEventListener('click', function (e) {
            if (e.target === this) fecharModal(id);
        });
    });
}

export function preencherCheckboxProdutos(containerId, selecionados) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    const cartoes = Array.from(document.getElementsByClassName('produto-card'));
    cartoes.sort((a, b) =>
        a.querySelector('.nome-produto').innerText.localeCompare(
        b.querySelector('.nome-produto').innerText, 'pt-BR'));

    cartoes.forEach(card => {
        const pid     = card.id.replace('card-', '');
        const nome    = card.querySelector('.nome-produto').innerText;
        const imgSrc  = card.querySelector('img').src;
        const checked = selecionados.includes(pid) ? 'checked' : '';
        const label   = document.createElement('label');
        label.className = 'checkbox-produto';
        label.innerHTML = `
            <input type="checkbox" name="produtos_categoria" value="${pid}" ${checked}>
            <img src="${imgSrc}" alt="${nome}">
            <span>${nome}</span>
        `;
        container.appendChild(label);
    });
}