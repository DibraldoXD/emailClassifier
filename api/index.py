from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# No Vercel, as importações devem considerar a estrutura da pasta /api
from api.utils import extrair_texto_arquivo, pre_processar_texto
from api.ai_engine import analisar_com_ia

app = FastAPI(title="AutoU Email Classifier")


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


# Configuração de CORS: No deploy, isso garante que seu frontend (Vercel)
# consiga conversar com o backend (Vercel) sem bloqueios.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analisar")
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
    resultado = analisar_com_ia(texto_limpo, conteudo_bruto)
    
    return resultado

# REMOVIDO: O bloco if __name__ == "__main__" e uvicorn.run().
# O Vercel ignora essa parte, pois ele mesmo instanciará o 'app'.