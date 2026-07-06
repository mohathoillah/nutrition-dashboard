# Validated categorical palette (light mode) — see dataviz skill reference palette
CATEGORICAL_PALETTE = [
    "#2a78d6",  # blue
    "#1baf7a",  # aqua
    "#eda100",  # yellow
    "#008300",  # green
    "#4a3aa7",  # violet
    "#e34948",  # red
    "#e87ba4",  # magenta
    "#eb6834",  # orange
]
OTHER_CATEGORY_COLOR = "#898781"


def build_categorical_color_groups(categories, priority_order=None):
    unique_categories = set(categories)

    if priority_order:
        ordered_categories = [c for c in priority_order if c in unique_categories]
        ordered_categories += sorted(unique_categories - set(ordered_categories))
    else:
        ordered_categories = sorted(unique_categories)

    named_categories = ordered_categories[:len(CATEGORICAL_PALETTE)]

    color_map = {
        category: CATEGORICAL_PALETTE[i]
        for i, category in enumerate(named_categories)
    }
    color_map["Other"] = OTHER_CATEGORY_COLOR

    category_order = named_categories + (
        ["Other"] if len(ordered_categories) > len(named_categories) else []
    )

    return named_categories, color_map, category_order
