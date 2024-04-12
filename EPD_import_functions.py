import requests
import re
from collections import defaultdict
import pandas as pd

#Connect to the first node of the API data
def connect_node_1(headers, params, valid_untill):
    api_url = f"https://data.eco-platform.org/resource/processes?search=true&distributed=true&virtual=true&metaDataOnly=false&validUntil={valid_untill}&format=json"
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        # The request was successful
        data = response.json()
        return data
    else:
        print('-'*30)
        print('Connection EcoPlatform failed')
        print('-'*30)
    

#Connect to the second node of the API data
def connect_node_2(keyword, data, print_url, print_data, headers, params):
    name_list_2 = []
    uri_list = []
    data_node_2_list = []
    #match_found = False  # Flag to track if a match has been found
    
    #Search by name and read the associated url
    for item in data['data']:
        # Check if 'name' key  exists in the current item
        if 'name' in item:
            name = item['name']
            # Check if the keyword is present in the name
            if keyword == name:# and not match_found:
                name_list_2.append(name)
                uri = item.get('uri')  
                uri_list.append(uri)
                if print_url == 'yes':
                    print(uri_list)
                else:
                    None
                # Extract the urls and access their EPDs
                for url in uri_list:
                    node_2 = requests.get(url, headers=headers, params=params)
                    if node_2.status_code == 200:
                        data_node_2 = node_2.json()
                        data_node_2_list.append(data_node_2)
                        #match_found = True  # Set the flag to True after processing the first match
                        if print_data == 'yes':
                            print(data_node_2_list)
                        else:
                            None
                    else:
                        print("data access not possible")
    return data_node_2_list, name_list_2

#search throug the api data based on a keyword
def search_by_keyword_name(keyword, data):
    name_list = []
    for item in data['data']:
        if 'name' in item:
            name = item['name']
            if keyword.lower() in name.lower():
                name_list.append(name)
    return name_list

#Get the functional unit of a particular EPD, or set of EPDs
def get_FU(keyword, data):
    fu_results = []  # Change variable name to fu_results
    for item in data:
        exchange_info = item.get('exchanges', {})
        if 'exchange' in exchange_info and exchange_info['exchange']:
            fu_quant = exchange_info['exchange'][0].get('resultingflowAmount', None)
            flow_properties = exchange_info['exchange'][0].get('flowProperties', [])
            
            if flow_properties:
                for prop in flow_properties:
                    fu_unit = prop.get('referenceUnit', None)
                    if fu_unit is not None:
                        fu_results.append((fu_quant, fu_unit))
                        break
                else:
                    fu_results.append((fu_quant, f"Unit unknown for '{keyword}' --> check epd online (set print_url = 'yes')"))
                        
    return fu_results  

# Filter the data to only the appropriate environmental data                   
def filter_by_stage(anies_value, target_modules):
    filtered_anies = []
    if 'A1-A3' in target_modules:
        combined_module = next((entry for entry in anies_value if entry.get('module') == 'A1-A3'), None)
        if combined_module:
            # If 'A1-A3' is present, prioritize it and exclude individual modules
            filtered_anies.append(combined_module)
    else:
    # If 'A1-A3' is not present, include individual modules
        filtered_anies.extend(entry for entry in anies_value if entry.get('module') in target_modules)
    return filtered_anies

#Search based on keyword and module --> options for printing EP data, url data
def search_by_keyword_data(keyword, data, target_module, print_url, print_data, headers, params, print_ep_data=None):
    name_list_2 = []
    data_node_2_list = []
    short_description_values = []
    anies_values_list = []
    unit_list = []
    FU_node = []
    combined_list = []
    
    data_node_2_list, name_list_2 = connect_node_2(keyword, data, print_url, print_data, headers, params)   
    FU_node = get_FU(keyword, data_node_2_list)
    
    for item_2 in data_node_2_list:
        lcia_results = item_2.get('LCIAResults')
        if lcia_results:
            for result in lcia_results['LCIAResult']:
                short_description_value = result['referenceToLCIAMethodDataSet']['shortDescription'][0]['value']
                anies_value = result['other']['anies']
                #print(anies_value)
                #consider for the changing structure of anies_value for different datasets
                index = -1 if 'name' in anies_value[-1] else 0
                units = anies_value[index]['value']['shortDescription'][0]['value']

                #remove last value of the environmental data
                if anies_value and isinstance(anies_value[-1], dict) and anies_value[-1].get('name') == 'referenceToUnitGroupDataSet':
                    anies_value = anies_value[:-1]            
                
                filtered_anies = filter_by_stage(anies_value, target_module)
                if print_ep_data == 'yes':
                    print(f"{short_description_value}, unit = {units}:")
                    
                    for entry in filtered_anies:
                        print(entry)
                    print('-' * 30)  # Separator for better readability
                else:
                    None                   
                #Append values to the lists
                short_description_values.append(short_description_value)
                anies_values_list.append(filtered_anies)
                unit_list.append(units)
                #create combined list
                for item in filtered_anies:
                    if 'value' in item:
                        combined_dict = {'label': short_description_value, 'value': item['value'], 'Unit': units, 'Module': item['module']}
                        combined_list.append(combined_dict)  
                    else:
                        print('EPD values missing')
    return name_list_2, FU_node, combined_list, unit_list

def transform_FU(fu_list):
    result_list = []

    for item in fu_list:
        # Split the item into value and unit
        value, unit = item.split(' ', 1)

        # Convert value to float and append to the result list as a tuple
        result_list.append((float(value), unit))

    return result_list

def import_excel_data(df):
    environmental_data = []
    for index, row in df.iterrows():

        data_entry = {
            'label': row['label'],
            'value': str(row['value']),
            'Unit': row['unit'],
            'Module': row['module']
        }
        environmental_data.append(data_entry)
    
    material_name = str(df.iloc[0, 4])
    functional_unit_str = [str(df.iloc[0, 5])]
    functional_unit = transform_FU(functional_unit_str)
    return environmental_data, material_name, functional_unit

