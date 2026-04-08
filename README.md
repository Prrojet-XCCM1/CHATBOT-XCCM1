# IAXCCM - Système Multi-Agents Éducatif

**IAXCCM** (*Education Multi-Agent System*) est le cœur conversationnel intelligent de la plateforme XCCM1. Construit en Python, ce système d'agents est conçu pour fournir des tuteurs spécialisés et interactifs aux étudiants. Il s'appuie sur des modèles de pointe (LLM via OpenRouter/OpenAI) combinés à la connaissance contextuelle sécurisée du backend de l'école.

## 🤖 Architecture des Agents

L'écosystème comprend plusieurs agents fonctionnant de manière concertée grâce au `RouterAgent` :

1. **Agents Spécialisés (Maths, Physique...)** : Tuteurs disciplinaires entraînés pour répondre à des requêtes précises selon le cours actif.
2. **StudentAssistantAgent** : Agent global d'assistance générale. Il est branché au client RAG pour injecter du contexte et gère la **pédagogie adaptative** en fonction du niveau calculé de l'étudiant (ex: "Explique simplement, cet étudiant a un niveau de 30/100").
3. **NotebookAgent** : Assistant privé confiné. Il n'utilise que la base de connaissance limitée aux notes et fichiers personnels de l'étudiant pour assurer des réponses **sans hallucination**.

## 🔄 Interaction avec `XCCM1-LLM-SERVICE`

Les agents ne sont pas "déconnectés" du reste de la plateforme :
1. Ils utilisent le **LLMServiceClient** natif pour requêter l'API RAG (`/search`).
2. Ils s'informent du niveau de l'étudiant (`/knowledge`) avant de formuler une explication.

---

## 🛠️ Pré-requis

- **Python 3.9+**
- Un compte et une clé API **OpenRouter** ou **OpenAI** configurés.
- (Le service `XCCM1-LLM-SERVICE` doit tourner sur le port 8000 pour que le RAG fonctionne).

---

## 📦 Installation & Déploiement Local

Le serveur Multi-Agent se trouve dans le sous-dossier de travail :

```bash
cd education_multiagent
```

### 1. Environnement Virtuel
```bash
python3 -m venv venv
```

### 2. Activation de l'Environnement
- **Sur Linux / macOS :**
  ```bash
  source venv/bin/activate
  ```
- **Sur Windows (PowerShell) :**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### 3. Installation des Dépendances
```bash
pip install -r requirements.txt
```

### 4. Variables d'Environnement
Créez un fichier `.env` ou configurez ces variables en local :
```env
OPENROUTER_API_KEY=votre_cle_api_ici
OPENROUTER_MODEL=anthropic/claude-3-haiku # Par exemple
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

---

## 🏃 Lancement du Serveur

Une fois l'environnement prêt, démarrez l'application web ou le script de lancement (Flask/Uvicorn tournant par défaut sur le port local `5000`) :

```bash
python run.py
```
*(OU `flask run` selon l'entrypoint configuré dans votre application)*