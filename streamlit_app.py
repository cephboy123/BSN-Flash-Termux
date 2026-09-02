import streamlit as st
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import os

st.title("💬 BSN-Flash Chat")

# Configuration des paramètres pour ne pas saturer la RAM de Streamlit
@st.cache_resource
def get_llm_instance():
    # Téléchargement sécurisé et mise en cache du modèle GGUF
    model_path = hf_hub_download(
        repo_id="Cephboy/BSN-Flash", 
        filename="bsn_flash_q4_k_m.gguf"
    )
    # Chargement en mode "low_vram" pour consommer moins de 500 Mo de RAM
    return Llama(
        model_path=model_path,
        n_ctx=512,        # Réduction de la taille du contexte
        n_threads=1,      # Utilisation d'un seul cœur CPU
        low_vram=True,    # Mode mémoire ultra-léger
        offload_kqv=False # Désactivation du déchargement GPU
    )

try:
    llm = get_llm_instance()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Écrivez votre message ici..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Formatage de l'historique Qwen2
            full_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            
            # Génération avec llama-cpp-python optimisé
            response = llm(
                full_prompt,
                max_tokens=256,
                stop=["<|im_end|>"],
                echo=False
            )
            output_text = response["choices"][0]["text"].strip()
            st.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})

except Exception as e:
    st.error(f"Démarrage du modèle en cours... Veuillez patienter 2 minutes et rafraîchir la page. ({e})")
          
