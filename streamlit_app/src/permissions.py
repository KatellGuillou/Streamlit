"""
Module de gestion des permissions utilisateur
Définit les utilisateurs et leurs droits d'accès aux documents
"""

from typing import Dict

# Définition des utilisateurs et leurs permissions
USERS: Dict[str, Dict] = {
    "Sophie (RH)": {
        "teams": ["RH"],
        "role": "conseiller",
        "accessible_docs": 12
    },
    "Marc (Finance)": {
        "teams": ["Finance"],
        "role": "conseiller",
        "accessible_docs": 8
    },
    "Admin": {
        "teams": ["RH", "Finance", "Legal", "IT", "Support", "Self-Care", "Academy"],
        "role": "admin",
        "accessible_docs": 20
    }
}


def get_user_permissions(username: str) -> Dict:
    """
    Récupère les permissions d'un utilisateur
    
    Args:
        username: Nom de l'utilisateur
        
    Returns:
        Dictionnaire contenant les permissions de l'utilisateur
        (teams, role, accessible_docs)
    """
    return USERS.get(username, {
        "teams": [],
        "role": "guest",
        "accessible_docs": 0
    })


def has_team_access(user_permissions: Dict, required_teams: list) -> bool:
    """
    Vérifie si l'utilisateur a accès à au moins une des équipes requises
    
    Args:
        user_permissions: Permissions de l'utilisateur
        required_teams: Liste des équipes autorisées pour la ressource
        
    Returns:
        True si l'utilisateur a accès, False sinon
    """
    if not required_teams:
        # Si aucune équipe requise, accès public
        return True
    
    user_teams = user_permissions.get("teams", [])
    return any(team in user_teams for team in required_teams)
