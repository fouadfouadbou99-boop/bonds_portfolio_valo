import pandas as pd

def generate_consolidated_report(df):
    """Génère un rapport consolidé du portefeuille."""
    report_df = df[[
        'Code', 'Description_Titles', 'Quantity', 'Unit_Nominal', 'Global_Nominal',
        'Settlement_Date', 'Maturity_Date', 'Residual_Maturity_Years', 'Facial_Rate',
        'Interpolated_Rate', 'Annual_Coupon', 'Accrued_Coupon',
        'Dirty_Price', 'Clean_Price', 'Unit_Valuation', 'Global_Valuation',
        'Macaulay_Duration', 'Modified_Duration', 'Sensitivity', 'DV01', 'Convexity',
        'Potential_Capital_Loss'
    ]].copy()
    print("Rapport consolidé du portefeuille généré.")
    return report_df

def generate_aggregated_metrics(df):
    """Calcule et génère les métriques agrégées du portefeuille."""
    portfolio_nominal_value = df['Global_Nominal'].sum()
    portfolio_market_value = df['Global_Valuation'].sum()

    total_global_valuation = df['Global_Valuation'].sum()
    weighted_avg_macaulay_duration = (df['Macaulay_Duration'] * df['Global_Valuation']).sum() / total_global_valuation if total_global_valuation else 0
    weighted_avg_modified_duration = (df['Modified_Duration'] * df['Global_Valuation']).sum() / total_global_valuation if total_global_valuation else 0
    weighted_avg_sensitivity = (df['Sensitivity'] * df['Global_Valuation']).sum() / total_global_valuation if total_global_valuation else 0
    weighted_avg_convexity = (df['Convexity'] * df['Global_Valuation']).sum() / total_global_valuation if total_global_valuation else 0

    aggregated_dv01 = df['DV01'].sum()
    total_potential_capital_loss = df['Potential_Capital_Loss'].sum()

    reporting_summary = pd.DataFrame({
        'Metric': [
            'Nominal Value (Global)',
            'Market Value (Global Valuation)',
            'Weighted Average Macaulay Duration',
            'Weighted Average Modified Duration',
            'Weighted Average Sensitivity',
            'Weighted Average Convexity',
            'Aggregated DV01',
            'Total Potential Capital Loss'
        ],
        'Value': [
            portfolio_nominal_value,
            portfolio_market_value,
            weighted_avg_macaulay_duration,
            weighted_avg_modified_duration,
            weighted_avg_sensitivity,
            weighted_avg_convexity,
            aggregated_dv01,
            total_potential_capital_loss
        ]
    })
    print("Métriques agrégées du portefeuille calculées.")
    return reporting_summary

def export_to_excel(df_portfolio, reporting_summary_df, output_path='portfolio_analysis_report.xlsx'):
    """Exporte les rapports consolidés et agrégés dans un fichier Excel."""
    try:
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df_portfolio.to_excel(writer, sheet_name='Portfolio_Analysis', index=False)
            reporting_summary_df.to_excel(writer, sheet_name='Aggregated_Metrics', index=False)
        print(f"Rapport d'analyse du portefeuille exporté vers '{output_path}'.")
        return True
    except Exception as e:
        print(f"Erreur lors de l'exportation du rapport Excel: {e}")
        return False
