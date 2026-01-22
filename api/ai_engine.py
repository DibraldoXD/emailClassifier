import time
import random
import json
import os
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash') # Modelo estável de 2026

def analisar_com_ia(texto_limpo):
    max_tentativas = 3
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
    for tentativa in range(max_tentativas):
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

        except exceptions.ResourceExhausted as e:
            if tentativa < max_tentativas - 1:
                tempo_espera = (10 ** tentativa) + random.uniform(0, 2) 
                print(f" Limite 429 atingido. Tentativa {tentativa + 1}. Reiniciando em {tempo_espera:.2f}s...")
                time.sleep(tempo_espera)
                continue
            else:
                return {
                    "categoria": "Estourou o limite de taxa",
                    "confianca": "0%",
                    "resposta_sugerida": "Recebemos sua mensagem e daremos retorno em breve.",
                    "erro_detalhado": str(e)
                }

        except Exception as e:
            # Tratamento de outros erros (JSON inválido, conexão, etc)
            return {
                "categoria": "Erro de Processamento",
                "confianca": "0%",
                "resposta_sugerida": "Recebemos sua mensagem e daremos retorno em breve.",
                "erro_detalhado": str(e)
            }




 
    
  
        

        
        