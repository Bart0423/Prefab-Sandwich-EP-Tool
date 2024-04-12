import re
import matplotlib.pyplot as plt
import numpy as np


#Function that extracts a list of commen abbreviations between all life stages in the result diciontairy 
def extract_abbreviations(LCA_result_dict):
    abbreviation_sets = []  # List to store sets of abbreviations for each stage

    for stage, stage_data in LCA_result_dict.items():
        abbreviation_set = set()
        for material_name, material_data in stage_data.items():
            for impact_category, impact_data in material_data.items():
                # Extract abbreviations from the impact category
                abbrev_match = re.search(r'\(([^(]*)\)$', impact_category)
                if abbrev_match:
                    abbreviation_set.add(abbrev_match.group(1))

        abbreviation_sets.append(abbreviation_set)

    # Find the common abbreviations across all stages
    common_abbreviations = set.intersection(*abbreviation_sets)

    return common_abbreviations

#function that finds the full impact category name and units for the matching abbreviations 
def find_full_name_and_unit(reference_stage_data, abbreviation):
    for material_data in reversed(list(reference_stage_data.values())):
        for impact_category, impact_data in reversed(material_data.items()):
            if f'({abbreviation})' in impact_category:
                return impact_category, impact_data['unit']
    return None, None


####DATA APPENDING, FILTERING, AND EXTRACTION#####


#Function that check for the precense of GWP, GWP-total or both. If only GWP is present, it replaces this abbreviation with GWP-total
def replace_GWP_GWPtotal(LCA_result_dict):
    modified_categories = {}  # Dictionary to store modified categories for each stage
    for stage, stage_data in LCA_result_dict.items():
        modified_categories[stage] = {}
        for materials, categories in stage_data.items():
            abr_list = []
            for impact_category, impact_data in categories.items():
                # Extract abbreviations from the impact category
                abbrev_match = re.search(r'\(([^(]*)\)$', impact_category)
                if abbrev_match:
                    abbreviations_list = abbrev_match.group(1)
                    abr_list.append(abbreviations_list)
            # Check if "GWP" is in the list and "GWP-total" is not
       
          
            if "GWP" in abr_list and "GWP-total" not in abr_list:
                print('-'*30)
                print(f'GPW/GWP-total verandering in {materials}')
                print('-'*30)
                # Replace "GWP" with "GWP-total" for the current material
                modified_categories[stage][materials] = {}
                for impact_category, impact_data in categories.items():
                    modified_category = impact_category.replace('GWP', 'GWP-total')
                    modified_categories[stage][materials][modified_category] = impact_data
            else:
                # No modification needed, store the original data
                modified_categories[stage][materials] = categories
       
            
    return modified_categories

#Function that creates and appends data to a final dictionairy for the creation of graphs and data visualizations
def append_final_dict(lca_dict, stage, name, multiplied_data):
    
    if stage not in lca_dict:
        lca_dict[stage] = {}
    if name not in lca_dict[stage]:
        lca_dict[stage][name] = {}

        for entry in multiplied_data:
            impact_category = entry['label']
            value = entry['value']
            unit = entry['Unit']

            if impact_category not in lca_dict[stage][name]:
                lca_dict[stage][name][impact_category] = {'value': value, 'unit': unit}
    else:
        for entry in multiplied_data:
            impact_category = entry['label']
            value = float(entry['value'])
            unit = entry['Unit']
            lca_dict[stage][name][impact_category]['value'] += value
    return lca_dict

#Function that filters out the LCA_result_dict to only include equal impact categories
def filter_impact_categories(LCA_result_dict):
    common_abbreviations = extract_abbreviations(LCA_result_dict)
    
    filtered_LCA_result_dict = {}
    for stage, stage_data in LCA_result_dict.items():
        filtered_LCA_result_dict[stage] = {}
        for material_name, material_data in stage_data.items():
            filtered_LCA_result_dict[stage][material_name] = {}
            for impact_category, impact_data in material_data.items():
                abbreviation_match = re.search(r'\(([^(]*)\)$', impact_category)
                if abbreviation_match and abbreviation_match.group(1) in common_abbreviations:
                    filtered_LCA_result_dict[stage][material_name][impact_category] = impact_data
    return filtered_LCA_result_dict

#Function that unifies the impact categories and unit notation for all life stages in the dictionairy. 
def unify_language(filtered_LCA_result_dict, reference_LCA_result_dict):
    unified_LCA_result_dict = {}

    for stage, stage_data in filtered_LCA_result_dict.items():
        unified_LCA_result_dict[stage] = {}
        
        for material_name, material_data in stage_data.items():
            unified_LCA_result_dict[stage][material_name] = {}
            
            for impact_category, impact_data in material_data.items():
                
                # Find the full name corresponding to the abbreviation
                abbreviation_match = re.search(r'\(([^(]*)\)$', impact_category)
                if abbreviation_match:
                    abbreviation = abbreviation_match.group(1)
                    full_name, unit = find_full_name_and_unit(reference_LCA_result_dict, abbreviation)
                   
                    if full_name:
                        unified_impact_category = impact_category.replace(f'{impact_category}', f'{full_name}')
                        unified_LCA_result_dict[stage][material_name][unified_impact_category] = {
                            'value': impact_data['value'],
                            'unit': unit
                            }
                    else:
                        unified_LCA_result_dict[stage][material_name][impact_category] = impact_data
                else:
                    unified_LCA_result_dict[stage][material_name][impact_category] = impact_data
    
    return unified_LCA_result_dict

#Function that divides the values of the LCA result dict by the entered surface are of the sandwich element
def divide_values_by_surface(LCA_dict, target_stage, surface=None):
    if surface is None:
        print("Error: 'surface' is not defined. Division not performed.")
        return
    for stage, stage_data in LCA_dict.items():
        if stage == target_stage:
            for material, material_data in stage_data.items():
                for impact, impact_data in material_data.items():
                    for key, value in impact_data.items():
                        if key == 'value':
                            LCA_dict[stage][material][impact][key] = value / surface
        else:
            continue
    return LCA_dict


###CREATION OF ADDITIONAL DICTIONAIREIS####


#Function that sums the values of an impact category for each life stage
def sum_values_by_impact_category_stages(LCA_dict, impact_category_abbreviation):
    summed_dict = {}
    
    for stage, stage_data in LCA_dict.items():
        stage_sum = {}
        for material_data in stage_data.values():
            for impact_category, impact_data in material_data.items():
                abbrev_match = re.search(r'\(([^(]*)\)$', impact_category)
                if abbrev_match:
                    abbreviation = abbrev_match.group(1)
                    if abbreviation == impact_category_abbreviation:
                        summed_dict[stage] = {impact_category: impact_data}
                        if impact_category not in stage_sum:
                            stage_sum[impact_category] = {'value': 0.0, 'unit': impact_data['unit']}
                        stage_sum[impact_category]['value'] += impact_data['value']
        summed_dict[stage] = stage_sum
    
    return summed_dict

#Function that creates a new dictionairy containing Materials and their values for a selected impact category and life cycle stage 
def filter_dict_by_impact_category(LCA_dict, life_cycle_stage, impact_category_abbreviation):
    filtered_dict = {}
    for material, material_data in LCA_dict[life_cycle_stage].items():
        for impact_category, impact_data in material_data.items():
            abbrev_match = re.search(r'\(([^(]*)\)$', impact_category)
            if abbrev_match:
                abbreviation = abbrev_match.group(1)
                if abbreviation == impact_category_abbreviation:
                    filtered_dict[material] = {impact_category: impact_data}
    return filtered_dict

#Function that creates a new dictionairy containing impact categories and their respective summed values across all life stages --> for visualizations
def create_dict_categories_totalsums(LCA_result_dict):
    
    filtered_abbreviations = extract_abbreviations(LCA_result_dict)

    summed_values_dict = {}
    for stage, stage_data in LCA_result_dict.items():
        for material_name, material_data in stage_data.items():
            for impact_category, impact_data in material_data.items():
                abbrev_match = re.search(r'\(([^(]*)\)$', impact_category)
                if abbrev_match:
                    abbreviation = abbrev_match.group(1)
                    if abbreviation in filtered_abbreviations:
                        # Sum values for the identified common impact categories
                        if abbreviation not in summed_values_dict:
                            summed_values_dict[abbreviation] = 0.0
                        summed_values_dict[abbreviation] += impact_data['value']

    return summed_values_dict

#Function that creates a new dictionairy containing the summed values for each impact category for each material across all life stages
def create_dict_material_categories_totalsums(abbreviation, input_dict):
    summed_dict = {}

    # Loop through each life cycle stage
    for stage, stage_data in input_dict.items():
        # Loop through each material in the stage
        for material, material_data in stage_data.items():
            if material not in summed_dict:
                # Initialize entry in summed_dict for the material
                summed_dict[material] = {}

            # Loop through each impact category in the material
            for impact_category, impact_data in material_data.items():
                abbrev_match = re.search(r'\(([^(]*)\)$', impact_category)
                # If the impact category doesn't exist in the summed_dict for the material, initialize it
                if abbrev_match and abbrev_match.group(1) == abbreviation:
                    if impact_category not in summed_dict[material]:
                        summed_dict[material][impact_category] = {'value': 0, 'unit': impact_data['unit']}

                    # Sum the values across all stages for the impact category
                    summed_dict[material][impact_category]['value'] += impact_data['value']

    return summed_dict


####FUNCTION FOR CREATING VISUALIZATIONS####


#Bar plot containing total impact category values for materials summed across all life cycle stages
def plot_material_impact_total_bar_chart(impact_category, LCA_dict):
    materials = list(LCA_dict['A1'].keys())
    bar_chart_dict = create_dict_material_categories_totalsums(impact_category, LCA_dict)
    values = []
    units = None
    
    for material, material_data in bar_chart_dict.items():
        for category, category_data in material_data.items():
            values.append(category_data['value'])
            units = category_data['unit']

    total_value = sum(values)
    
    # Change color palette
    colors = plt.cm.get_cmap('viridis')(np.linspace(0, 1, len(materials)))

    # Bar chart
    plt.figure(figsize=(8, 9))
    bars = plt.bar(np.arange(len(materials)), values, color=colors, edgecolor='black')  # Add edge color
    plt.xlabel('Materials', weight = 'bold')
    plt.ylabel(f'{units}/m2')
    plt.title(f'{impact_category} Impact Across Materials', weight = 'bold')

    

    # Add horizontal gridlines
    #plt.grid(axis='y', linestyle='--', zorder=0)

    # Remove x-axis ticks
    plt.xticks([])

    ymax = max(values) * 1.2

    # Add dashed line for the x-axis to highlight negative values
    plt.axhline(0, color='black', linestyle='dashed', linewidth=1)

    # Add percentages above each bar
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_value) * 100
        if height < 0:
            
            plt.text(bar.get_x() + bar.get_width() / 2, 0, f'{percentage:.1f}%', ha='center', va='bottom')
        else:
            plt.text(bar.get_x() + bar.get_width() / 2, height + (0.025*ymax), f'{percentage:.1f}%', ha='center', va='bottom')

    ymax = ymax+0.06*ymax
    ymin = min(values) * 1.5 if min(values) < 0 else 0
    
    # Set ymax
    plt.ylim(ymin, ymax)
    
    # Display total quantity
    plt.text(1, (ymax-0.05*ymax), f'{impact_category}: {sum(values):.2f} {units}/m2', ha='center', fontsize='10')
    
    # Create legend
    plt.legend(bars, materials, title="Legend", title_fontproperties={'weight':'bold', 'size': 'large'}, bbox_to_anchor=(0.5, -0.1), loc="upper center", fancybox=True, shadow=False, ncol=1, fontsize='medium')
    #plt.xticks(np.arange(len(materials)), materials, rotation=45, ha='right')  # Adjust rotation for material names
    plt.tight_layout()
    plt.show()

#Bar plot containing total impact category values for materials for a selected life cycle stage
def plot_material_impact_stage_bar_chart(impact_category, stage, LCA_dict):
    materials = list(LCA_dict[stage].keys())
    bar_chart_dict = filter_dict_by_impact_category(LCA_dict, stage, impact_category)
    values = []
    units = None
    
    for material, material_data in bar_chart_dict.items():
        for category, category_data in material_data.items():
            values.append(category_data['value'])
            units = category_data['unit']

    total_value = sum(values)
    
    # Change color palette
    colors = plt.cm.get_cmap('viridis')(np.linspace(0, 1, len(materials)))

    # Bar chart
    plt.figure(figsize=(8, 9))

    # Draw horizontal gridlines
    
    
    bars = plt.bar(np.arange(len(materials)), values, color=colors, edgecolor='black')  # Add edge color
    plt.xlabel('Materials', weight = 'bold')
    plt.ylabel(f'{units}/m2')
    plt.title(f'{impact_category} Impact Across Materials for stage {stage}', weight = 'bold')

    # Add light grey grid lines behind the bars
    
    #plt.grid(axis='y', color='lightgrey', linestyle='-', linewidth=0.5, zorder=0)

    
    
    # Remove x-axis ticks
    plt.xticks([])

    # Add dashed line for the x-axis to highlight negative values
    plt.axhline(0, color='black', linestyle='dashed', linewidth=1)

    ymax = max(values) * 1.2
    
    
    # Add percentages above each bar for negative values, otherwise below
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_value) * 100
        if height < 0:
            plt.text(bar.get_x() + bar.get_width() / 2, 0, f'{percentage:.1f}%', ha='center', va='bottom')
        else:
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.025 * ymax, f'{percentage:.1f}%', ha='center', va='bottom')
    
    
    ymax = ymax+0.06*ymax
    ymin = min(values) * 1.5 if min(values) < 0 else 0
    
    
    # Set ymax
    plt.ylim(ymin, ymax)
    
    # Display total quantity
    plt.text(1, (ymax-0.05*ymax), f'{impact_category}: {sum(values):.2f} {units}/m2', ha='center', fontsize='10')

    # Create legend
    plt.legend(bars, materials, title="Legend", title_fontproperties={'weight':'bold', 'size': 'large'}, bbox_to_anchor=(0.5, -0.1), loc="upper center", fancybox=True, shadow=False, ncol=1, fontsize='medium')

    
    
    plt.tight_layout()
    plt.show()

#Bar plot containing total impact category values for each life cycle stage
def plot_stage_impact_total_bar_chart(impact_category, LCA_dict):
    stages = list(LCA_dict.keys())
    bar_chart_dict = sum_values_by_impact_category_stages(LCA_dict, impact_category)
    values = []
    units = None
    
    for material, material_data in bar_chart_dict.items():
        for category, category_data in material_data.items():
            values.append(category_data['value'])
            units = category_data['unit']

    total_value = sum(values)
    
    # Change color palette
    colors = plt.cm.get_cmap('viridis')(np.linspace(0, 1, len(stages)))

    # Bar chart
    plt.figure(figsize=(8, 9))
    bars = plt.bar(np.arange(len(stages)), values, color=colors, edgecolor='black')  # Add edge color
    plt.xlabel('Stages', weight = 'bold')
    plt.ylabel(f'{units}/m2')
    plt.title(f'{impact_category} Impact Across Stages', weight = 'bold')
    #plt.grid(axis='y', linestyle='--')
    ymax = max(values) * 1.2

    # Add dashed line for the x-axis to highlight negative values
    plt.axhline(0, color='black', linestyle='dashed', linewidth=1)

    # Add percentages above each bar
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_value) * 100
        perc_place = height - 0.025
        if height < 0:
            
            plt.text(bar.get_x() + bar.get_width() / 2, 0, f'{percentage:.1f}%', ha='center', va='bottom')
        else:
            plt.text(bar.get_x() + bar.get_width() / 2, height + (0.025*ymax), f'{percentage:.1f}%', ha='center', va='bottom')

    ymax = ymax+0.06*ymax
    ymin = perc_place * 1.5 if min(values) < 0 else 0
    
    # Set ymax
    plt.ylim(ymin, ymax)
    
    # Display total quantity
    plt.text(1, (ymax-0.05*ymax), f'{impact_category}: {sum(values):.2f} {units}/m2', ha='center', fontsize='10')
    
    # Place stage names under the bars
    plt.xticks(np.arange(len(stages)), stages)


    # Create legend
    #plt.legend(bars, stages, title="Legend", bbox_to_anchor=(0.5, -0.1), loc="upper center", fancybox=True, shadow=False, ncol=1)

    
    plt.tight_layout()
    plt.show()