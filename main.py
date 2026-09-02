from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Téléchargement local sécurisé sur le serveur Render
MODEL_PATH = hf_hub_download(
    repo_id="Cephboy/BSN-Flash", 
    filename="bsn_flash_q4_k_m.gguf"
)

# Chargement ultra-optimisé (conso RAM < 300 Mo) pour le serveur gratuit
llm = Llama(
    model_path=MODEL_PATH, 
    n_ctx=512, 
    n_threads=1, 
    low_vram=True,
    offload_kqv=False
)

@app.post("/chat")
def chat(data: dict):
    user_message = data.get("message", "")
    full_prompt = f"<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n"
    
    try:
        response = llm(
            full_prompt, 
            max_tokens=150, 
            stop=["<|im_end|>"], 
            echo=False
        )
        return {"response": response["choices"]["text"].strip()}
    except Exception as e:
        return {"response": f"Erreur interne du moteur : {e}"}

@app.get("/")
def home():
    return {"status": "Serveur BSN-Flash 100% autonome et actif !"}
  
