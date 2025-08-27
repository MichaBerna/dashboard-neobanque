# Dashboard Néobanque

Solution pour Néobanque, permettant d'avoir les éléments financiers des clients mais aussi un score d’éligibilité au prêt. Contient un dashboard et une API permettant d'exploiter un modèle IA.  
Etude de bloc 4 - Dashboard conseiller Néobanque

## Licence
Ce projet est sous licence [MIT](LICENSE). Vous êtes libre de l'utiliser, le modifier et le redistribuer, à condition de citer l'auteur original.

## Installation

```bash
# Mise à jour pip
python -m pip install --upgrade pip

# Installation des dépendances et outils
pip install black flake8 isort pre-commit commitizen

# Activation pre-commit
pre-commit install
```

## Présentation des outils utilisés
Ce projet est construit avec Python 3.12.

Autre outils :
- Black : Formatteur de code (standardise l’indentation, les espaces, etc.).
- Flake8 : Linter (détecte les erreurs de style et les problèmes de syntaxe).
- isort : Trie les imports de manière cohérente.
- pre-commit : Exécute automatiquement les vérifications avant chaque commit.
- commitizen : Standardise les messages de commit ([Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/))

