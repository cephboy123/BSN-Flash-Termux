import streamlit as st
import requests

st.title("💬 BSN-Flash Chat")

hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("Veuillez configurer la variable HF_TOKEN dans les paramètres de Streamlit.")
else:
    # URL d'inférence universelle pour réveiller et interroger le modèle
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
            full_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            
            try:
                # Requête JSON directe compatible avec toutes les versions de Python
                payload = {"inputs": full_prompt, "parameters": {"max_new_tokens": 256}}
                response = requests.post(API_URL, headers=headers, json=payload)
                result = response.json()
                
                # Système anti-sommeil (Cold Start)
                if isinstance(result, dict) and "estimated_time" in result:
                    wait_time = int(result["estimated_time"])
                    response_placeholder.warning(f"⏳ Hugging Face réveille votre modèle... Attente de {wait_time}s.")
                    import time
                    time.sleep(wait_time)
                    response = requests.post(API_URL, headers=headers, json=payload)
                    result = response.json()

                # Extraction propre de la réponse texte
                if isinstance(result, list) and len(result) > 0:
                    output_text = result[0].get("generated_text", "").replace(full_prompt, "").strip()
                elif isinstance(result, dict) and "generated_text" in result:
                    output_text = result["generated_text"].replace(full_prompt, "").strip()
                else:
                    output_text = "Le modèle s'est réveillé ! Renvoyez votre message pour obtenir la réponse."

                response_placeholder.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})

            except Exception as e:
                response_placeholder.error(f"Erreur de transmission : {e}")
                  
