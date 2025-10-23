#!/bin/bash

################################################################################
# Script de déploiement Git pour Streamlit app
# Usage: ./deploy.sh [commit-message]
# 
# Ce script va :
# 1. Vérifier l'état du repository Git
# 2. Ajouter tous les fichiers modifiés
# 3. Créer un commit
# 4. Pusher sur GitHub
################################################################################

set -e  # Exit on error

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/KatellGuillou/Streamlit.git"
REPO_NAME="KatellGuillou/Streamlit"
DEFAULT_BRANCH="main"

echo -e "${BLUE}🚀 Déploiement de l'app Streamlit sur GitHub...${NC}\n"

################################################################################
# 1. Vérifier que nous sommes dans le bon dossier
################################################################################

if [ ! -d "streamlit_app" ]; then
    echo -e "${RED}❌ Erreur: Le dossier 'streamlit_app/' n'existe pas${NC}"
    echo "   Assurez-vous d'être à la racine du projet"
    exit 1
fi

echo -e "${GREEN}✓${NC} Dossier streamlit_app/ trouvé"

################################################################################
# 2. Vérifier/Initialiser Git
################################################################################

if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠${NC}  Git n'est pas initialisé. Initialisation..."
    git init
    echo -e "${GREEN}✓${NC} Repository Git initialisé"
else
    echo -e "${GREEN}✓${NC} Repository Git déjà initialisé"
fi

################################################################################
# 3. Configurer le remote (si nécessaire)
################################################################################

if git remote get-url origin &>/dev/null; then
    CURRENT_REMOTE=$(git remote get-url origin)
    echo -e "${GREEN}✓${NC} Remote origin déjà configuré: ${CURRENT_REMOTE}"
    
    # Vérifier si c'est le bon remote
    if [[ "$CURRENT_REMOTE" != *"KatellGuillou/Streamlit"* ]]; then
        echo -e "${YELLOW}⚠${NC}  Le remote actuel ne correspond pas au repo attendu"
        echo "   Remote actuel: $CURRENT_REMOTE"
        echo "   Remote attendu: $REPO_URL"
        read -p "   Voulez-vous changer le remote ? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git remote set-url origin "$REPO_URL"
            echo -e "${GREEN}✓${NC} Remote origin mis à jour"
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC}  Configuration du remote origin..."
    git remote add origin "$REPO_URL"
    echo -e "${GREEN}✓${NC} Remote origin configuré: $REPO_URL"
fi

################################################################################
# 4. Vérifier la branche actuelle
################################################################################

CURRENT_BRANCH=$(git branch --show-current)

if [ -z "$CURRENT_BRANCH" ]; then
    echo -e "${YELLOW}⚠${NC}  Aucune branche active. Création de la branche ${DEFAULT_BRANCH}..."
    git checkout -b "$DEFAULT_BRANCH"
    CURRENT_BRANCH="$DEFAULT_BRANCH"
    echo -e "${GREEN}✓${NC} Branche ${DEFAULT_BRANCH} créée"
else
    echo -e "${GREEN}✓${NC} Branche actuelle: ${CURRENT_BRANCH}"
fi

################################################################################
# 5. Vérifier s'il y a des changements
################################################################################

if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}ℹ${NC}  Aucun changement détecté (working tree clean)"
    echo "   Vérification des commits non pushés..."
    
    # Vérifier s'il y a des commits à pusher
    git fetch origin "$CURRENT_BRANCH" 2>/dev/null || true
    
    if git log origin/"$CURRENT_BRANCH".."$CURRENT_BRANCH" --oneline 2>/dev/null | grep -q .; then
        echo -e "${YELLOW}⚠${NC}  Des commits locaux ne sont pas sur GitHub"
        read -p "   Voulez-vous pusher ces commits ? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}📤 Push vers GitHub...${NC}"
            git push -u origin "$CURRENT_BRANCH"
            echo -e "${GREEN}✅ Push réussi !${NC}"
        fi
    else
        echo -e "${GREEN}✅ Tout est à jour sur GitHub !${NC}"
    fi
    
    echo -e "\n${BLUE}📦 Repository:${NC} https://github.com/$REPO_NAME"
    echo -e "${BLUE}🌿 Branche:${NC} $CURRENT_BRANCH"
    echo -e "${BLUE}🔗 Déploiement Streamlit Cloud:${NC} https://streamlit.io/cloud"
    exit 0
fi

echo -e "${YELLOW}ℹ${NC}  Changements détectés:"
git status --short

################################################################################
# 6. Ajouter les fichiers
################################################################################

echo -e "\n${BLUE}📝 Ajout des fichiers...${NC}"

# Exclure les fichiers inutiles
if [ ! -f ".gitignore" ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml
EOL
fi

git add .
echo -e "${GREEN}✓${NC} Fichiers ajoutés au staging"

################################################################################
# 7. Créer le commit
################################################################################

# Message de commit (utiliser l'argument ou demander)
if [ -z "$1" ]; then
    echo -e "\n${BLUE}💬 Message de commit:${NC}"
    read -p "   Entrez un message (ou appuyez sur Enter pour le message par défaut): " COMMIT_MSG
    
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="Update Streamlit app - $(date '+%Y-%m-%d %H:%M')"
    fi
else
    COMMIT_MSG="$1"
fi

echo -e "${BLUE}📦 Création du commit...${NC}"
git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓${NC} Commit créé: \"$COMMIT_MSG\""

################################################################################
# 8. Push sur GitHub
################################################################################

echo -e "\n${BLUE}📤 Push vers GitHub...${NC}"

# Tenter de pusher
if git push -u origin "$CURRENT_BRANCH" 2>&1 | tee /tmp/git_push.log; then
    echo -e "\n${GREEN}✅ Déploiement terminé avec succès !${NC}"
else
    echo -e "\n${RED}❌ Erreur lors du push${NC}"
    
    # Vérifier si c'est un problème d'authentification
    if grep -q "Authentication failed\|Permission denied" /tmp/git_push.log; then
        echo -e "${YELLOW}⚠${NC}  Problème d'authentification GitHub"
        echo "   Solutions:"
        echo "   1. Vérifiez votre token GitHub (PAT)"
        echo "   2. Ou configurez SSH: https://docs.github.com/en/authentication"
        echo "   3. Ou utilisez: git push (et entrez vos identifiants)"
    fi
    
    exit 1
fi

################################################################################
# 9. Résumé final
################################################################################

echo -e "\n${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ DÉPLOIEMENT RÉUSSI !${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "\n${BLUE}📦 Repository:${NC} https://github.com/$REPO_NAME"
echo -e "${BLUE}🌿 Branche:${NC} $CURRENT_BRANCH"
echo -e "${BLUE}💬 Commit:${NC} \"$COMMIT_MSG\""
echo -e "\n${BLUE}🔗 Prochaine étape:${NC} Déployer sur Streamlit Cloud"
echo -e "   👉 https://streamlit.io/cloud"
echo -e "\n${BLUE}Configuration pour Streamlit Cloud:${NC}"
echo -e "   Repository: ${REPO_NAME}"
echo -e "   Branch: ${CURRENT_BRANCH}"
echo -e "   Main file path: ${YELLOW}streamlit_app/app.py${NC}"
echo -e "\n${GREEN}═══════════════════════════════════════════════════════${NC}"

# Nettoyer
rm -f /tmp/git_push.log
