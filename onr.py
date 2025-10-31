
# === added part: grouping into sections ===
def group_component(comp):
    grouped = {
        "identifiers": {
            "id": comp.get("id"),
            "Manufacturer_Part_No": comp.get("Manufacturer_Part_No"),
            "Manufacturer_Part_Name": comp.get("Manufacturer_Part_Name"),
            "Manufacturer_Part _No": comp.get("Manufacturer_Part _No"),
            "Manufacturer_Name": comp.get("Manufacturer_Name"),
        },
        "repository_levels": {
            "level_1": comp.get("level_1"),
            "level_2": comp.get("level_2"),
            "level_3": comp.get("level_3"),
            "level_4": comp.get("level_4"),
        },
        "preference": {
            "Final_Preference_Level": comp.get("Final_Preference_Level"),
        },
        "mechanical_electrical_specs": {}
    }

    ignore_keys = set(
        grouped["identifiers"].keys()
        | grouped["repository_levels"].keys()
        | grouped["preference"].keys()
    )

    for k, v in comp.items():
        if k not in ignore_keys and v not in [None, "", "NaN"]:
            grouped["mechanical_electrical_specs"][k] = v

    return grouped

grouped_data = [group_component(comp) for comp in flattened]

with open(r'C:\Users\u127900\OneDrive -ies\Desktop\RAG\test\cleaned_json.json', 'w', encoding='utf-8') as f:
    json.dump(grouped_data, f, indent=3)

print("✅ Cleaned, flattened, and grouped JSON saved successfully.")