import streamlit as st
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

st.title("💬 BSN-Flash Chat")

# Téléchargement sécurisé du modèle depuis votre dépôt Hugging Face actuel
@st.cache_resource
def load_model():
    model_path = hf_hub_download(
        repo_id="Cephboy/BSN-Flash", 
        filename="bsn_flash_q4_k_m.gguf"
    )
    return Llama(model_path=model_path, n_ctx=2048, n_threads=2)

llm = load_model()

# Gestion de l'historique de discussion dans l'interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Écrivez votre message ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Préparation du prompt selon le format Qwen2
    full_prompt = ""
    for msg in st.session_state.messages:
        full_prompt += f"<|im_start|>{msg['role']}\n{msg['content']}<|im_end|>\n"
    full_prompt += "<|im_start|>assistant\n"

    with st.chat_message("assistant"):
        response = llm(full_prompt, max_tokens=512, stop=["<|im_end|>"], echo=False)
        output_text = response["choices"]["text"].strip()
        st.markdown(output_text)
        
    st.session_state.messages.append({"role": "assistant", "content": output_text})

