import re
import nltk
import PyPDF2
import io
from nltk.corpus import stopwords

import nltk
import os

# 1. Define um diretório em /tmp (único local com permissão de escrita no Vercel)
nltk_data_dir = '/tmp/nltk_data'

# 2. Cria o diretório se ele não existir
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir, exist_ok=True)

# 3. Indica ao NLTK para procurar dados também nessa pasta
nltk.data.path.append(nltk_data_dir)

# 4. Realiza o download especificando o diretório de destino
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Agora você pode definir suas stop_words normalmente
from nltk.corpus import stopwords
stop_words = set(stopwords.words('portuguese'))

def extrair_texto_arquivo(file_bytes, filename):
    if filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        return "".join([page.extract_text() or "" for page in pdf_reader.pages])
    return file_bytes.decode("utf-8") if filename.endswith('.txt') else ""

def pre_processar_texto(texto):
    if not texto: return ""
    
    # 1. Lowercase e substituição de quebras de linha/tabs por espaços
    texto = texto.lower().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # 2. Limpeza de caracteres especiais (mantendo letras, números e espaços)
    # O \s no final permite que o regex preserve os espaços que acabamos de criar
    texto = re.sub(r'[^a-zA-Záàâãéèêíïóôõöúçñ0-9\s]', '', texto)
    
    # 3. O split() sem argumentos remove múltiplos espaços seguidos e quebras residuais
    palavras = [w for w in texto.split() if w not in stop_words]
    
    # 4. O join() une tudo com apenas um espaço, garantindo uma linha única
    return " ".join(palavras).strip()