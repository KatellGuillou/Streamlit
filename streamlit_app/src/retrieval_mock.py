"""
Module de retrieval mock (simulation)
Simule un système de retrieval en matchant par mots-clés
"""

import json
import os
from typing import List, Dict


def load_documents() -> List[Dict]:
    """
    Charge les documents depuis le fichier JSON
    
    Returns:
        Liste des documents
    """
    try:
        # Chemin relatif au fichier
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


def match_keywords(query: str, document: Dict) -> float:
    """
    Calcule un score de matching simple entre la query et les keywords du document
    
    Args:
        query: Question de l'utilisateur
        document: Document à scorer
        
    Returns:
        Score entre 0 et 1 (1 = match parfait)
    """
    # Normalisation de la query
    query_words = set(query.lower().split())
    
    # Récupération des keywords du document
    doc_keywords = set([kw.lower() for kw in document.get("keywords", [])])
    
    # Ajout du titre et du contenu pour améliorer le matching
    title_words = set(document.get("title", "").lower().split())
    content_words = set(document.get("content", "").lower().split())
    
    # Combinaison de tous les termes du document
    all_doc_terms = doc_keywords | title_words | content_words
    
    if not all_doc_terms:
        return 0.0
    
    # Calcul de l'intersection
    common_words = query_words & all_doc_terms
    
    if not common_words:
        return 0.0
    
    # Score basé sur le ratio de mots communs
    # Bonus si keywords match (plus pertinent que title/content)
    keyword_matches = query_words & doc_keywords
    score = len(common_words) / len(query_words)
    
    # Bonus si les keywords spécifiques matchent
    if keyword_matches:
        score += 0.3 * (len(keyword_matches) / len(doc_keywords))
    
    return min(score, 1.0)


def retrieve_documents(
    query: str,
    user_permissions: Dict,
    top_k: int = 5
) -> List[Dict]:
    """
    Simule un retrieval en matchant les mots-clés puis filtre par permissions
    
    Args:
        query: Question de l'utilisateur
        user_permissions: Permissions de l'utilisateur (teams, role, etc.)
        top_k: Nombre maximum de documents à retourner
        
    Returns:
        Liste des documents les plus pertinents et accessibles
    """
    documents = load_documents()
    
    if not documents:
        return []
    
    # 1. Calculer les scores pour tous les documents
    scored_docs = []
    for doc in documents:
        score = match_keywords(query, doc)
        if score > 0:
            scored_docs.append({
                **doc,
                "score": score
            })
    
    # 2. Filtrer par permissions (vérifier que l'équipe est dans les permissions)
    user_teams = user_permissions.get("teams", [])
    filtered_docs = []
    
    for doc in scored_docs:
        doc_team = doc.get("team", "")
        
        # Documents publics (Self-Care, Support, Academy accessibles à tous)
        public_teams = ["Self-Care", "Support", "Academy"]
        
        if doc_team in public_teams or doc_team in user_teams:
            filtered_docs.append(doc)
    
    # 3. Trier par score décroissant et limiter au top_k
    filtered_docs.sort(key=lambda x: x["score"], reverse=True)
    
    return filtered_docs[:top_k]


def count_accessible_documents(user_permissions: Dict) -> int:
    """
    Compte le nombre de documents accessibles pour un utilisateur
    
    Args:
        user_permissions: Permissions de l'utilisateur
        
    Returns:
        Nombre de documents accessibles
    """
    documents = load_documents()
    user_teams = user_permissions.get("teams", [])
    public_teams = ["Self-Care", "Support", "Academy"]
    
    accessible_count = 0
    for doc in documents:
        doc_team = doc.get("team", "")
        if doc_team in public_teams or doc_team in user_teams:
            accessible_count += 1
    
    return accessible_count
