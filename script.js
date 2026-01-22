
// 1. FUNÇÃO PARA PROCESSAR EMAIL
async function processarEmail() {
    const text = document.getElementById('emailText').value;
    const fileInput = document.getElementById('emailFile');
    const loading = document.getElementById('loading');
    const resultSection = document.getElementById('resultSection');

    if (!text.trim() && (!fileInput.files || fileInput.files.length === 0)) {
        alert("Por favor, insira um texto ou selecione um arquivo para análise.");
        return;
    }

    loading.scrollIntoView({ behavior: 'smooth', block: 'center' });
    loading.classList.remove('hidden');
    resultSection.classList.add('hidden');

    const formData = new FormData();
    if (fileInput.files.length > 0) {
        formData.append('arquivo', fileInput.files[0]);
    }
    if (text.trim()) {
        formData.append('texto', text);
    }

    try {
        // Conexão com o backend local do desafio
        const response = await fetch('/analisar', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error("Erro na resposta do servidor");

        const data = await response.json();

        // Renderização dos dados da IA Gemini
        const category = data.categoria || 'Não Identificado';
        const confidence = data.confianca || '0%';
        const responseText = data.resposta_sugerida || 'Sem sugestão.';

        document.getElementById('categoryResult').innerText = category;
        document.getElementById('confidenceResult').innerText = confidence;
        document.getElementById('responseResult').innerText = responseText;

        // Animação da barra de confiança
        const confidenceValue = parseInt(confidence.replace('%', '')) || 0;
        setTimeout(() => {
            document.getElementById('confidenceBar').style.width = `${confidenceValue}%`;
        }, 100);

        // Ajuste visual dinâmico
        const card = document.getElementById('categoryCard');
        const confidenceBar = document.getElementById('confidenceBar');

        card.classList.remove('border-brand-orange', 'border-emerald-500', 'shadow-brand-orange/20', 'shadow-emerald-500/20');
        confidenceBar.classList.remove('bg-brand-orange', 'bg-emerald-500');

        if (category === 'Produtivo') {
            card.classList.add('border-brand-orange', 'shadow-brand-orange/20');
            confidenceBar.classList.add('bg-brand-orange');
        } else {
            card.classList.add('border-emerald-500', 'shadow-emerald-500/20');
            confidenceBar.classList.add('bg-emerald-500');
        }

        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error("Erro no processamento:", error);
        alert("Erro ao conectar com o Backend. Verifique se o servidor FastAPI/Uvicorn está rodando!");
    } finally {
        loading.classList.add('hidden');
    }
}

// 2. FUNÇÃO VISUAL DE UPLOAD
function mostrarArquivoSelecionado() {
    const fileInput = document.getElementById('emailFile');
    const fileInfo = document.getElementById('fileInfo');
    const dropzone = document.getElementById('dropzone');
    const uploadIcon = document.getElementById('uploadIcon');
    const btnRemove = document.getElementById('btnRemoveFile');

    if (fileInput.files && fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const fileSize = file.size > 1024 * 1024
            ? (file.size / (1024 * 1024)).toFixed(2) + ' MB'
            : (file.size / 1024).toFixed(2) + ' KB';

        dropzone.classList.add('border-brand-orange/50', 'bg-brand-card');
        dropzone.classList.remove('border-slate-700', 'bg-brand-card/50');

        uploadIcon.innerHTML = `<i class="fa-solid fa-file-circle-check text-4xl text-brand-orange drop-shadow-[0_0_10px_rgba(249,115,22,0.3)]"></i>`;
        fileInfo.innerHTML = `
            <span class="font-bold text-brand-orange text-lg block mb-1 truncate max-w-[250px]">${file.name}</span>
            <span class="text-xs text-brand-muted font-medium bg-brand-dark/50 px-3 py-1 rounded-full border border-brand-orange/20">${fileSize} • Pronto</span>
        `;

        btnRemove.classList.remove('hidden');
        btnRemove.classList.add('flex');
    }
}

// 3. FUNÇÃO PARA REMOVER ARQUIVO
function removerArquivo(event) {
    event.preventDefault();
    event.stopPropagation();

    const fileInput = document.getElementById('emailFile');
    const fileInfo = document.getElementById('fileInfo');
    const dropzone = document.getElementById('dropzone');
    const uploadIcon = document.getElementById('uploadIcon');
    const btnRemove = document.getElementById('btnRemoveFile');

    fileInput.value = "";

    dropzone.classList.remove('border-brand-orange/50', 'bg-brand-card');
    dropzone.classList.add('border-slate-700', 'bg-brand-card/50');

    uploadIcon.innerHTML = `<i class="fa-solid fa-cloud-arrow-up text-3xl text-brand-orange"></i>`;
    fileInfo.innerHTML = `<span class="font-semibold text-brand-orange">Clique para carregar</span> ou arraste <br> arquivos .PDF ou .TXT`;

    btnRemove.classList.add('hidden');
    btnRemove.classList.remove('flex');
}

// 4. FUNÇÃO DE CÓPIA
function copyResponse() {
    const textToCopy = document.getElementById('responseResult').innerText;

    navigator.clipboard.writeText(textToCopy).then(() => {
        const btn = document.querySelector('button[onclick="copyResponse()"]');
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `<i class="fa-solid fa-check mr-3 text-emerald-500"></i> Copiado!`;
        setTimeout(() => { btn.innerHTML = originalHtml; }, 2000);
    });
}