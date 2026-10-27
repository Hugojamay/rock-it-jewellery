import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
from openai import OpenAI
from config import Config # Utiliza las llaves generales de tu .env
from niche_config import SEARCH_QUERIES, get_evaluator_prompt, CLIENT_NAME
from database import init_db, is_already_processed, mark_as_processed
from notifier import send_whatsapp_alert, send_email_alert

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def run_client_agent():
    print(f"🚀 Iniciando Agente Comercial Autónomo para: {CLIENT_NAME}...")
    init_db()
    
    posts = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 1. Búsqueda web basada en el nicho configurado
    for query in SEARCH_QUERIES:
        try:
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            response = requests.get(search_url, headers=headers, timeout=8)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', class_='result')
                
                for r in results[:2]:
                    title_elem = r.find('a', class_='result__snippet')
                    title_text = title_elem.get_text() if title_elem else ""
                    link_elem = r.find('a', class_='result__url')
                    link = link_elem['href'] if link_elem else "https://duckduckgo.com"
                    
                    if title_text:
                        post_id = f"lead_{abs(hash(title_text)) % 100000:05d}"
                        if not is_already_processed(post_id):
                            posts.append({
                                "id": post_id,
                                "username": f"comprador_{post_id[-4:]}",
                                "platform": "Web Pública",
                                "post_text": title_text,
                                "post_url": link
                            })
        except Exception as e:
            print(f"⚠️ Error en query '{query}': {str(e)}")

    print(f"🔍 Prospectos crudos capturados: {len(posts)}")

    # 2. Evaluación con IA y Despacho de Alertas
    for post in posts:
        post_id = post["id"]
        if is_already_processed(post_id):
            continue

        prompt = get_evaluator_prompt(post["post_text"])
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            
            if data.get("is_valid_prospect", False):
                print(f"✅ ¡PROSPECTO VÁLIDO ENCONTRADO! [{data.get('problem_detected')}]")
                
                payload = {
                    "username": post["username"],
                    "platform": post["platform"],
                    "problem": data.get("problem_detected"),
                    "urgency": data.get("urgency"),
                    "post_text": post["post_text"],
                    "suggested_message": data.get("suggested_message")
                }

                # Disparar alertas a tu WhatsApp / Correo
                send_whatsapp_alert(payload, post["post_url"])
                send_email_alert(payload, post["post_url"])
            else:
                print(f"❌ Descartado: {data.get('reasoning')}")

            mark_as_processed(post_id, post["username"])
            
        except Exception as e:
            print(f"❌ Error procesando IA: {str(e)}")

if __name__ == "__main__":
    run_client_agent()