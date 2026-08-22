
import pandas as pd
import numpy as np

def calculate_annual_coupon(df):
    """Calcule le coupon annuel pour chaque obligation."""
    df['Annual_Coupon'] = df['Unit_Nominal'] * df['Facial_Rate']
    print("Coupon annuel calculé.")
    return df

def get_last_coupon_payment_date(settlement_date, enjoyment_date, maturity_date):
    """Détermine la dernière date de paiement de coupon égale ou antérieure à la date de règlement."""
    coupon_dates = []
    current_date = enjoyment_date
    while current_date <= maturity_date:
        coupon_dates.append(current_date)
        current_date = current_date + pd.DateOffset(years=1)

    last_coupon_date = None
    for c_date in reversed(coupon_dates):
        if c_date <= settlement_date:
            last_coupon_date = c_date
            break

    if last_coupon_date is None:
        return enjoyment_date

    return last_coupon_date

def calculate_accrued_coupon(row):
    """Calcule le coupon couru pour une obligation."""
    settlement_date = row['Settlement_Date']
    enjoyment_date = row['Enjoyment_Date']
    maturity_date = row['Maturity_Date']
    annual_coupon = row['Annual_Coupon']

    last_coupon_payment_date = get_last_coupon_payment_date(settlement_date, enjoyment_date, maturity_date)

    next_coupon_payment_date = last_coupon_payment_date + pd.DateOffset(years=1)

    if next_coupon_payment_date > maturity_date:
        next_coupon_payment_date = maturity_date

    if settlement_date == last_coupon_payment_date:
        return 0.0

    days_since_last_coupon = (settlement_date - last_coupon_payment_date).days
    total_days_in_coupon_period = (next_coupon_payment_date - last_coupon_payment_date).days

    if total_days_in_coupon_period <= 0:
        return 0.0

    accrued = (days_since_last_coupon / total_days_in_coupon_period) * annual_coupon

    if days_since_last_coupon < 0:
        return 0.0

    return accrued

def apply_accrued_coupon_calculation(df):
    """Applique le calcul du coupon couru à chaque obligation."""
    df['Accrued_Coupon'] = df.apply(calculate_accrued_coupon, axis=1)
    print("Coupon couru calculé.")
    return df

def generate_cash_flows(row):
    """Génère les flux de trésorerie (coupons et principal) pour une obligation."""
    unit_nominal = row['Unit_Nominal']
    facial_rate = row['Facial_Rate']
    maturity_date = row['Maturity_Date']
    enjoyment_date = row['Enjoyment_Date']
    settlement_date = row['Settlement_Date']

    cash_flows = []

    current_coupon_date = enjoyment_date
    while current_coupon_date <= settlement_date:
        current_coupon_date = current_coupon_date + pd.DateOffset(years=1)

    while current_coupon_date <= maturity_date:
        cash_flows.append({
            'Date': current_coupon_date,
            'Type': 'Coupon',
            'Amount': unit_nominal * facial_rate
        })
        current_coupon_date = current_coupon_date + pd.DateOffset(years=1)

    if maturity_date >= settlement_date:
        cash_flows.append({
            'Date': maturity_date,
            'Type': 'Principal',
            'Amount': unit_nominal
        })

    return cash_flows

def apply_cash_flow_generation(df):
    """Applique la génération de flux de trésorerie à chaque obligation."""
    df['Cash_Flows'] = df.apply(generate_cash_flows, axis=1)
    print("Flux de trésorerie générés pour chaque obligation.")
    return df

def calculate_bond_price(row):
    """Calcule le prix sale et le prix propre d'une obligation."""
    cash_flows = row['Cash_Flows']
    interpolated_rate = row['Interpolated_Rate']
    settlement_date = row['Settlement_Date']
    accrued_coupon = row['Accrued_Coupon']

    dirty_price = 0.0
    for cf in cash_flows:
        cf_date = cf['Date']
        cf_amount = cf['Amount']

        time_to_cf = (cf_date - settlement_date).days / 365.25

        if time_to_cf > 0:
            present_value = cf_amount / ((1 + interpolated_rate)**time_to_cf)
            dirty_price += present_value

    clean_price = dirty_price - accrued_coupon

    return dirty_price, clean_price

def apply_bond_valuation(df):
    """Applique la fonction de valorisation des obligations."""
    df[['Dirty_Price', 'Clean_Price']] = df.apply(
        lambda row: pd.Series(calculate_bond_price(row)), axis=1
    )
    df['Unit_Valuation'] = df['Clean_Price']
    df['Global_Valuation'] = df['Unit_Valuation'] * df['Quantity']
    print("Valorisation des obligations effectuée (prix sale, propre, valorisation unitaire et globale).")
    return df

def calculate_macaulay_duration(row):
    """Calcule la Duration de Macaulay pour une obligation."""
    cash_flows = row['Cash_Flows']
    interpolated_rate = row['Interpolated_Rate']
    settlement_date = row['Settlement_Date']
    dirty_price = row['Dirty_Price']

    if dirty_price == 0:
        return 0.0

    sum_pv_times_t = 0.0
    for cf in cash_flows:
        cf_date = cf['Date']
        cf_amount = cf['Amount']
        time_to_cf = (cf_date - settlement_date).days / 365.25

        if time_to_cf > 0:
            pv_cf = cf_amount / ((1 + interpolated_rate)**time_to_cf)
            sum_pv_times_t += time_to_cf * pv_cf

    macaulay_duration = sum_pv_times_t / dirty_price
    return macaulay_duration

def apply_macaulay_duration_calculation(df):
    """Applique le calcul de la Duration de Macaulay."""
    df['Macaulay_Duration'] = df.apply(calculate_macaulay_duration, axis=1)
    print("Duration de Macaulay calculée.")
    return df

def calculate_modified_duration_sensitivity(df):
    """Calcule la Duration Modifiée et la Sensibilité."""
    df['Modified_Duration'] = df['Macaulay_Duration'] / (1 + df['Interpolated_Rate'])
    df['Sensitivity'] = df['Modified_Duration']
    print("Duration Modifiée et Sensibilité calculées.")
    return df

def calculate_dv01(df):
    """Calcule le DV01."""
    df['DV01'] = df['Modified_Duration'] * df['Clean_Price'] * 0.0001
    print("DV01 calculé.")
    return df

def calculate_convexity(row):
    """Calcule la Convexité pour une obligation."""
    cash_flows = row['Cash_Flows']
    interpolated_rate = row['Interpolated_Rate']
    settlement_date = row['Settlement_Date']
    dirty_price = row['Dirty_Price']

    if dirty_price == 0:
        return 0.0

    sum_pv_t_squared = 0.0
    for cf in cash_flows:
        cf_date = cf['Date']
        cf_amount = cf['Amount']
        time_to_cf = (cf_date - settlement_date).days / 365.25

        if time_to_cf > 0:
            pv_cf = cf_amount / ((1 + interpolated_rate)**time_to_cf)
            sum_pv_t_squared += (time_to_cf * (time_to_cf + 1)) * pv_cf

    convexity = sum_pv_t_squared / (dirty_price * ((1 + interpolated_rate)**2))
    return convexity

def apply_convexity_calculation(df):
    """Applique le calcul de la Convexité."""
    df['Convexity'] = df.apply(calculate_convexity, axis=1)
    print("Convexité calculée.")
    return df

def calculate_potential_capital_loss(df):
    """Calcule la Perte en Capital Potentielle (PCP) pour un choc de 100 bps."""
    df['Potential_Capital_Loss'] = df['Sensitivity'] * df['Global_Valuation'] * 0.01
    print("Perte en Capital Potentielle (PCP) calculée.")
    return df
