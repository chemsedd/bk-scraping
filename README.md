# Spider Scrapy avec Défilement Infini

Spider Scrapy pour extraire des données de sites web avec défilement infini et boutons "charger plus", avec gestion optimisée de la mémoire.

## 🚀 Fonctionnalités

- Défilement automatique et clic sur boutons "charger plus"
- Gestion mémoire optimisée pour traiter des centaines d'éléments
- Traitement par lots et suppression automatique des éléments traités

## 📋 Installation

```bash
pip install scrapy selenium webdriver-manager
```

## ⚙️ Configuration

Personnalisez ces sélecteurs dans le fichier :

```python
self.load_more_selector = 'button.load-more'  # Bouton "charger plus"
self.item_selector = '.item'                  # Éléments à scraper
```

## 🔧 Utilisation

```bash
# Exécution directe
python endless_scroll_spider.py

# Avec Scrapy CLI
scrapy crawl endless_scroll_spider -a start_url="https://votre-site.com"
```

## 🎯 Personnalisation

Modifiez `extract_item_data()` selon vos besoins :

```python
def extract_item_data(self, item):
    title = item.find_element(By.CSS_SELECTOR, '.titre').text
    price = item.find_element(By.CSS_SELECTOR, '.prix').text
    return {'titre': title, 'prix': price}
```

## ⚠️ Notes

- Mode headless par défaut (supprimez `--headless` pour débogage)
- Ajustez les sélecteurs selon votre site cible
