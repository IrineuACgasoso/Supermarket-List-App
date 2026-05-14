// ─────────────────────────────────────────
// Catálogo — filtro por texto e categoria
// ─────────────────────────────────────────

let categoriaAtiva = 0;

function normalizar(str) {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

export function filtrarProdutos() {
    const texto   = normalizar(document.getElementById('barraPesquisa').value);
    const cartoes = document.getElementsByClassName('produto-card');

    for (const c of cartoes) {
        const nome     = normalizar(c.querySelector('.nome-produto').innerText);
        const cats     = (c.dataset.categorias || '').split(',').filter(Boolean);
        const passaTxt = nome.includes(texto);
        const passaCat = categoriaAtiva === 0 || cats.includes(String(categoriaAtiva));
        c.style.display = (passaTxt && passaCat) ? '' : 'none';
    }
}

export function filtrarCategoria(catId, botao) {
    categoriaAtiva = catId;
    document.querySelectorAll('.tab-cat').forEach(t => t.classList.remove('active'));
    if (botao) botao.classList.add('active');
    filtrarProdutos();
}

export function ordenarCatalogo() {
    const catalogo = document.getElementById('catalogoProdutos');
    const cartoes  = Array.from(catalogo.getElementsByClassName('produto-card'));
    cartoes.sort((a, b) =>
        a.querySelector('.nome-produto').innerText.localeCompare(
        b.querySelector('.nome-produto').innerText, 'pt-BR'));
    cartoes.forEach(c => catalogo.appendChild(c));
}