import pandas as pd

def rename_columns(df):
    """Renomme les colonnes du DataFrame du portefeuille pour une meilleure lisibilité."""
    df.rename(columns={
        'Description Titres': 'Description_Titles',
        'Date Emission': 'Issue_Date',
        'Date Jouissance': 'Enjoyment_Date',
        'Date Règlement': 'Settlement_Date',
        'Date Echéance': 'Maturity_Date',
        'Taux facial': 'Facial_Rate',
        'Périodicité Coupon': 'Coupon_Periodicity',
        'Fréquence': 'Frequency',
        'Périodicité Remboursement': 'Redemption_Periodicity',
        'Quantité': 'Quantity',
        'Nominal Unitaire': 'Unit_Nominal',
        'Nominal Global': 'Global_Nominal',
        'MATURITE': 'Maturity_Years',
        'TAUX_INTERPOLE': 'Interpolated_Rate_Initial', # Renamed to avoid conflict later
        'VALO_UNITAIRE': 'Unit_Valuation_Initial', # Renamed to avoid conflict later
        'VALO_GLOBALE': 'Global_Valuation_Initial', # Renamed to avoid conflict later
        'SENSIBILITE': 'Sensitivity_Initial' # Renamed to avoid conflict later
    }, inplace=True)
    print("Colonnes du DataFrame du portefeuille renommées.")
    return df

def validate_dates(df):
    """Valide que la Date d'échéance est postérieure à la Date de règlement."""
    invalid_dates = df[df['Maturity_Date'] <= df['Settlement_Date']]
    if not invalid_dates.empty:
        print("Erreur de validation: La Date d'échéance n'est pas systématiquement postérieure à la Date de règlement pour les entrées suivantes:")
        print(invalid_dates[['Code', 'Maturity_Date', 'Settlement_Date']])
        raise ValueError("Validation des dates échouée.")
    else:
        print("Validation des dates réussie: Toutes les Dates d'échéance sont postérieures aux Dates de règlement.")
    return df

def calculate_residual_maturity(df):
    """Calcule la maturité résiduelle en années (approximation ANNEE.FRAC)."""
    def calculate_year_fraction(start_date, end_date):
        if pd.isna(start_date) or pd.isna(end_date):
            return pd.NA
        delta = end_date - start_date
        return delta.days / 365.25 # Approximation pour la fraction d'année

    df['Residual_Maturity_Years'] = df.apply(
        lambda row: calculate_year_fraction(row['Settlement_Date'], row['Maturity_Date']),
        axis=1
    )
    print("Maturité Résiduelle calculée en années.")
    return df
