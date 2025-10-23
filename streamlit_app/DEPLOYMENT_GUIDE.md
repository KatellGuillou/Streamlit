# 🚀 Guide de Déploiement Streamlit Cloud

## 📋 Vue d'ensemble

Votre application Mayday Assistant sera déployée sur **Streamlit Cloud** (gratuit) et accessible via une URL publique.

**Repository GitHub :** `KatellGuillou/Streamlit`  
**Branche :** `cursor/build-mock-rag-assistant-with-streamlit-0978`  
**Dossier app :** `streamlit_app/`

---

## 🌐 Étapes de déploiement

### Étape 1 : Créer un compte Streamlit Cloud

1. Allez sur **https://streamlit.io/cloud**
2. Cliquez sur **"Sign up"** ou **"Get started"**
3. **Connectez-vous avec GitHub** (obligatoire)
4. Autorisez Streamlit à accéder à vos repositories

### Étape 2 : Créer une nouvelle app

1. Une fois connecté, cliquez sur **"New app"** (ou "Create app")

2. Remplissez les informations :
   
   **Repository :**  
   ```
   KatellGuillou/Streamlit
   ```
   
   **Branch :**  
   ```
   cursor/build-mock-rag-assistant-with-streamlit-0978
   ```
   
   **Main file path :**  
   ```
   streamlit_app/app.py
   ```
   
   **App URL (optionnel) :**  
   ```
   mayday-assistant (ou votre choix)
   ```

3. Cliquez sur **"Deploy!"**

### Étape 3 : Attendre le déploiement

- ⏱️ Le déploiement prend **2-5 minutes**
- Vous verrez les logs en temps réel
- Streamlit installe automatiquement les dépendances depuis `requirements.txt`

### Étape 4 : Accéder à votre application

Une fois déployé, votre app sera accessible à :

```
https://mayday-assistant-[random].streamlit.app
```

ou

```
https://[votre-username]-streamlit-[nom-app].streamlit.app
```

**Exemple :** `https://katellguillou-streamlit-mayday-assistant.streamlit.app`

---

## 🎯 Configuration avancée (optionnel)

### Personnaliser l'URL

Dans les paramètres de l'app sur Streamlit Cloud :
- Settings → General → App URL
- Choisissez un nom personnalisé

### Configurer les secrets (si besoin futur)

Si vous ajoutez des API keys plus tard :
1. Settings → Secrets
2. Ajoutez vos secrets au format TOML :
```toml
OPENAI_API_KEY = "sk-..."
```

### Mettre à jour l'app

Streamlit Cloud **se met à jour automatiquement** :
- À chaque push sur la branche GitHub
- Ou cliquez sur "Reboot app" manuellement

---

## 📱 Partager votre application

### Lien public
```
https://[votre-url].streamlit.app
```

### QR Code
Streamlit Cloud génère automatiquement un QR code pour mobile

### Embed
Vous pouvez embed l'app dans un iframe :
```html
<iframe src="https://[votre-url].streamlit.app" 
        width="100%" height="800px"></iframe>
```

---

## 🔧 Résolution de problèmes

### Erreur : "No module named 'streamlit'"
✅ **Solution :** Vérifiez que `requirements.txt` est bien à la racine de `streamlit_app/`

### Erreur : "FileNotFoundError"
✅ **Solution :** Vérifiez que le **Main file path** est correct :
```
streamlit_app/app.py
```

### Erreur : "Port already in use"
✅ **Solution :** Ignorez cette erreur en local. Sur Streamlit Cloud, elle ne se produira pas.

### L'app ne démarre pas
✅ **Solutions :**
1. Vérifiez les logs de déploiement
2. Cliquez sur "Reboot app"
3. Vérifiez que tous les fichiers sont bien committé sur GitHub

### Erreur d'import des modules
✅ **Solution :** Assurez-vous que la structure des fichiers est correcte :
```
streamlit_app/
├── app.py          ✅
├── requirements.txt ✅
├── data/           ✅
│   ├── mock_documents.json
│   └── mock_responses.json
└── src/            ✅
    ├── __init__.py
    ├── permissions.py
    └── ...
```

---

## 📊 Limites du plan gratuit

**Streamlit Cloud (Free tier) :**
- ✅ Apps publiques illimitées
- ✅ 1 app privée
- ✅ 1 GB RAM par app
- ✅ 1 CPU par app
- ✅ Pas de limite de visiteurs
- ✅ Auto-sleep après 7 jours d'inactivité (se réveille automatiquement)

**Pour votre POC Mayday :** C'est largement suffisant ! 🎉

---

## 🔐 Rendre l'app privée (optionnel)

Par défaut, l'app est **publique**. Pour la rendre privée :

1. Settings → Sharing
2. Cochez "Require viewers to log in"
3. Ajoutez les emails autorisés

**Note :** Les apps privées nécessitent un compte Streamlit Cloud (gratuit) pour y accéder.

---

## 🎨 Personnaliser le domaine (Pro uniquement)

Le plan gratuit utilise : `*.streamlit.app`

Pour un domaine personnalisé (`assistant.mayday.com`) :
- Passez au plan **Teams** (99$/mois)
- Ou utilisez un reverse proxy (Cloudflare, Vercel)

---

## 📈 Analytics

Streamlit Cloud fournit des analytics de base :
- Nombre de visiteurs
- Sessions actives
- Temps de chargement

Pour des analytics avancés, intégrez Google Analytics dans votre app.

---

## ✅ Checklist finale

Avant de déployer, vérifiez :

- [x] Code poussé sur GitHub
- [x] Branch correcte : `cursor/build-mock-rag-assistant-with-streamlit-0978`
- [x] `requirements.txt` présent dans `streamlit_app/`
- [x] `app.py` fonctionne en local
- [x] Fichiers JSON valides
- [x] Compte Streamlit Cloud créé
- [ ] App déployée sur Streamlit Cloud
- [ ] URL partagée avec l'équipe

---

## 🎊 Une fois déployé

**Testez votre app en ligne :**

1. Changez d'utilisateur (Sophie, Marc, Admin)
2. Posez les questions disponibles
3. Vérifiez les permissions
4. Partagez le lien avec votre équipe ! 🚀

---

## 📞 Support

**Streamlit Cloud :**
- Documentation : https://docs.streamlit.io/streamlit-community-cloud
- Forum : https://discuss.streamlit.io
- Status : https://streamlit.statuspage.io

**Votre app :**
- README : `/streamlit_app/README.md`
- Quickstart : `/streamlit_app/QUICKSTART.md`

---

**Bon déploiement ! 🎉**

*Temps estimé : 5-10 minutes pour le déploiement complet*
