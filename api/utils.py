import re
import nltk
import PyPDF2
import io
import os
from nltk.corpus import stopwords

# Define um diretório em /tmp (único local com permissão de escrita no Vercel)
nltk_data_dir = '/tmp/nltk_data'

# Cria o diretório se ele não existir
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir, exist_ok=True)

# Indica ao NLTK para procurar dados também nessa pasta
nltk.data.path.append(nltk_data_dir)

# Realiza o download especificando o diretório de destino
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Definir Stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('portuguese'))

# Função para extrair texto de arquivos (PDF e TXT)
def extrair_texto_arquivo(file_bytes, filename):
    if filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        return "".join([page.extract_text() or "" for page in pdf_reader.pages])
    return file_bytes.decode("utf-8") if filename.endswith('.txt') else ""

# Função para pré-processar o texto para melhorar a eficiência da IA
def pre_processar_texto(texto):
    if not texto: return ""
    
    # Lowercase e substituição de quebras de linha/tabs por espaços
    texto = texto.lower().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # Limpeza de caracteres especiais (mantendo letras e espaços)
    texto = re.sub(r'[^a-zA-Záàâãéèêíïóôõöúçñ\s]', '', texto)
    
    # O split() sem argumentos remove múltiplos espaços seguidos e quebras residuais
    palavras = [w for w in texto.split() if w not in stop_words]
    
    # O join() une tudo com apenas um espaço, garantindo uma linha única
    return " ".join(palavras).strip()