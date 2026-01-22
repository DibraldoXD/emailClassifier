import re
import nltk
import PyPDF2
import io
from nltk.corpus import stopwords

nltk.download('stopwords')
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