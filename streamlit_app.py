import streamlit as st
from huggingface_hub import InferenceClient
import time

st.title("💬 BSN-Flash Chat")

hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("Veuillez configurer la variable HF_TOKEN dans les paramètres de Streamlit.")
else:
    client = InferenceClient(model="Cephboy/BSN-Flash", token=hf_token)

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
            # Système de boucles pour forcer le réveil si le modèle dort
            for attempt in range(3):
                try:
                    full_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
                    response = client.text_generation(
                        full_prompt,
                        max_new_tokens=512,
                        stop=["<|im_end|>"]
                    )
                    output_text = response.strip()
                    response_placeholder.markdown(output_text)
                    st.session_state.messages.append({"role": "assistant", "content": output_text})
                    break  # Succès, on sort de la boucle
                except Exception as e:
                    if "Model" in str(e) and "loading" in str(e).lower():
                        response_placeholder.warning(f"⏳ Hugging Face réveille votre modèle (Tentative {attempt+1}/3)... Patientez 20 secondes.")
                        time.sleep(20)  # Laisse le temps à Hugging Face d'allumer le serveur
                    else:
                        response_placeholder.error(f"Erreur d'API : {e}. Vérifiez que votre modèle sur Hugging Face n'est pas totalement désactivé.")
                        break
                  
