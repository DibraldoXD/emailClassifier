# emailClassifier

O emailClassifier é uma solução inteligente para triagem e classificação de e-mails, desenvolvida para otimizar o fluxo de trabalho acadêmico e profissional. Utilizando o Google Gemini AI, o sistema analisa o conteúdo de e-mails (via texto direto ou upload de arquivos) e fornece uma classificação (Proudtivo ou Improdutivo), nível de confiança e uma sugestão de resposta imediata.

Tecnologias Utilizadas:

Backend: FastAPI (Python)
Inteligência Artificial: Google Generative AI (Gemini)
Frontend: HTML5, JavaScript (ES6+) e Tailwind CSS
Processamento de Texto: NLTK e PyPDF2
Deploy: Otimizado para Vercel ou local

Funcionalidades:

Análise Híbrida: Suporte para entrada de texto manual ou upload de arquivos .pdf e .txt.
Exclusividade Mútua: Interface inteligente que gerencia campos de entrada para evitar conflitos de dados.
IA Generativa: Classificação automática em categorias e geração de respostas automáticas.
UI/UX Moderna: Interface em Dark Mode com efeito glassmorphism e feedback visual de progresso.

Site para uso da ferramenta:
https://email-classifier-vqdn.vercel.app

Instalação para Execução Local:
1. Requisitos Próximos
Certifique-se de ter o Python 3.9+ instalado.

2. Clonar o Repositório
git clone https://github.com/seu-usuario/autou-email-classifier.git
cd autou-email-classifier

3. Instalar Dependências
pip install -r requirements.txt

4. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto e adicione sua chave da API do Google:

GEMINI_API_KEY=sua_chave_aqui

5. Iniciar o Servidor
python main.py

O servidor estará disponível em http://127.0.0.1:8000.

Estrutura do Projeto:

├── api/
|   |
│   ├── ai_engine.py      # Conexão e lógica com Google Gemini
|   |
│   └── utils.py          # Extração de texto e pré-processamento
├── static/
│   ├── index.html        # Interface principal
│   ├── script.js         # Lógica de front-end e chamadas de API
│   └── autou_logo.jpg    # Identidade visual
├── main.py               # Ponto de entrada da aplicação FastAPI
├── requirements.txt      # Dependências do sistema
└── vercel.json           # Configurações de deploy

Autor:
Desenvolvido por João Luiz de Miranda Cilli. O projeto visa aplicar conceitos de IA e desenvolvimento full-stack para resolver problemas reais de produtividade.




