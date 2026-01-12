DOSE_PER_KG = {
    "DRUG_A": 2.0,  # fictional mg/kg
    "DRUG_B": 0.5,  # fictional mg/kg
    "DRUG_C": 1.2  # fictional mg/kg
}

PEDIATRIC_AGE_LIMIT = 12
PEDIATRIC_DOSE_FACTOR = 0.8

def calculate_medication_dose(weight_kg, age_years, code, urgent=False):
    """
    Calculates medication dose based on weight.

    PARAMS:
        weight_kg: float - patient body mass in kg
        age_years: years
        code: (str) name of drug: "DRUG_A", "DRUG_B", etc.
        urgent: optional flag for emergency use only dose
    Returns: dose in mg

    Notes:
    - This function does not check for allergies.
    - Based on hospital guidelines 2021 (todo: update to 2025)
    - If weight is negative it raises ValueError
    """

    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")

    if age_years < 0:
        raise ValueError("age_years cannot be negative")

    if code not in DOSE_PER_KG:
        raise ValueError(f"Unknown drug_code: {code}")

    base_dose_mg = weight_kg * DOSE_PER_KG[code]

    if age_years < PEDIATRIC_AGE_LIMIT:
        base_dose_mg *= PEDIATRIC_DOSE_FACTOR

    return round(base_dose_mg, 2)
