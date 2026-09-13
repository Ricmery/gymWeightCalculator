LB_TO_KG = 0.45359237
KG_TO_LB = 2.20462262

def lb_to_kg(weight):
    return round(weight * LB_TO_KG, 2)

def kg_to_lb(weight):
    return round(weight * KG_TO_LB, 2)

def convert(weight, unit):
    if unit.upper() == "LB":
        return lb_to_kg(weight), "KG"
    elif unit.upper() == "KG":
        return kg_to_lb(weight), "LB"
    else:
        raise ValueError("Unit must be LB or KG")