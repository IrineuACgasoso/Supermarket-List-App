// ─────────────────────────────────────────
// main.js — inicialização geral do app
// ─────────────────────────────────────────
import { adicionarItem, removerItem }               from './lista.js';
import { filtrarProdutos, filtrarCategoria,
         ordenarCatalogo }                           from './catalogo.js';
import { configurarDropzone, iniciarColarImagem }   from './dropzone.js';
import { iniciarFecharModalEsc,
         iniciarFecharModalClicandoFora,
         fecharModal }                               from './modais.js';
import { abrirModalEdicao, salvarEdicaoProduto,
         abrirModalNovaCategoria,
         abrirModalEditarCategoria,
         toggleMenuCategoria, fecharMenusCategoria,
         confirmarRemocao }                          from './produtos.js';

// ── Expõe funções usadas inline no HTML ──────────────────────────────────────
// (necessário porque o HTML usa onclick="adicionarItem(...)" etc.)
window.adicionarItem           = adicionarItem;
window.removerItem             = removerItem;
window.filtrarProdutos         = filtrarProdutos;
window.filtrarCategoria        = filtrarCategoria;
window.abrirModalEdicao        = abrirModalEdicao;
window.salvarEdicaoProduto     = salvarEdicaoProduto;
window.abrirModalNovaCategoria = abrirModalNovaCategoria;
window.abrirModalEditarCategoria = abrirModalEditarCategoria;
window.toggleMenuCategoria     = toggleMenuCategoria;
window.fecharMenusCategoria    = fecharMenusCategoria;
window.fecharModal             = fecharModal;
window.confirmarRemocao        = confirmarRemocao;

// ── Salvar posição do scroll entre reloads ───────────────────────────────────
window.salvarScroll = function () {
    sessionStorage.setItem('scrollY', window.scrollY);
};

// ── Inicialização ─────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
    // Restaura scroll
    const y = sessionStorage.getItem('scrollY');
    if (y !== null) { window.scrollTo(0, parseInt(y)); sessionStorage.removeItem('scrollY'); }

    ordenarCatalogo();

    configurarDropzone('dropzone-novo', 'imagem_produto_novo', 'dropzone-texto-novo', 'preview-imagem-novo');
    configurarDropzone('dropzone-edit', 'imagem_produto_edit', 'dropzone-texto-edit', 'preview-imagem-edit');
    iniciarColarImagem();

    iniciarFecharModalEsc();
    iniciarFecharModalClicandoFora();

    // Botão salvar edição
    document.getElementById('btnSalvarEdicao')
            .addEventListener('click', salvarEdicaoProduto);

    // Enter no input de nome do modal de edição
    document.getElementById('modalNomeInput')
            .addEventListener('keypress', e => {
                if (e.key === 'Enter') { e.preventDefault(); salvarEdicaoProduto(); }
            });

    // Fecha menus de categoria ao clicar fora
    document.addEventListener('click', e => {
        if (!e.target.closest('.cat-menu-wrapper')) fecharMenusCategoria();
    });
});