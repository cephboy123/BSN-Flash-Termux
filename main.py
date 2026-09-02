from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Autoriser les connexions depuis n'importe quel navigateur (indispensable pour ton téléphone)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://huggingface.co"

@app.post("/chat")
def chat(data: dict):
    user_message = data.get("message", "")
    full_prompt = f"<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n"
    
    # Requête simplifiée qui ne consomme aucune RAM sur ton serveur Render
    payload = {"inputs": full_prompt, "parameters": {"max_new_tokens": 256}}
    response = requests.post(API_URL, json=payload)
    
    try:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return {"response": result[0].get("generated_text", "").replace(full_prompt, "").strip()}
        elif isinstance(result, dict) and "generated_text" in result:
            return {"response": result["generated_text"].replace(full_prompt, "").strip()}
        else:
            return {"response": "Le modèle est en cours de réveil sur Hugging Face, réessaye dans 20 secondes !"}
    except:
        return {"response": "Erreur de communication avec le stockage du modèle."}

@app.get("/")
def home():
    return {"status": "L'API BSN-Flash est en ligne et opérationnelle 24h/24 et 7j/7 !"}
                                                                 
