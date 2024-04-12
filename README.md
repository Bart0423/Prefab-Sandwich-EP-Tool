# Prefab-Sandwich-EP-Tool
A Python based LCA tool for quick environmental performance calculations for prefabricated sandwich element


**Code structure:**
EP-Calculation tool.py: The main file that contains the PyQt program. 

EPD_import_functions.py: Contains functions for connecting to the EcoPlatfrom EPD database. It contains additional functions for searching through this database and extracting and filtering data from it.  

IFC_EPD_functions.py: Contains function of extracting data from a Sandwich element IFC as well as multiplication functions for multiplying material quantities with EPD data.

DATA_functions.py: Contains functions for uniform data storage and creating visualizations using this stored data. 

