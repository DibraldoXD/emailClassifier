import time
import random
import json
import os
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv


# Carregar modelo e a chave da API do Gemini a partir de variáveis de ambiente
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash') 

# Função para classificar e responder e-mails usando

def analisar_com_ia(texto_limpo, texto_bruto):
    # Tentativas com backoff para lidar com limites de taxa de requisições por minuto (RPM)
    max_tentativas = 3
    prompt = f"""
    Você é um assistente de marketing financeiro da empresa AutoU. 
    Analise o email abaixo e retorne um JSON com classificação, confiança e resposta.

    Email para classificação: {texto_limpo}

    CRITÉRIOS DE CLASSIFICAÇÃO:
    - 'Produtivo': Requisições, dúvidas técnicas, status de boletos, envio de arquivos ou que necessitem de suporte.
    - 'Improdutivo': E-mails vazios ou sem sentido, Saudações, agradecimentos, mensagens festivas ou spans.

    Email para resposta: {texto_bruto}

    DIRETRIZES PARA A RESPOSTA:
    - Se for 'Produtivo', gere uma resposta profissional e empática informando que o time técnico já está analisando.
    - Se for 'Improdutivo', responda com a mensagem padrão: "Agradecemos o contato. Desejamos um excelente dia!"
    
    Retorne APENAS um JSON no formato:
    {{
      "categoria": "Produtivo ou Improdutivo",
      "confianca": "0-100%",
      "resposta_sugerida": "Sua resposta aqui"
    }}
    """
    for tentativa in range(max_tentativas):
        try:
            # Gerar Json de resposta usando o modelo Gemini
            response = model.generate_content(prompt)
            json_text = response.text.replace('```json', '').replace('```', '').strip()
            resultado = json.loads(json_text)     
            return resultado

        except exceptions.ResourceExhausted as e:
            # Tratamento específico para limite de taxa (código 429)
            # Backoff exponencial com jitter
            if tentativa < max_tentativas - 1:
                tempo_espera = (10 ** tentativa) + random.uniform(0, 2) 
                print(f" Limite 429 atingido. Tentativa {tentativa + 1}. Reiniciando em {tempo_espera:.2f}s...")
                time.sleep(tempo_espera)
                continue
            else:
                # Mensagem de erro e resposta padrão após esgotar tentativas
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




 
    
  
        

        
        