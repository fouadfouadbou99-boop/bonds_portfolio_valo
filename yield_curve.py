import pandas as pd

def interpolate_rate(residual_maturity, curve_df):
    """Implémente une interpolation linéaire pour trouver le taux approprié."""
    # Assurer que la courbe est triée par ténor
    curve_df = curve_df.sort_values(by='tenor')

    # Gérer les cas où la maturité résiduelle est en dehors de la plage de la courbe
    if residual_maturity <= curve_df['tenor'].min():
        return curve_df['rate'].iloc[0]
    if residual_maturity >= curve_df['tenor'].max():
        return curve_df['rate'].iloc[-1]

    # Trouver les deux points d'encadrement pour l'interpolation
    lower_bound = curve_df[curve_df['tenor'] <= residual_maturity].iloc[-1]
    upper_bound = curve_df[curve_df['tenor'] >= residual_maturity].iloc[0]

    # Effectuer l'interpolation linéaire
    x1, y1 = lower_bound['tenor'], lower_bound['rate']
    x2, y2 = upper_bound['tenor'], upper_bound['rate']

    interpolated_rate = y1 + (y2 - y1) * ((residual_maturity - x1) / (x2 - x1))
    return interpolated_rate

def apply_interpolation(df_portfolio, df_curve):
    """Applique la fonction d'interpolation à chaque obligation du portefeuille."""
    df_portfolio['Interpolated_Rate'] = df_portfolio['Residual_Maturity_Years'].apply(
        lambda x: interpolate_rate(x, df_curve)
    )
    print("Taux interpolés calculés pour le portefeuille.")
    return df_portfolio
