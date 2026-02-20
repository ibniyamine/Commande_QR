# Dashboard Analyse Commandes QR

Dashboard interactif professionnel pour l'analyse des commandes QR et des montants par compagnie d'assurance.

## 🚀 Installation et Lancement

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement du dashboard
```bash
streamlit run dashboard_qr.py
```

Le dashboard sera accessible dans votre navigateur à l'adresse : `http://localhost:8501`

## 📊 Fonctionnalités

### 🎯 Filtres Interactifs
- **Filtres de période** : Sélection personnalisée des dates de début et de fin
- **Filtre par compagnie** : Choix d'une compagnie spécifique ou affichage de toutes
- **Filtre par mois** : Sélection d'un mois particulier
- **Filtre par année** : Sélection d'une année spécifique

### 📈 Indicateurs Clés de Performance (KPI)
- Total des commandes QR
- Montant total des commandes
- Taux de variation mensuel
- Taux de variation annuel  
- Variation globale

### 📊 Visualisations
1. **Tableau récapitulatif** : Commandes et montants par compagnie
2. **Histogramme** : Top 10 des compagnies par montant
3. **Courbe d'évolution** : Tendance mensuelle des montants
4. **Graphique circulaire** : Répartition des commandes QR par compagnie
5. **Part de marché** : Pourcentage de marché par compagnie
6. **Tendance par compagnie** : Évolution temporelle des top 5 compagnies

### 🎨 Design Professionnel
- Interface moderne et responsive
- Cartes KPI stylisées avec effets visuels
- Palette de couleurs professionnelle
- Mise en page claire et intuitive
- Adapté pour un usage entreprise

## 📁 Structure du Projet

```
Assurance_commande_QR/
├── dashboard_qr.py          # Application Streamlit principale
├── Assurance_Commandes_QR.csv # Fichier de données
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

## 🔧 Configuration des Données

Le dashboard utilise le fichier `Assurance_Commandes_QR.csv` avec les colonnes suivantes :
- `Compagnie` : Nom de la compagnie d'assurance
- `NbQR` : Nombre de commandes QR
- `cmd_montant` : Montant de la commande
- `DateCmde` : Date de commande
- `DateValidation` : Date de validation (utilisée pour les analyses temporelles)

## 💡 Utilisation

1. **Lancer le dashboard** avec la commande `streamlit run dashboard_qr.py`
2. **Utiliser les filtres** dans la sidebar et en haut de page pour affiner l'analyse
3. **Explorer les KPI** pour obtenir une vue d'ensemble rapide
4. **Analyser les graphiques** pour identifier les tendances et patterns
5. **Exporter les données** si nécessaire (fonctionnalité intégrée de Streamlit)

## 🎯 Points Forts

- **Performance optimisée** : Utilisation du cache de Streamlit pour des chargements rapides
- **Code clair et maintenable** : Structure modulaire et commentaires détaillés
- **Responsive design** : Adaptation à différentes tailles d'écran
- **Analyse complète** : Multiples angles d'analyse des données
- **Interface intuitive** : Facile à utiliser même pour les non-techniciens

## 📞 Support

Pour toute question ou amélioration du dashboard, n'hésitez pas à consulter la documentation ou à modifier le code source selon vos besoins spécifiques.
