# =========================================================
# WEIGHT CONVERSION
# =========================================================
LB_TO_KG = 0.45359237
KG_TO_LB = 2.20462262
# =========================================================
# CONVERT LB TO KG
# =========================================================
def lbs_to_kg(weight):
    return round(weight * LB_TO_KG, 2)
# =========================================================
# CONVERT KG TO LB
# =========================================================
def kg_to_lbs(weight):
    return round(weight * KG_TO_LB, 2)
# =========================================================
# FORMAT LB WITH KG
# =========================================================
def lbs_with_kg(weight):
    kg = lbs_to_kg(weight)
    return f"{weight:.2f} LB ({kg:.2f} KG)"
# =========================================================
# FORMAT KG WITH LB
# =========================================================
def kg_with_lbs(weight):
    lbs = kg_to_lbs(weight)
    return f"{weight:.2f} KG ({lbs:.2f} LB)"
# =========================================================
# FORMAT WEIGHT IN BOTH UNITS
# =========================================================
def both_units(weight, unit):
    unit = unit.upper()
    if unit == "LB":
        return lbs_with_kg(weight)
    if unit == "KG":
        return kg_with_lbs(weight)
    raise ValueError("Unit must be LB or KG")