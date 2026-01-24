import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from api.utils import extrair_texto_arquivo, pre_processar_texto
from api.ai_engine import analisar_com_ia

# Instancia o servidor FastAPI
app = FastAPI(title="AutoU Email Classifier")

# Utiliza a estrategia de servir arquivos estáticos (HTML, CSS, JS) para possibiltar o uso do vercel
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota raiz do frontend
@app.get("/", response_class=HTMLResponse)
def read_root():
    # Abre o arquivo da interface HTML com a codificação utf-8 
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# Configuração do Middleware CORS com todas as permissões liberadas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_methods=["*"],   
    allow_headers=["*"],   
)

# Rota do processamento da IA via POST, aceitando texto e arquivos
@app.post("/api/analisar")
async def rota_analisar(
    texto: str = Form(None),      
    arquivo: UploadFile = File(None) 
):
    conteudo_bruto = ""

    # Verifica se o usuário enviou um arquivo e extrai o texto, senão usa o texto puro
    if arquivo:
        file_bytes = await arquivo.read()
        conteudo_bruto = extrair_texto_arquivo(file_bytes, arquivo.filename)
    else:
        conteudo_bruto = texto

    # Se nada foi enviado, retorna uma mensagem de erro
    if not conteudo_bruto:
        return {"erro": "Nenhum conteúdo enviado."}

    # Limpa o texto 
    texto_limpo = pre_processar_texto(conteudo_bruto)
    
    # Classifica e gera resposta usando a IA
    resultado = analisar_com_ia(texto_limpo, conteudo_bruto)
    
    # Devolve a resposta final (JSON) 
    return resultado

# Executa o servidor Uvicorn se o script for executado diretamente, descomente para usar

#  if __name__ == "__main__":
#   uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True) 