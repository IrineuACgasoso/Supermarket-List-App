// ─────────────────────────────────────────
// Dropzone — drag & drop + colar imagem
// ─────────────────────────────────────────
 
export function configurarDropzone(dropzoneId, inputId, textoId, previewId) {
    const dz      = document.getElementById(dropzoneId);
    const input   = document.getElementById(inputId);
    const texto   = document.getElementById(textoId);
    const preview = document.getElementById(previewId);

    dz.addEventListener('click', () => input.click());
    dz.addEventListener('dragover',  e => { e.preventDefault(); dz.classList.add('arrastando'); });
    dz.addEventListener('dragleave', () => dz.classList.remove('arrastando'));
    dz.addEventListener('drop', e => {
        e.preventDefault(); dz.classList.remove('arrastando');
        if (e.dataTransfer.files.length) { input.files = e.dataTransfer.files; mostrarPreview(input, preview, texto, dz); }
    });
    input.addEventListener('change', () => mostrarPreview(input, preview, texto, dz));
}


export function mostrarPreview(input, preview, texto, dz) {
    if (!input.files || !input.files[0]) return;
    const leitor = new FileReader();
    leitor.onload = e => {
        preview.src            = e.target.result;
        preview.style.display  = 'block';
        texto.innerText        = '✅ Imagem pronta!';
        dz.style.borderColor   = '#2ecc71';
    };
    leitor.readAsDataURL(input.files[0]);
}
 
export function iniciarColarImagem() {
    document.addEventListener('paste', e => {
        if (!e.clipboardData.files.length) return;
        const modalAberto = document.getElementById('modalEdicao').classList.contains('aberto');
        const prefix  = modalAberto ? 'edit' : 'novo';
        const input   = document.getElementById(`imagem_produto_${prefix}`);
        const preview = document.getElementById(`preview-imagem-${prefix}`);
        const texto   = document.getElementById(`dropzone-texto-${prefix}`);
        const dz      = document.getElementById(`dropzone-${prefix}`);
        input.files = e.clipboardData.files;
        mostrarPreview(input, preview, texto, dz);
    });
}