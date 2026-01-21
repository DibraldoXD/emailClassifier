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
    texto = texto.lower()
    texto = re.sub(r'[^a-zA-Záàâãéèêíïóôõöúçñ0-9\s]', '', texto)
    palavras = [w for w in texto.split() if w not in stop_words]
    return " ".join(palavras)