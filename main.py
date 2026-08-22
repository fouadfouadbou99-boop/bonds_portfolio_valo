import pandas as pd
import sys
import os

# Ajoute le répertoire courant au PYTHONPATH pour les imports relatifs
# Note: Dans un environnement local, assurez-vous que les modules sont dans le même répertoire
sys.path.append(os.path.dirname(__file__))

import data_loader
import data_preprocessing
import yield_curve
import bond_calculations
import reporting

def run_analysis(input_excel_path, output_excel_path='portfolio_analysis_report.xlsx'):
    print(f"\nDémarrage de l'analyse du portefeuille avec le fichier: {input_excel_path}")

    # 1. Chargement des données
    df_portefeuille = data_loader.load_portfolio_data(input_excel_path)
    df_curve_rate = data_loader.load_curve_rate_data(input_excel_path)

    if df_portefeuille is None or df_curve_rate is None:
        print("Impossible de charger toutes les données nécessaires. Arrêt de l'analyse.")
        return

    # 2. Prétraitement des données
    df_portefeuille = data_preprocessing.rename_columns(df_portefeuille)
    try:
        df_portefeuille = data_preprocessing.validate_dates(df_portefeuille)
    except ValueError as e:
        print(e)
        return # Arrête l'exécution si la validation des dates échoue
    df_portefeuille = data_preprocessing.calculate_residual_maturity(df_portefeuille)

    # 3. Interpolation de la courbe de taux
    df_portefeuille = yield_curve.apply_interpolation(df_portefeuille, df_curve_rate)

    # 4. Calculs financiers des obligations
    df_portefeuille = bond_calculations.calculate_annual_coupon(df_portefeuille)
    df_portefeuille = bond_calculations.apply_accrued_coupon_calculation(df_portefeuille)
    df_portefeuille = bond_calculations.apply_cash_flow_generation(df_portefeuille)
    df_portefeuille = bond_calculations.apply_bond_valuation(df_portefeuille)
    df_portefeuille = bond_calculations.apply_macaulay_duration_calculation(df_portefeuille)
    df_portefeuille = bond_calculations.calculate_modified_duration_sensitivity(df_portefeuille)
    df_portefeuille = bond_calculations.calculate_dv01(df_portefeuille)
    df_portefeuille = bond_calculations.apply_convexity_calculation(df_portefeuille)
    df_portefeuille = bond_calculations.calculate_potential_capital_loss(df_portefeuille)

    # 5. Génération des rapports
    consolidated_report = reporting.generate_consolidated_report(df_portefeuille)
    aggregated_metrics = reporting.generate_aggregated_metrics(df_portefeuille)

    # Affichage des premières lignes pour vérification (peut être retiré en production)
    print("\n--- Aperçu du rapport consolidé (premières 5 lignes) ---")
    print(consolidated_report.head())
    print("\n--- Métriques agrégées du portefeuille ---")
    print(aggregated_metrics)

    # 6. Exportation vers Excel
    reporting.export_to_excel(consolidated_report, aggregated_metrics, output_excel_path)

    print("\nAnalyse du portefeuille terminée. Le rapport est disponible dans le fichier Excel.")

if __name__ == "__main__":
    # Chemin vers votre fichier Excel d'entrée (à adapter)
    input_file = 'Modele_Complet_Portefeuille_Valorisation_FR.xlsx'
    # Chemin du fichier de sortie (sera créé dans le même répertoire)
    output_file = 'portfolio_analysis_report.xlsx'

    run_analysis(input_file, output_file)
