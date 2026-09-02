import streamlit as st
from huggingface_hub import InferenceClient

st.title("💬 BSN-Flash Chat")

# Récupération sécurisée du Token Hugging Face
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("Veuillez configurer la variable HF_TOKEN dans les paramètres de Streamlit.")
else:
    # Connexion directe à l'API gratuite de votre modèle
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
            try:
                # Interrogation de l'API Hugging Face (Format Qwen2)
                full_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
                response = client.text_generation(
                    full_prompt,
                    max_new_tokens=512,
                    stop=["<|im_end|>"]
                )
                output_text = response.strip()
                st.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
            except Exception as e:
                st.error(f"L'API du modèle est en cours de démarrage ou indisponible : {e}")

