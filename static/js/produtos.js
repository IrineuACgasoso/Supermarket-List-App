// ─────────────────────────────────────────
// Produtos — editar via AJAX + menu categorias
// ─────────────────────────────────────────
import { abrirModal, fecharModal, preencherCheckboxProdutos } from './modais.js';

let _produtoIdEditando = null;

// ── Editar produto (sem reload) ───────────────────────────────────────────────

export function abrirModalEdicao(btn) {
    _produtoIdEditando = btn.dataset.id;

    document.getElementById('modalNomeInput').value = btn.dataset.nome;
    document.getElementById('modalImgAtual').src    = btn.dataset.img;

    const prev = document.getElementById('preview-imagem-edit');
    prev.style.display = 'none';
    prev.src = '';
    document.getElementById('dropzone-texto-edit').innerText = '📁 Nova foto (opcional)';
    document.getElementById('dropzone-edit').style.borderColor = '#3498db';
    document.getElementById('imagem_produto_edit').value = '';
    document.getElementById('modalEdicaoErro').style.display = 'none';

    abrirModal('modalEdicao');
    document.getElementById('modalNomeInput').focus();
}

export function salvarEdicaoProduto() {
    const nome   = document.getElementById('modalNomeInput').value.trim();
    const imagem = document.getElementById('imagem_produto_edit').files[0];
    const btn    = document.getElementById('btnSalvarEdicao');
    const erro   = document.getElementById('modalEdicaoErro');

    erro.style.display = 'none';

    if (!nome) {
        erro.textContent   = 'Nome não pode ser vazio.';
        erro.style.display = 'block';
        return;
    }

    const form = new FormData();
    form.append('novo_nome', nome);
    if (imagem) form.append('imagem_produto', imagem);

    btn.disabled    = true;
    btn.textContent = 'Salvando...';

    fetch(`/api/editar_produto/${_produtoIdEditando}`, { method: 'POST', body: form })
        .then(r => r.json())
        .then(dados => {
            if (dados.erro) {
                erro.textContent   = dados.erro;
                erro.style.display = 'block';
                return;
            }
            _atualizarCard(dados);
            fecharModal('modalEdicao');
        })
        .catch(() => {
            erro.textContent   = 'Erro de conexão. Tente novamente.';
            erro.style.display = 'block';
        })
        .finally(() => {
            btn.disabled    = false;
            btn.textContent = '💾 Salvar alterações';
        });
}

function _atualizarCard(dados) {
    const card = document.getElementById(`card-${dados.id}`);
    card.querySelector('.nome-produto').textContent     = dados.nome;
    card.querySelector('img').src                       = dados.imagem + '?t=' + Date.now();
    card.querySelector('.btn-editar-card').dataset.nome = dados.nome;
    card.querySelector('.btn-editar-card').dataset.img  = dados.imagem;
    card.querySelector('.btn-excluir-card').href =
        card.querySelector('.btn-excluir-card').href
            .replace(/\/[^/]+$/, '/' + encodeURIComponent(dados.nome));
    card.querySelector('.btn-excluir-card').dataset.nome = dados.nome;
    card.querySelector('button[onclick]').setAttribute(
        'onclick', `window.adicionarItem('${dados.nome.replace(/'/g, "\\'")}', this)`);
}

// ── Categorias ────────────────────────────────────────────────────────────────

export function abrirModalNovaCategoria() {
    document.getElementById('nomeNovaCategoria').value = '';
    preencherCheckboxProdutos('checkboxProdutosNova', []);
    abrirModal('modalNovaCategoria');
    document.getElementById('nomeNovaCategoria').focus();
}

export function abrirModalEditarCategoria(btn) {
    const catId = btn.dataset.id;
    document.getElementById('nomeEditarCategoria').value = btn.dataset.nome;
    document.getElementById('formEditarCategoria').action = '/editar_categoria/' + catId;

    const selecionados = [];
    document.querySelectorAll('.produto-card').forEach(card => {
        const cats = (card.dataset.categorias || '').split(',').filter(Boolean);
        if (cats.includes(catId)) selecionados.push(card.id.replace('card-', ''));
    });

    preencherCheckboxProdutos('checkboxProdutosEditar', selecionados);
    abrirModal('modalEditarCategoria');
    document.getElementById('nomeEditarCategoria').focus();
}

export function toggleMenuCategoria(btn) {
    const dropdown   = btn.nextElementSibling;
    const estaAberto = dropdown.classList.contains('aberto');
    fecharMenusCategoria();
    if (!estaAberto) dropdown.classList.add('aberto');
}

export function fecharMenusCategoria() {
    document.querySelectorAll('.cat-dropdown.aberto')
            .forEach(d => d.classList.remove('aberto'));
}

export function confirmarRemocao(tipo, nome) {
    const msg = tipo === 'produto'
        ? `Remover o produto "${nome}" do catálogo?`
        : `Remover a categoria "${nome}"?\nOs produtos não serão apagados.`;
    return confirm(msg);
}