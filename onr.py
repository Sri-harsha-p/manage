import json
import re

data = json.load(open(r"C:\User\Desktop\RAG\comp.json"))

def clean_dict(d):
    """
    Recursively remove keys from dictionaries where the value is 'Not Available' or 'Not Applicable' or 'To be identified'
    """
    if isinstance(d, dict):
        return {
            k: clean_dict(v) 
            for k, v in d.items() 
            if v not in ["Not Available", "Not Applicable", "To be identified", "", None]
        }
    elif isinstance(d, list):
        return [clean_dict(item) for item in d]
    else:
        return d

cleaned_data = clean_dict(data)

def parse_temperature_range(temp_str):
    """Extract min and max temperature from string like '-40 TO 80C'"""
    if not temp_str or temp_str in ["Not Available", "Not Applicable"]:
        return None, None
    
    # Match patterns like "-40 TO 80C" or "-40 to 125"
    match = re.search(r'(-?\d+)\s*(?:TO|to)\s*(-?\d+)', str(temp_str))
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def restructure_component(comp):
    """
    Restructure component data following the paper's 7-field approach
    """
    
    # Extract raw fields with safety checks
    def safe_get(key, default=""):
        return comp.get(key, default) if comp.get(key) not in [None, ""] else default
    
    # Parse temperature range
    temp_min, temp_max = parse_temperature_range(safe_get("Operating_Temperature_range_in_Degree_Celsius"))
    
    # FIELD 1: TITLE
    title_parts = [
        safe_get("Manufacturer"),
        safe_get("Manufacturer_Part_No"),
        safe_get("Manufacturer_Part_Name")
    ]
    title = " ".join([p for p in title_parts if p]).strip()
    
    # FIELD 2: DESCRIPTION
    # Build natural language description
    desc_parts = []
    
    # For Cables/Wires
    if safe_get("level_4") in ["Cables", "Wires"]:
        cable_type = safe_get("Cable_Type_example_SGX_or_SXL_or_GXL_or_SGT_or_UL Style_etc")
        if cable_type:
            desc_parts.append(f"{cable_type} type cable")
        
        shielded = safe_get("Shielded_or_Not Shielded")
        if shielded == "Shielded":
            shield_type = safe_get("Type_of_Shield _If_applicable")
            desc_parts.append(f"shielded with {shield_type}" if shield_type else "shielded")
        
        conductors = safe_get("Number_of_conductors")
        if conductors:
            desc_parts.append(f"{conductors} conductor")
        
        twisted = safe_get("Twisted_Pair _or_No_Number_of_Twisted_pairs")
        if twisted == "YES":
            desc_parts.append("twisted pair")
    
    # For Connectors
    elif safe_get("level_4") == "Connectors":
        conn_type = safe_get("Connection_Type")
        if conn_type:
            desc_parts.append(conn_type.lower())
        
        conn_family = safe_get("Connector Family_or_Series")
        if conn_family:
            desc_parts.append(f"{conn_family} series")
        
        sealed = safe_get("Sealed_or_Unsealed")
        if sealed == "Sealed":
            ip_rating = safe_get("Degree_of_Protection_IP_rating")
            desc_parts.append(f"sealed ({ip_rating})" if ip_rating else "sealed")
        
        plug_type = safe_get("Type_Plug Receptacle")
        if plug_type:
            desc_parts.append(f"{plug_type} type")
    
    description = ", ".join(desc_parts) if desc_parts else safe_get("Manufacturer_Part_Name")
    
    # FIELD 3: CATEGORY (Hierarchical)
    category = " > ".join([
        safe_get("level_1"),
        safe_get("level_2"),
        safe_get("level_3"),
        safe_get("level_4")
    ])
    
    # FIELD 4: METADATA (Qualitative attributes)
    metadata_parts = []
    
    # Material information
    outer_material = safe_get("Material_of_Outer_Jacket")
    if outer_material:
        metadata_parts.append(f"Outer jacket: {outer_material}")
    
    conductor_material = safe_get("Material_of_Individual_Conductors")
    if conductor_material:
        metadata_parts.append(f"Conductor: {conductor_material}")
    
    # Color information
    outer_color = safe_get("Color_of_Outer_Jacket")
    wire_colors = safe_get("Color_of_Individual_Wires")
    if outer_color:
        metadata_parts.append(f"Color: {outer_color}")
    if wire_colors:
        metadata_parts.append(f"Wire colors: {wire_colors}")
    
    # For connectors - additional metadata
    if safe_get("level_4") == "Connectors":
        material = safe_get("Material")
        if material:
            metadata_parts.append(f"Material: {material}")
        
        color_finish = safe_get("Color_or_Finish")
        if color_finish:
            metadata_parts.append(f"Finish: {color_finish}")
        
        mounting = safe_get("Inline Mounting feature_type")
        if mounting:
            metadata_parts.append(f"Mounting: {mounting}")
    
    metadata = ", ".join(metadata_parts)
    
    # FIELD 5: NUMERIC SPECIFICATIONS
    numeric_parts = []
    
    # Common numeric specs
    awg = safe_get("AWG_or_Wire Size_For_Individual_Wires") or safe_get("AWG_or_Mire Size_For_Individual Wires")
    if awg:
        numeric_parts.append(f"Wire size: {awg}")
    
    voltage = safe_get("Voltage_ Rating_for_Cable") or safe_get("Voltage_ratingin_Volts") or safe_get("Voltage Rating for_Cable")
    if voltage:
        numeric_parts.append(f"Voltage rating: {voltage}V")
    
    if temp_min is not None and temp_max is not None:
        numeric_parts.append(f"Operating temperature: {temp_min}°C to {temp_max}°C")
    
    # Connector-specific numerics
    poles = safe_get("Number_of_poles") or safe_get("Humber_of_poles")
    if poles:
        numeric_parts.append(f"Poles: {poles}")
    
    current = safe_get("Current Rating_in_Amps") or safe_get("Current_Rating_in_Amps")
    if current:
        numeric_parts.append(f"Current rating: {current}A")
    
    diameter = safe_get("Outer_ Diameter_for_Cable_in_MM")
    if diameter:
        numeric_parts.append(f"Outer diameter: {diameter}mm")
    
    pitch = safe_get("Pitch_in ")
    if pitch:
        numeric_parts.append(f"Pitch: {pitch}mm")
    
    numeric_specs = ", ".join(numeric_parts)
    
    # FIELD 6: BRAND
    brand_parts = []
    
    manufacturer = safe_get("Manufacturer")
    if manufacturer:
        brand_parts.append(f"Manufacturer: {manufacturer}")
    
    series = safe_get("Connector Family_or_Series")
    if series:
        brand_parts.append(f"Series: {series}")
    
    preference = safe_get("Final_Preference_Level")
    if preference:
        brand_parts.append(f"Preference: {preference}")
    
    brand = ", ".join(brand_parts)
    
    # FIELD 7: TECHNICAL DETAILS
    technical_parts = []
    
    # Shield details
    drain_wire = safe_get("Drain Wire_Yes_or_No") or safe_get("Drain Wire Yes_or_No")
    if drain_wire == "YES":
        drain_size = safe_get("AWG_or_Wire Size_of_Drain_Wire")
        technical_parts.append(f"Drain wire: {drain_size}" if drain_size else "Drain wire: Yes")
    
    # Connector technical specs
    ip_rating = safe_get("Degree_of_Protection_IP_rating")
    if ip_rating:
        technical_parts.append(f"IP rating: {ip_rating}")
    
    rohs = safe_get("ROHS_Compliant_Yes_or_to") or safe_get("ROHS_Compliant_Yes_or_No")
    if rohs:
        technical_parts.append(f"ROHS: {rohs}")
    
    ul94 = safe_get("UL 94_Approved_Yes_or_to")
    if ul94:
        technical_parts.append(f"UL94: {ul94}")
    
    weight = safe_get("Weight\n") or safe_get("Base Material weight_in_Grams_Optional")
    if weight:
        technical_parts.append(f"Weight: {weight}")
    
    insulation = safe_get("Insulation resistance")
    if insulation:
        technical_parts.append(f"Insulation: {insulation}")
    
    technical = ", ".join(technical_parts)
    
    # Build structured output following paper's architecture
    structured_component = {
        # Original ID and metadata
        "_id": safe_get("_id"),
        "Manufacturer_Part_No": safe_get("Manufacturer_Part_No"),
        "Internal_Part_Number_1": safe_get("Internal_Part_Number_1"),
        
        # 7 FIELDS for semantic matching (as per paper)
        "fields": {
            "title": title,
            "description": description,
            "category": category,
            "metadata": metadata,
            "numeric_specs": numeric_specs,
            "brand": brand,
            "technical": technical
        },
        
        # FILTERABLE ATTRIBUTES (for pre-filtering before semantic search)
        "filters": {
            "level_4": safe_get("level_4"),
            "manufacturer": safe_get("Manufacturer"),
            "preference_level": safe_get("Final_Preference_Level"),
            # Numeric filters
            "voltage": voltage if voltage else None,
            "poles": int(poles) if poles and str(poles).replace('.','').isdigit() else None,
            "current_rating": float(current) if current and str(current).replace('.','').isdigit() else None,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "conductors": float(safe_get("Number_of_conductors")) if safe_get("Number_of_conductors") else None,
            # Boolean filters
            "shielded": safe_get("Shielded_or_Not Shielded") == "Shielded",
            "sealed": safe_get("Sealed_or_Unsealed") == "Sealed",
            "twisted_pair": safe_get("Twisted_Pair _or_No_Number_of_Twisted_pairs") == "YES",
            "drain_wire": drain_wire == "YES",
            "rohs_compliant": rohs == "yes"
        },
        
        # COMBINED TEXT for fallback/legacy search
        "text": f"{title}. {description}. Category: {category}. Specs: {numeric_specs}. {metadata}. {technical}. {brand}.",
        
        # Keep original raw data for reference
        "raw": comp
    }
    
    return structured_component

# Process all components
restructured_data = [restructure_component(comp) for comp in cleaned_data]

# Save restructured data
with open(r'C:\Users\test\restructured_components.json', 'w', encoding='utf-8') as f:
    json.dump(restructured_data, f, indent=2, ensure_ascii=False)

print(f"✓ Restructured {len(restructured_data)} components")
print(f"✓ Saved to: restructured_components.json")

# Print sample output
if restructured_data:
    print("\n--- SAMPLE STRUCTURED COMPONENT ---")
    sample = restructured_data[0]
    print(f"ID: {sample['_id']}")
    print(f"\nFIELD 1 - Title: {sample['fields']['title']}")
    print(f"FIELD 2 - Description: {sample['fields']['description']}")
    print(f"FIELD 3 - Category: {sample['fields']['category']}")
    print(f"FIELD 4 - Metadata: {sample['fields']['metadata']}")
    print(f"FIELD 5 - Numeric: {sample['fields']['numeric_specs']}")
    print(f"FIELD 6 - Brand: {sample['fields']['brand']}")
    print(f"FIELD 7 - Technical: {sample['fields']['technical']}")
    print(f"\nFilters: {sample['filters']}")