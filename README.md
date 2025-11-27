# Analyse de Données - Impact de la Publicité sur les Ventes

## Description

Ce projet analyse les données transactionnelles d'une marque et l'impact de ses campagnes publicitaires (TV et Programmatique) sur les ventes.

## Structure du Projet

```
data_challenge_mie/
├── input_data/
│   └── X_2025/
│       ├── retailer.csv                          # Données transactionnelles
│       ├── tv_publisher.csv                      # Données publicitaires TV
│       ├── programmatic_publisher.csv            # Données publicitaires programmatiques
│       ├── mapping_transac_publisher_tv.csv      # Table de mapping
│       ├── socio_demo.csv                        # Données socio-démographiques
│       └── readme_EN.txt                         # Instructions
├── data_analysis.ipynb                           # Notebook principal d'analyse
├── requirements.txt                               # Dépendances Python
└── README.md                                      # Ce fichier
```

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou avec conda:

```bash
conda install pandas polars numpy matplotlib seaborn scipy jupyter
```

**Note:** Ce projet utilise **Polars** pour des opérations de jointure ultra-rapides, ce qui améliore considérablement les performances sur les gros volumes de données.

## Utilisation

1. **Lancer Jupyter Notebook:**

```bash
jupyter notebook
```

2. **Ouvrir le notebook:** `data_analysis.ipynb`

3. **Exécuter les cellules:** Lancez toutes les cellules dans l'ordre (Cell → Run All)

## Contenu de l'Analyse

### 1. Chargement des Données
- Import et exploration des 5 datasets
- Vérification de la qualité des données

### 2. Analyse du Marché
- **KPIs principaux:**
  - Panier moyen
  - Nombre de transactions
  - Fréquence d'achat par client
  - Distribution par marque et produit
  
- **Analyses temporelles:**
  - Évolution des ventes quotidiennes
  - Saisonnalité

- **Analyse socio-démographique:**
  - Performance par tranche d'âge
  - Performance par niveau de revenu
  - Performance par breed

### 3. Impact de la Publicité

- **Investissements publicitaires:**
  - Répartition TV vs Programmatique
  - CPM (Coût pour 1000 impressions)

- **Segmentation des clients:**
  - Clients exposés TV
  - Clients exposés Programmatique
  - Clients exposés aux deux
  - Clients non exposés

- **Attribution et ROI:**
  - Analyse d'attribution temporelle (fenêtre 7 jours)
  - Calcul du ROI par canal
  - ROAS (Return on Ad Spend)

- **Performance par campagne:**
  - Top campagnes programmatiques
  - ROI par campagne

### 4. Insights et Recommandations

- Synthèse des KPIs clés
- Corrélations entre dépenses publicitaires et ventes
- Recommandations stratégiques

## Résultats Attendus

Le notebook génère:
- **~20+ graphiques** illustrant les différentes analyses
- **Tableaux de KPIs** pour chaque dimension analysée
- **Insights actionnables** pour optimiser les investissements publicitaires

## Méthodologie

### Attribution Publicitaire

L'analyse utilise un modèle d'attribution **Last-Touch** avec une fenêtre de **7 jours**:
- Un achat est attribué à un canal si le client a été exposé à la publicité dans les 7 jours précédant l'achat
- Cette approche permet de mesurer l'impact direct de la publicité sur les conversions

### Métriques Clés

- **ROI (Return on Investment):** `(Revenus - Coûts) / Coûts × 100`
- **ROAS (Return on Ad Spend):** `Revenus / Coûts`
- **CPM (Cost Per Mille):** `Coût / Impressions × 1000`

## Notes Techniques

### Performance avec Polars

Ce projet utilise **Polars** pour les opérations de jointure et d'intersection sur les datasets clients:
- ✅ **10-100x plus rapide** que NumPy pour les intersections/différences sur de grands datasets
- ✅ **Utilisation optimale de la mémoire** grâce à l'implémentation en Rust
- ✅ **Jointures optimisées** : semi-join, anti-join, inner-join au lieu de np.intersect1d
- ✅ **Lazy evaluation** pour une exécution encore plus performante

**Exemple de gain:**
- Avant (NumPy): `np.intersect1d(buyers, customers_tv)` → ~3-5 secondes
- Après (Polars): `pl_buyers.join(pl_customers_tv, how='semi')` → ~0.1-0.3 secondes

### Autres notes

- Les fichiers de données sont volumineux (>200MB)
- Le chargement peut prendre quelques minutes
- L'analyse d'attribution est computationnellement intensive pour les merges

## Auteur

Analyse réalisée pour le Data Challenge MIE 2025

## Contact

Pour toute question concernant l'analyse:
- gabriel.zibi-meyer@numberly.com
- mathieu.josserand@numberly.com
- erinda@numberly.com
- lucie@numberly.com
