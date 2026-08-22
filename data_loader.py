import pandas as pd

def load_portfolio_data(file_path, sheet_name='portfolio_data'):
    """Charge les données du portefeuille à partir d'une feuille Excel."""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Données du portefeuille chargées depuis la feuille '{sheet_name}'.")
        return df
    except Exception as e:
        print(f"Erreur lors du chargement des données du portefeuille: {e}")
        return None

def load_curve_rate_data(file_path, sheet_name='curve_rate'):
    """Charge les données de la courbe de taux à partir d'une feuille Excel."""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Données de la courbe de taux chargées depuis la feuille '{sheet_name}'.")
        return df
    except Exception as e:
        print(f"Erreur lors du chargement des données de la courbe de taux: {e}")
        return None
