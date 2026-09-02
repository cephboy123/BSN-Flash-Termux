import streamlit as st
import requests

st.title("💬 BSN-Flash Chat")

hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("Veuillez configurer la variable HF_TOKEN dans les paramètres de Streamlit.")
else:
    # URL de l'API de votre modèle spécifique sur Hugging Face
    API_URL = "https://huggingface.co"
    headers = {"Authorization": f"Bearer {hf_token}"}

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
            response_placeholder = st.empty()
            
            # Formatage du prompt Qwen2
            full_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            
            try:
                # Requête directe au serveur Hugging Face
                payload = {"inputs": full_prompt, "parameters": {"max_new_tokens": 512}}
                response = requests.post(API_URL, headers=headers, json=payload)
                result = response.json()
                
                # Gestion du réveil du modèle (Cold Start)
                if isinstance(result, dict) and "estimated_time" in result:
                    wait_time = int(result["estimated_time"])
                    st.warning(f"⏳ Le modèle se réveille sur Hugging Face... Attente de {wait_time} secondes.")
                    import time
                    time.sleep(wait_time)
                    # Deuxième tentative après le temps d'attente
                    response = requests.post(API_URL, headers=headers, json=payload)
                    result = response.json()

                if isinstance(result, list) and len(result) > 0:
                    output_text = result[0].get("generated_text", "").replace(full_prompt, "").strip()
                elif isinstance(result, dict) and "generated_text" in result:
                    output_text = result["generated_text"].replace(full_prompt, "").strip()
                else:
                    output_text = "Le modèle est en cours de chargement. Réessayez dans 30 secondes !"

                response_placeholder.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})

            except Exception as e:
                response_placeholder.error(f"Erreur de connexion : {e}")
              
