# 🤖 Mayday Assistant Conversationnel - POC Mode Mock

## 📋 Description

POC (Proof of Concept) d'assistant conversationnel pour Mayday avec **réponses pré-générées**.

Ce système simule un assistant RAG (Retrieval Augmented Generation) avec :
- ✅ Interface conversationnelle intuitive
- ✅ Gestion des permissions utilisateur par équipe
- ✅ Citations de sources avec métadonnées complètes
- ✅ Score de confiance pour chaque réponse
- ✅ 15 questions types pré-générées
- ✅ **Zéro coût** (pas d'API externe, pas de clé requise)

## 🏗️ Architecture

```
streamlit_app/
├── app.py                          # Interface Streamlit principale
├── requirements.txt                # Dépendances Python
├── README.md                       # Documentation
├── data/
│   ├── mock_documents.json        # 20 documents fictifs Mayday
│   └── mock_responses.json        # 15 réponses pré-générées
└── src/
    ├── __init__.py
    ├── permissions.py             # Gestion permissions utilisateur
    ├── utils.py                   # Fonctions utilitaires
    ├── retrieval_mock.py          # Matching par mots-clés
    └── generation_mock.py         # Sélection réponses mockées
```

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip

### Installation rapide

```bash
# 1. Se placer dans le dossier
cd streamlit_app

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 👥 Utilisateurs de démonstration

L'application propose **3 profils utilisateurs** avec des permissions différentes :

### 1. Sophie (RH)
- **Équipes :** RH uniquement
- **Rôle :** Conseiller
- **Accès :** 12 documents (RH + documents publics)
- **Use case :** Conseillère RH qui a besoin d'informations sur les procédures internes, congés, onboarding, etc.

### 2. Marc (Finance)
- **Équipes :** Finance uniquement
- **Rôle :** Conseiller
- **Accès :** 8 documents (Finance + documents publics)
- **Use case :** Conseiller financier qui consulte les budgets, validations de dépenses, clôtures comptables, etc.

### 3. Admin
- **Équipes :** Toutes (RH, Finance, Legal, IT, Support, Self-Care, Academy)
- **Rôle :** Administrateur
- **Accès :** 20 documents (accès total)
- **Use case :** Manager ou direction avec accès complet à toute la knowledge base

## 💡 Questions disponibles

### 🏢 RH (accessible par Sophie + Admin)
- Quelle est la politique de remboursement ?
- Comment gérer une demande de congé parental ?
- Procédure d'onboarding nouveau salarié
- Politique de télétravail
- Évaluation annuelle et performance
- Formation continue et budget CPF

### 💰 Finance (accessible par Marc + Admin)
- Quel est le budget marketing Q1 ?
- Comment valider une dépense supérieure à 10 000€ ?
- Procédure de remboursement des frais
- Gestion de la trésorerie
- Facturation clients

### 🎧 Support (accessible par tous)
- Comment escalader un ticket prioritaire ?
- Quels sont les SLA par type de ticket ?
- Procédure de création de ticket
- Gestion des réclamations clients

### 🛠️ Self-Care (accessible par tous)
- Mon produit ne s'allume pas, que faire ?
- Comment réinitialiser mon mot de passe ?

### 🎓 Academy (accessible par tous)
- Comment accéder au module de formation CRM ?

## 🎯 Fonctionnalités principales

### 1. Interface conversationnelle
- Chat en temps réel style ChatGPT
- Historique de conversation persistant
- Support multi-tour (follow-ups)

### 2. Gestion des permissions
- Filtrage automatique des documents par équipe
- Messages d'erreur clairs si pas de permission
- Affichage des permissions dans la sidebar

### 3. Citations de sources
- Chaque réponse cite ses sources avec [Source X]
- Métadonnées complètes (produit, catégorie, équipe, date MAJ)
- Expandable sections pour consulter le contenu des sources

### 4. Score de confiance
- 🟢 **Haute** : 3+ sources concordantes
- 🟡 **Moyenne** : Sources partielles
- 🔴 **Faible** : Peu de sources
- ⚪ **Aucune** : Pas de source disponible

### 5. Feedback utilisateur
- Boutons 👍 👎 pour noter les réponses
- Bouton 📋 pour copier la réponse

### 6. Statistiques
- Nombre de queries
- Nombre de messages
- Documents accessibles par utilisateur

## 🔧 Fonctionnement technique

### Matching par mots-clés
Le système utilise un **matching simple** sans IA :
1. Extraction des mots-clés de la question
2. Comparaison avec les keywords des documents
3. Calcul d'un score de pertinence
4. Filtrage par permissions utilisateur
5. Retour des top 5 documents

### Sélection de réponses
Les réponses sont **pré-générées** et stockées dans `mock_responses.json` :
1. La question est comparée à des patterns prédéfinis
2. Si match trouvé → vérification des permissions
3. Si permissions OK → retour de la réponse + sources
4. Sinon → message d'erreur clair ou suggestions

### Gestion des cas limites

**Cas 1 : Question sans permission**
```
🔒 Accès restreint

Je n'ai pas accès à des informations sur ce sujet dans vos documents disponibles.
Pour cette question, vous devez avoir accès à l'équipe : Finance
```

**Cas 2 : Question inconnue**
```
❓ Question non reconnue

Je n'ai pas trouvé de réponse exacte...
💡 Questions suggérées : [liste]
```

## 📊 Données mockées

### Documents (20)
- **8 documents RH** : Remboursements, congés, onboarding, télétravail, évaluations, formations
- **5 documents Finance** : Budget, validations, trésorerie, facturation, comptabilité
- **4 documents Support** : Escalades, SLA, tickets, réclamations
- **3 documents Self-Care** : Dépannage produit, mot de passe, compte

### Réponses (15)
Chaque réponse contient :
- **query_patterns** : Variations de la question
- **response** : Texte de réponse (200-300 mots, Markdown)
- **sources** : IDs des documents sources
- **confidence** : Niveau de confiance (high/medium/low/none)
- **required_teams** : Équipes autorisées

## 🎨 Customisation

### Ajouter une nouvelle question

1. **Ajouter le document** dans `data/mock_documents.json` :
```json
{
  "id": "kb_021",
  "title": "Nouveau document",
  "content": "Contenu détaillé...",
  "product": "Knowledge",
  "team": "RH",
  "category": "Procédures",
  "last_updated": "2025-01-23",
  "keywords": ["mot1", "mot2", "mot3"]
}
```

2. **Ajouter la réponse** dans `data/mock_responses.json` :
```json
"nouvelle_question": {
  "query_patterns": ["question 1", "question 2"],
  "response": "Réponse avec [Source 1]",
  "sources": ["kb_021"],
  "confidence": "high",
  "required_teams": ["RH"]
}
```

3. **Relancer l'app** : Les changements sont automatiquement pris en compte

### Ajouter un nouvel utilisateur

Modifier `src/permissions.py` :
```python
USERS = {
    "Nouveau (Legal)": {
        "teams": ["Legal"],
        "role": "conseiller",
        "accessible_docs": 5
    }
}
```

## 🚦 Tests

### Test de permissions
1. Connectez-vous comme **Sophie (RH)**
2. Posez la question : *"Quel est le budget marketing Q1 ?"*
3. ✅ Attendu : Message d'accès restreint (document Finance)

### Test de retrieval
1. Connectez-vous comme **Admin**
2. Posez la question : *"Politique de remboursement"*
3. ✅ Attendu : Réponse complète avec 2 sources

### Test de question inconnue
1. Posez : *"Quel est le salaire du CEO ?"*
2. ✅ Attendu : Message "Question non reconnue" avec suggestions

## 📈 Améliorations futures

Pour passer en production, considérez :

### Phase 1 : Mock avancé
- [ ] Ajout de 50+ documents réalistes
- [ ] 30+ réponses pré-générées
- [ ] Synonymes et variations linguistiques
- [ ] Gestion des fautes de frappe

### Phase 2 : RAG réel
- [ ] Intégration avec OpenAI API
- [ ] Vector database (Pinecone, Weaviate)
- [ ] Embeddings pour semantic search
- [ ] Fine-tuning du modèle

### Phase 3 : Production
- [ ] Authentification SSO
- [ ] Base de données PostgreSQL
- [ ] Analytics et tracking
- [ ] A/B testing
- [ ] API REST

## 🐛 Dépannage

### L'app ne démarre pas
```bash
# Vérifier Python
python --version  # Doit être 3.10+

# Réinstaller les dépendances
pip install --upgrade streamlit
```

### Erreur "FileNotFoundError"
Assurez-vous d'être dans le dossier `streamlit_app/` avant de lancer :
```bash
cd streamlit_app
streamlit run app.py
```

### L'app ne répond pas aux questions
Vérifiez que les fichiers JSON sont valides :
```bash
python -m json.tool data/mock_documents.json
python -m json.tool data/mock_responses.json
```

## 📞 Support

Pour toute question ou suggestion :
- 📧 Email : ai-team@mayday.com
- 💬 Slack : #mayday-ai-assistant
- 📝 GitHub Issues : (à créer)

## 📄 Licence

© 2025 Mayday - Usage interne uniquement

---

**Développé avec ❤️ par l'équipe AI de Mayday**

*Version 1.0.0 - Mode POC - Janvier 2025*
