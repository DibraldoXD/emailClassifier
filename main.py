from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from utils import extrair_texto_arquivo, pre_processar_texto
from ai_engine import analisar_com_ia

app = FastAPI(title="AutoU Email Classifier")

# Configuração de CORS para permitir acesso do seu Frontend HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analisar")
async def rota_analisar(
    texto: str = Form(None), 
    arquivo: UploadFile = File(None)
):
    # 1. Obtém o texto original
    conteudo_bruto = ""
    if arquivo:
        file_bytes = await arquivo.read()
        conteudo_bruto = extrair_texto_arquivo(file_bytes, arquivo.filename)
    else:
        conteudo_bruto = texto

    if not conteudo_bruto:
        return {"erro": "Nenhum conteúdo enviado."}

    # 2. Processamento e IA
    texto_limpo = pre_processar_texto(conteudo_bruto)
    resultado = analisar_com_ia(texto_limpo)
    
    return resultado

if __name__ == "__main__":
    import uvicorn
    # Inicia o servidor local na porta 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)