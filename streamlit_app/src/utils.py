"""
Module utilitaire avec fonctions d'aide
"""

from typing import Tuple


def calculate_confidence_display(confidence: str) -> Tuple[str, str, str]:
    """
    Retourne l'affichage visuel pour le score de confiance
    
    Args:
        confidence: Niveau de confiance ('high', 'medium', 'low', 'none')
        
    Returns:
        Tuple (emoji, message, color_type) pour l'affichage Streamlit
    """
    confidence_mapping = {
        "high": (
            "🟢",
            "Confiance élevée (3+ sources concordantes)",
            "success"
        ),
        "medium": (
            "🟡",
            "Confiance moyenne (sources partielles)",
            "warning"
        ),
        "low": (
            "🔴",
            "Confiance faible (peu de sources)",
            "error"
        ),
        "none": (
            "⚪",
            "Aucune source disponible",
            "info"
        )
    }
    
    return confidence_mapping.get(confidence, confidence_mapping["none"])


def format_source_metadata(source: dict) -> str:
    """
    Formate les métadonnées d'une source pour l'affichage
    
    Args:
        source: Dictionnaire contenant les informations de la source
        
    Returns:
        Chaîne formatée avec les métadonnées
    """
    return (
        f"{source.get('product', 'N/A')} > {source.get('category', 'N/A')} • "
        f"Équipe {source.get('team', 'N/A')} • "
        f"Mis à jour le {source.get('last_updated', 'N/A')}"
    )


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Tronque un texte à une longueur maximale
    
    Args:
        text: Texte à tronquer
        max_length: Longueur maximale (par défaut 200)
        
    Returns:
        Texte tronqué avec "..." si nécessaire
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def is_follow_up_query(query: str) -> bool:
    """
    Détecte si une query est une question de suivi
    
    Args:
        query: Question de l'utilisateur
        
    Returns:
        True si c'est une question de suivi
    """
    follow_up_patterns = [
        "et les",
        "et le",
        "plus de détails",
        "autre chose",
        "et pour",
        "et si",
        "comment",
        "pourquoi"
    ]
    
    query_lower = query.lower().strip()
    
    # Questions très courtes sont souvent des follow-ups
    if len(query_lower.split()) <= 3:
        return True
    
    return any(pattern in query_lower for pattern in follow_up_patterns)
