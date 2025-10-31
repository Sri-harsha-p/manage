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
        return val if val not in [None, ""] else default
    
    # Paper's 7 fields (Table 1) - put ALL specs in appropriate fields
    restructured = {
        "_id": safe_get("_id"),
        
        # Field 1: Title
        "Title": safe_get("Manufacturer_Part_Name"),
        
        # Field 2: Description - ALL descriptive text
        "Description": " ".join(filter(None, [
            safe_get("Cable_Type_example_SGX_or_SXL_or_GXL_or_SGT_or_UL Style_etc"),
            safe_get("Shielded_or_Not Shielded"),
            safe_get("Type_of_Shield _If_applicable"),
            safe_get("Connection_Type"),
            safe_get("Connector Family_or_Series"),
            safe_get("Sealed_or_Unsealed"),
            safe_get("Inline Mounting feature_type"),
            safe_get("Appplication_type _Communication_or_Power")
        ])),
        
        # Field 3: Product category
        "Product_category": " > ".join(filter(None, [
            safe_get("level_1"),
            safe_get("level_2"), 
            safe_get("level_3"),
            safe_get("level_4")
        ])),
        
        # Field 4: Metadata - ALL material, color, texture specs
        "Metadata": " ".join(filter(None, [
            safe_get("Color_of_Outer_Jacket"),
            safe_get("Color_of_Individual_Wires"),
            safe_get("Color_or_Finish"),
            safe_get("Material_of_Outer_Jacket"),
            safe_get("Material_of_Individual_Conductors"),
            safe_get("Material_of_Shield"),
            safe_get("Material"),
            safe_get("Twisted_Pair _or_No_Number_of_Twisted_pairs"),
            safe_get("Drain Wire_Yes_or_No"),
            safe_get("Drain Wire Yes_or_No"),
            safe_get("AWG_or_Wire Size_of_Drain_Wire"),
            safe_get("Keying Yes or No"),
            safe_get("Integrated_Sealed_or_wire_seal"),
            safe_get("ROHS_Compliant_Yes_or_No"),
            safe_get("ROHS_Compliant_Yes_or_to"),
            safe_get("UL 94_Approved_Yes_or_to"),
            safe_get("TPA Available_Yes_or_to"),
            safe_get("CPA_Available_Yes_or_to")
        ])),
        
        # Field 5: Brand
        "Brand": " ".join(filter(None, [
            safe_get("Manufacturer"),
            safe_get("Final_Preference_Level")
        ])),
        
        # Field 6: Numeric - ALL numeric values
        "Numeric": " ".join(filter(None, [
            str(safe_get("Voltage_ Rating_for_Cable")),
            str(safe_get("Voltage_ratingin_Volts")),
            str(safe_get("Number_of_poles")),
            str(safe_get("Humber_of_poles")),
            str(safe_get("Operating_Temperature_range_in_Degree_Celsius")),
            str(safe_get("Number_of_conductors")),
            str(safe_get("AWG_or_Wire Size_For_Individual_Wires")),
            str(safe_get("AWG_or_Mire Size_For_Individual Wires")),
            str(safe_get("Outer_ Diameter_for_Cable_in_MM")),
            str(safe_get("Current Rating_in_Amps")),
            str(safe_get("Current_Rating_in_Amps")),
            str(safe_get("Pitch_in ")),
            str(safe_get("Weight\n")),
            str(safe_get("Base Material weight_in_Grams_Optional")),
            str(safe_get("No_of_rows")),
            str(safe_get("Insulation resistance")),
            str(safe_get("Mating Force Optional")),
            str(safe_get("Unmatting force_Optional")),
            str(safe_get("Contact size"))
        ])),
        
        # Field 7: Additional technical details
        "Technical_details": " ".join(filter(None, [
            safe_get("Degree_of_Protection_IP_rating"),
            safe_get("Type_Plug Receptacle"),
            safe_get("Panel Mountable_Yes_or_to"),
            safe_get("Internal_Part_Number_1"),
            safe_get("Manufacturer_Part _No")
        ]))
    }
    
    return restructured

restructured = [restructure_component(comp) for comp in cleaned_data]

with open(r'C:\Users\test\restructured_json.json', 'w') as f:
    json.dump(restructured, f, indent=2)