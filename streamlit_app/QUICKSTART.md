# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1. Installer Streamlit
```bash
pip install streamlit
```

### 2. Lancer l'application
```bash
cd streamlit_app
streamlit run app.py
```

### 3. Tester dans le navigateur
L'application s'ouvre automatiquement à `http://localhost:8501`

## 🎯 Scénarios de démonstration

### Scénario 1 : Test des permissions RH
1. Sélectionner **Sophie (RH)** dans la sidebar
2. Poser : *"Quelle est la politique de remboursement ?"*
3. ✅ **Résultat attendu** : Réponse complète avec 2 sources

### Scénario 2 : Test du refus d'accès
1. Rester connecté comme **Sophie (RH)**
2. Poser : *"Quel est le budget marketing Q1 ?"*
3. ✅ **Résultat attendu** : Message "🔒 Accès restreint"

### Scénario 3 : Test Admin (accès total)
1. Sélectionner **Admin** dans la sidebar
2. Poser : *"Quel est le budget marketing Q1 ?"*
3. ✅ **Résultat attendu** : Réponse complète avec détails financiers

### Scénario 4 : Test question inconnue
1. Poser : *"Quel est le salaire du CEO ?"*
2. ✅ **Résultat attendu** : Message avec suggestions de questions

### Scénario 5 : Test documents publics (Self-Care)
1. Sélectionner n'importe quel utilisateur
2. Poser : *"Mon produit ne s'allume pas"*
3. ✅ **Résultat attendu** : Guide de dépannage accessible à tous

## 💡 Questions pré-testées

### RH (Sophie + Admin)
```
Quelle est la politique de remboursement ?
Comment gérer une demande de congé parental ?
Procédure d'onboarding nouveau salarié
Politique de télétravail
```

### Finance (Marc + Admin)
```
Quel est le budget marketing Q1 ?
Comment valider une dépense de 10000 euros ?
Procédure de remboursement des frais
```

### Support (Tous)
```
Comment escalader un ticket prioritaire ?
Quels sont les SLA par type de ticket ?
Comment créer un ticket support ?
```

### Self-Care (Tous)
```
Mon produit ne s'allume pas
Réinitialiser mon mot de passe
```

### Academy (Tous)
```
Comment accéder au module de formation CRM ?
```

## 📊 Vérifications

### ✅ Checklist avant démonstration

- [ ] L'application démarre sans erreur
- [ ] Les 3 utilisateurs sont disponibles dans le sélecteur
- [ ] Les permissions s'affichent correctement dans la sidebar
- [ ] Une question RH retourne une réponse avec sources
- [ ] Une question sans permission affiche un message d'erreur clair
- [ ] Les sources sont expandables et affichent les métadonnées
- [ ] Le score de confiance s'affiche avec l'emoji approprié
- [ ] Les boutons feedback (👍 👎 📋) fonctionnent
- [ ] Le compteur de queries s'incrémente
- [ ] Le bouton "Nouvelle conversation" réinitialise le chat

## 🐛 Résolution de problèmes

### Erreur "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### Erreur "FileNotFoundError"
Assurez-vous d'être dans le bon dossier :
```bash
cd streamlit_app
pwd  # Doit afficher: .../streamlit_app
streamlit run app.py
```

### L'application ne répond pas aux questions
Vérifiez les fichiers JSON :
```bash
python3 -m json.tool data/mock_documents.json
python3 -m json.tool data/mock_responses.json
```

### Port déjà utilisé
Si le port 8501 est occupé :
```bash
streamlit run app.py --server.port 8502
```

## 🎨 Personnalisation rapide

### Ajouter une nouvelle question

1. **Ajouter un document** dans `data/mock_documents.json`
2. **Ajouter une réponse** dans `data/mock_responses.json`
3. Relancer l'app (Ctrl+C puis `streamlit run app.py`)

### Modifier les permissions

Éditer `src/permissions.py` :
```python
USERS = {
    "Nouveau User": {
        "teams": ["RH", "Finance"],
        "role": "manager",
        "accessible_docs": 15
    }
}
```

## 📞 Support

Pour des questions ou problèmes :
- Consulter le `README.md` complet
- Vérifier les logs dans le terminal

---

**Bon test ! 🚀**
