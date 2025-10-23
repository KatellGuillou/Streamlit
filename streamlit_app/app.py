"""
Mayday Assistant Conversationnel - Interface Streamlit
Application de démonstration avec réponses mockées
"""

import streamlit as st
from src.generation_mock import generate_response, get_available_questions
from src.permissions import get_user_permissions, USERS
from src.retrieval_mock import count_accessible_documents
from src.utils import calculate_confidence_display, format_source_metadata, truncate_text

# Configuration de la page
st.set_page_config(
    page_title="Mayday Assistant Conversationnel - MODE DÉMO",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #e8f4f8;
        padding: 0.8rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation de l'état de session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_user" not in st.session_state:
    st.session_state.current_user = "Sophie (RH)"
if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# Banner mode démo
st.info("🎭 **MODE DÉMO** : Cet assistant utilise des réponses pré-générées pour la démonstration. Aucune clé API requise.")

# === SIDEBAR ===
with st.sidebar:
    st.markdown("# 🤖 Mayday Assistant")
    st.caption("Version POC - Mode Mock")
    
    st.divider()
    
    # Sélecteur utilisateur
    st.subheader("👤 Utilisateur")
    user = st.selectbox(
        "Choisir un profil",
        list(USERS.keys()),
        index=list(USERS.keys()).index(st.session_state.current_user)
    )
    
    # Si changement d'utilisateur, réinitialiser la conversation
    if user != st.session_state.current_user:
        st.session_state.current_user = user
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()
    
    # Afficher les permissions
    permissions = get_user_permissions(user)
    
    st.markdown("**📋 Permissions actuelles :**")
    st.markdown(f"- **Équipes :** {', '.join(permissions['teams'])}")
    st.markdown(f"- **Rôle :** {permissions['role']}")
    
    # Calculer le nombre de documents accessibles
    accessible_count = count_accessible_documents(permissions)
    st.markdown(f"- **Documents accessibles :** {accessible_count}")
    
    st.divider()
    
    # Questions disponibles
    with st.expander("💡 Questions disponibles", expanded=False):
        st.markdown("""
        **🏢 RH :**
        - Quelle est la politique de remboursement ?
        - Comment gérer une demande de congé parental ?
        - Procédure d'onboarding nouveau salarié
        - Politique de télétravail
        - Évaluation annuelle
        - Formation continue
        
        **💰 Finance :**
        - Quel est le budget marketing Q1 ?
        - Comment valider une dépense > 10k€ ?
        - Note de frais
        
        **🎧 Support :**
        - Comment escalader un ticket prioritaire ?
        - Quels sont les SLA par type de ticket ?
        - Créer un ticket support
        
        **🛠️ Self-Care :**
        - Mon produit ne s'allume pas, que faire ?
        - Réinitialiser mon mot de passe
        
        **🎓 Academy :**
        - Formation CRM
        """)
    
    st.divider()
    
    # Statistiques
    st.subheader("📊 Statistiques")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.query_count)
    with col2:
        st.metric("Messages", len(st.session_state.messages))
    
    st.divider()
    
    # Bouton reset
    if st.button("🔄 Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()
    
    st.divider()
    
    # Informations
    with st.expander("ℹ️ À propos", expanded=False):
        st.markdown("""
        **Mayday Assistant Conversationnel**
        
        Version : 1.0.0 (POC)
        Mode : Mock (sans API)
        
        Cette démo illustre les capacités d'un assistant RAG avec :
        - ✅ Gestion des permissions
        - ✅ Citations de sources
        - ✅ Score de confiance
        - ✅ Conversation multi-tour
        
        Développé avec ❤️ par l'équipe Mayday
        """)

# === MAIN CONTENT ===
st.markdown('<div class="main-header">🤖 Assistant Conversationnel Mayday</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Bonjour {st.session_state.current_user} ! Posez vos questions sur les procédures, produits et clients Mayday</div>', unsafe_allow_html=True)

# Afficher l'historique de conversation
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Afficher les sources si c'est une réponse de l'assistant
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            st.markdown("---")
            with st.expander(f"📚 **Sources utilisées** ({len(message['sources'])})", expanded=False):
                for i, source in enumerate(message["sources"]):
                    st.markdown(f"**[Source {i+1}] {source['title']}**")
                    st.caption(format_source_metadata(source))
                    
                    # Afficher un extrait du contenu
                    with st.container():
                        st.markdown(f"*{truncate_text(source['content'], 250)}*")
                    
                    if i < len(message["sources"]) - 1:
                        st.markdown("")

# Zone de saisie utilisateur
if prompt := st.chat_input("💬 Posez votre question ici..."):
    # Incrémenter le compteur de queries
    st.session_state.query_count += 1
    
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Générer la réponse de l'assistant
    with st.chat_message("assistant"):
        with st.spinner("🔍 Recherche dans la knowledge base..."):
            # Récupérer les permissions de l'utilisateur actuel
            user_permissions = get_user_permissions(st.session_state.current_user)
            
            # Générer la réponse mockée
            response, sources, confidence = generate_response(
                prompt,
                user_permissions,
                st.session_state.messages
            )
            
            # Afficher la réponse
            st.markdown(response)
            
            # Afficher le score de confiance
            st.markdown("---")
            emoji, message_conf, color = calculate_confidence_display(confidence)
            
            if color == "success":
                st.success(f"{emoji} **{message_conf}**")
            elif color == "warning":
                st.warning(f"{emoji} **{message_conf}**")
            elif color == "error":
                st.error(f"{emoji} **{message_conf}**")
            else:
                st.info(f"{emoji} **{message_conf}**")
            
            # Boutons de feedback
            col1, col2, col3, col4 = st.columns([1, 1, 1, 7])
            with col1:
                if st.button("👍", key=f"like_{len(st.session_state.messages)}"):
                    st.toast("✅ Merci pour votre feedback positif !", icon="👍")
            with col2:
                if st.button("👎", key=f"dislike_{len(st.session_state.messages)}"):
                    st.toast("📝 Merci, nous allons améliorer cette réponse", icon="👎")
            with col3:
                if st.button("📋", key=f"copy_{len(st.session_state.messages)}"):
                    st.toast("📋 Réponse copiée dans le presse-papier", icon="📋")
            
            # Afficher les sources si disponibles
            if sources:
                st.markdown("---")
                with st.expander(f"📚 **Sources utilisées** ({len(sources)})", expanded=False):
                    for i, source in enumerate(sources):
                        st.markdown(f"**[Source {i+1}] {source['title']}**")
                        st.caption(format_source_metadata(source))
                        
                        # Afficher un extrait du contenu
                        with st.container():
                            st.markdown(f"*{truncate_text(source['content'], 250)}*")
                        
                        if i < len(sources) - 1:
                            st.markdown("")
    
    # Sauvegarder la réponse dans l'historique
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "sources": sources,
        "confidence": confidence
    })
    
    # Rafraîchir pour afficher les nouveaux messages
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; font-size: 0.9rem;">'
    'Mayday Assistant Conversationnel v1.0 - Mode POC | '
    'Propulsé par Streamlit 🚀'
    '</div>',
    unsafe_allow_html=True
)
