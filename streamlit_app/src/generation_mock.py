"""
Module de génération de réponses mockées
Sélectionne et retourne des réponses pré-générées basées sur la query
"""

import json
import os
from typing import Dict, Tuple, List, Optional


def load_responses() -> Dict:
    """
    Charge les réponses pré-générées depuis le fichier JSON
    
    Returns:
        Dictionnaire des réponses mockées
    """
    try:
        current_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(current_dir, "data", "mock_responses.json")
        
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Fichier mock_responses.json introuvable")
        return {}
    except json.JSONDecodeError:
        print(f"Erreur : Format JSON invalide dans mock_responses.json")
        return {}


def load_documents() -> List[Dict]:
    """
    Charge les documents depuis le fichier JSON
    
    Returns:
        Liste des documents
    """
    try:
        current_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(current_dir, "data", "mock_documents.json")
        
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Fichier mock_documents.json introuvable")
        return []
    except json.JSONDecodeError:
        print(f"Erreur : Format JSON invalide dans mock_documents.json")
        return []


def match_query_pattern(query: str, patterns: List[str]) -> bool:
    """
    Vérifie si la query matche un des patterns définis
    
    Args:
        query: Question de l'utilisateur
        patterns: Liste de patterns à matcher
        
    Returns:
        True si un pattern matche
    """
    query_lower = query.lower().strip()
    return any(pattern.lower() in query_lower for pattern in patterns)


def get_document_by_id(doc_id: str, documents: List[Dict]) -> Optional[Dict]:
    """
    Récupère un document par son ID
    
    Args:
        doc_id: ID du document à récupérer
        documents: Liste de tous les documents
        
    Returns:
        Le document trouvé ou None
    """
    for doc in documents:
        if doc.get("id") == doc_id:
            return doc
    return None


def generate_response(
    query: str,
    user_permissions: Dict,
    conversation_history: Optional[List[Dict]] = None
) -> Tuple[str, List[Dict], str]:
    """
    Génère une réponse mockée basée sur les patterns de query
    
    Args:
        query: Question de l'utilisateur
        user_permissions: Permissions de l'utilisateur
        conversation_history: Historique de conversation (optionnel)
        
    Returns:
        Tuple (response_text, sources, confidence_level)
    """
    responses = load_responses()
    documents = load_documents()
    
    if not responses:
        return (
            "Erreur : Impossible de charger les réponses. Veuillez réessayer.",
            [],
            "none"
        )
    
    # 1. Chercher la réponse qui matche la query
    matched_response = None
    matched_key = None
    
    for key, response_data in responses.items():
        if match_query_pattern(query, response_data.get("query_patterns", [])):
            # Vérifier les permissions
            required_teams = response_data.get("required_teams", [])
            
            # Si pas d'équipe requise, c'est public
            if not required_teams:
                matched_response = response_data
                matched_key = key
                break
            
            # Vérifier si l'utilisateur a accès à au moins une équipe
            user_teams = user_permissions.get("teams", [])
            if any(team in user_teams for team in required_teams):
                matched_response = response_data
                matched_key = key
                break
            else:
                # Pas les permissions nécessaires
                team_list = ", ".join(required_teams)
                return (
                    f"🔒 **Accès restreint**\n\nJe n'ai pas accès à des informations sur ce sujet dans vos documents disponibles.\n\n"
                    f"Pour cette question, vous devez avoir accès à l'équipe : **{team_list}**\n\n"
                    f"Contactez votre manager ou l'équipe {required_teams[0]} pour plus d'informations.",
                    [],
                    "none"
                )
    
    # 2. Si pas de match, réponse par défaut avec suggestions
    if not matched_response:
        return (
            """❓ **Question non reconnue**

Je n'ai pas trouvé de réponse exacte à votre question dans ma base de connaissances.

**Voici ce que je peux faire :**
- Reformuler votre question avec d'autres termes
- Explorer les sujets disponibles ci-dessous

**💡 Questions suggérées :**

**RH :**
- "Quelle est la politique de remboursement ?"
- "Comment gérer une demande de congé parental ?"
- "Procédure d'onboarding nouveau salarié"
- "Politique de télétravail"

**Finance :**
- "Quel est le budget marketing Q1 ?"
- "Comment valider une dépense supérieure à 10 000€ ?"
- "Procédure de remboursement des frais"

**Support :**
- "Comment escalader un ticket prioritaire ?"
- "Quels sont les SLA par type de ticket ?"
- "Comment créer un ticket support ?"

**Self-Care :**
- "Mon produit ne s'allume pas, que faire ?"
- "Comment réinitialiser mon mot de passe ?"

**Astuce :** Essayez d'utiliser des mots-clés spécifiques de votre domaine !
""",
            [],
            "low"
        )
    
    # 3. Récupérer les sources complètes
    sources = []
    source_ids = matched_response.get("sources", [])
    
    for source_id in source_ids:
        doc = get_document_by_id(source_id, documents)
        if doc:
            # Vérifier que l'utilisateur a accès au document
            doc_team = doc.get("team", "")
            user_teams = user_permissions.get("teams", [])
            public_teams = ["Self-Care", "Support", "Academy"]
            
            if doc_team in public_teams or doc_team in user_teams:
                sources.append({
                    "id": doc.get("id", ""),
                    "title": doc.get("title", ""),
                    "content": doc.get("content", ""),
                    "product": doc.get("product", ""),
                    "category": doc.get("category", ""),
                    "team": doc.get("team", ""),
                    "last_updated": doc.get("last_updated", "")
                })
    
    # 4. Retourner la réponse avec ses sources et score de confiance
    return (
        matched_response.get("response", ""),
        sources,
        matched_response.get("confidence", "medium")
    )


def get_available_questions() -> Dict[str, List[str]]:
    """
    Retourne la liste des questions disponibles par catégorie
    
    Returns:
        Dictionnaire {catégorie: [liste de questions]}
    """
    responses = load_responses()
    
    questions_by_category = {
        "RH": [],
        "Finance": [],
        "Support": [],
        "Self-Care": [],
        "Academy": []
    }
    
    for key, response_data in responses.items():
        patterns = response_data.get("query_patterns", [])
        if patterns:
            # Prendre le premier pattern comme question exemple
            example_question = patterns[0].capitalize()
            
            # Catégoriser selon les équipes requises
            required_teams = response_data.get("required_teams", [])
            
            if not required_teams:
                questions_by_category["Support"].append(example_question)
            elif "RH" in required_teams:
                questions_by_category["RH"].append(example_question)
            elif "Finance" in required_teams:
                questions_by_category["Finance"].append(example_question)
            elif "Self-Care" in required_teams:
                questions_by_category["Self-Care"].append(example_question)
            elif "Academy" in required_teams:
                questions_by_category["Academy"].append(example_question)
    
    return questions_by_category
