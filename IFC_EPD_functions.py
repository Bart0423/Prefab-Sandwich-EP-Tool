import ifcopenshell
import re
from collections import defaultdict

#Import the weight of the rebar out of the .ifc file
def ifc_import_weight_rebar(model, leaf_type=None):
    bars = model.by_type('IfcReinforcingBar')
    total_weight = 0

    for bar in bars:
        psets_bars = ifcopenshell.util.element.get_psets(bar) 

        # Check if 'Byldis_wapening' exists in psets_bars
        if 'Byldis_wapening' in psets_bars:
            wapening_data = psets_bars['Byldis_wapening']

            # Check if 'Betonstaal kwaliteit' and 'Aantal staven in groep' exist
            if 'Aantal staven in groep' in wapening_data:
                # Check if 'Wapening_groep' exists and contains 'BU' or outer leaf
                
                if leaf_type is None or (leaf_type.lower() == 'inner leaf' and 'Wapening_groep' in wapening_data and 'bu' not in wapening_data['Wapening_groep'].lower()) or (leaf_type.lower() == 'outer leaf' and 'Wapening_groep' in wapening_data and 'bu' in wapening_data['Wapening_groep'].lower()):
                    quantity = wapening_data['Aantal staven in groep']
                    
                    # Check if 'Default' exists in psets_bars
                    if 'Default' in psets_bars:
                        weight_per_bar = psets_bars['Default']['WEIGHT']
                        total_weight += weight_per_bar * quantity
                        
    return total_weight


def ifc_import_volume(model, material_type=None):
    element_volumes = 0

    elements = model.by_type('IfcElement')
    for element in elements:
        if element.is_a('IfcWall') or element.is_a('IfcSlab'):
            # Retrieve the BaseQuantities and Byldis_onderdeel gegevens property sets
            psets = ifcopenshell.util.element.get_psets(element)
            base_quantities = psets.get('BaseQuantities', {})
            onderdeel_gegevens = psets.get('Byldis_onderdeel gegevens', {})

            # Check if Onderdeel_01_groep exists for the wall or slab
            if 'Onderdeel_01_groep' in onderdeel_gegevens:
                onderdeel_name = onderdeel_gegevens['Onderdeel_01_groep']

                # Check for material type
                if material_type is None or onderdeel_name.lower() in [mt.lower() for mt in material_type]:
                    # Check if BaseQuantities exists for the wall or slab
                    if base_quantities:
                        for prop_name, prop_value in base_quantities.items():
                            if prop_name == 'NetVolume':
                                
                                element_volumes +=  prop_value

    return element_volumes

#multipy the extracted .ifc weights with the EPD data 
def multiply_weight(api_data, api_fu, ifc_weight):
    matching_fu = next((fu for fu in api_fu if fu[1] is not None), None)
    if matching_fu:
        fu_quant, fu_unit = matching_fu
        # Check if the functional unit quantity is not 0 to avoid division by zero
        if fu_quant != 0:
            divided_weight = ifc_weight / fu_quant

    
    multiplied_list_weight = []
    for entry in api_data:
        value = float(entry['value'].replace(',', '.'))
        multiplied_entry = {
        'label': entry['label'],
        'value': str(value * divided_weight),  # Multiply by the corresponding divided weight
        'Unit': entry['Unit'],
        'Module': entry['Module']
        }
        multiplied_list_weight.append(multiplied_entry)
    return multiplied_list_weight

#multiply the extracted .ifc volumes with the EPD data
def multiply_volume(api_data, api_FU, ifc_volume):
    divisor_value = api_FU[0][0] if api_FU else 1.0 
    normalized_volume = ifc_volume / divisor_value
   
    multiplied_list_volume = []

    for entry in api_data:
        value = float(entry['value'].replace(',', '.'))
        multiplied_entry = {
        'label': entry['label'],
        'value': str(value * normalized_volume),  # Convert to float, multiply, and convert back to string
        'Unit': entry['Unit'],
        'Module': entry['Module']
        }
        multiplied_list_volume.append(multiplied_entry)
    return multiplied_list_volume

