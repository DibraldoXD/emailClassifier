import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega a chave do arquivo .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Modelo estável recomendado para 2026
MODEL_NAME = 'gemini-2.5-flash-lite' 
model = genai.GenerativeModel(MODEL_NAME)

import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash') # Modelo estável de 2026

def analisar_com_ia(texto_limpo):
    # Prompt que funde as definições de categoria e a persona da AutoU
    prompt = f"""
    Você é um assistente de marketing financeiro da empresa AutoU. 
    Analise o email abaixo e retorne um JSON com classificação, confiança e resposta.

    CRITÉRIOS DE CLASSIFICAÇÃO:
    - 'Produtivo': Requisições, dúvidas técnicas, status de boletos ou envio de arquivos.
    - 'Improdutivo': Saudações, agradecimentos, mensagens festivas ou spans.

    DIRETRIZES PARA A RESPOSTA:
    - Se for 'Produtivo', gere uma resposta curta, profissional e empática informando que o time técnico já está analisando.
    - Se for 'Improdutivo', a resposta sugerida deve ser apenas um agradecimento genérico.

    Email para análise: {texto_limpo}

    Retorne APENAS um JSON no formato:
    {{
      "categoria": "Produtivo ou Improdutivo",
      "confianca": "0-100%",
      "resposta_sugerida": "Sua resposta aqui"
    }}
    """
    
    try:
        # Chamada única à IA
        response = model.generate_content(prompt)
        json_text = response.text.replace('```json', '').replace('```', '').strip()
        resultado = json.loads(json_text)

        # --- REGRA DE NEGÓCIO (FUSÃO DA LÓGICA) ---
        # Garante a resposta padrão exata para improdutivos conforme solicitado
        if resultado.get("categoria") == "Improdutivo":
            resultado["resposta_sugerida"] = "Agradecemos o contato. Desejamos um excelente dia!"
        
        return resultado

    except Exception as e:
        # Em 2026, erros de limite de taxa (429) são comuns se o RPM for excedido
        return {
            "categoria": "Erro",
            "confianca": "0%",
            "resposta_sugerida": "Recebemos sua mensagem e daremos retorno em breve.",
            "erro_detalhado": str(e)
        }
    

