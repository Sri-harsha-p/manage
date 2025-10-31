import json

data = json.load(open(r"C:\User\Desktop\RAG\comp.json"))

def clean_dict(d):
    if isinstance(d, dict):
        return {
            k: clean_dict(v) 
            for k, v in d.items() 
            if v not in ["Not Available", "Not Applicable", "To be identified"]
        }
    elif isinstance(d, list):
        return [clean_dict(item) for item in d]
    else:
        return d

cleaned_data = clean_dict(data)

def restructure_component(comp):
    def safe_get(key, default=""):
        val = comp.get(key, default)
        return val if val not in [None, "", "na"] else default
    
    # Get all keys present in this component
    keys = comp.keys()
    
    # Field 1: Title
    title = safe_get("Manufacturer_Part_Name")
    
    # Field 2: Description
    desc_fields = []
    if "Connection_Type" in keys:
        desc_fields.append(safe_get("Connection_Type"))
    if "Connector_Family_or_Series" in keys:
        desc_fields.append(safe_get("Connector_Family_or_Series"))
    if "Sealed_or_Unsealed" in keys:
        desc_fields.append(safe_get("Sealed_or_Unsealed"))
    if "Type_Plug_Receptacle" in keys:
        desc_fields.append(safe_get("Type_Plug_Receptacle"))
    if "Inline_Mounting_feature_type" in keys:
        desc_fields.append(safe_get("Inline_Mounting_feature_type"))
    if "Shielded_Unshielded" in keys:
        desc_fields.append(safe_get("Shielded_Unshielded"))
    
    # Field 3: Product category
    category = " > ".join(filter(None, [
        safe_get("level_1"),
        safe_get("level_2"), 
        safe_get("level_3"),
        safe_get("level_4")
    ]))
    
    # Field 4: Metadata
    meta_fields = []
    if "Color_or_Finish" in keys:
        meta_fields.append(safe_get("Color_or_Finish"))
    if "Material" in keys:
        meta_fields.append(safe_get("Material"))
    if "Keying_Yes_or_No" in keys:
        meta_fields.append(safe_get("Keying_Yes_or_No"))
    if "ROHS_Compliant_Yes_or_No" in keys:
        meta_fields.append(safe_get("ROHS_Compliant_Yes_or_No"))
    if "UL_94_Approved_Yes_or_No" in keys:
        meta_fields.append(safe_get("UL_94_Approved_Yes_or_No"))
    if "TPA_Available_Yes_or_No" in keys:
        meta_fields.append(safe_get("TPA_Available_Yes_or_No"))
    if "CPA_Available_Yes_or_No" in keys:
        meta_fields.append(safe_get("CPA_Available_Yes_or_No"))
    if "Panel_Mountable_Yes_or_No" in keys:
        meta_fields.append(safe_get("Panel_Mountable_Yes_or_No"))
    if "Backshell_Available_Yes_or_No" in keys:
        meta_fields.append(safe_get("Backshell_Available_Yes_or_No"))
    if "Secondary_Lock_Available_Yes_or_No" in keys:
        meta_fields.append(safe_get("Secondary_Lock_Available_Yes_or_No"))
    if "Dust_Shipping_Cap_Available_Yes_or_No" in keys:
        meta_fields.append(safe_get("Dust_Shipping_Cap_Available_Yes_or_No"))
    if "Flammability_Rating" in keys:
        meta_fields.append(safe_get("Flammability_Rating"))
    if "SAE_J2030_Test_Set_Yes_or_No" in keys:
        meta_fields.append(safe_get("SAE_J2030_Test_Set_Yes_or_No"))
    
    # Field 5: Brand
    brand_fields = []
    if "Manufacturer_Name" in keys:
        brand_fields.append(safe_get("Manufacturer_Name"))
    if "Final_Preference_Level" in keys:
        brand_fields.append(safe_get("Final_Preference_Level"))
    
    # Field 6: Numeric
    numeric_fields = []
    if "Voltage_ratingin_Volts" in keys:
        numeric_fields.append(str(safe_get("Voltage_ratingin_Volts")))
    if "Number_of_poles" in keys:
        numeric_fields.append(str(safe_get("Number_of_poles")))
    if "Operating_Temperature_range_in_Degree_Celsius" in keys:
        numeric_fields.append(str(safe_get("Operating_Temperature_range_in_Degree_Celsius")))
    if "Pitch_in_" in keys:
        numeric_fields.append(str(safe_get("Pitch_in_")))
    if "No_of_rows" in keys:
        numeric_fields.append(str(safe_get("No_of_rows")))
    if "Insulation_resistance" in keys:
        numeric_fields.append(str(safe_get("Insulation_resistance")))
    if "Terminal_retention_Strength_terminal_inside_connector_in_Newton_Optional" in keys:
        numeric_fields.append(str(safe_get("Terminal_retention_Strength_terminal_inside_connector_in_Newton_Optional")))
    if "Mating_Cycle" in keys:
        numeric_fields.append(str(safe_get("Mating_Cycle")))
    if "Wire_Size_Range" in keys:
        numeric_fields.append(str(safe_get("Wire_Size_Range")))
    
    # Field 7: Technical details
    tech_fields = []
    if "Degree_of_Protection_IP_rating" in keys:
        tech_fields.append(safe_get("Degree_of_Protection_IP_rating"))
    if "Manufacturer_Part _No" in keys:
        tech_fields.append(safe_get("Manufacturer_Part _No"))
    if "Manufacturer_Part_No" in keys:
        tech_fields.append(safe_get("Manufacturer_Part_No"))
    
    restructured = {
        "_id": safe_get("_id"),
        "Title": title,
        "Description": " ".join(filter(None, desc_fields)),
        "Product_category": category,
        "Metadata": " ".join(filter(None, meta_fields)),
        "Brand": " ".join(filter(None, brand_fields)),
        "Numeric": " ".join(filter(None, numeric_fields)),
        "Technical_details": " ".join(filter(None, tech_fields))
    }
    
    return restructured

restructured = [restructure_component(comp) for comp in cleaned_data]

with open(r'C:\Users\test\restructured_json.json', 'w') as f:
    json.dump(restructured, f, indent=2)