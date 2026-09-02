import streamlit as st
from huggingface_hub import hf_hub_download
import os

st.title("💬 BSN-Flash Chat (Mode Secours)")

# On vérifie juste si le fichier se télécharge bien
try:
    with st.spinner("Vérification du fichier de modèle sur les serveurs..."):
        model_path = hf_hub_download(
            repo_id="Cephboy/BSN-Flash", 
            filename="bsn_flash_q4_k_m.gguf"
        )
    
    st.success("✅ Le modèle est bien synchronisé et stocké sur le cloud !")
    st.info("Pour discuter en direct 24h/24 sans les bugs de serveurs Streamlit, utilisez un jeton d'accès API direct.")
    
    # Interface de Chat visuelle basique
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Écrivez ici..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            st.markdown("Système de secours actif : L'infrastructure Python 3.14 bloque l'exécution locale de ce modèle. Votre fichier est cependant sécurisé.")

except Exception as e:
    st.error(f"Erreur d'accès au fichier : {e}")
  
