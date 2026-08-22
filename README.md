# Analyse et Valorisation d'un Portefeuille Obligataire

Ce projet fournit une solution Python modulaire pour l'analyse, la valorisation, le suivi des risques et le reporting d'un portefeuille obligataire. Il est conçu pour être exécuté localement et générer un rapport Excel détaillé.

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Structure du Projet](#structure-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Fichier d'Entrée Excel](#fichier-dentree-excel)
- [Fichier de Sortie Excel](#fichier-de-sortie-excel)

## Fonctionnalités

Le modèle implémente les fonctionnalités suivantes :

1.  **Centralisation des Positions** : Gère les positions obligataires et leurs caractéristiques.
2.  **Valorisation Automatique** : Valorise chaque titre en utilisant une courbe de taux de référence interpolée.
3.  **Indicateurs de Risque** : Calcule les principaux indicateurs de risque de taux d'intérêt (Durée, Durée Modifiée, Sensibilité, DV01, Convexité, Perte en Capital Potentielle).
4.  **Reporting Synthétique** : Génère des rapports consolidés et agrégés pour le suivi du portefeuille.

## Structure du Projet

Le projet est organisé en plusieurs modules Python, un script principal, un fichier de dépendances et un script d'exécution :

-   `data_loader.py` : Pour charger les données du portefeuille et de la courbe de taux.
-   `data_preprocessing.py` : Pour renommer les colonnes, valider les dates et calculer la maturité résiduelle.
-   `yield_curve.py` : Pour l'interpolation linéaire de la courbe de taux.
-   `bond_calculations.py` : Pour tous les calculs financiers (coupons, flux de trésorerie, valorisation, indicateurs de risque).
-   `reporting.py` : Pour la génération des rapports consolidés et agrégés, ainsi que l'exportation vers Excel.
-   `main.py` : Le script principal qui orchestre l'exécution de l'analyse.
-   `requirements.txt` : Liste des dépendances Python.
-   `run_analysis.sh` : Script shell pour installer les dépendances et exécuter l'analyse (pour Linux/macOS).

## Prérequis

Assurez-vous d'avoir Python 3.x installé sur votre système.

## Installation

1.  **Clonez le dépôt GitHub** :

    ```bash
    git clone <URL_DE_VOTRE_DEPOT_GITHUB>
    cd bond_portfolio_analysis # Ou le nom de votre dossier
    ```

2.  **Copiez les fichiers de l'analyse** :
    Placez tous les fichiers `.py`, `requirements.txt` et `run_analysis.sh` (ou `run_analysis.bat` pour Windows) dans le répertoire cloné.

3.  **Placez le fichier d'entrée Excel** :
    Assurez-vous que votre fichier Excel d'entrée (`Modele_Complet_Portefeuille_Valorisation_FR.xlsx`) est dans le même répertoire que les scripts Python.

4.  **Installez les dépendances Python** :

    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Pour exécuter l'analyse, utilisez le script `run_analysis.sh` (ou `run_analysis.bat` pour Windows).

### Sur Linux / macOS

1.  Ouvrez un terminal.
2.  Naviguez jusqu'au répertoire du projet :
    ```bash
    cd /chemin/vers/votre/dossier/bond_portfolio_analysis
    ```
3.  Rendez le script exécutable (si ce n'est pas déjà fait) :
    ```bash
    chmod +x run_analysis.sh
    ```
4.  Exécutez le script :
    ```bash
    ./run_analysis.sh
    ```

### Sur Windows

1.  Ouvrez l'invite de commande ou PowerShell.
2.  Naviguez jusqu'au répertoire du projet :
    ```cmd
    cd C:\chemin\vers\votre\dossier\bond_portfolio_analysis
    ```
3.  Exécutez le script batch :
    ```cmd
    run_analysis.bat
    ```

## Fichier d'Entrée Excel

Le script attend un fichier Excel nommé `Modele_Complet_Portefeuille_Valorisation_FR.xlsx` (ce nom peut être modifié dans `main.py` si nécessaire) avec les feuilles suivantes :

-   `portfolio_data` : Contient les caractéristiques détaillées de chaque obligation du portefeuille.
-   `curve_rate` : Contient les données de la courbe de taux de référence (colonnes `tenor` et `rate`).

## Fichier de Sortie Excel

Après l'exécution, un fichier `portfolio_analysis_report.xlsx` sera généré dans le même répertoire. Ce fichier contient deux feuilles :

-   `Portfolio_Analysis` : Un rapport consolidé avec tous les détails calculés pour chaque obligation.
-   `Aggregated_Metrics` : Un tableau récapitulatif des métriques agrégées du portefeuille (valeurs nominales et de marché, durées moyennes pondérées, DV01 total, etc.).
"""

with open('README.md', 'w') as f:
    f.write(readme_content)

print("Fichier README.md créé avec succès.")
