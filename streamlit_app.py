import streamlit as st
import requests

st.title("💬 BSN-Flash Chat Immortel")

# URL de votre propre serveur Render qui ne dort jamais !
API_URL = "https://onrender.com"

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
        
        try:
            # Envoi du message à votre serveur Render
            response = requests.post(API_URL, json={"message": prompt})
            result = response.json()
            output_text = result.get("response", "Pas de réponse reçue.")
            
            response_placeholder.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            response_placeholder.error(f"Erreur de connexion au serveur Render : {e}")
          
