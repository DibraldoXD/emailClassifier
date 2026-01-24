

// EXCLUSIVIDADE MÚTUA entre entradas de texto e upload de arquivo
function gerenciarCampos() {
    // Captura o elemento da caixa de texto e do upload de arquivo
    const textInput = document.getElementById('emailText');
    const fileInput = document.getElementById('emailFile');

    // Captura o container visual que envolve a área de texto e de upload
    const containerTexto = document.getElementById('containerTexto');
    const containerUpload = document.getElementById('containerUpload');

    // Verifica se existe algum texto digitado ou arquivo selecionado
    const temTexto = textInput.value.trim().length > 0;
    const temArquivo = fileInput.files.length > 0;

    // Se o usuário começou a digitar texto, bloqueia o upload de arquivo
    if (temTexto) {
        containerUpload.classList.add('opacity-30', 'pointer-events-none', 'grayscale');
        containerUpload.style.cursor = 'not-allowed';

        // Caso o usuário tenha selecionado um arquivo, bloqueia a entrada de texto
    } else if (temArquivo) {
        containerTexto.classList.add('opacity-30', 'pointer-events-none');
        textInput.disabled = true;

        // Se ambos os campos estiverem vazios, libere os dois para uso
    } else {
        containerUpload.classList.remove('opacity-30', 'pointer-events-none', 'grayscale');
        containerUpload.style.cursor = 'pointer';
        containerTexto.classList.remove('opacity-30', 'pointer-events-none');
        textInput.disabled = false;
    }
}

// Função que envia os dados para o backend e processa a resposta
async function processarEmail() {
    // Obtém os dados iniciais e elementos da página
    console.log("Iniciando processamento do email...");
    const text = document.getElementById('emailText').value;
    const fileInput = document.getElementById('emailFile');
    const loading = document.getElementById('loading');
    const resultSection = document.getElementById('resultSection');

    // Se não houver texto nem arquivo, interrompe e avisa o usuário
    if (!text.trim() && (!fileInput.files || fileInput.files.length === 0)) {
        alert("Por favor, insira um texto ou selecione um arquivo para análise.");
        return;
    }

    // Feedback visual de carregamento
    loading.scrollIntoView({ behavior: 'smooth', block: 'center' });
    loading.classList.remove('hidden');
    resultSection.classList.add('hidden');

    // Empacota os dados para envio 
    const formData = new FormData();
    if (fileInput.files.length > 0) {
        formData.append('arquivo', fileInput.files[0]);

    } else if (text.trim()) {
        formData.append('texto', text);
    }

    try {
        // Requisição HTTP POST para o backend 
        const response = await fetch('/api/analisar', {
            method: 'POST',
            body: formData
        });

        // Dispara exceção em caso de erro na resposta
        if (!response.ok) throw new Error("Erro na resposta do servidor");

        // Converte a resposta bruta em um objeto JSON 
        const data = await response.json();

        // Valores padrão em caso de ausência de dados
        const category = data.categoria || 'Não Identificado';
        const confidence = data.confianca || '0%';
        const responseText = data.resposta_sugerida || 'Sem sugestão.';

        // Atualiza o conteúdo dos elementos na página com os resultados
        document.getElementById('categoryResult').innerText = category;
        document.getElementById('confidenceResult').innerText = confidence;
        document.getElementById('responseResult').innerText = responseText;

        // Exibição animada da barra de confiança
        const confidenceValue = parseInt(confidence.replace('%', '')) || 0;
        setTimeout(() => {
            document.getElementById('confidenceBar').style.width = `${confidenceValue}%`;
        }, 100);

        // Ajusta a paleta de cores
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

        // Mostra resultados prontos
        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });


        // Em caso de erro de conexão ou processamento
    } catch (error) {
        console.error("Erro no processamento:", error); l
        alert("Erro ao conectar com o Backend. Verifique se o servidor está ativo!");
    } finally {
        loading.classList.add('hidden');
    }
}



// Função que atualiza a interface para mostrar o arquivo selecionado
function mostrarArquivoSelecionado() {
    const fileInput = document.getElementById('emailFile');
    const fileInfo = document.getElementById('fileInfo');
    const dropzone = document.getElementById('dropzone');
    const uploadIcon = document.getElementById('uploadIcon');
    const btnRemove = document.getElementById('btnRemoveFile');

    if (fileInput.files && fileInput.files.length > 0) {
        const file = fileInput.files[0];
        //Calcula o tamanho do arquivo em KB ou MB
        const fileSize = file.size > 1024 * 1024
            ? (file.size / (1024 * 1024)).toFixed(2) + ' MB'
            : (file.size / 1024).toFixed(2) + ' KB';

        // Feedback visual de arquivo carregado
        dropzone.classList.add('border-brand-orange/50', 'bg-brand-card');
        dropzone.classList.remove('border-slate-700', 'bg-brand-card/50');
        uploadIcon.innerHTML = `<i class="fa-solid fa-file-circle-check text-4xl text-brand-orange drop-shadow-[0_0_10px_rgba(249,115,22,0.3)]"></i>`;
        fileInfo.innerHTML = `
            <span class="font-bold text-brand-orange text-lg block mb-1 truncate max-w-[250px]">${file.name}</span>
            <span class="text-xs text-brand-muted font-medium bg-brand-dark/50 px-3 py-1 rounded-full border border-brand-orange/20">${fileSize} • Pronto</span>
        `;

        // Torna o botão de "remover arquivo" visível
        btnRemove.classList.remove('hidden');
        btnRemove.classList.add('flex');

        // Aciona o bloqueio da área de texto
        gerenciarCampos();
    }
}

// Função para remover o arquivo selecionado e restaurar o estado inicial
function removerArquivo(event) {
    // Previne o comportamento padrão do clique
    event.preventDefault();
    event.stopPropagation();

    const fileInput = document.getElementById('emailFile');
    const fileInfo = document.getElementById('fileInfo');
    const dropzone = document.getElementById('dropzone');
    const uploadIcon = document.getElementById('uploadIcon');
    const btnRemove = document.getElementById('btnRemoveFile');

    // Limpa o valor do input (remove o arquivo da memória do navegador)
    fileInput.value = "";

    // Restaura o estilo original da área de upload
    dropzone.classList.remove('border-brand-orange/50', 'bg-brand-card');
    dropzone.classList.add('border-slate-700', 'bg-brand-card/50');
    uploadIcon.innerHTML = `<i class="fa-solid fa-cloud-arrow-up text-3xl text-brand-orange"></i>`;
    fileInfo.innerHTML = `<span class="font-semibold text-brand-orange">Clique para carregar</span> ou arraste <br> arquivos .PDF ou .TXT`;
    btnRemove.classList.add('hidden');
    btnRemove.classList.remove('flex');

    // Reabilita a área de texto se estiver vazia
    gerenciarCampos();
}

// Função para copiar o texto gerado pela IA para a área de transferência
function copyResponse() {
    // Obtém o texto da resposta gerada
    const textToCopy = document.getElementById('responseResult').innerText;

    // Copia o texto para a área de transferência
    navigator.clipboard.writeText(textToCopy).then(() => {
        const btn = document.querySelector('button[onclick="copyResponse()"]');
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `<i class="fa-solid fa-check mr-3 text-emerald-500"></i> Copiado!`;
        setTimeout(() => { btn.innerHTML = originalHtml; }, 2000);
    });
}