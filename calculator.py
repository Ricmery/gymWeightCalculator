#Weight Calculator and Barbell Plate Setup Finder

#At this point, Only God know how this works in it's entirety. I will try to add comments and documentation as I go, but it is a work in progress.
#If you are reading this, and you are not me, you are probably confused. I am too. But it works, and that is what matters.

# =========================================================
# PLATE CALCULATOR
# =========================================================
from converter import lbs_to_kg, kg_to_lbs
# =========================================================
# Helper Functions
# =========================================================
def convert_weight(weight, from_unit, to_unit):
    if from_unit == to_unit:
        return weight
    if from_unit == "LB" and to_unit == "KG":
        return lbs_to_kg(weight)
    if from_unit == "KG" and to_unit == "LB":
        return kg_to_lbs(weight)
    raise ValueError("Unit must be LB or KG")
def normalize_unit(unit):
    unit = unit.upper()
    if unit in ("LB", "LBS"):
        return "LB"
    if unit == "KG":
        return "KG"
    raise ValueError("Unit must be LB or KG")
# =========================================================
# Expand Plate Inventory
# =========================================================
def expand_inventory(plates):
    expanded = []
    for plate in plates:
        weight = plate["weight"]
        quantity = plate["quantity"]
        unit = normalize_unit(plate["unit"])
        color = plate.get("color", "none")
        for _ in range(quantity):
            expanded.append({
                "weight": weight,
                "unit": unit,
                "color": color
            })
    return expanded
# =========================================================
# Find Best Combination
# =========================================================
def find_best_combination(target, plates):
    best_combination = None
    best_weight = None
    best_count = None
    best_difference = None
    def search(index, remaining, current):
        nonlocal best_combination
        nonlocal best_weight
        nonlocal best_count
        nonlocal best_difference
        current_weight = target - remaining
        difference = abs(target - current_weight)
        plate_count = len(current)
        if best_combination is None:
            best_combination = current.copy()
            best_weight = current_weight
            best_count = plate_count
            best_difference = difference
        else:
            if (
                difference < best_difference - 0.001
                or (
                    abs(difference - best_difference) < 0.001
                    and plate_count < best_count
                )
            ):
                best_combination = current.copy()
                best_weight = current_weight
                best_count = plate_count
        if index >= len(plates):
            return
        if remaining <= 0:
            return
        for i in range(index, len(plates)):
            plate = plates[i]
            if plate["weight"] <= remaining + 0.001:
                search(
                    i + 1,
                    remaining - plate["weight"],
                    current + [plate]
                )
    search(0, target, [])
    return {
        "plates": best_combination,
        "weight": round(best_weight, 2),
        "difference": round(best_difference, 2),
        "plate_count": best_count
    }
# =========================================================
# Find Under / Over
# =========================================================
def find_under_over(target, plates):
    best_under = None
    best_over = None
    best_under_weight = None
    best_over_weight = None
    best_under_difference = float("inf")
    best_over_difference = float("inf")
    def search(index, current_weight, current):
        nonlocal best_under
        nonlocal best_over
        nonlocal best_under_weight
        nonlocal best_over_weight
        nonlocal best_under_difference
        nonlocal best_over_difference
        if current:
            if current_weight <= target + 0.001:
                difference = target - current_weight
                if (
                    difference < best_under_difference - 0.001
                    or (
                        abs(
                            difference -
                            best_under_difference
                        ) < 0.001
                        and (
                            best_under is None
                            or len(current) < len(best_under)
                        )
                    )
                ):
                    best_under = current.copy()
                    best_under_weight = current_weight
                    best_under_difference = difference
            if current_weight >= target - 0.001:
                difference = current_weight - target
                if (
                    difference < best_over_difference - 0.001
                    or (
                        abs(
                            difference -
                            best_over_difference
                        ) < 0.001
                        and (
                            best_over is None
                            or len(current) < len(best_over)
                        )
                    )
                ):
                    best_over = current.copy()
                    best_over_weight = current_weight
                    best_over_difference = difference
        if index >= len(plates):
            return
        for i in range(index, len(plates)):
            plate = plates[i]
            search(
                i + 1,
                current_weight + plate["weight"],
                current + [plate]
            )
    search(0, 0, [])
    return {
        "under": best_under,
        "under_weight": (
            round(best_under_weight, 2)
            if best_under_weight is not None
            else None
        ),
        "under_difference": (
            round(best_under_difference, 2)
            if best_under is not None
            else None
        ),
        "over": best_over,
        "over_weight": (
            round(best_over_weight, 2)
            if best_over_weight is not None
            else None
        ),
        "over_difference": (
            round(best_over_difference, 2)
            if best_over is not None
            else None
        )
    }
# =========================================================
# Calculate Plate Setup
# =========================================================
def calculate(goal_weight, input_unit, gym_plates, bar_weight):
    input_unit = normalize_unit(input_unit)
    if not gym_plates:
        return {
            "success": False,
            "error": "The selected gym has no plates."
        }
    gym_unit = normalize_unit(
        gym_plates[0]["unit"]
    )
    for plate in gym_plates:
        plate_unit = normalize_unit(
            plate["unit"]
        )
        if plate_unit != gym_unit:
            return {
                "success": False,
                "error": (
                    "The selected gym contains mixed plate units. "
                    "Separate LB and KG inventories are required."
                )
            }
    gym_goal = convert_weight(
        goal_weight,
        input_unit,
        gym_unit
    )
    gym_bar = convert_weight(
        bar_weight,
        input_unit,
        gym_unit
    )
    per_side = (
        gym_goal - gym_bar
    ) / 2
    if per_side < 0:
        return {
            "success": False,
            "error": "The goal weight is less than the bar weight."
        }
    expanded_plates = expand_inventory(
        gym_plates
    )
    expanded_plates.sort(
        key=lambda plate: plate["weight"],
        reverse=True
    )
    result = find_best_combination(
        per_side,
        expanded_plates
    )
    under_over = find_under_over(
        per_side,
        expanded_plates
    )
    actual_per_side = result["weight"]
    actual_total = (
        gym_bar +
        (actual_per_side * 2)
    )
    difference = (
        actual_total -
        gym_goal
    )
    actual_total_input = convert_weight(
        actual_total,
        gym_unit,
        input_unit
    )
    difference_input = convert_weight(
        abs(difference),
        gym_unit,
        input_unit
    )
    per_side_input = convert_weight(
        actual_per_side,
        gym_unit,
        input_unit
    )
    return {
        "success": True,
        "input_weight": round(
            goal_weight,
            2
        ),
        "input_unit": input_unit,
        "gym_unit": gym_unit,
        "gym_weight": round(
            gym_goal,
            2
        ),
        "bar_weight": round(
            gym_bar,
            2
        ),
        "target_per_side": round(
            per_side,
            2
        ),
        "actual_per_side": round(
            actual_per_side,
            2
        ),
        "actual_total": round(
            actual_total,
            2
        ),
        "actual_total_input": round(
            actual_total_input,
            2
        ),
        "difference": round(
            difference,
            2
        ),
        "difference_input": round(
            difference_input,
            2
        ),
        "per_side_input": round(
            per_side_input,
            2
        ),
        "plate_count": result[
            "plate_count"
        ],
        "plates": result[
            "plates"
        ],
        "under": under_over[
            "under"
        ],
        "under_weight": under_over[
            "under_weight"
        ],
        "under_difference": under_over[
            "under_difference"
        ],
        "over": under_over[
            "over"
        ],
        "over_weight": under_over[
            "over_weight"
        ],
        "over_difference": under_over[
            "over_difference"
        ]
    }
# =========================================================
# Format Plate Setup
# =========================================================
def format_plate_setup(result):
    if not result["success"]:
        return result["error"]
    lines = []
    for plate in result["plates"]:
        weight = plate["weight"]
        unit = plate["unit"]
        color = plate["color"]
        if color and color != "none":
            lines.append(
                f"{weight:.2f} {unit} ({color})"
            )
        else:
            lines.append(
                f"{weight:.2f} {unit}"
            )
    return lines