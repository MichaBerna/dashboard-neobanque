# Dashboard Néobanque

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Formatter: Black](https://img.shields.io/badge/Formatter-Black-000000.svg)](https://github.com/psf/black)
[![Linter: Flake8](https://img.shields.io/badge/Linter-Flake8-222222?logo=flake8)](https://flake8.pycqa.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Introduction
Solution pour Néobanque, permettant d'avoir les éléments financiers des clients mais aussi un score d’éligibilité au prêt. Contient un dashboard et une API permettant d'exploiter un modèle IA.  
Etude de bloc 4 - Dashboard conseiller Néobanque

## Licence
Ce projet est sous licence [MIT](LICENSE). Vous êtes libre de l'utiliser, le modifier et le redistribuer, à condition de citer l'auteur original.

## Installation & lancements

### Globale

Dans le dossier racine :

```bash
# Mise à jour pip
python -m pip install --upgrade pip

# Installation des dépendances et outils
pip install -r requirements.txt

# Activation pre-commit
pre-commit install
```

Quelques commandes utiles :

```bash
# Formattage
ruff format .

# Linter
ruff check --fix .
```

Ces deux commandes sont systématiquement jouées par le commit hook et par le workflow GitHub Actions.

### Dashboard

```bash
# Dossier dashboard
cd dashboard

# Installation des dépendances et outils
pip install -r requirements.txt

# Lancement du serveur pour l'API
streamlit run main.py
```

Le dashboard sera à retrouver sur http://localhost:8501/

### API

```bash
# Dossier API
cd api

# Installation des dépendances et outils
pip install -r requirements.txt

# Lancement du serveur pour l'API
uvicorn main:app --reload
```

L'API sera à retrouver sur http://localhost:8000/

### Modèle IA

Le modèle IA est enregitré dans le dossier **modele**, dans le fichier **modele_prediction_credit.joblib**.
Si vous souhaitez rejouer l'entraînement du modèle et sa sauvegarde :

```bash
# Dossier modèle IA
cd modele/entrainement

# Installation des dépendances et outils
pip install -r requirements.txt
```

Il suffira ensuite de jouer le notebook **neobanque-credit.ipynb**.

**Notes** :
- Les données sont compressées par facilité, GitHub limitant les fichiers uploadés à 100Mo. La décompression est faite dans le notebook.
- Le modèle se base en partie sur le travail effectué sur [Kaggle - Applied Predictive Modelling (Brief Overview)](https://www.kaggle.com/code/moizzz/applied-predictive-modelling-brief-overview/report).

## Présentation des outils utilisés
Ce projet est construit avec Python 3.12.

### Dashboard

- Streamlit : Framework permettant de créer un dashboard interactif sur une application web
- Requests : Pour créer rapidement des requêtes HTTP

Le Dashboard est déployé sur [Streamlit](https://streamlit.io/).

### API

- FastAPI : Framework permettant de créer une API
- Uvicorn : Serveur web ASGI pour déployer notre API

L'API est déployée sur [Render](https://render.com/).

### Modèle IA (entraînement)

- Pandas : Manipulation et analyse de données 
- Numpy : Calculs, opérations sur tableaux et matrices
- Scikit-learn : Machine learning et entraînement de modèles
- Matplotlib : Visualisation graphique 
- Seaborn : Visualisation graphique avancée
- Xgboost : Modèles de boosting extrême
- Imblearn : Traitement des données, SMOTE pour le rééquilibrage des classes
- Joblib : Sauvegarde/chargement de modèles 

### Autres outils

- Ruff : Linter & formatteur de code
- Pre-commit : Exécute automatiquement les vérifications avant chaque commit.
- Commitizen : Standardise les messages de commit ([Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/))

