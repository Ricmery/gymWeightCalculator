
LB_TO_KG = 0.45359237
KG_TO_LB = 2.20462262

def lbs_to_kg(weight):
    return round(weight * LB_TO_KG, 2)

def kg_to_lbs(weight):
    return round(weight * KG_TO_LB, 2)

def lbs_with_kg(weight):
    kg = lbs_to_kg(weight)
    return f"{weight:.2f} LB ({kg:.2f} KG)"

def kg_with_lbs(weight):
    lbs = kg_to_lbs(weight)
    return f"{weight:.2f} KG ({lbs:.2f} LB)"