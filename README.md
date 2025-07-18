# Spider Scrapy avec Défilement Infini

Spider Scrapy pour extraire des données de sites web avec défilement infini et boutons "charger plus", avec gestion optimisée de la mémoire.

## 🚀 Fonctionnalités

- Défilement automatique et clic sur boutons "charger plus"
- Gestion mémoire optimisée pour traiter des centaines d'éléments
- Traitement par lots et suppression automatique des éléments traités

## 📋 Installation

```bash
uv venv
uv sync
```

## ⚙️ Configuration

Personnalisez ces sélecteurs dans le fichier :

```python
self.load_more_selector = 'button.load-more'  # Bouton "charger plus"
self.item_selector = '.item'                  # Éléments à scraper
```

## 🔧 Utilisation

```bash
uv run main.py
```

## ⚠️ Notes

- Mode headless par défaut (supprimez `--headless` pour débogage)
- Ajustez les sélecteurs selon votre site cible
