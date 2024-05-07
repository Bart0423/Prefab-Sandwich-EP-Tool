import math
import pandas as pd
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint, Qt
import ifcopenshell.util.element

from EPD_import_functions import *
from IFC_EPD_functions import *
from DATA_functions import *
import sys
import json

class LineWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LineWidget, self).__init__(parent)
        self.frames = []
        self.draw_arrowhead = True  # Toggle for drawing arrowhead
    def addFrames(self, *frames):
        self.frames.extend(frames)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)  # Enable antialiasing
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))  # Set pen color and width
        for i in range(0, len(self.frames), 2):
            frame1 = self.frames[i]
            frame2 = self.frames[i + 1]
            rect1 = frame1.geometry()
            rect2 = frame2.geometry()
            border_width = frame1.frameWidth()  # Assuming all frames have the same border width
            # Calculate the coordinates of the top center of the first frame
            center1_top = (rect1.topLeft().x() + rect1.topRight().x()) // 2, rect1.top() + border_width -10
            # Calculate the coordinates of the left center of the second frame
            center2_left = rect2.left() + border_width -10, ((rect2.topLeft().y() + rect2.bottomLeft().y()) // 2) -5
            # Draw line connecting the desired points
            painter.drawLine(center1_top[0], center1_top[1], center2_left[0], center2_left[1])

class HopperCapacityWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label_hoppercapacity = QLabel('Capacity of hopper:')
        self.input_field_hoppercapacity = QLineEdit()
        self.save_button_hoppercapacity = QPushButton('Save')

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_hoppercapacity)
        layout.addWidget(self.input_field_hoppercapacity)
        self.input_field_hoppercapacity.setText('1.5')
        layout.addWidget(self.save_button_hoppercapacity)

        # Connect button click event to calculate method
        self.save_button_hoppercapacity.clicked.connect(self.save_hoppercapacity)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Define Sandwich Element Properties')
        self.setGeometry(300, 300, 400, 200)

    def save_hoppercapacity(self):
        try:
            # Get the input value
            self.hoppercapacity_factor = float(self.input_field_hoppercapacity.text())
            self.close()
            # Perform some calculation (you can replace this with your own logic)
            
            
        except ValueError:
            # Handle invalid input
            print('no data entered')

class MouldReuseWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label_mouldreuse = QLabel('Amount of time mould can be reused:')
        self.input_field_mouldreuse = QLineEdit()
        self.save_button_mouldreuse = QPushButton('Save')

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_mouldreuse)
        layout.addWidget(self.input_field_mouldreuse)
        layout.addWidget(self.save_button_mouldreuse)

        # Connect button click event to calculate method
        self.save_button_mouldreuse.clicked.connect(self.save_mouldreuse)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Define Sandwich Element Properties')
        self.setGeometry(300, 300, 400, 200)
        
    def save_mouldreuse(self):
        try:
            # Get the input value
            self.moldreuse_factor = float(self.input_field_mouldreuse.text())
            self.close()
            # Perform some calculation (you can replace this with your own logic)
            
            
        except ValueError:
            # Handle invalid input
            print('no data entered')

class SquareMeterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label_surface = QLabel('Enter Amount of Square Meters:')
        self.input_field_surface = QLineEdit()
        self.result_label = QLabel('')
        self.calculate_button = QPushButton('Save')

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_surface)
        layout.addWidget(self.input_field_surface)
        layout.addWidget(self.result_label)
        layout.addWidget(self.calculate_button)

        # Connect button click event to calculate method
        self.calculate_button.clicked.connect(self.calculate)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Define Sandwich Element Properties')
        self.setGeometry(300, 300, 400, 200)
        
    def calculate(self):
        try:
            # Get the input value
            self.square_meters = float(self.input_field_surface.text())
            # Perform some calculation (you can replace this with your own logic)
            result = f"The entered surface is {self.square_meters} square meters"
            self.result_label.setText(result)
            
        except ValueError:
            # Handle invalid input
            self.result_label.setText('Please enter a valid number.')

class EmissionFactorsWindow_A3(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Process Emission Factors Editor")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()

        self.emission_factors_A3 = {}

        self.add_emission_factor_A3("Electricity", "GWP-total", "kgCO2/kWh", default_value= 0.37)
        self.add_emission_factor_A3("Vibration table", "GWP-total", "kgCO2 per use", default_value= 1.8)
        self.add_emission_factor_A3("Loading hopper", "GWP-total", "kgCO2/kg", default_value=0.01981)
        self.add_emission_factor_A3("Hopper transport (by crane)", "GWP-total", "kgCO2 per use", default_value= 48.03)
        self.add_emission_factor_A3("Gantry crane (1 crane)", "GWP-total", "kgCO2 per use", default_value=48.03)
        self.add_emission_factor_A3("Gantry crane (2 cranes)", "GWP-total", "kgCO2 per use", default_value=96.06)
        self.add_emission_factor_A3("Rebar transportation (by crane)", "GWP-total", "kgCO2 per use", default_value= 48.03)


        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_emission_factor_A3)

        self.layout.addWidget(save_button)
        self.setLayout(self.layout)

    

    def add_emission_factor_A3(self, process, label_text, unit, default_value=0.0):
        # Find the existing layout for the transport mode or create a new one
        existing_layout = None
        for i in range(1, self.layout.count()):
            row_layout = self.layout.itemAt(i)
            if hasattr(row_layout, 'Process') and row_layout.process == process:
                existing_layout = row_layout
                break

        if existing_layout is None:
            # If the layout for the transport mode doesn't exist, create it
            transport_layout = QHBoxLayout()
            transport_label = QLabel(process, self)
            font = transport_label.font()
            font.setBold(True)
            transport_label.setFont(font)
            transport_layout.addWidget(transport_label)
            self.layout.addLayout(transport_layout)

        # Create a new layout for the emission factor
        row_layout = QHBoxLayout()

        # Label for the emission factor
        emission_label = QLabel(label_text, self)
        row_layout.addWidget(emission_label)

        # Line edit for entering the emission factor
        line_edit = QLineEdit(str(default_value), self)
        row_layout.addWidget(line_edit)

        # Label for the unit
        unit_label = QLabel(unit, self)
        row_layout.addWidget(unit_label)

        # Store the transport mode along with the line edit widget
        row_layout.process = process
        row_layout.line_edit = line_edit

        # Add the row layout to the main layout
        self.layout.addLayout(row_layout)

    def save_emission_factor_A3(self):
        for i in range(1, self.layout.count() -1):
            row_layout = self.layout.itemAt(i)

            if row_layout is not None and hasattr(row_layout, 'line_edit'):
                process = row_layout.process
                emission_factor_label_A3 = row_layout.itemAt(0).widget().text()
                entered_value_A3 = float(row_layout.line_edit.text())

                if process not in self.emission_factors_A3:
                    self.emission_factors_A3[process] = {}
                
                self.emission_factors_A3[process][emission_factor_label_A3] = entered_value_A3

        self.close()
      
        return self.emission_factors_A3

class EmissionFactorsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Emission Factors Editor")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()

        # Add the dictionairy
        self.emission_factors_A2 = {}
        # Add rows for each emission factor
        self.add_emission_factor_row("Truck-fully laden", "GWP-total", "gCO2e/kg/km", default_value=0.07375)
        #self.add_emission_factor_row("Truck-fully laden","POCP", "gNMVOCe/kg/km", default_value= 0.123)
        
        self.add_emission_factor_row("Truck-average laden","GWP-total", "gCO2e/kg/km", default_value=0.10749 )
        #self.add_emission_factor_row("Truck-average laden","POCP", "gNMVOCe/kg/km", default_value= 0.123)
        
        self.add_emission_factor_row("Sea transport", "GWP-total", "gCO2e/kg/km", default_value=0.01614)
        #self.add_emission_factor_row("Sea transport","POCP", "gNMVOCe/kg/km", default_value= 0.12345)
       
        # Save button to save the entered values
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_emission_factors)

        # Add the button to the main layout
        self.layout.addWidget(save_button)

        self.setLayout(self.layout)
        
    #Function that allows for adding rows for different impact categories
    def add_emission_factor_row(self, transport_mode, label_text, unit, default_value=0.0):
        # Find the existing layout for the transport mode or create a new one
        existing_layout = None
        for i in range(1, self.layout.count()):
            row_layout = self.layout.itemAt(i)
            if hasattr(row_layout, 'transport_mode') and row_layout.transport_mode == transport_mode:
                existing_layout = row_layout
                break

        if existing_layout is None:
            # If the layout for the transport mode doesn't exist, create it
            transport_layout = QHBoxLayout()
            transport_label = QLabel(transport_mode, self)
            font = transport_label.font()
            font.setBold(True)
            transport_label.setFont(font)
            transport_layout.addWidget(transport_label)
            self.layout.addLayout(transport_layout)

        # Create a new layout for the emission factor
        row_layout = QHBoxLayout()

        # Label for the emission factor
        emission_label = QLabel(label_text, self)
        row_layout.addWidget(emission_label)

        # Line edit for entering the emission factor
        line_edit = QLineEdit(str(default_value), self)
        row_layout.addWidget(line_edit)

        # Label for the unit
        unit_label = QLabel(unit, self)
        row_layout.addWidget(unit_label)

        # Store the transport mode along with the line edit widget
        row_layout.transport_mode = transport_mode
        row_layout.line_edit = line_edit

        # Add the row layout to the main layout
        self.layout.addLayout(row_layout)

    #Function that saves the entered emission factors
    def save_emission_factors(self):
        # Iterate through all line edits and retrieve entered values
        for i in range(1, self.layout.count() - 1):
            row_layout = self.layout.itemAt(i)

            if row_layout is not None and hasattr(row_layout, 'line_edit'):
                transport_mode = row_layout.transport_mode
                emission_factor_label = row_layout.itemAt(0).widget().text()
                entered_value = float(row_layout.line_edit.text())

                # Store the values in the dictionary
                if transport_mode not in self.emission_factors_A2:
                    self.emission_factors_A2[transport_mode] = {}

                self.emission_factors_A2[transport_mode][emission_factor_label] = entered_value
        # Close the window when Save button is clicked
        self.close()
        return self.emission_factors_A2
    
class DensitiesWindow(QtWidgets.QDialog):
    def __init__(self, names, parent=None):
        super(DensitiesWindow, self).__init__(parent)
        self.names = names
        self.densities = {}

        self.setWindowTitle("Set Densities")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        for name in self.names:
            label = QtWidgets.QLabel(name)
            densityLineEdit = QtWidgets.QLineEdit()
            layout.addWidget(label)
            layout.addWidget(densityLineEdit)

            # Store the QLineEdit in a dictionary with the name as the key
            self.densities[name] = densityLineEdit

        setDensitiesButton = QtWidgets.QPushButton("Set Densities")
        setDensitiesButton.clicked.connect(self.setDensities)
        layout.addWidget(setDensitiesButton)

        self.setLayout(layout)
        
    def setDensities(self):
        # Extract densities from the line edits and store them in a dictionary
        self.density_values = {name: float(density.text()) for name, density in self.densities.items() if density.text()}

        # Do something with the density values (e.g., update the original data structure)
        if self.density_values is not None:
            self.close()
            return self.density_values
        # Close the window
        
class SearchResultsDialog(QtWidgets.QDialog):
    def __init__(self, name_list, parent=None):
        super(SearchResultsDialog, self).__init__(parent)
        self.setWindowTitle("Search Results")

        self.resize(700, 700)
        
        # Create a label to display the number of search results
        self.search_result_number_label = QtWidgets.QLabel(self)
        self.search_result_number_label.setObjectName("search_result_number_label")
        self.search_result_number_label.setText(f"Number of Results: {len(name_list)}")

        self.name_list_widget = QtWidgets.QListWidget(self)
        self.name_list_widget.addItems(name_list)
        
        self.ok_button = QtWidgets.QPushButton("OK", self)
        self.ok_button.clicked.connect(self.on_ok_button_clicked)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.search_result_number_label, alignment=QtCore.Qt.AlignTop)  # Align the label to the top
        layout.addWidget(self.name_list_widget)
        layout.addWidget(self.ok_button)
    # function that enters the selected name into the line edit box
    def on_ok_button_clicked(self):
        selected_item = self.name_list_widget.currentItem()

        if selected_item is not None:
            self.accept()

class Eco_settingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Eco_settingsDialog, self).__init__(parent)

        self.setWindowTitle("Set Valid Until Year")
        self.setGeometry(250, 250, 250, 50)
        
        self.valid_until_label = QtWidgets.QLabel("EPDs valid until:", self)
        self.valid_until_spinbox = QtWidgets.QSpinBox(self)
        self.valid_until_spinbox.setRange(2024, 2100)  # Set the range 
        self.valid_until_spinbox.setValue(2028)  # Set a default value 

        self.ok_button = QtWidgets.QPushButton("Connect to Eco Platform", self)
        self.ok_button.clicked.connect(self.accept)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.valid_until_label)
        layout.addWidget(self.valid_until_spinbox)
        layout.addWidget(self.ok_button)

class ImportSelectionWindow(QtWidgets.QWidget):
    dataProcessed = QtCore.pyqtSignal(object, object, object, object, object)
    def __init__(self, selected_file):
        super().__init__()
        self.setWindowTitle("Import Selection")
        self.resize(300, 200)
        layout = QVBoxLayout(self)
        self.selected_file = selected_file  # Set selected_file as an attribute of ImportSelectionWindow

        # Initialize the checkboxes dictionary
        self.checkboxes = {}

        # Insulation section
        insulation_label = QtWidgets.QLabel("Insulation", self)
        font = insulation_label.font()
        font.setBold(True)
        insulation_label.setFont(font)
        layout.addWidget(insulation_label)
        insulation_checkbox = QtWidgets.QCheckBox("Insulation material volume", self)
        insulation_checkbox.stateChanged.connect(self.handle_checkbox_state)
        layout.addWidget(insulation_checkbox)
        self.checkboxes["Insulation material volume"] = insulation_checkbox

        # Inner leaf section
        inner_leaf_label = QtWidgets.QLabel("Inner leaf", self)
        font = insulation_label.font()
        font.setBold(True)
        inner_leaf_label.setFont(font)
        layout.addWidget(inner_leaf_label)
        concrete_volume_checkbox_inner = QtWidgets.QCheckBox("Concrete volume", self)
        concrete_volume_checkbox_inner.stateChanged.connect(self.handle_checkbox_state)
        layout.addWidget(concrete_volume_checkbox_inner)
        self.checkboxes["Concrete volume - Inner leaf"] = concrete_volume_checkbox_inner

        rebar_weight_checkbox_inner = QtWidgets.QCheckBox("Rebar weight", self)
        rebar_weight_checkbox_inner.stateChanged.connect(self.handle_checkbox_state)
        layout.addWidget(rebar_weight_checkbox_inner)
        self.checkboxes["Rebar weight - Inner leaf"] = rebar_weight_checkbox_inner

        # Outer leaf section
        outer_leaf_label = QtWidgets.QLabel("Outer leaf", self)
        font = insulation_label.font()
        font.setBold(True)
        outer_leaf_label.setFont(font)
        layout.addWidget(outer_leaf_label)
        concrete_volume_checkbox_outer = QtWidgets.QCheckBox("Concrete volume", self)
        concrete_volume_checkbox_outer.stateChanged.connect(self.handle_checkbox_state)
        layout.addWidget(concrete_volume_checkbox_outer)
        self.checkboxes["Concrete volume - Outer leaf"] = concrete_volume_checkbox_outer

        rebar_weight_checkbox_outer = QtWidgets.QCheckBox("Rebar weight", self)
        rebar_weight_checkbox_outer.stateChanged.connect(self.handle_checkbox_state)
        layout.addWidget(rebar_weight_checkbox_outer)
        self.checkboxes["Rebar weight - Outer leaf"] = rebar_weight_checkbox_outer

        # Add Import IFC File button
        import_button = QPushButton("Import IFC File", self)
        import_button.clicked.connect(self.import_and_process_data)
        layout.addWidget(import_button)

        self.result_ifc_ins = None
        self.result_ifc_inner_con = None
        self.result_ifc_inner_rebar = None
        self.result_ifc_outer_con = None
        self.result_ifc_outer_rebar = None

    def handle_checkbox_state(self):
        self.process_selected_data()

    def import_and_process_data(self):
        file_dialog = QFileDialog(self, "Open IFC File", "", "IFC Files (*.ifc);;All Files (*)")
        if file_dialog.exec_() == QFileDialog.Accepted:
            self.selected_file = file_dialog.selectedFiles()[0]
            print(f"Importing file: {self.selected_file}")
            # Process data based on selected checkboxes
            self.process_selected_data()
            self.dataProcessed.emit(
            self.result_ifc_ins,
            self.result_ifc_inner_con,
            self.result_ifc_inner_rebar,
            self.result_ifc_outer_con,
            self.result_ifc_outer_rebar
        )
            self.close()
        else:
            print("No file selected.")  # Print a message if the user cancels the file dialog

    def process_selected_data(self):
        if self.selected_file is not None:
            model = ifcopenshell.open(self.selected_file)
            selected_checkboxes = []
            for index, checkbox in self.checkboxes.items():
                if checkbox.isChecked():
                    selected_checkboxes.append(index)
                    
                    if index == 'Insulation material volume':
                        material_type = ['Insulation', 'isolatie']
                        self.result_ifc_ins = ifc_import_volume(model, material_type)

                    elif index == 'Concrete volume - Inner leaf':
                        material_type = ["Inner leaf", 'binnenblad']
                        self.result_ifc_inner_con = ifc_import_volume(model, material_type)
        
                    elif index == 'Rebar weight - Inner leaf':
                        leaf = 'Inner leaf'
                        self.result_ifc_inner_rebar = ifc_import_weight_rebar(model, leaf)
                    elif index == 'Concrete volume - Outer leaf':
                        material_type = ['Outer leaf', 'buitenblad']
                        self.result_ifc_outer_con = ifc_import_volume(model, material_type)

                    elif index == 'Rebar weight - Outer leaf':
                        leaf = 'Outer leaf'
                        self.result_ifc_outer_rebar = ifc_import_weight_rebar(model, leaf)
                        
            if not selected_checkboxes:
                print('No checkboxes selected')
        
        return self.result_ifc_ins, self.result_ifc_inner_con, self.result_ifc_inner_rebar, self.result_ifc_outer_con, self.result_ifc_outer_rebar

class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
         
    def setupUi(self, MainWindow):
        # Initialize line count
        self.line_count = 1
        self.line_count_inner = 51
        self.line_count_outer = 101
        self.line_count_mould = 251
        self.line_counter_A2 = 5
        self.linecounter_sand_A3 = 1
        self.line_counter_A4 = 5
        
        


        MainWindow.resize(1060, 850)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create a tab widget and set it as the central widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1051, 791))
        self.tabWidget.setObjectName("tabWidget")
        # Create the first tab
        self.tab_1 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_1, "A1")
        # Set the layout for the first tab
        self.tabLayout_1 = QtWidgets.QGridLayout(self.tab_1)
        
        #Large insulation label
        self.label_Insulation = QtWidgets.QLabel(self.tab_1)
        self.label_Insulation.setFont(QFont("Arial", 12, QFont.Bold))  # Set font size and make it bold
        self.label_Insulation.setFrameShape(QtWidgets.QFrame.Box)
        self.label_Insulation.setTextFormat(QtCore.Qt.PlainText)
        self.label_Insulation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Insulation.setIndent(-1)
        self.label_Insulation.setObjectName("label_Insulation")
        self.tabLayout_1.addWidget(self.label_Insulation, 0, 0, 1, 100)
        
        #large inner leaf label
        self.label_InnerLeaf = QtWidgets.QLabel(self.tab_1)
        self.label_InnerLeaf.setFont(QFont("Arial", 12, QFont.Bold))  # Set font size and make it bold
        self.label_InnerLeaf.setFrameShape(QtWidgets.QFrame.Box)
        self.label_InnerLeaf.setTextFormat(QtCore.Qt.PlainText)
        self.label_InnerLeaf.setAlignment(QtCore.Qt.AlignCenter)
        self.label_InnerLeaf.setIndent(-1)
        self.label_InnerLeaf.setObjectName("Label_InnerLeaf")
        self.tabLayout_1.addWidget(self.label_InnerLeaf, self.line_count+50, 0, 1, 100)
        
        #large outer leaf label
        self.label_OuterLeaf = QtWidgets.QLabel(self.tab_1)
        self.label_OuterLeaf.setFont(QFont("Arial", 12, QFont.Bold))  # Set font size and make it bold
        self.label_OuterLeaf.setFrameShape(QtWidgets.QFrame.Box)
        self.label_OuterLeaf.setTextFormat(QtCore.Qt.PlainText)
        self.label_OuterLeaf.setAlignment(QtCore.Qt.AlignCenter)
        self.label_OuterLeaf.setIndent(-1)
        self.label_OuterLeaf.setObjectName("Label_OuterLeaf")
        self.tabLayout_1.addWidget(self.label_OuterLeaf, self.line_count+100, 0, 1, 100)

        #large mould label
        self.label_mould = QtWidgets.QLabel(self.tab_1)
        self.label_mould.setFont(QFont("Arial", 12, QFont.Bold))
        self.label_mould.setFrameShape(QtWidgets.QFrame.Box)
        self.label_mould.setTextFormat(QtCore.Qt.PlainText)
        self.label_mould.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mould.setIndent(-1)
        self.label_mould.setObjectName("Label_mould")
        self.tabLayout_1.addWidget(self.label_mould, self.line_count+250, 0, 1, 100)

        

        # combobox material/product
        self.comboBox_matpro_ins = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_matpro_ins.setObjectName("comboBox_matpro_ins")
        self.comboBox_matpro_ins.addItem("")
        self.comboBox_matpro_ins.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_matpro_ins, 1, 0, 1, 10)
        
        self.comboBox_matpro_inner = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_matpro_inner.setObjectName("comboBox_matpro_inner")
        self.comboBox_matpro_inner.addItem("")
        self.comboBox_matpro_inner.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_matpro_inner, 52, 0, 1, 10)

        self.comboBox_matpro_outer = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_matpro_outer.setObjectName("comboBox_matpro_outer")
        self.comboBox_matpro_outer.addItem("")
        self.comboBox_matpro_outer.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_matpro_outer, 102, 0, 1, 10)

        self.comboBox_matpro_mould = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_matpro_mould.setObjectName("comboBox_matpro_mould")
        self.comboBox_matpro_mould.addItem("")
        self.comboBox_matpro_mould.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_matpro_mould, 252, 0, 1, 10)

        #Material/product line edit box
        self.lineEdit_matpro_ins = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_matpro_ins.setObjectName("lineEdit_matpro_ins")
        self.tabLayout_1.addWidget(self.lineEdit_matpro_ins, 1, 10, 1, 40)

        self.lineEdit_matpro_inner = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_matpro_inner.setObjectName("lineEdit_matpro_inner")
        self.tabLayout_1.addWidget(self.lineEdit_matpro_inner, 52, 10, 1, 40)

        self.lineEdit_matpro_outer = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_matpro_outer.setObjectName("lineEdit_matpro_outer")
        self.tabLayout_1.addWidget(self.lineEdit_matpro_outer, 102, 10, 1, 40)

        self.lineEdit_matpro_mould = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_matpro_mould.setObjectName("lineEdit_matpro_mould")
        self.tabLayout_1.addWidget(self.lineEdit_matpro_mould, 252, 10, 1, 40)
        
        #search button
        self.pushButton_search_matpro_ins = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_search_matpro_ins.setObjectName("pushButton_search_matpro_ins")
        self.tabLayout_1.addWidget(self.pushButton_search_matpro_ins, 1, 50, 1, 10)
        
        self.pushButton_search_matpro_inner = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_search_matpro_inner.setObjectName("pushButton_search_matpro_inner")
        self.tabLayout_1.addWidget(self.pushButton_search_matpro_inner, 52, 50, 1, 10)

        self.pushButton_search_matpro_outer = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_search_matpro_outer.setObjectName("pushButton_search_matpro_outer")
        self.tabLayout_1.addWidget(self.pushButton_search_matpro_outer, 102, 50, 1, 10)

        self.pushButton_search_matpro_mould = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_search_matpro_mould.setObjectName("pushButton_search_matpro_mould")
        self.tabLayout_1.addWidget(self.pushButton_search_matpro_mould, 252, 50, 1, 10)

        #Label: Quantity
        self.label_quantity_ins = QtWidgets.QLabel(self.tab_1)
        self.label_quantity_ins.setObjectName("label_quantity_ins")
        self.tabLayout_1.addWidget(self.label_quantity_ins, 1, 60, 1, 10)

        self.label_quantity_inner = QtWidgets.QLabel(self.tab_1)
        self.label_quantity_inner.setObjectName("label_quantity_inner")
        self.tabLayout_1.addWidget(self.label_quantity_inner, 52, 60, 1, 10)

        self.label_quantity_outer = QtWidgets.QLabel(self.tab_1)
        self.label_quantity_outer.setObjectName("label_quantity_outer")
        self.tabLayout_1.addWidget(self.label_quantity_outer, 102, 60, 1, 10)

        self.label_quantity_mould = QtWidgets.QLabel(self.tab_1)
        self.label_quantity_mould.setObjectName("label_quantity_mould")
        self.tabLayout_1.addWidget(self.label_quantity_mould, 252, 60, 1, 10)
       
        #Quanitity line edit box
        self.lineEdit_quantity_ins = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_quantity_ins.setObjectName("lineEdit_quantity_ins")
        self.tabLayout_1.addWidget(self.lineEdit_quantity_ins, 1, 70, 1, 10)
        
        self.lineEdit_quantity_inner = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_quantity_inner.setObjectName("lineEdit_quantity_inner")
        self.tabLayout_1.addWidget(self.lineEdit_quantity_inner, 52, 70, 1, 10)

        self.lineEdit_quantity_outer = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_quantity_outer.setObjectName("lineEdit_quantity_outer")
        self.tabLayout_1.addWidget(self.lineEdit_quantity_outer, 102, 70, 1, 10)

        self.lineEdit_quantity_mould = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_quantity_mould.setObjectName("lineEdit_quantity_mould")
        self.tabLayout_1.addWidget(self.lineEdit_quantity_mould, 252, 70, 1, 10)

        #Label: Unit
        self.label_unit_ins = QtWidgets.QLabel(self.tab_1)
        self.label_unit_ins.setObjectName("label_unit_ins")
        self.tabLayout_1.addWidget(self.label_unit_ins, 1, 80, 1, 5)

        self.label_unit_inner = QtWidgets.QLabel(self.tab_1)
        self.label_unit_inner.setObjectName("label_unit_inner")
        self.tabLayout_1.addWidget(self.label_unit_inner, 52, 80, 1, 5)

        self.label_unit_outer = QtWidgets.QLabel(self.tab_1)
        self.label_unit_outer.setObjectName("label_unit_outer")
        self.tabLayout_1.addWidget(self.label_unit_outer, 102, 80, 1, 5)
        
        self.label_unit_mould = QtWidgets.QLabel(self.tab_1)
        self.label_unit_mould.setObjectName("label_unit_mould")
        self.tabLayout_1.addWidget(self.label_unit_mould, 252, 80, 1, 5)

        #combobox for unit
        self.comboBox_unit_ins = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_unit_ins.setObjectName("comboBox_unit_ins")
        self.comboBox_unit_ins.addItem("")
        self.comboBox_unit_ins.addItem("")
        self.comboBox_unit_ins.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_unit_ins, 1, 85, 1, 5)

        self.comboBox_unit_inner = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_unit_inner.setObjectName("comboBox_unit_inner")
        self.comboBox_unit_inner.addItem("")
        self.comboBox_unit_inner.addItem("")
        self.comboBox_unit_inner.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_unit_inner, 52, 85, 1, 5)

        self.comboBox_unit_outer = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_unit_outer.setObjectName("comboBox_unit_outer")
        self.comboBox_unit_outer.addItem("")
        self.comboBox_unit_outer.addItem("")
        self.comboBox_unit_outer.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_unit_outer, 102, 85, 1, 5)

        self.comboBox_unit_mould = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_unit_mould.setObjectName("comboBox_unit_mould")
        self.comboBox_unit_mould.addItem("")
        self.comboBox_unit_mould.addItem("")
        self.comboBox_unit_mould.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_unit_mould, 252, 85, 1, 5)

      
        # + button to add line
        self.pushButton_add_line_ins = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_add_line_ins.setObjectName("pushButton_add_line_ins")
        self.tabLayout_1.addWidget(self.pushButton_add_line_ins, 1, 90, 1, 5)

        self.pushButton_add_line_inner = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_add_line_inner.setObjectName("pushButton_add_line_inner")
        self.tabLayout_1.addWidget(self.pushButton_add_line_inner, 52, 90, 1, 5)

        self.pushButton_add_line_outer = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_add_line_outer.setObjectName("pushButton_add_line_outer")
        self.tabLayout_1.addWidget(self.pushButton_add_line_outer, 102, 90, 1, 5)

        self.pushButton_add_line_mould = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_add_line_mould.setObjectName("pushButton_add_line_mould")
        self.tabLayout_1.addWidget(self.pushButton_add_line_mould, 252, 90, 1, 5)
        
        # - button to delete line
        self.pushButton_delete_line_ins = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_delete_line_ins.setObjectName("pushButton_delete_line_ins")
        self.tabLayout_1.addWidget(self.pushButton_delete_line_ins, 1, 95, 1, 5)

        self.pushButton_delete_line_inner = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_delete_line_inner.setObjectName("pushButton_delete_line_inner")
        self.tabLayout_1.addWidget(self.pushButton_delete_line_inner, 52, 95, 1, 5)

        self.pushButton_delete_line_outer = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_delete_line_outer.setObjectName("pushButton_delete_line_outer")
        self.tabLayout_1.addWidget(self.pushButton_delete_line_outer, 102, 95, 1, 5)
        
        self.pushButton_delete_line_mould = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_delete_line_mould.setObjectName("pushButton_delete_line_mould")
        self.tabLayout_1.addWidget(self.pushButton_delete_line_mould, 252, 95, 1, 5)

        #save EPD button
        self.pushButton_get_EPD = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_get_EPD.setObjectName("pushButton_get_EPD")
        self.tabLayout_1.addWidget(self.pushButton_get_EPD, self.line_count_mould + 100, 0, 1, 100)

        #tab 2
        self.tab_2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_2, "A2")
        self.tabLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.tabLayout_2.setAlignment(QtCore.Qt.AlignTop)
       
        self.pushButton_import_A1_button = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_import_A1_button.setObjectName('Import button A2')
        self.tabLayout_2.addWidget(self.pushButton_import_A1_button, 1, 0, 1, 2)  # Adjust column span as needed

        self.pushButton_calculate_A2_button = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_calculate_A2_button.setObjectName("Calculate A2")
        self.tabLayout_2.addWidget(self.pushButton_calculate_A2_button, 10000, 0, 1, 2)

        #tab 3
        self.tab_3 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_3, "A3")
        self.tabLayout_3 = QtWidgets.QGridLayout(self.tab_3)
        self.tabLayout_3.setAlignment(QtCore.Qt.AlignBottom)
        self.tabLayout_3.setSpacing(0)
        num_rows = 31
        num_columns = 31
        
        for i in range(num_columns):
            self.tabLayout_3.setColumnStretch(i, 1)
        for i in range(num_rows):
            self.tabLayout_3.setRowStretch(i, 1)
        
        self.pushButton_GenerateUI_A3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_GenerateUI_A3.setObjectName("Generate UI A3")
        self.tabLayout_3.addWidget(self.pushButton_GenerateUI_A3, 0, 0, 1, 4)

        
        
        #tab4
        self.tab_4 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_4, "A4")
        self.tabLayout_4 = QtWidgets.QGridLayout(self.tab_4)
        self.tabLayout_4.setAlignment(QtCore.Qt.AlignTop)

        self.pushButton_importWeight_A2 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_importWeight_A2.setObjectName("Import Weight A2")
        self.tabLayout_4.addWidget(self.pushButton_importWeight_A2, 0, 0, 1, 10)
        
        self.sandwichname = "Sandwich Element Transportation to Site"
        self.label_A4 = QLabel(self.sandwichname, self.tab_4)
        font = self.label_A4.font()
        font.setPointSize(10)  # Set the font size to 12
        font.setBold(True)    # Set the font to bold
        self.label_A4.setFont(font)
        self.label_A4.setAlignment(QtCore.Qt.AlignCenter)
        self.tabLayout_4.addWidget(self.label_A4, 1, 0, 1, 10)
        self.tabLayout_4.addWidget(QtWidgets.QWidget(), 2, 0, 1, 10)

        # Label "Quantity:"
        self.label_weight = QLabel("Quantity:", self.tab_4)
        self.tabLayout_4.addWidget(self.label_weight, 2, 0, 1, 1)  # Span 1 column       

        # LineEdit box
        self.line_edit_weight_A4 = QLineEdit(self.tab_4)
        self.tabLayout_4.addWidget(self.line_edit_weight_A4, 2, 1, 1, 1)  # Span 1 column

        # Label "Transport mode:"
        self.label_transport_mode_A4 = QLabel("Transport mode:", self.tab_4)
        self.tabLayout_4.addWidget(self.label_transport_mode_A4, 2, 3, 1, 1)  # Span 1 column

        # ComboBox with options: "Truck", "Ferry"
        self.combo_transport_mode_A4 = QtWidgets.QComboBox(self.tab_4)
        self.combo_transport_mode_A4.addItems(["Truck-fully laden", "Truck-average laden", "Sea transport"])
        self.tabLayout_4.addWidget(self.combo_transport_mode_A4, 2, 4, 1, 1)  # Span 1 column

        # Label "Distance:"
        self.label_distance_A4 = QLabel("Distance:", self.tab_4)
        self.tabLayout_4.addWidget(self.label_distance_A4, 2, 5, 1, 1)  # Span 1 column

        # LineEdit box (empty for now)
        self.line_edit_distance_A4 = QLineEdit(self.tab_4)
        self.tabLayout_4.addWidget(self.line_edit_distance_A4, 2, 6, 1, 1)  # Span 1 column

        # Label "kg"
        self.label_kg_A4 = QLabel("kg", self.tab_4)
        self.tabLayout_4.addWidget(self.label_kg_A4, 2, 2, 1, 1)  # Span 1 column

        #label km
        self.label_km_A4 = QLabel("km", self.tab_4)
        self.tabLayout_4.addWidget(self.label_km_A4, 2, 7, 1, 1)  # Span 1 column

        self.pushButton_button_add_A4 = QPushButton("+", self.tab_4)
        self.pushButton_button_add_A4.clicked.connect(lambda _, r=2: self.duplicate_row_A4(r))
        self.tabLayout_4.addWidget(self.pushButton_button_add_A4, 2, 8, 1, 1)  # Span 1 column
        
        self.pushButton_button_remove_A4 = QPushButton("-", self.tab_4)
        self.pushButton_button_remove_A4.clicked.connect(lambda _, r=2: self.remove_row(r))
        self.tabLayout_4.addWidget(self.pushButton_button_remove_A4, 2, 9, 1, 1)  # Span 1 column

        self.pushButton_calculate_A4 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_calculate_A4.setObjectName("Calculate A4")
        self.tabLayout_4.addWidget(self.pushButton_calculate_A4, 20, 0, 1, 10)
        
        self.pushButton_calculate_All = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_calculate_All.setObjectName("Calculate All")
        self.tabLayout_4.addWidget(self.pushButton_calculate_All, 25, 0, 1, 10)
        

        


        #Items of the file menu
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.actionImport_ifc_file = QtWidgets.QAction(MainWindow)
        self.actionImport_ifc_file.setCheckable(False)
        self.actionImport_ifc_file.setObjectName("actionImport_ifc_file")
        self.menuFile.addAction(self.actionImport_ifc_file)
        self.menuFile.addSeparator()
        
        self.actionImport_manual_import = QtWidgets.QAction(MainWindow)
        self.actionImport_manual_import.setCheckable(False)
        self.actionImport_manual_import.setObjectName("actionManual_import")   
        self.menuFile.addAction(self.actionImport_manual_import)
        self.menuFile.addSeparator()

        self.actionMould_reuse = QtWidgets.QAction(MainWindow)
        self.actionMould_reuse.setCheckable(False)
        self.actionMould_reuse.setObjectName("actionMould_reuse")   
        self.menuFile.addAction(self.actionMould_reuse)
        self.menuFile.addSeparator()

        self.transport_factors_A2 = QtWidgets.QAction(MainWindow)
        self.transport_factors_A2.setCheckable(False)
        self.transport_factors_A2.setObjectName("transport_factors")
        self.menuFile.addAction(self.transport_factors_A2)
        self.menuFile.addSeparator()
        
        self.actionProcessEmFactors = QtWidgets.QAction(MainWindow)
        self.actionProcessEmFactors.setCheckable(False)
        self.actionProcessEmFactors.setObjectName("process emissions factors")
        self.menuFile.addAction(self.actionProcessEmFactors)
        self.menuFile.addSeparator()

        self.action_settings_A3 = QtWidgets.QAction(MainWindow)
        self.action_settings_A3.setCheckable(False)
        self.action_settings_A3.setObjectName("A3 settings")
        self.menuFile.addAction(self.action_settings_A3)
        self.menuFile.addSeparator()

        

        self.actionEco_settings = QtWidgets.QAction(MainWindow)
        self.actionEco_settings.setCheckable(False)
        self.actionEco_settings.setObjectName("actionEco_settings")
        self.menuFile.addAction(self.actionEco_settings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addSeparator()

        self.actionSurface_setting = QtWidgets.QAction(MainWindow)
        self.actionSurface_setting.setCheckable(False)
        self.actionSurface_setting.setObjectName("surface definer")
        self.menuFile.addAction(self.actionSurface_setting)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addSeparator()

        


        self.retranslateUi(MainWindow)
        return MainWindow

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        ###TAB_1####:
        
        #Insulation items:
        self.label_Insulation.setText(_translate("MainWindow", "Insulation"))
        self.comboBox_matpro_ins.setItemText(0, _translate("MainWindow", "Material:"))
        self.comboBox_matpro_ins.setItemText(1, _translate("MainWindow", "Product:"))
        self.pushButton_search_matpro_ins.setText(_translate("MainWindow", "Search"))
        self.label_quantity_ins.setText(_translate("MainWindow", "Quantity:"))
        self.comboBox_unit_ins.setItemText(0, _translate("MainWindow", "m3"))
        self.comboBox_unit_ins.setItemText(1, _translate("MainWindow", "kg"))
        self.comboBox_unit_ins.setItemText(2, _translate("MainWindow", "m2"))
        self.label_unit_ins.setText(_translate("MainWindow", "Unit:"))
        self.pushButton_add_line_ins.setText(_translate("MainWindow", "+"))
        self.pushButton_delete_line_ins.setText(_translate("MainWindow", "-"))
        
        #inner leaf items:
        self.label_InnerLeaf.setText(_translate("MainWindow", "Inner leaf"))
        self.comboBox_matpro_inner.setItemText(0, _translate("MainWindow","Material:"))
        self.comboBox_matpro_inner.setItemText(1, _translate("MainWindow", "Product:"))
        self.pushButton_search_matpro_inner.setText(_translate("MainWindow", "Search"))
        self.label_quantity_inner.setText(_translate("MainWindow", "Quantity:"))
        self.comboBox_unit_inner.setItemText(0, _translate("MainWindow", "m3"))
        self.comboBox_unit_inner.setItemText(1, _translate("MainWindow", "kg"))
        self.comboBox_unit_inner.setItemText(2, _translate("MainWindow", "m2"))
        self.label_unit_inner.setText(_translate("MainWindow", "Unit:"))
        self.pushButton_add_line_inner.setText(_translate("MainWindow", "+"))
        self.pushButton_delete_line_inner.setText(_translate("MainWindow", "-"))

        #Outer leaf items:
        self.label_OuterLeaf.setText(_translate("MainWindow", "Outer leaf"))
        self.comboBox_matpro_outer.setItemText(0, _translate("MainWindow","Material:"))
        self.comboBox_matpro_outer.setItemText(1, _translate("MainWindow", "Product:"))
        self.pushButton_search_matpro_outer.setText(_translate("MainWindow", "Search"))
        self.label_quantity_outer.setText(_translate("MainWindow", "Quantity:"))
        self.comboBox_unit_outer.setItemText(0, _translate("MainWindow", "m3"))
        self.comboBox_unit_outer.setItemText(1, _translate("MainWindow", "kg"))
        self.comboBox_unit_outer.setItemText(2, _translate("MainWindow", "m2"))
        self.label_unit_outer.setText(_translate("MainWindow", "Unit:"))
        self.pushButton_add_line_outer.setText(_translate("MainWindow", "+"))
        self.pushButton_delete_line_outer.setText(_translate("MainWindow", "-"))
        self.pushButton_get_EPD.setText(_translate("MainWindow", "Calculate A1"))
        
        #Mould items:
        self.label_mould.setText(_translate("MainWindow", "Mold"))
        self.comboBox_matpro_mould.setItemText(0, _translate("MainWindow","Material:"))
        self.comboBox_matpro_mould.setItemText(1, _translate("MainWindow", "Product:"))
        self.pushButton_search_matpro_mould.setText(_translate("MainWindow", "Search"))
        self.label_quantity_mould.setText(_translate("MainWindow", "Quantity:"))
        self.comboBox_unit_mould.setItemText(0, _translate("MainWindow", "m3"))
        self.comboBox_unit_mould.setItemText(1, _translate("MainWindow", "kg"))
        self.comboBox_unit_mould.setItemText(2, _translate("MainWindow", "m2"))
        self.label_unit_mould.setText(_translate("MainWindow", "Unit:"))
        self.pushButton_add_line_mould.setText(_translate("MainWindow", "+"))
        self.pushButton_delete_line_mould.setText(_translate("MainWindow", "-"))

        ###TAB_2###:
        self.pushButton_import_A1_button.setText(_translate("MainWindow", "(re)Generate UI based on A1 data"))
        self.pushButton_calculate_A2_button.setText(_translate("MainWindow", "Calculate A2"))

        #items of the file menu
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionImport_ifc_file.setText(_translate("MainWindow", "A1: Import .ifc-file"))
        self.actionImport_manual_import.setText(_translate("MainWindow", "A1: Import manual data"))
        self.actionMould_reuse.setText(_translate("MainWindow", "A1: Mold reuse factor"))
        self.transport_factors_A2.setText(_translate("MainWindow", "A2: Transport emission factors"))
        self.actionProcessEmFactors.setText(_translate("MainWindow", "A3: Process emission factors"))
        self.action_settings_A3.setText(_translate("MainWindow", "A3: Capacity settings"))
        
        self.actionEco_settings.setText(_translate("MainWindow", "EcoPlatform settings"))
        self.actionSurface_setting.setText(_translate("MainWindow", "Set sandwich element surface"))

        ###TAB_3###
        self.pushButton_GenerateUI_A3.setText(_translate("MainWindow", "(re)Generate UI"))
  
        ###TAB_4###
        self.pushButton_importWeight_A2.setText(_translate("MainWindow", "Import total sandwich element weight"))
        self.label_A4.setText(_translate("MainWindow", "Sandwich Element Transportation to Site"))
        self.pushButton_calculate_A4.setText(_translate("MainWindow", "Calculate A4"))
        self.pushButton_calculate_All.setText(_translate("MainWindow", "Calculate All"))

    def add_line_insulation(self, MainWindow):
        # Create a new combobox
        self.comboBox_matpro_ins = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_matpro_ins.setObjectName("comboBox_matpro_ins")
        self.comboBox_matpro_ins.addItem("")
        self.comboBox_matpro_ins.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_matpro_ins, 1+self.line_count, 0, 1, 10)
        #Material/product line edit box
        self.lineEdit_matpro_ins = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_matpro_ins.setObjectName("lineEdit_matpro_ins")
        self.tabLayout_1.addWidget(self.lineEdit_matpro_ins, 1+self.line_count, 10, 1, 40)
        #search button
        self.pushButton_search_matpro_ins = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_search_matpro_ins.setObjectName("pushButton_search_matpro_ins")
        self.tabLayout_1.addWidget(self.pushButton_search_matpro_ins, 1+self.line_count, 50, 1, 10)
        #Label: Quantity
        self.label_quantity_ins = QtWidgets.QLabel(self.tab_1)
        self.label_quantity_ins.setObjectName("label_quantity_ins")
        self.tabLayout_1.addWidget(self.label_quantity_ins, 1+self.line_count, 60, 1, 10)
        #Quanitity line edit box
        self.lineEdit_quantity_ins = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_quantity_ins.setObjectName("lineEdit_quantity_ins")
        self.tabLayout_1.addWidget(self.lineEdit_quantity_ins, 1+self.line_count, 70, 1, 10)
        #Label: Unit
        self.label_unit_ins = QtWidgets.QLabel(self.tab_1)
        self.label_unit_ins.setObjectName("label_unit_ins")
        self.tabLayout_1.addWidget(self.label_unit_ins, 1+self.line_count, 80, 1, 5)
        #combobox for unit
        self.comboBox_unit_ins = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_unit_ins.setObjectName("comboBox_unit_ins")
        self.comboBox_unit_ins.addItem("")
        self.comboBox_unit_ins.addItem("")
        self.comboBox_unit_ins.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_unit_ins, 1+self.line_count, 85, 1, 5)
        
        #define button_key f
        button_key = f'SearchButton-{hex(id(self.pushButton_search_matpro_ins))}'
       
        #dictionariy for epd search:
        self.line_search_dict['insulation'] = (self.lineEdit_matpro_ins, self.pushButton_search_matpro_ins)

        #the dictionairy for EPD data extraction:
        key = 'insulation'
        if key in self.line_data_dict:
        # Check if the existing value is a list
            if isinstance(self.line_data_dict[key], list):
                # Update existing entry
                self.line_data_dict[key].append((self.lineEdit_matpro_ins, self.pushButton_search_matpro_ins))
            else:
                # Convert existing tuple to a list and append the new tuple
                self.line_data_dict[key] = list(self.line_data_dict[key]) + [(self.lineEdit_matpro_ins, self.pushButton_search_matpro_ins)]
        else:
        # Create a new entry
            self.line_data_dict[key] = [(self.lineEdit_matpro_ins, self.pushButton_search_matpro_ins)]
        
        #connecting the button to the search button clicked function
        self.pushButton_search_matpro_ins.clicked.connect(lambda _, button_name=hex(id(self.pushButton_search_matpro_ins)): self.search_button_clicked('insulation', button_name))
        
        #adding to self.line_data_dict_2 for matching search buttons and line boxes
        if key in self.line_data_dict_2:
            self.line_data_dict_2[key][button_key] = (f'LineEditCode: {hex(id(self.lineEdit_matpro_ins))}', self.lineEdit_matpro_ins)
        else:
            # Create a new entry
            self.line_data_dict_2[key] = {button_key: (f'LineEditCode: {hex(id(self.lineEdit_matpro_ins))}')}
        
        #the dictionairy for quantity extraction:
        if key in self.quantity_unit_dict:
            if isinstance(self.quantity_unit_dict[key], list):
                self.quantity_unit_dict[key].append((self.lineEdit_quantity_ins, self.comboBox_unit_ins))
            else:
                self.quantity_unit_dict[key] = list(self.quantity_unit_dict[key]) + [(self.lineEdit_quantity_ins, self.comboBox_unit_ins)]
        else:
            self.quantity_unit_dict[key] = [(self.lineEdit_quantity_ins, self.comboBox_unit_ins)]
        
        # Increment the line count for the next line
        self.line_count += 1
        
        #Refresh the layout
        self.tab_1.setLayout(self.tabLayout_1)
        self.retranslateUi(MainWindow)

    def add_line_inner(self):
        # Create a new combobox
        self.comboBox_matpro_inner = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_matpro_inner.setObjectName("comboBox_matpro_inner")
        self.comboBox_matpro_inner.addItem("")
        self.comboBox_matpro_inner.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_matpro_inner, (self.line_count+(self.line_count_inner+1)), 0, 1, 10)
        #Material/product line edit box
        self.lineEdit_matpro_inner = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_matpro_inner.setObjectName("lineEdit_matpro_inner")
        self.tabLayout_1.addWidget(self.lineEdit_matpro_inner, (self.line_count+(self.line_count_inner+1)), 10, 1, 40)
        #search button
        self.pushButton_search_matpro_inner = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_search_matpro_inner.setObjectName("pushButton_search_matpro_inner")
        self.tabLayout_1.addWidget(self.pushButton_search_matpro_inner, (self.line_count+(self.line_count_inner+1)), 50, 1, 10)
        #Label: Quantity
        self.label_quantity_inner = QtWidgets.QLabel(self.tab_1)
        self.label_quantity_inner.setObjectName("label_quantity_inner")
        self.tabLayout_1.addWidget(self.label_quantity_inner, (self.line_count+(self.line_count_inner+1)), 60, 1, 10)
        #Quanitity line edit box
        self.lineEdit_quantity_inner = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_quantity_inner.setObjectName("lineEdit_quantity_inner")
        self.tabLayout_1.addWidget(self.lineEdit_quantity_inner, (self.line_count+(self.line_count_inner+1)), 70, 1, 10)
        #Label: Unit
        self.label_unit_inner = QtWidgets.QLabel(self.tab_1)
        self.label_unit_inner.setObjectName("label_unit_inner")
        self.tabLayout_1.addWidget(self.label_unit_inner, (self.line_count+(self.line_count_inner+1)), 80, 1, 5)
        #combobox for unit
        self.comboBox_unit_inner = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_unit_inner.setObjectName("comboBox_unit_inner")
        self.comboBox_unit_inner.addItem("")
        self.comboBox_unit_inner.addItem("")
        self.comboBox_unit_inner.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_unit_inner, (self.line_count+(self.line_count_inner+1)), 85, 1, 5)
        
        #define button key
        button_key = f'SearchButton-{hex(id(self.pushButton_search_matpro_inner))}'
        
        #dictionairy for epd search:
        self.line_search_dict['inner'] = (self.lineEdit_matpro_inner, self.pushButton_search_matpro_inner)
        
        #the dictionairy for EPD data extraction:
        key = 'inner'
        if key in self.line_data_dict:
        # Check if the existing value is a list
            if isinstance(self.line_data_dict[key], list):
                # Update existing entry
                self.line_data_dict[key].append((self.lineEdit_matpro_inner, self.pushButton_search_matpro_inner))
            else:
                # Convert existing tuple to a list and append the new tuple
                self.line_data_dict[key] = list(self.line_data_dict[key]) + [(self.lineEdit_matpro_inner, self.pushButton_search_matpro_inner)]
        else:
        # Create a new entry
            self.line_data_dict[key] = [(self.lineEdit_matpro_inner, self.pushButton_search_matpro_inner)]
        
        #connect the button the the search button clicked function
        self.pushButton_search_matpro_inner.clicked.connect(lambda _, button_name=hex(id(self.pushButton_search_matpro_inner)): self.search_button_clicked('inner', button_name))
        
        #adding to self.line_data_dict_2 for matching search buttons and line boxes
        if key in self.line_data_dict_2:
            self.line_data_dict_2[key][button_key] = (f'LineEditCode: {hex(id(self.lineEdit_matpro_inner))}', self.lineEdit_matpro_inner)
        else:
            # Create a new entry
            self.line_data_dict_2[key] = {button_key: (f'LineEditCode: {hex(id(self.lineEdit_matpro_inner))}')}

        #the dictionairy for quantity extraction:
        if key in self.quantity_unit_dict:
            if isinstance(self.quantity_unit_dict[key], list):
                self.quantity_unit_dict[key].append((self.lineEdit_quantity_inner, self.comboBox_unit_inner))  
            else:
                self.quantity_unit_dict[key] = list(self.quantity_unit_dict[key]) + [(self.lineEdit_quantity_inner, self.comboBox_unit_inner)]
        else:
            self.quantity_unit_dict[key] = [(self.lineEdit_quantity_inner, self.comboBox_unit_inner)]
        
        # Increment the line count for the next line
        self.line_count_inner += 1
        # Refresh the layout
        self.tab_1.setLayout(self.tabLayout_1)
        self.retranslateUi(MainWindow)

    def add_line_outer(self):
        # Create a new combobox
        self.comboBox_matpro_outer = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_matpro_outer.setObjectName("comboBox_matpro_outer")
        self.comboBox_matpro_outer.addItem("")
        self.comboBox_matpro_outer.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_matpro_outer, (self.line_count_inner+(self.line_count_outer+1)), 0, 1, 10)
        #Material/product line edit box
        self.lineEdit_matpro_outer = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_matpro_outer.setObjectName("lineEdit_matpro_outer")
        self.tabLayout_1.addWidget(self.lineEdit_matpro_outer, (self.line_count_inner+(self.line_count_outer+1)), 10, 1, 40)
        #search button
        self.pushButton_search_matpro_outer = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_search_matpro_outer.setObjectName("pushButton_search_matpro_outer")
        self.tabLayout_1.addWidget(self.pushButton_search_matpro_outer, (self.line_count_inner+(self.line_count_outer+1)), 50, 1, 10)
        
        #Label: Quantity
        self.label_quantity_outer = QtWidgets.QLabel(self.tab_1)
        self.label_quantity_outer.setObjectName("label_quantity_outer")
        self.tabLayout_1.addWidget(self.label_quantity_outer, (self.line_count_inner+(self.line_count_outer+1)), 60, 1, 10)
        #Quanitity line edit box
        self.lineEdit_quantity_outer = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_quantity_outer.setObjectName("lineEdit_quantity_outer")
        self.tabLayout_1.addWidget(self.lineEdit_quantity_outer, (self.line_count_inner+(self.line_count_outer+1)), 70, 1, 10)
        #Label: Unit
        self.label_unit_outer = QtWidgets.QLabel(self.tab_1)
        self.label_unit_outer.setObjectName("label_unit_outer")
        self.tabLayout_1.addWidget(self.label_unit_outer, (self.line_count_inner+(self.line_count_outer+1)), 80, 1, 5)
        #combobox for unit
        self.comboBox_unit_outer = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_unit_outer.setObjectName("comboBox_unit_outer")
        self.comboBox_unit_outer.addItem("")
        self.comboBox_unit_outer.addItem("")
        self.comboBox_unit_outer.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_unit_outer, (self.line_count_inner+(self.line_count_outer+1)), 85, 1, 5)
        
        #define button key
        button_key = f'SearchButton-{hex(id(self.pushButton_search_matpro_outer))}'
        
        #the dictionairy epd search
        self.line_search_dict['outer'] = (self.lineEdit_matpro_outer, self.pushButton_search_matpro_outer)
        
        #the dictionairy for EPD data extraction:
        key = 'outer'
        if key in self.line_data_dict:
        # Check if the existing value is a list
            if isinstance(self.line_data_dict[key], list):
                # Update existing entry
                self.line_data_dict[key].append((self.lineEdit_matpro_outer, self.pushButton_search_matpro_outer))
            else:
                # Convert existing tuple to a list and append the new tuple
                self.line_data_dict[key] = list(self.line_data_dict[key]) + [(self.lineEdit_matpro_outer, self.pushButton_search_matpro_outer)]
        else:
        # Create a new entry
            self.line_data_dict[key] = [(self.lineEdit_matpro_outer, self.pushButton_search_matpro_outer)]
        
        self.pushButton_search_matpro_outer.clicked.connect(lambda _, button_name=hex(id(self.pushButton_search_matpro_outer)): self.search_button_clicked('outer', button_name))
    
       #adding to self.line_data_dict_2 for matching search buttons and line boxes
        if key in self.line_data_dict_2:
            self.line_data_dict_2[key][button_key] = (f'LineEditCode: {hex(id(self.lineEdit_matpro_outer))}', self.lineEdit_matpro_outer)
        else:
            # Create a new entry
            self.line_data_dict_2[key] = {button_key: (f'LineEditCode: {hex(id(self.lineEdit_matpro_outer))}')}
        
        #the dictionairy for quantity extraction:
        if key in self.quantity_unit_dict:
            if isinstance(self.quantity_unit_dict[key], list):
                self.quantity_unit_dict[key].append((self.lineEdit_quantity_outer, self.comboBox_unit_outer))
            else:               
                self.quantity_unit_dict[key] = list(self.quantity_unit_dict[key]) + [(self.lineEdit_quantity_outer, self.comboBox_unit_outer)]
        else:  
            self.quantity_unit_dict[key] = [(self.lineEdit_quantity_outer, self.comboBox_unit_outer)]
        
        # Increment the line count for the next line
        self.line_count_outer += 1
        # Refresh the layout
        self.tab_1.setLayout(self.tabLayout_1)
        self.retranslateUi(MainWindow)
    
    def add_line_mould(self):
        # Create a new combobox
        self.comboBox_matpro_mould = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_matpro_mould.setObjectName("comboBox_matpro_mould")
        self.comboBox_matpro_mould.addItem("")
        self.comboBox_matpro_mould.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_matpro_mould, (self.line_count+(self.line_count_mould+1)), 0, 1, 10)
        #Material/product line edit box
        self.lineEdit_matpro_mould = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_matpro_mould.setObjectName("lineEdit_matpro_mould")
        self.tabLayout_1.addWidget(self.lineEdit_matpro_mould, (self.line_count+(self.line_count_mould+1)), 10, 1, 40)
        #search button
        self.pushButton_search_matpro_mould = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_search_matpro_mould.setObjectName("pushButton_search_matpro_mould")
        self.tabLayout_1.addWidget(self.pushButton_search_matpro_mould, (self.line_count+(self.line_count_mould+1)), 50, 1, 10)
        #Label: Quantity
        self.label_quantity_mould = QtWidgets.QLabel(self.tab_1)
        self.label_quantity_mould.setObjectName("label_quantity_mould")
        self.tabLayout_1.addWidget(self.label_quantity_mould, (self.line_count+(self.line_count_mould+1)), 60, 1, 10)
        #Quanitity line edit box
        self.lineEdit_quantity_mould = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_quantity_mould.setObjectName("lineEdit_quantity_mould")
        self.tabLayout_1.addWidget(self.lineEdit_quantity_mould, (self.line_count+(self.line_count_mould+1)), 70, 1, 10)
        #Label: Unit
        self.label_unit_mould = QtWidgets.QLabel(self.tab_1)
        self.label_unit_mould.setObjectName("label_unit_mould")
        self.tabLayout_1.addWidget(self.label_unit_mould, (self.line_count+(self.line_count_mould+1)), 80, 1, 5)
        #combobox for unit
        self.comboBox_unit_mould = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_unit_mould.setObjectName("comboBox_unit_mould")
        self.comboBox_unit_mould.addItem("")
        self.comboBox_unit_mould.addItem("")
        self.comboBox_unit_mould.addItem("")
        self.tabLayout_1.addWidget(self.comboBox_unit_mould, (self.line_count+(self.line_count_mould+1)), 85, 1, 5)
        
        #define button key
        button_key = f'SearchButton-{hex(id(self.pushButton_search_matpro_mould))}'
        
        #dictionairy for epd search:
        self.line_search_dict['mould'] = (self.lineEdit_matpro_mould, self.pushButton_search_matpro_mould)
        
        #the dictionairy for EPD data extraction:
        key = 'mould'
        if key in self.line_data_dict:
        # Check if the existing value is a list
            if isinstance(self.line_data_dict[key], list):
                # Update existing entry
                self.line_data_dict[key].append((self.lineEdit_matpro_mould, self.pushButton_search_matpro_mould))
            else:
                # Convert existing tuple to a list and append the new tuple
                self.line_data_dict[key] = list(self.line_data_dict[key]) + [(self.lineEdit_matpro_mould, self.pushButton_search_matpro_mould)]
        else:
        # Create a new entry
            self.line_data_dict[key] = [(self.lineEdit_matpro_mould, self.pushButton_search_matpro_mould)]
        
        #connect the button the the search button clicked function
        self.pushButton_search_matpro_mould.clicked.connect(lambda _, button_name=hex(id(self.pushButton_search_matpro_mould)): self.search_button_clicked('mould', button_name))
        
        #adding to self.line_data_dict_2 for matching search buttons and line boxes
        if key in self.line_data_dict_2:
            self.line_data_dict_2[key][button_key] = (f'LineEditCode: {hex(id(self.lineEdit_matpro_mould))}', self.lineEdit_matpro_mould)
        else:
            # Create a new entry
            self.line_data_dict_2[key] = {button_key: (f'LineEditCode: {hex(id(self.lineEdit_matpro_mould))}')}

        #the dictionairy for quantity extraction:
        if key in self.quantity_unit_dict:
            if isinstance(self.quantity_unit_dict[key], list):
                self.quantity_unit_dict[key].append((self.lineEdit_quantity_mould, self.comboBox_unit_mould))  
            else:
                self.quantity_unit_dict[key] = list(self.quantity_unit_dict[key]) + [(self.lineEdit_quantity_mould, self.comboBox_unit_mould)]
        else:
            self.quantity_unit_dict[key] = [(self.lineEdit_quantity_mould, self.comboBox_unit_mould)]
        
        # Increment the line count for the next line
        self.line_count_mould += 1
        # Refresh the layout
        self.tab_1.setLayout(self.tabLayout_1)
        self.retranslateUi(MainWindow)

    def delete_line_insulation(self):
        if self.line_count > 1:
            # Remove widgets from the layout for each column in the current row
            for column in range(100):  # Assuming there are 100 columns
                item = self.tabLayout_1.itemAtPosition(self.line_count, column)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

            # Decrement the line count
            self.line_count -= 1
            # Refresh the layout
            self.tab_1.setLayout(self.tabLayout_1)
     
    def delete_line_inner(self):
        if self.line_count_inner > 51:
            # Remove widgets from the layout for each column in the current row
            for column in range(100):  # Assuming there are 100 columns
                item_inner = self.tabLayout_1.itemAtPosition(self.line_count_inner, column)
                if item_inner is not None:
                    widget = item_inner.widget()
                    if widget:
                        widget.deleteLater()

            # Decrement the line count after removing widgets
            self.line_count_inner -= 1
            
            # Refresh the layout
            self.tab_1.setLayout(self.tabLayout_1)

    def delete_line_outer(self):
        if self.line_count_outer > 101:
            # Remove widgets from the layout for each column in the current row
            for column in range(200):  # Assuming there are 100 columns
                item_outer = self.tabLayout_1.itemAtPosition(self.line_count_outer, column)
                if item_outer is not None:
                    widget = item_outer.widget()
                    if widget:
                        widget.deleteLater()

            # Decrement the line count
            self.line_count_outer -= 1
            # Refresh the layout
            self.tab_1.setLayout(self.tabLayout_1)

    #Function that duplicates the rows for tab A4
    def duplicate_row_A4(self, row):
        label_transport_mode_A4 = QLabel("Transport mode:", self.tab_4)
        self.tabLayout_4.addWidget(label_transport_mode_A4, row + self.line_counter_A4, 3, 1, 1)

        self.combo_transport_mode_A4 = QtWidgets.QComboBox(self.tab_4)
        self.combo_transport_mode_A4.addItems(["Truck-fully laden", "Truck-average laden", "Sea transport"])
        self.tabLayout_4.addWidget(self.combo_transport_mode_A4, row + self.line_counter_A4, 4, 1, 1)  # Span 1 column

        label_distance_A4 = QLabel("Distance:", self.tab_4)
        self.tabLayout_4.addWidget(label_distance_A4, row + self.line_counter_A4, 5, 1, 1)

        self.line_edit_distance_A4 = QLineEdit(self.tab_4)
        self.tabLayout_4.addWidget(self.line_edit_distance_A4, row + self.line_counter_A4, 6, 1, 1)

        label_km_A4 = QLabel("km", self.tab_4)
        self.tabLayout_4.addWidget(label_km_A4, row + self.line_counter_A4, 7, 1, 1)
        self.line_counter_A4 += 1
        key = 'Sandwich element'
        if key in self.name_transport_dict_A4:
        
            self.name_transport_dict_A4[key] = list(self.name_transport_dict_A4[key]) + [(self.combo_transport_mode_A4, self.line_edit_distance_A4)]

        else:
            print('er gaat iets verkeerd')
        
    #Function that duplicates rows for tab A2
    def duplicate_row(self, row, rows, name_list):
        # Duplicate labels and input elements
        label_transport_mode = QLabel("Transport mode:", self.tab_2)
        self.tabLayout_2.addWidget(label_transport_mode, row + self.line_counter_A2, 3, 1, 1)  # Span 1 column

        self.combo_transport_mode = QtWidgets.QComboBox(self.tab_2)
        self.combo_transport_mode.addItems(["Truck-fully laden", "Truck-average laden", "Sea transport"])
        self.tabLayout_2.addWidget(self.combo_transport_mode, row + self.line_counter_A2, 4, 1, 1)  # Span 1 column

        label_distance = QLabel("Distance:", self.tab_2)
        self.tabLayout_2.addWidget(label_distance, row + self.line_counter_A2, 5, 1, 1)  # Span 1 column

        self.line_edit_distance = QLineEdit(self.tab_2)
        self.tabLayout_2.addWidget(self.line_edit_distance, row + self.line_counter_A2, 6, 1, 1)  # Span 1 column

        label_km = QLabel("km", self.tab_2)
        self.tabLayout_2.addWidget(label_km, row + self.line_counter_A2, 7, 1, 1)  # Span 1 column
        self.line_counter_A2 += 1
        
       
        # create dictionairy for data extraction
        try:
            index = rows.index(row)
            name_to_append = name_list[index]
            if name_to_append in self.name_transport_dict_tab2:
                if isinstance(self.name_transport_dict_tab2[name_to_append], list):
                    self.name_transport_dict_tab2[name_to_append].append((self.combo_transport_mode, self.line_edit_distance ))
                else:
                    self.name_transport_dict_tab2[name_to_append] = list(self.name_transport_dict_tab2[name_to_append]) + [(self.combo_transport_mode, self.line_edit_distance)]
            else:
                self.name_transport_dict_tab2[name_to_append] = [(self.combo_transport_mode, self.line_edit_distance)]
        except ValueError:
            print(f"Value {row} not found in the list.")
        
        return self.name_transport_dict_tab2

    def remove_row(self, row):
        # Remove widgets associated with the row
        if row < 10:
            for col in range(3, 8):
                item = self.tabLayout_2.itemAtPosition(row + self.line_counter_A2, col)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()
        if row <110:
            for col in range(3, 8):
                item = self.tabLayout_2.itemAtPosition(row + (100+self.line_counter_A2), col)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()
        
        self.line_counter_A2 -= 1
 
    #Function that creates the UI for Tab A2 and transforms Tab A1 quantity data and inserts it in Tab A2
    def generate_UI_A2(self):
        self.name_weight_dict_tab2 = {}
        self.name_transport_dict_tab2 = {}
        all_names = []
        quantities = []
        units = []
        self.name_list_duplicate = []
        self.rows = []
        all_names_mould_A3_tab2 = []
        for key, data in self.line_data_dict.items():
            # Extract  the mould materials names from line_data_dict
            if key == 'mould':
                for item in data:
                    if isinstance(item, tuple):
                        line_edit, _ = item
                        name = line_edit.text().strip()
                        all_names_mould_A3_tab2.append(name)
                    elif isinstance(item, QtWidgets.QLineEdit):
                        # Handle the case where an individual QLineEdit is present
                        name = item.text().strip()
                        all_names_mould_A3_tab2.append(name)
        
        # Extract names from line_data_dict
        for section, elements in self.line_data_dict.items():
            for element in elements:
                if isinstance(element, tuple):
                    line_edit, _ = element
                    name = line_edit.text().strip()
                    all_names.append(name)

                elif isinstance(element, QtWidgets.QLineEdit):
                    # Handle the case where an individual QLineEdit is present
                    name = element.text().strip()
                    all_names.append(name)
                    
        # Extract quantities and units from quantity_unit_dict
        for section, items in self.quantity_unit_dict.items():
            for item in items:
                if isinstance(item, tuple):
                    line_edit_2, combo_box  = item
                    quantity = line_edit_2.text().strip()
                    unit = combo_box.currentText().strip()
                    if quantity:
                        quantities.append(quantity)
                        units.append(unit)
                elif isinstance(item, QtWidgets.QLineEdit):
                    quantity = item.text().strip()
                    if quantity:
                        quantities.append(quantity)
                elif isinstance(item, QtWidgets.QComboBox):
                    unit = item.currentText().strip()
                    if unit:
                        units.append(unit)

        #Create a dictionairy containing the names, quanitities, and units from tab A1
        self.name_quantity_dict = {}
        
        #Remove any empty values from the list in case a new was nut filled out in tab A1 --> avoids error for generating tab 2 UI
        #makes sure that the lenght of the names list and unit list are equal
        indices_to_remove = [i for i, item in enumerate(all_names) if item == '']
        all_names = [item for i, item in enumerate(all_names) if i not in indices_to_remove]
        units = [item for i, item in enumerate(units) if i not in indices_to_remove]
       
        for i in range(len(all_names)):
            name = all_names[i]
            quantity = float(quantities[i])
            unit = units[i]
            
            #Create the dictionairy and check if duplicate names exists. if they do, summ the quanities
            if name not in self.name_quantity_dict:
                self.name_quantity_dict[name] = {'quantity': quantity, 'unit': unit}
            else:
                existing_unit = self.name_quantity_dict[name]['unit']

                if existing_unit == unit:
                    self.name_quantity_dict[name]['quantity'] += quantity
                else:
                    print(f"Warning: Units don't match for {name}. Existing unit: {existing_unit}, New unit: {unit}")

        #Create a list of names where the quantities are expressed in m3
        self.names_with_m3 = [name for name, data in self.name_quantity_dict.items() if data['unit'] in ['m3', 'm2']]

        #open the DensityWindow with the m3 names
        Dens_window = DensitiesWindow(self.names_with_m3)
        Dens_window.exec_()
        densities_value = Dens_window.density_values
       
       #transforms m3 to kg using the entered densities.
        for name in self.names_with_m3:
            density_value = densities_value.get(name, 1.0)
            density_value = float(density_value)
            self.name_quantity_dict[name]['quantity'] *= density_value
            self.name_quantity_dict[name]['unit'] = 'kg'

        #Create the UI
        for i in reversed(range(self.tabLayout_2.count())):
            self.tabLayout_2.itemAt(i).widget().setParent(None)
        
        self.pushButton_import_A1_button = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_import_A1_button.setObjectName('Import button A2')
        self.tabLayout_2.addWidget(self.pushButton_import_A1_button, 0, 0, 1, 11)  # Adjust column span as needed
        self.pushButton_import_A1_button.clicked.connect(self.generate_UI_A2)

        line = QtWidgets.QFrame(self.tab_2)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tabLayout_2.addWidget(line, 9999, 0, 1, 11)

        self.pushButton_calculate_A2_button = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_calculate_A2_button.setObjectName("Calculate A2")
        self.tabLayout_2.addWidget(self.pushButton_calculate_A2_button, 100000, 0, 1, 11)
        self.pushButton_calculate_A2_button.clicked.connect(self.calculate_A2)
   
        row = 1
        
        #create a list of names and the list of row value for this specific number of materials --> needed for data dictionairy creation of data extraction
        self.number_of_names = len(self.name_quantity_dict)
        self.rows = list(range(row, self.number_of_names * 100 + 1, 100))
        self.name_list_duplicate = list(self.name_quantity_dict.keys())
        
        #Divide mold material quantities by the MRF
        for name, data in self.name_quantity_dict.items():
            if name in all_names_mould_A3_tab2:
                self.name_quantity_dict[name]['quantity'] /= float(self.mould_reuse_window.moldreuse_factor)
        
        for name, data in self.name_quantity_dict.items():
            quantity = data['quantity']
            unit = data['unit']
            line = QtWidgets.QFrame(self.tab_2)
            line.setFrameShape(QtWidgets.QFrame.HLine)
            line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.tabLayout_2.addWidget(line, row, 0, 1, 10)
            
            # Label with the names
            label_name = QLabel(name, self.tab_2)
            font = label_name.font()
            font.setPointSize(10)  # Set the font size to 12
            font.setBold(True)    # Set the font to bold
            label_name.setFont(font)
            label_name.setAlignment(QtCore.Qt.AlignCenter)
            self.tabLayout_2.addWidget(label_name, row+1, 0, 1, 9)
            self.tabLayout_2.addWidget(QtWidgets.QWidget(), row + 2, 0, 1, 10)
            
            # Label "Quantity:"
            label_quantity = QLabel("Quantity:", self.tab_2)
            self.tabLayout_2.addWidget(label_quantity, row+3, 0, 1, 1)  # Span 1 column
            
            # LineEdit box
            self.line_edit_quantity = QLineEdit(self.tab_2)
            self.line_edit_quantity.setText(str(quantity))
            self.tabLayout_2.addWidget(self.line_edit_quantity, row+3, 1, 1, 1)  # Span 1 column

            # Label "kg"
            label_kg = QLabel("kg", self.tab_2)
            self.tabLayout_2.addWidget(label_kg, row+3, 2, 1, 1)  # Span 1 column

            # Label "Transport mode:"
            label_transport_mode = QLabel("Transport mode:", self.tab_2)
            self.tabLayout_2.addWidget(label_transport_mode, row+3, 3, 1, 1)  # Span 1 column

            # ComboBox with options: "Truck", "Ferry"
            self.combo_transport_mode = QtWidgets.QComboBox(self.tab_2)
            self.combo_transport_mode.addItems(["Truck-fully laden", "Truck-average laden", "Sea transport"])
            self.tabLayout_2.addWidget(self.combo_transport_mode, row+3, 4, 1, 1)  # Span 1 column

            # Label "Distance:"
            label_distance = QLabel("Distance:", self.tab_2)
            self.tabLayout_2.addWidget(label_distance, row+3, 5, 1, 1)  # Span 1 column

            # LineEdit box (empty for now)
            self.line_edit_distance = QLineEdit(self.tab_2)
            self.tabLayout_2.addWidget(self.line_edit_distance, row+3, 6, 1, 1)  # Span 1 column

            # Label "km"
            label_km = QLabel("km", self.tab_2)
            self.tabLayout_2.addWidget(label_km, row+3, 7, 1, 1)  # Span 1 column

            self.pushButton_button_add_A2 = QPushButton("+", self.tab_2)
            self.pushButton_button_add_A2.clicked.connect(lambda _, r=row: self.duplicate_row(r, self.rows, self.name_list_duplicate))
            self.tabLayout_2.addWidget(self.pushButton_button_add_A2, row+3, 8, 1, 1)  # Span 1 column
            
            self.pushButton_button_remove_A2 = QPushButton("-", self.tab_2)
            self.pushButton_button_remove_A2.clicked.connect(lambda _, r=row: self.remove_row(r))
            self.tabLayout_2.addWidget(self.pushButton_button_remove_A2, row+3, 9, 1, 1)  # Span 1 column
            # Add a horizontal line after the second row 
            row += 100
            #create the dictionairy that includes the quanities line edit box
            if name not in self.name_weight_dict_tab2:
                self.name_weight_dict_tab2[name] = [(self.line_edit_quantity)]
                
            #create the dictionairy that includes the first instances of the combobox and distance line edit box --> further appended in the row duplication function
            if name in self.name_transport_dict_tab2:
                if isinstance(self.name_transport_dict_tab2[name], list):
                    self.name_transport_dict_tab2[name].append((self.combo_transport_mode, self.line_edit_distance ))
                else:
                    self.name_transport_dict_tab2[name] = list(self.name_transport_dict_tab2[name]) + [(self.combo_transport_mode, self.line_edit_distance)]
            else:
                self.name_transport_dict_tab2[name] = [(self.combo_transport_mode, self.line_edit_distance)]
            
        self.retranslateUi(MainWindow)

    #Fucntion that creates the UI for Tab A3
    def generate_UI_A3(self):
        _translate = QtCore.QCoreApplication.translate
        self.sandwich_frame_dict = {}
        self.mould_frame_dict = {}
        self.sandwich_process_mat_dict = {}
        self.sandwich_process_unit_dict = {}
        self.mould_process_mat_dict = {}
        self.mould_process_unit_dict = {}

        all_names_sandwich_A3 = []
        all_names_mould_A3 = []
        self.unique_names_sanwich = []
        self.unique_names_mould = []
        self.linecounter_sand_A3 = 2
        self.linecounter_mould_A3 = 2

        for key, data in self.line_data_dict.items():
            # Extract  the mould materials names from line_data_dict
            if key == 'mould':
                for item in data:
                    if isinstance(item, tuple):
                        line_edit, _ = item
                        name = line_edit.text().strip()
                        all_names_mould_A3.append(name)

                    elif isinstance(item, QtWidgets.QLineEdit):
                        # Handle the case where an individual QLineEdit is present
                        name = item.text().strip()
                        all_names_mould_A3.append(name)
            # Extract the sandwich materials names for mthe line_data_dict
            else:
                for item in data:
                    if isinstance(item, tuple):
                        line_edit, _ = item
                        name = line_edit.text().strip()
                        all_names_sandwich_A3.append(name)

                    elif isinstance(item, QtWidgets.QLineEdit):
                        name = item.text().strip()
                        all_names_sandwich_A3.append(name)
        #remove duplicated materials names from list    
        for item in all_names_mould_A3:
            if item not in self.unique_names_mould:
                self.unique_names_mould.append(item)
        for item in all_names_sandwich_A3:
            if item not in self.unique_names_sanwich:
                self.unique_names_sanwich.append(item)
            
        ####Create the UI#####
        for i in reversed(range(self.tabLayout_3.count())):
            self.tabLayout_3.itemAt(i).widget().setParent(None)
        
        self.pushButton_GenerateUI_A3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_GenerateUI_A3.setObjectName("Generate UI A3")
        self.tabLayout_3.addWidget(self.pushButton_GenerateUI_A3, 0, 0, 1, 4)
        self.pushButton_GenerateUI_A3.setText(_translate("MainWindow", "(re)Generate UI"))
        self.pushButton_GenerateUI_A3.clicked.connect(self.generate_UI_A3)

        self.pushButton_calculate_A3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_calculate_A3.setObjectName("calcualte a3")
        self.tabLayout_3.addWidget(self.pushButton_calculate_A3, 28, 26, 2, 4)
        self.pushButton_calculate_A3.setText(_translate("MainWindow", "Calculate A3"))
        self.pushButton_calculate_A3.clicked.connect(lambda: self.calculate_A3(A1_A3=None))

        self.pushButton_calculate_A1_A3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_calculate_A1_A3.setObjectName("calcualte A1-A3")
        self.tabLayout_3.addWidget(self.pushButton_calculate_A1_A3, 28, 1, 2, 4)
        self.pushButton_calculate_A1_A3.setText(_translate("MainWindow", "Calculate A1-A3"))
        self.pushButton_calculate_A1_A3.clicked.connect(lambda: self.calculate_A3(A1_A3='yes'))

        #Add electrictiy label with frame
        self.electricitylabel = "Electricity: "
        elecFrame = QFrame(self.tab_3)
        elecFrame.setFrameStyle(QFrame.Box)       
        self.labelElectricityA3 = QLabel(self.electricitylabel, self.tab_3)
        self.labelElectricityA3.setAlignment(QtCore.Qt.AlignCenter) 
        self.line_edit_elec = QtWidgets.QLineEdit(self.tab_3)
        self.line_edit_elec.setObjectName("Electricity quanitity")
        self.ElectricityLabelunit = QLabel("kWh", self.tab_3)
        elecFrame_layout = QGridLayout(elecFrame)
        elecFrame_layout.addWidget(self.labelElectricityA3, 0, 0, 1, 4)
        elecFrame_layout.addWidget(self.line_edit_elec, 0, 5, 1, 1)
        elecFrame_layout.addWidget(self.ElectricityLabelunit, 0, 7, 1, 1)
        self.tabLayout_3.addWidget(elecFrame, 1, 12, 1, 7)
        #add ratio division for electricity use
        self.elecratio_sandwich = QtWidgets.QSpinBox(self.tab_3)
        self.elecratio_sandwich.setRange(0, 100)
        self.elecratio_sandwich.setSuffix('%')
        self.elecratio_sandwich.setSingleStep(1)
        self.tabLayout_3.addWidget(self.elecratio_sandwich, 3, 16, 1, 1)

        self.elecratio_mould = QtWidgets.QSpinBox(self.tab_3)
        self.elecratio_mould.setRange(0, 100)
        self.elecratio_mould.setSuffix('%')
        self.elecratio_mould.setSingleStep(1)
        self.tabLayout_3.addWidget(self.elecratio_mould, 3, 26, 1, 1)

        #add sandwich production label with frame
        self.Sandwichprolabel = "Sandwich element Production"
        SandwichproFrame = QFrame(self.tab_3)
        SandwichproFrame.setFrameStyle(QFrame.Box)
        self.labelSandwichpro = QLabel(self.Sandwichprolabel, self.tab_3)
        font = self.labelSandwichpro.font()
        font.setPointSize(10)
        font.setBold(True)
        self.labelSandwichpro.setFont(font)
        self.labelSandwichpro.setAlignment(QtCore.Qt.AlignCenter)
        SandwichproFrame_layout = QGridLayout(SandwichproFrame)
        SandwichproFrame_layout.addWidget(self.labelSandwichpro)
        self.tabLayout_3.addWidget(SandwichproFrame, 5, 12, 2, 7)
        #add mould production label with frame
        self.Mouldprolabel = "Mold Production"
        MouldproFrame = QFrame(self.tab_3)
        MouldproFrame.setFrameStyle(QFrame.Box)
        self.labelMouldpro = QLabel(self.Mouldprolabel, self.tab_3)
        self.labelMouldpro.setAlignment(QtCore.Qt.AlignCenter)
        MouldproFrame_layout = QGridLayout(MouldproFrame)
        MouldproFrame_layout.addWidget(self.labelMouldpro)
        self.tabLayout_3.addWidget(MouldproFrame, 5, 22, 2, 7)
        #create frame for sandwich elements proces
        self.SandwichprocessFrame = QFrame(self.tab_3)
        self.SandwichprocessFrame.setFrameStyle(QFrame.Box)       
        #create the duplciate button for the sandwich element processes
        self.pushButton_add_sandwichprocess = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_add_sandwichprocess.setObjectName("Add sandwich process")
        self.pushButton_add_sandwichprocess.setFixedSize(20, 20)  # Adjust width and height as needed
        self.pushButton_add_sandwichprocess.setText(_translate("MainWindow", "+"))
        self.pushButton_add_sandwichprocess.clicked.connect(self.duplicate_process_sandwich_A3)
        #create the sandwich element combobox
        self.combo_sandwichprocess = QtWidgets.QComboBox(self.tab_3)
        #self.combo_mouldprocess.setFixedWidth(160)
        self.combo_sandwichprocess.addItems(["Vibration table", "Loading hopper", "Hopper transport (by crane)", "Gantry crane (1 crane)", "Gantry crane (2 cranes)", "Rebar transportation (by crane)"])
        #add the + buttons and the combobox to the frame
        SandwichprocessFrame_layout = QGridLayout(self.SandwichprocessFrame)
        SandwichprocessFrame_layout.addWidget(self.pushButton_add_sandwichprocess, 0, 0)
        SandwichprocessFrame_layout.addWidget(self.combo_sandwichprocess, 0, 1, 1, 3)
        #place the frame 
        self.tabLayout_3.addWidget(self.SandwichprocessFrame, 9, 0, 1, 6)
        #create the sandwich mat frame
        self.SandwichmatFrame = QFrame(self.tab_3)
        self.SandwichmatFrame.setFrameStyle(QFrame.Box)
        #Create the sandwich material combobox and add the names
        self.combo_sandwichmat = QtWidgets.QComboBox(self.tab_3)
        self.combo_sandwichmat.setFixedWidth(195)
        for item in self.unique_names_sanwich:
            self.combo_sandwichmat.addItems([item])
        
        #Create the duplicate button for the materials
        self.pushButton_add_sandwichmat = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_add_sandwichmat.setObjectName("Add sandwich material")
        self.pushButton_add_sandwichmat.setFixedSize(20, 20)  # Adjust width and height as needed
        self.pushButton_add_sandwichmat.setText(_translate("MainWindow", "+"))
        self.pushButton_add_sandwichmat.clicked.connect(lambda: self.duplicate_material_A3(self.combo_sandwichmat, self.pushButton_add_sandwichmat, self.combo_sandwichprocess))
        #add items to the sandwichmat frame
        self.SandwichmatFrame_layout = QGridLayout(self.SandwichmatFrame)
        self.SandwichmatFrame_layout.addWidget(self.combo_sandwichmat, 0, 0, 1, 4)
        self.SandwichmatFrame_layout.addWidget(self.pushButton_add_sandwichmat, 0, 7, 1, 1)
        self.tabLayout_3.addWidget(self.SandwichmatFrame, 9, 7, 1, 8)
        #create the duplcate button for the mold materials
        self.pushButton_add_mouldmat = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_add_mouldmat.setObjectName("Add mould materials")
        self.pushButton_add_mouldmat.setFixedSize(20, 20)
        self.pushButton_add_mouldmat.setText(_translate("MainWindow", "+"))
        self.pushButton_add_mouldmat.clicked.connect(lambda: self.duplicate_material_mould_A3(self.combo_mouldmat, self.pushButton_add_mouldmat, self.combo_mouldprocess))
        
        #create mould materials material combobox and add the names
        self.combo_mouldmat = QtWidgets.QComboBox(self.tab_3)
        self.combo_mouldmat.setFixedWidth(195)
        for item in self.unique_names_mould:
            self.combo_mouldmat.addItems([item])
        #add items to the mould material frame
        self.MouldmatFrame = QFrame(self.tab_3)
        self.MouldmatFrame.setFrameStyle(QFrame.Box)
        self.MouldmatFrame_layout = QGridLayout(self.MouldmatFrame)
        self.MouldmatFrame_layout.addWidget(self.pushButton_add_mouldmat, 0, 0, 1, 1)
        self.MouldmatFrame_layout.addWidget(self.combo_mouldmat, 0, 4, 1, 4)
        self.tabLayout_3.addWidget(self.MouldmatFrame, 9, 16, 1, 8 )
        #create the mould process frame
        MouldprocessFrame = QFrame(self.tab_3)
        MouldprocessFrame.setFrameStyle(QFrame.Box)
        #create the duplicate mould proces button
        self.pushButton_add_mouldprocess = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_add_mouldprocess.setObjectName("Add mould process")
        self.pushButton_add_mouldprocess.setFixedSize(20, 20)
        self.pushButton_add_mouldprocess.setText(_translate("MainWindow", "+"))
        self.pushButton_add_mouldprocess.clicked.connect(self.duplicate_process_mould_A3)
        #create the mould process combobox
        self.combo_mouldprocess = QtWidgets.QComboBox(self.tab_3)
        self.combo_mouldprocess.setFixedWidth(160)
        self.combo_mouldprocess.addItems(["Vibration table", "Loading hopper", "Hopper transport (by crane)", "Gantry crane (1 crane)", "Gantry crane (2 cranes)", "Rebar transportation (by crane)"])
        #add items to the mouldproces frame
        MouldprocessFrame_layout = QGridLayout(MouldprocessFrame)
        MouldprocessFrame_layout.addWidget(self.combo_mouldprocess, 0, 0, 1, 5)
        MouldprocessFrame_layout.addWidget(self.pushButton_add_mouldprocess, 0, 6, 1, 1)
        self.tabLayout_3.addWidget(MouldprocessFrame, 9, 25, 1, 6)
        
        #add to dictionairy for linking sandwich material frame to + buttons
        if self.pushButton_add_sandwichmat not in self.sandwich_frame_dict:
            self.sandwich_frame_dict[self.pushButton_add_sandwichmat] = self.SandwichmatFrame
        #add to dictioniary for linking sanwich materials with processes
        if self.combo_sandwichprocess not in self.sandwich_process_mat_dict:
            self.sandwich_process_mat_dict[self.combo_sandwichprocess] = [self.combo_sandwichmat]
        #add to dictionairy linking mould material frame to + buttons
        if self.pushButton_add_mouldmat not in self.mould_frame_dict:
            self.mould_frame_dict[self.pushButton_add_mouldmat] = self.MouldmatFrame
        #add to dictioniary for linking mould materials with processes
        if self.combo_mouldprocess not in self.mould_process_mat_dict:
            self.mould_process_mat_dict[self.combo_mouldprocess] = [self.combo_mouldmat]
        self.retranslateUi(MainWindow)
        return self.SandwichmatFrame_layout
        
    #Function that duplicates the mould process box in tab A3
    def duplicate_process_mould_A3(self):
        _translate = QtCore.QCoreApplication.translate
        # Create a new frame
        new_mouldprocessFrame = QtWidgets.QFrame(self.tab_3)
        new_mouldprocessFrame.setFrameStyle(QtWidgets.QFrame.Box)
        
        # Create a combobox and add items (assuming it's the same as the original)
        combo_box_process_copy = QtWidgets.QComboBox(new_mouldprocessFrame)
        combo_box_process_copy.setFixedWidth(180)
        combo_box_process_copy.addItems([self.combo_mouldprocess.itemText(i) for i in range(self.combo_mouldprocess.count())])

        # Create a layout for the new frame
        new_mouldprocessFrame_layout = QtWidgets.QGridLayout(new_mouldprocessFrame)
        new_mouldprocessFrame_layout.addWidget(combo_box_process_copy, 1, 1, 1, 3)  # Assuming combo box spans 3 columns

        #Create a new mat Frame
        self.new_mat_Frame = QtWidgets.QFrame(self.tab_3)
        self.new_mat_Frame.setFrameStyle(QtWidgets.QFrame.Box)
        #Create a new material combobox
        self.combo_box_mat_copy = QtWidgets.QComboBox(self.new_mat_Frame)
        self.combo_box_mat_copy.setFixedWidth(195)
        self.combo_box_mat_copy.addItems([self.combo_mouldmat.itemText(i) for i in range(self.combo_mouldmat.count())])
        #Create a new duplicate button
        pushbutton_mat_copy = QtWidgets.QPushButton(self.new_mat_Frame)
        pushbutton_mat_copy.setObjectName("Add mould material")
        pushbutton_mat_copy.setFixedSize(20, 20)  # Adjust width and height as needed
        pushbutton_mat_copy.setText(_translate("MainWindow", "+"))
        pushbutton_mat_copy.clicked.connect(lambda: self.duplicate_material_mould_A3(self.combo_box_mat_copy, pushbutton_mat_copy, combo_box_process_copy))

        #create a new material frame layout
        new_mat_Frame_layout = QtWidgets.QGridLayout(self.new_mat_Frame)
        new_mat_Frame_layout.addWidget(self.combo_box_mat_copy, 0, 4, 1, 4 )
        new_mat_Frame_layout.addWidget(pushbutton_mat_copy, 0, 0, 1, 1)

        # Insert the new frame underneath the original frame
        self.tabLayout_3.addWidget(new_mouldprocessFrame, 9 + self.linecounter_mould_A3, 25, 1, 6 )
        self.tabLayout_3.addWidget(self.new_mat_Frame, 9 + self.linecounter_mould_A3, 16, 1, 8)
        self.linecounter_mould_A3 += 2

        #add the pushbutton and associated frame to the dictionairy --> for linking the correct buttons to the correct frames
        if pushbutton_mat_copy not in self.mould_frame_dict:
            self.mould_frame_dict[pushbutton_mat_copy] = self.new_mat_Frame

        #add the process and associated material combobox to the ditionairy 
        if combo_box_process_copy not in self.mould_process_mat_dict:
            self.mould_process_mat_dict[combo_box_process_copy] = [self.combo_box_mat_copy]
            
    #Function that duplicates the sandwich process box in tab A3
    def duplicate_process_sandwich_A3(self):
        _translate = QtCore.QCoreApplication.translate
        # Create a new frame
        new_sandwichprocessFrame = QtWidgets.QFrame(self.tab_3)
        new_sandwichprocessFrame.setFrameStyle(QtWidgets.QFrame.Box)
        
        # Create a combobox and add items (assuming it's the same as the original)
        combo_box_process_copy = QtWidgets.QComboBox(new_sandwichprocessFrame)
        combo_box_process_copy.setFixedWidth(180)
        combo_box_process_copy.addItems([self.combo_sandwichprocess.itemText(i) for i in range(self.combo_sandwichprocess.count())])

        # Create a layout for the new frame
        new_sandwichprocessFrame_layout = QtWidgets.QGridLayout(new_sandwichprocessFrame)
        new_sandwichprocessFrame_layout.addWidget(combo_box_process_copy, 1, 1, 1, 3)  # Assuming combo box spans 3 columns

        #Create a new mat Frame
        self.new_mat_Frame = QtWidgets.QFrame(self.tab_3)
        self.new_mat_Frame.setFrameStyle(QtWidgets.QFrame.Box)
        #Create a new material combobox
        self.combo_box_mat_copy = QtWidgets.QComboBox(self.new_mat_Frame)
        self.combo_box_mat_copy.setFixedWidth(195)
        self.combo_box_mat_copy.addItems([self.combo_sandwichmat.itemText(i) for i in range(self.combo_sandwichmat.count())])
        #Create a new duplicate button
        pushbutton_mat_copy = QtWidgets.QPushButton(self.new_mat_Frame)
        pushbutton_mat_copy.setObjectName("Add sandwich material")
        pushbutton_mat_copy.setFixedSize(20, 20)  # Adjust width and height as needed
        pushbutton_mat_copy.setText(_translate("MainWindow", "+"))
        pushbutton_mat_copy.clicked.connect(lambda: self.duplicate_material_A3(self.combo_box_mat_copy, pushbutton_mat_copy, combo_box_process_copy))

        #create a new material frame layout
        new_mat_Frame_layout = QtWidgets.QGridLayout(self.new_mat_Frame)
        new_mat_Frame_layout.addWidget(self.combo_box_mat_copy, 0, 0, 1, 4 )
        new_mat_Frame_layout.addWidget(pushbutton_mat_copy, 0, 7, 1, 1)

        # Insert the new frame underneath the original frame
        self.tabLayout_3.addWidget(new_sandwichprocessFrame, 9 + self.linecounter_sand_A3, 0, 1, 6 )
        self.tabLayout_3.addWidget(self.new_mat_Frame, 9 + self.linecounter_sand_A3, 7, 1, 8)
        self.linecounter_sand_A3 += 2

        #add the pushbutton and associated frame to the dictionairy --> for linking the correct buttons to the correct frames
        if pushbutton_mat_copy not in self.sandwich_frame_dict:
            self.sandwich_frame_dict[pushbutton_mat_copy] = self.new_mat_Frame

        #add the process and associated material combobox to the ditionairy 
        if combo_box_process_copy not in self.sandwich_process_mat_dict:
            self.sandwich_process_mat_dict[combo_box_process_copy] = [self.combo_box_mat_copy]
            
    #Function that duplicates the material combo box for mould materials in tab A3
    def duplicate_material_mould_A3(self, combo_mouldmat, pushbutton, combo_mould_process):
        #Duplicate the material combobox
        combo_mouldmat_copy = QtWidgets.QComboBox(self.tab_3)
        combo_mouldmat_copy.setFixedWidth(235)
        #copy items from original
        combo_mouldmat_copy.addItems([combo_mouldmat.itemText(i) for i in range(combo_mouldmat.count())])

        #take the frame belonging to the pushed button
        frame_2 = self.mould_frame_dict[pushbutton]

        #add duplicates to the layout inside the original frame
        layout = frame_2.layout()
        row = layout.rowCount()
        layout.addWidget(combo_mouldmat_copy, row, 0, 1, 8)

        #layout.setAlignment(QtCore.Qt.AlignBottom)

        #add the materials to hte associated process dicitonairy 
        if combo_mould_process in self.mould_process_mat_dict:
            self.mould_process_mat_dict[combo_mould_process].append(combo_mouldmat_copy)
        else:
            print('dit zou niet mogelijk moeten zijn')

        #refresh the layout
        layout.update()
    
    #Function that duplicates the material combo box for sandwich materials in tab A3
    def duplicate_material_A3(self, combo_sandwichmat, pushbutton, combo_process):
        # Duplicate material combobox
        combo_sandwichmat_copy = QtWidgets.QComboBox(self.tab_3)
        combo_sandwichmat_copy.setFixedWidth(235)  # Set the same width as the original
        # Copy items from the original combobox   
        combo_sandwichmat_copy.addItems([combo_sandwichmat.itemText(i) for i in range(combo_sandwichmat.count())])
        
        #take the frame bellongin to the pushed button
        frame = self.sandwich_frame_dict[pushbutton]

        # Add duplicates to the layout inside the original frame
        layout = frame.layout()  # Get the layout of the frame
        row = layout.rowCount()  # Get the next available row
        layout.addWidget(combo_sandwichmat_copy, row, 0, 1, 8)  # Add material combobox
        #layout.addWidget(combo_sandwichunit_copy, row, 5, 1, 1)  # Add unit combobox

        #layout.setAlignment(QtCore.Qt.AlignBottom)
        
        #add the materials to the associated process dictionairy
        if combo_process in self.sandwich_process_mat_dict:
            self.sandwich_process_mat_dict[combo_process].append(combo_sandwichmat_copy)
        else:
            print('dit zou niet mogelijk moeten zijn')
        
        # Refresh the layout
        layout.update()

class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        #set window title
        self.setWindowTitle("Sandwich Element EP Calculator")
        #create the required list for importing the manual excel data
        
        self.imported_names = []
        self.imported_env_data = []
        self.imported_FU = []
        #set a default year of the connection with the first node of the API
        self.valid_until = '2028'
        #parameters for the calling of the connect node 1 fuction
        self.headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer #insert key
        }
        self.params = {
        "pageSize": "10000",
        "format": "JSON",   
        }
        self.params_2 = {
        "pageSize": "10000",
        "format": "JSON",
        "view": "extended",
        }
        #Connection is made to the first node of the API on startup
        self.data_node_1 = connect_node_1(self.headers, self.params, self.valid_until)
        
        #save the emission factors for A2 and A4 on startup
        self.transport_emission_window = EmissionFactorsWindow()
        self.transport_emission_window.__init__()
        self.transport_emission_window.save_emission_factors()
        #save the process emission factors for A3 on startup
        self.processFactors = EmissionFactorsWindow_A3()
        self.processFactors.__init__()
        self.processFactors.save_emission_factor_A3()

        #save the hopper capacity factor on startup
        self.hoppercapacity = HopperCapacityWindow()
        self.hoppercapacity.__init__()
        self.hoppercapacity.save_hoppercapacity()

        self.surface_setting_window = SquareMeterWindow()
        self.surface_setting_window.__init__()
        self.surface_setting_window.square_meters = 1.0


        #creation of the dictionairy required for linking certain items in the UI
        self.line_search_dict = {}
        self.name_quantity_dict = {}
        self.line_data_dict = {}
        self.quantity_unit_dict = {}
        self.LCA_result_dict = {}
        self.name_transport_dict_tab2 = {}
        self.name_weight_dict_tab2 = {}

        self.line_data_dict_2 = {
            'insulation': {},  # Initialize an empty dictionary for 'insulation'
            'inner': {},       # Initialize an empty dictionary for 'inner'
            'outer': {},        # Initialize an empty dictionary for 'outer'
            'mould': {}
        }

        self.name_transport_dict_A4 = {}
        self.name_weight_dict_A4 = {}
        #set selected file as None on startup
        self.selected_file = None
        
        #run the UI setup from Ui_Mainwindow
        self.setupUi(self)  
        
        #add the initial button combos to the data_dict_2 dictionairy --> for the connection between combos when new lines are added
        self.line_data_dict_2['insulation'][f'SearchButton-{hex(id(self.pushButton_search_matpro_ins))}'] = (f'LineEditCode: {hex(id(self.lineEdit_matpro_ins))}', self.lineEdit_matpro_ins)
        self.line_data_dict_2['inner'][f'SearchButton-{hex(id(self.pushButton_search_matpro_inner))}'] = (f'LineEditCode: {hex(id(self.lineEdit_matpro_inner))}', self.lineEdit_matpro_inner)
        self.line_data_dict_2['outer'][f'SearchButton-{hex(id(self.pushButton_search_matpro_outer))}'] = (f'LineEditCode: {hex(id(self.lineEdit_matpro_outer))}', self.lineEdit_matpro_outer)
        self.line_data_dict_2['mould'][f'SearchButton-{hex(id(self.pushButton_search_matpro_mould))}'] = (f'LineEditCode: {hex(id(self.lineEdit_matpro_mould))}', self.lineEdit_matpro_mould)
        # add the intial search buttons combos to the data_dict --> for the extraction of names filled in the line edit boxes
        self.line_data_dict['insulation'] = (self.lineEdit_matpro_ins, self.pushButton_search_matpro_ins)
        self.line_data_dict['inner'] = (self.lineEdit_matpro_inner, self.pushButton_search_matpro_inner)
        self.line_data_dict['outer'] = (self.lineEdit_matpro_outer, self.pushButton_search_matpro_outer)
        self.line_data_dict['mould'] = (self.lineEdit_matpro_mould, self.pushButton_search_matpro_mould)
        #add the intial quantity buttons combos to the data_dict --> for the extraction of quantities filled in the line edit boxes
        self.quantity_unit_dict['insulation'] = (self.lineEdit_quantity_ins, self.comboBox_unit_ins)
        self.quantity_unit_dict['inner'] = (self.lineEdit_quantity_inner, self.comboBox_unit_inner)
        self.quantity_unit_dict['outer'] = (self.lineEdit_quantity_outer, self.comboBox_unit_outer)
        self.quantity_unit_dict['mould'] = (self.lineEdit_quantity_mould, self.comboBox_unit_mould)
        #add the intital items to the dictionairy for tab A4
        self.name_weight_dict_A4['Sandwich element'] = [(self.line_edit_weight_A4)]
        self.name_transport_dict_A4['Sandwich element'] = [(self.combo_transport_mode_A4, self.line_edit_distance_A4)]
        #Establisch the connections between buttons and functions
        self.setup_connections()

    #Function that creates the connection between the buttons and the functions
    def setup_connections(self):
        # #Establish connection for the + and - buttons
        self.pushButton_add_line_ins.clicked.connect(self.add_line_insulation)  
        self.pushButton_add_line_inner.clicked.connect(self.add_line_inner)
        self.pushButton_add_line_outer.clicked.connect(self.add_line_outer)
        self.pushButton_delete_line_ins.clicked.connect(self.delete_line_insulation)
        self.pushButton_delete_line_inner.clicked.connect(self.delete_line_inner)
        self.pushButton_delete_line_outer.clicked.connect(self.delete_line_outer)
        self.pushButton_add_line_mould.clicked.connect(self.add_line_mould)
        # #Establish connection for the search buttons
        self.pushButton_search_matpro_ins.clicked.connect(lambda _, button_name=hex(id(self.pushButton_search_matpro_ins)): self.search_button_clicked('insulation', button_name))
        self.pushButton_search_matpro_inner.clicked.connect(lambda _, button_name=hex(id(self.pushButton_search_matpro_inner)): self.search_button_clicked('inner', button_name))
        self.pushButton_search_matpro_outer.clicked.connect(lambda _, button_name=hex(id(self.pushButton_search_matpro_outer)): self.search_button_clicked('outer', button_name))
        self.pushButton_search_matpro_mould.clicked.connect(lambda _, button_name=hex(id(self.pushButton_search_matpro_mould)): self.search_button_clicked('mould', button_name))
        #Establish the connetion for the EPD save button
        self.pushButton_get_EPD.clicked.connect(self.calculate_A1)
        # #Establish connections for the items of the file menu
        self.actionImport_ifc_file.triggered.connect(self.show_import_selection_window)  
        self.actionImport_manual_import.triggered.connect(self.import_and_process_excel)
        self.actionEco_settings.triggered.connect(self.show_eco_settings_dialog)  
        self.actionMould_reuse.triggered.connect(self.show_mould_reuse_window)
        self.transport_factors_A2.triggered.connect(self.show_transport_emission_window)
        self.actionProcessEmFactors.triggered.connect(self.show_process_emission_window)
        self.actionSurface_setting.triggered.connect(self.show_surface_settings_window)
        self.action_settings_A3.triggered.connect(self.show_hopper_capacity_window)
        #TAB 2
        self.pushButton_import_A1_button.clicked.connect(self.generate_UI_A2)

        #TAB 3
        self.pushButton_GenerateUI_A3.clicked.connect(self.generate_UI_A3)
        #TAB4
        self.pushButton_importWeight_A2.clicked.connect(self.import_weight_A4)
        self.pushButton_calculate_A4.clicked.connect(self.calculate_A4)
        self.pushButton_calculate_All.clicked.connect(self.calculate_All)
        
    #Function that searches through the first node of the API data for matching names; creates the correct links between search buttons and line edit boxes
    def search_button_clicked(self, section, button):
   
        for section, data in self.line_data_dict_2.items():
            for key, values in data.items():
                if button in key:
                    if isinstance(values, tuple) and len(values) == 2:
                        line_edit_code, line_edit = values
                        keyword = line_edit.text()
                        name_list = search_by_keyword_name(keyword, self.data_node_1)
                        #search through the manually added names through the excel import function and add them to the name_list if keyword matches
                        if self.imported_names is not None:
                            for name in self.imported_names:
                                if keyword.lower() in name.lower() and name not in name_list:
                                    name_list.append(name)
                        dialog = SearchResultsDialog(name_list, self.centralwidget)
                        result = dialog.exec_()
                        if result == QtWidgets.QDialog.Accepted:
                            selected_item = dialog.name_list_widget.currentItem()
                            if selected_item is not None:
                                line_edit.setText(selected_item.text())
                    else:
                        print(f'Invalid structure for values in key {key}')
    
    #Function that extracts and sums the weights from tab A2 and places the summed weight in tab A4
    def import_weight_A4(self):
        self.mould_names = []
        self.total_weight = []
        weights = []
        
        #sort through the line_data_dict to find the material names that are under the key mould --> needed to filter out mould materials for total weight sandwich element calculation
        for key, data in self.line_data_dict.items():
            if key == 'mould':
                for item in data:
                    if isinstance(item, tuple):
                        line_edit, _ = item
                        name = line_edit.text().strip()
                        self.mould_names.append(name)

                    elif isinstance(item, QtWidgets.QLineEdit):
                        # Handle the case where an individual QLineEdit is present
                        name = item.text().strip()
                        self.mould_names.append(name)
    
        for names, weightboxes in self.name_weight_dict_tab2.items():
            for weightbox in weightboxes: 
                if isinstance(weightbox, QtWidgets.QLineEdit):
                    material_name = names
                    if material_name not in self.mould_names:
                        weight = float(weightbox.text().strip())
                        weights.append(weight)
        
        self.total_weight = sum(weights)
       
        for name, items in self.name_weight_dict_A4.items():
            for item in items:
                if isinstance(item, QtWidgets.QLineEdit):
                    item.setText(str(self.total_weight))

    #Function that calculates all stages at once
    def calculate_All(self):
        
        self.calculate_A1()
        self.calculate_A2()
        self.calculate_A3()
        self.calculate_A4()
        
        #sum the values for each individual impact category
        #self.summed_LCA_result_dict = create_dict_categories_totalsums(self.LCA_result_dict)   
        
        print(self.LCA_result_dict)
        
        #filtered_abbreviations = extract_abbreviations(self.LCA_result_dict)
        abr = 'GWP-total'
        plot_material_impact_total_bar_chart(abr, self.LCA_result_dict)
        plot_stage_impact_total_bar_chart(abr, self.LCA_result_dict)
    
    #Function that calculates the A4 stage
    def calculate_A4(self):
        total_impact_dict_A4 = {}
        category_impacts_list_A4 = []
        stage = 'A4'

        if stage in self.LCA_result_dict:
            self.LCA_result_dict[stage] = {}
        for element, transport_combinations in self.name_transport_dict_A4.items():
            total_impact_dict_A4 = {}
            if element in self.name_weight_dict_A4:
                weight_lineedit_A4 = self.name_weight_dict_A4[element][0]
                weight = float(weight_lineedit_A4.text())

            for transport_combination in transport_combinations:
                transport_mode_combobox_A4, distance_lineedit_A4 = transport_combination
                transport_mode_A4 = transport_mode_combobox_A4.currentText()
                distance = float(distance_lineedit_A4.text())

                if transport_mode_A4 in self.transport_emission_window.emission_factors_A2:
                    for category in self.transport_emission_window.emission_factors_A2[transport_mode_A4]:
                        emission_factor_A4 = (self.transport_emission_window.emission_factors_A2[transport_mode_A4][category])/1000
                        impact = weight * distance * emission_factor_A4
                        
                        if category not in total_impact_dict_A4:
                            total_impact_dict_A4[category] = impact
                        else:
                            total_impact_dict_A4[category] += impact

            fraction = 0
            for name, weightboxes in self.name_weight_dict_tab2.items():
                for weightbox in weightboxes:
                    if isinstance(weightbox, QtWidgets.QLineEdit):
                            mat_name = name
                            
                            if mat_name not in self.mould_names:
                                weight_2 = float(weightbox.text().strip())
                            else:
                                weight_2 = 0
                fraction = weight_2/self.total_weight
                category_impacts_list_A4 = [{'label': f'({category})', 'value': total_impact*fraction, 'Unit': 'x'} for category, total_impact in total_impact_dict_A4.items()]
                
                #append the A4 data to the final dictionairy
                self.LCA_result_dict = append_final_dict(self.LCA_result_dict, stage, name, category_impacts_list_A4)
        
        
        self.LCA_result_dict = filter_impact_categories(self.LCA_result_dict)
        #Divide the values in the LCA results dictionairy by the entered surface area of the sandwich element
        self.LCA_result_dict = divide_values_by_surface(self.LCA_result_dict, stage, self.surface_setting_window.square_meters)
        
        
        #Remove the mould materials from the A4 key in the final dictioniary (because the value are 0)
        # mat_to_remove = []
        # for material, properties in self.LCA_result_dict['A4'].items():
        #     if all(value['value'] == 0 for value in properties.values()):
        #     # If all values are zero, remove the material from A4 stage
        #         mat_to_remove.append(material)
        # for material in mat_to_remove:
        #     del self.LCA_result_dict['A4'][material]

        if 'A1' in self.LCA_result_dict:
            #unify the language and units for all stages in the dictionairy based on the used language used in stage A1
            self.LCA_result_dict = unify_language(self.LCA_result_dict, self.LCA_result_dict['A1'])
        else:
            print('Cannot unify language stage A4 because stage A1 was not calulated')
        
        abr = 'GWP-total'
        plot_material_impact_stage_bar_chart(abr, stage, self.LCA_result_dict)
        
    #Function that calculates the A3 stage
    def calculate_A3(self, A1_A3=None):
        if A1_A3 is not None:
            self.calculate_A1()
            self.calculate_A2()
        
        self.sandwich_process_impact_dict = {}
        self.mould_process_impact_dict = {}
        self.name_volume_dict_A3 = {}
        all_names_A3 = []
        quantities_A3 = []
        units_A3 = []
        self.mould_names = []
        self.sandwich_names = []
        sandwich_weight= []
        mould_weight = []
        concrete_weight = []
        stage = 'A3'
        if stage in self.LCA_result_dict:
            self.LCA_result_dict[stage] = {}

        # Extracting the names from the QLineEdit objects under the 'mould' key in self.line_data_dict
        mould_line_edits = self.line_data_dict.get('mould', [])
        mould_names = set()
        for item in mould_line_edits:
            if isinstance(item, tuple):
                # If item is a tuple, extract text from the first element of the tuple
                mould_names.add(item[0].text())
            elif isinstance(item, QtWidgets.QLineEdit):
                # If item is a QLineEdit object, extract text directly
                mould_names.add(item.text())
        
        # Filtering self.name_weight_dict_tab2 based on the names present in the 'mould' line edits --> creates dictionariy containing only mould materials or sandwich materials
        #needed for calculating energy costs between materials
        filtered_name_weight_dict_sandwich = {}
        filtered_name_weight_dict_mould = {}
        for name, weightboxes in self.name_weight_dict_tab2.items():
            if name not in mould_names:
                filtered_name_weight_dict_sandwich[name] = weightboxes
            if name in mould_names:
                filtered_name_weight_dict_mould[name] = weightboxes

        ###########################################################
        ####EXTRACTING THE REQUIRED DATA FOR FUTURE CALCULATION####
        ###########################################################
        
        # Extract names from line_data_dict
        for section, elements in self.line_data_dict.items():
            for element in elements:
                if isinstance(element, tuple):
                    line_edit, _ = element
                    name = line_edit.text().strip()
                    all_names_A3.append(name)

                elif isinstance(element, QtWidgets.QLineEdit):
                    # Handle the case where an individual QLineEdit is present
                    name = element.text().strip()
                    all_names_A3.append(name)
                    
        
        # Extract quantities and units from quantity_unit_dict
        for section, items in self.quantity_unit_dict.items():
            for item in items:
                if isinstance(item, tuple):
                    line_edit_2, combo_box  = item
                    quantity = line_edit_2.text().strip()
                    unit = combo_box.currentText().strip()
                    if quantity:
                        quantities_A3.append(quantity)
                        units_A3.append(unit)
                elif isinstance(item, QtWidgets.QLineEdit):
                    quantity = item.text().strip()
                    if quantity:
                        quantities_A3.append(quantity)
                elif isinstance(item, QtWidgets.QComboBox):
                    unit = item.currentText().strip()
                    if unit:
                        units_A3.append(unit)

        #Create a dictionairy containing the names, quanitities, and units from tab A1
        self.name_quantity_dict_A3 = {}
        print(all_names_A3)
        indices_to_remove = [i for i, item in enumerate(all_names_A3) if item == '']
        all_names_A3 = [item for i, item in enumerate(all_names_A3) if i not in indices_to_remove]
        units_A3 =    [item for i, item in enumerate(units_A3) if i not in indices_to_remove]
        print(all_names_A3)
        for i in range(len(all_names_A3)):
            name = all_names_A3[i]
            quantity = float(quantities_A3[i])
            unit = units_A3[i]
            
            #Create the dictionairy and check if duplicate names exists. if they do, summ the quanities
            if name not in self.name_quantity_dict_A3:
                self.name_quantity_dict_A3[name] = {'quantity': quantity, 'unit': unit}
            else:
                existing_unit = self.name_quantity_dict_A3[name]['unit']

                if existing_unit == unit:
                    self.name_quantity_dict_A3[name]['quantity'] += quantity
                else:
                    print(f"Warning: Units don't match for {name}. Existing unit: {existing_unit}, New unit: {unit}")
    
        ###EXTRACT TOTAL SANDWICH AND MOULD WEIGHTS####
        for key, data in self.line_data_dict.items():
            if key != 'mould':
                for item in data:
                    if isinstance(item, tuple):
                        line_edit, _ = item
                        name = line_edit.text().strip()
                        self.sandwich_names.append(name)

                    elif isinstance(item, QtWidgets.QLineEdit):
                        # Handle the case where an individual QLineEdit is present
                        name = item.text().strip()
                        self.sandwich_names.append(name)

            
            if key == 'mould':
                for item in data:
                    if isinstance(item, tuple):
                        line_edit, _ = item
                        name = line_edit.text().strip()
                        self.mould_names.append(name)

                    elif isinstance(item, QtWidgets.QLineEdit):
                        # Handle the case where an individual QLineEdit is present
                        name = item.text().strip()
                        self.mould_names.append(name)
    
        for names, weightboxes in self.name_weight_dict_tab2.items():
            for weightbox in weightboxes: 
                if isinstance(weightbox, QtWidgets.QLineEdit):
                    material_name = names
                    if material_name not in self.mould_names:
                        weight = float(weightbox.text().strip())
                        sandwich_weight.append(weight)
                    if material_name in self.mould_names:
                        weight = float(weightbox.text().strip())
                        mould_weight.append(weight)
        self.sandwich_total_weight = sum(sandwich_weight)
        self.mould_total_weight = sum(mould_weight) 
        
        ###########################################################
        ##############CALCULATING ELECTRICITY IMPACT###############
        ###########################################################
                   
        self.electricity_process = "Electricity"
        self.total_elec = float(self.line_edit_elec.text().strip())
        self.elec_ratio_sandwich = float((self.elecratio_sandwich.value()/100))
        self.elec_ratio_mould = float((self.elecratio_mould.value()/100))
        
        for category in self.processFactors.emission_factors_A3[self.electricity_process]:
            emission_factor_elec = float(self.processFactors.emission_factors_A3[self.electricity_process][category])
            self.sandwich_mat_impact_dict_elec = {}  # Reset the dict for each category
            self.mould_mat_impact_dict_elec = {}
            for names, weightboxes in filtered_name_weight_dict_sandwich.items():
                for weightbox in weightboxes: 
                    if isinstance(weightbox, QtWidgets.QLineEdit):
                        material_name = names
                        weight = float(weightbox.text().strip())
                        mat_impact_elec_sandwich = ((self.total_elec * emission_factor_elec) * self.elec_ratio_sandwich) * (weight / self.sandwich_total_weight)
                        # Accumulate impacts within the same category
                        self.sandwich_mat_impact_dict_elec.setdefault(category, {}).setdefault(material_name, 0.0)
                        self.sandwich_mat_impact_dict_elec[category][material_name] += mat_impact_elec_sandwich
            for names, weightboxes in filtered_name_weight_dict_mould.items():
                for weightbox in weightboxes: 
                    if isinstance(weightbox, QtWidgets.QLineEdit):
                        material_name = names
                        weight = float(weightbox.text().strip())
                        mat_impact_elec_mould = ((self.total_elec * emission_factor_elec) * self.elec_ratio_mould) * (weight / self.mould_total_weight)
                        # Accumulate impacts within the same category
                        self.mould_mat_impact_dict_elec.setdefault(category, {}).setdefault(material_name, 0.0)
                        self.mould_mat_impact_dict_elec[category][material_name] += mat_impact_elec_mould

        # Assign the final result to self.sandwich_process_impact_dict
        self.sandwich_process_impact_dict[self.electricity_process] = self.sandwich_mat_impact_dict_elec
        self.mould_process_impact_dict[self.electricity_process] = self.mould_mat_impact_dict_elec
        
        ###########################################################
        ####CALCULATING PROCESS IMPACTS FOR SANDWICH MATERIALS#####
        ###########################################################
        
        
        for process, matlist in self.sandwich_process_mat_dict.items():
            self.sandwich_mat_impact_dict = {}
            self.sandwich_mat_impact_dict_1 = {}
            #Extract process
            self.sandwich_process = process.currentText()
            #Calculate the total weight of a set of materials assocaited with 
            for mats in matlist:
                self.sandwich_material_name = mats.currentText()
                line_edit_weight = self.name_weight_dict_tab2[self.sandwich_material_name][0]
                self.sandwich_mat_weight = float(line_edit_weight.text())
                concrete_weight.append(self.sandwich_mat_weight)
                total_concrete_weight = sum(concrete_weight)
                
            for material in matlist:
                self.sandwich_material_name = material.currentText()
                if self.sandwich_material_name in self.name_weight_dict_tab2:   
                    line_edit_weight = self.name_weight_dict_tab2[self.sandwich_material_name][0]
                    self.sandwich_mat_weight = float(line_edit_weight.text())
                    self.name_volume_dict_A3 = {key: value for key, value in self.name_quantity_dict_A3.items() if key == self.sandwich_material_name and value['unit'] == 'm3'}

                    if self.sandwich_process == "Gantry crane (1 crane)":
                        if self.sandwich_process in self.processFactors.emission_factors_A3:
                            for category in self.processFactors.emission_factors_A3[self.sandwich_process]:
                                emission_factor = self.processFactors.emission_factors_A3[self.sandwich_process][category]
                                mat_impact = (self.sandwich_mat_weight/self.sandwich_total_weight) * emission_factor
                                self.sandwich_mat_impact_dict_1[self.sandwich_material_name] = mat_impact
                                self.sandwich_mat_impact_dict[category] = self.sandwich_mat_impact_dict_1
                    elif self.sandwich_process == "Gantry crane (2 cranes)":
                        if self.sandwich_process in self.processFactors.emission_factors_A3:
                            for category in self.processFactors.emission_factors_A3[self.sandwich_process]:
                                emission_factor = self.processFactors.emission_factors_A3[self.sandwich_process][category]
                                mat_impact = (self.sandwich_mat_weight/self.sandwich_total_weight) * emission_factor
                                self.sandwich_mat_impact_dict_1[self.sandwich_material_name] = mat_impact
                                self.sandwich_mat_impact_dict[category] = self.sandwich_mat_impact_dict_1
                    elif self.sandwich_process == "Loading hopper":
                        if self.sandwich_process in self.processFactors.emission_factors_A3:
                            for category in self.processFactors.emission_factors_A3[self.sandwich_process]:
                                emission_factor = self.processFactors.emission_factors_A3[self.sandwich_process][category]
                                mat_impact = self.sandwich_mat_weight*emission_factor
                                self.sandwich_mat_impact_dict_1[self.sandwich_material_name] = mat_impact
                                self.sandwich_mat_impact_dict[category] = self.sandwich_mat_impact_dict_1
                    elif self.sandwich_process == "Vibration table":
                        if self.sandwich_process in self.processFactors.emission_factors_A3:
                            for category in self.processFactors.emission_factors_A3[self.sandwich_process]:
                                emission_factor = self.processFactors.emission_factors_A3[self.sandwich_process][category]
                                mat_impact = emission_factor
                                self.sandwich_mat_impact_dict_1[self.sandwich_material_name] = mat_impact
                                self.sandwich_mat_impact_dict[category] = self.sandwich_mat_impact_dict_1
                    elif self.sandwich_process == "Hopper transport (by crane)":
                        if self.sandwich_process in self.processFactors.emission_factors_A3:
                            for category in self.processFactors.emission_factors_A3[self.sandwich_process]:
                                emission_factor = self.processFactors.emission_factors_A3[self.sandwich_process][category]
                                self.sandwich_mat_volume = self.name_volume_dict_A3[self.sandwich_material_name]['quantity']
                                #amount of trips is equal to the capacity of the hopper divided by mat quantity
                                amount_of_trips = math.ceil(self.sandwich_mat_volume/self.hoppercapacity.hoppercapacity_factor) 
                                mat_impact = emission_factor * amount_of_trips
                                self.sandwich_mat_impact_dict_1[self.sandwich_material_name] = mat_impact
                                self.sandwich_mat_impact_dict[category] = self.sandwich_mat_impact_dict_1
                    elif self.sandwich_process == "Rebar transportation (by crane)":
                        if self.sandwich_process in self.processFactors.emission_factors_A3:
                            for category in self.processFactors.emission_factors_A3[self.sandwich_process]:
                                emission_factor = self.processFactors.emission_factors_A3[self.sandwich_process][category]
                                #asusming two trips for rebar inner leaf and outer leaf
                                mat_impact = emission_factor*2
                                self.sandwich_mat_impact_dict_1[self.sandwich_material_name] = mat_impact
                                self.sandwich_mat_impact_dict[category] = self.sandwich_mat_impact_dict_1


         
            self.sandwich_process_impact_dict[self.sandwich_process] = self.sandwich_mat_impact_dict
        
        
        ###########################################################
        ##############DATA TRANSFORMATION AND APPENDING############
        ###########################################################
        sandwich_append_dict = {}
        mould_append_dict = {}
        print(self.sandwich_process_impact_dict)
        for process, material_dict in self.sandwich_process_impact_dict.items():
            for category, impact_subdict in material_dict.items():
                for material, value in impact_subdict.items():
                    if material not in sandwich_append_dict:
                        sandwich_append_dict[material] = {'label': f'({category})', 'value': 0, 'Unit': 'x'}
                    sandwich_append_dict[material]['value'] += value

        for process, material_dict in self.mould_process_impact_dict.items():
            for category, impact_subdict in material_dict.items():
                for material, value in impact_subdict.items():
                    if material not in mould_append_dict:
                        mould_append_dict[material] = {'label': f'({category})', 'value': 0, 'Unit': 'x'}
                    mould_append_dict[material]['value'] += value

        combined_dict = sandwich_append_dict.copy()
        combined_dict.update(mould_append_dict)
     
        
        
        for name, data in combined_dict.items():
            self.LCA_result_dict = append_final_dict(self.LCA_result_dict, stage, name, [data])
        
        self.LCA_result_dict = filter_impact_categories(self.LCA_result_dict)
        #Divide the values in the LCA results dictionairy by the entered surface area of the sandwich element
        self.LCA_result_dict = divide_values_by_surface(self.LCA_result_dict, stage, self.surface_setting_window.square_meters)

        if 'A1' in self.LCA_result_dict:
            #unify the language and units for all stages in the dictionairy based on the used language used in stage A1
            self.LCA_result_dict = unify_language(self.LCA_result_dict, self.LCA_result_dict['A1'])
        else:
            print('Cannot unify language stage A3 because stage A1 was not calulated')
        
        abr = 'GWP-total'
        plot_material_impact_stage_bar_chart(abr, stage, self.LCA_result_dict)

        if A1_A3 is not None:
            plot_material_impact_total_bar_chart(abr, self.LCA_result_dict)
            plot_stage_impact_total_bar_chart(abr, self.LCA_result_dict)

    #Function that calculates the A2 stage 
    def calculate_A2(self):  
        total_impact_dict = {}
        category_impacts_list = []
        stage = 'A2'
        if stage in self.LCA_result_dict:
            self.LCA_result_dict[stage] = {}
        for material_name, transport_combinations in self.name_transport_dict_tab2.items():
            total_impact_dict = {}
            if material_name in self.name_weight_dict_tab2:
                weight_lineedit = self.name_weight_dict_tab2[material_name][0]
                weight = float(weight_lineedit.text())

            for transport_combination in transport_combinations:
                transport_mode_combobox, distance_lineedit = transport_combination
                transport_mode = transport_mode_combobox.currentText()
                distance = float(distance_lineedit.text())
                
                if transport_mode in self.transport_emission_window.emission_factors_A2:
                    for category in self.transport_emission_window.emission_factors_A2[transport_mode]:
                        emission_factor = (self.transport_emission_window.emission_factors_A2[transport_mode][category])/1000 #covert from gCO2/kg/km to kgCO2kg/km
                       
                        impact = weight * distance * emission_factor
                       
                        if category not in total_impact_dict:
                            total_impact_dict[category] = impact
                            
                        else:
                            total_impact_dict[category] += impact
                 
            category_impacts_list = [{'label': f'({category})', 'value': total_impact, 'Unit': 'x'} for category, total_impact in total_impact_dict.items()]
            
           #Append the A2 data to the LCA_result dictionairy
            self.LCA_result_dict = append_final_dict(self.LCA_result_dict, stage, material_name, category_impacts_list)
        #Filter the LCA_result dictionairy based on common impact categories
        self.LCA_result_dict = filter_impact_categories(self.LCA_result_dict)
        #Divide the values in the LCA results dictionairy by the entered surface area of the sandwich element
        self.LCA_result_dict = divide_values_by_surface(self.LCA_result_dict, stage, self.surface_setting_window.square_meters)
        
        if 'A1' in self.LCA_result_dict:
            #unify the language and units for all stages in the dictionairy based on the used language used in stage A1
            self.LCA_result_dict = unify_language(self.LCA_result_dict, self.LCA_result_dict['A1'])
        else:
            print('Cannot unify language stage A2 because stage A1 was not calulated')

        abr = 'GWP-total'
        plot_material_impact_stage_bar_chart(abr, stage, self.LCA_result_dict)

    #Function that searches trought the manually added data and the second node of the API data based on the names present in the line edit boxes, multipies it with the quanties and creates a dictionairy to store the results   
    def calculate_A1(self):
        quantities = []
        all_names = []
        units = []
        LCA_dict = {} #the complete dictionairy that will contain all the EP data for the creation of the graphs, the dictionairy is emptied every time the function is called
        self.LCA_result_dict = {}
        stage = 'A1'
        self.summed_LCA_result_dict = {}
        if stage in self.LCA_result_dict:
            self.LCA_result_dict[stage] = {}
        #extract the names from the UI
        for section, elements in self.line_data_dict.items():
            for element in elements:
                if isinstance(element, tuple):
                    line_edit, _ = element
                    name = line_edit.text().strip()
                    if name:
                        all_names.append(name)
                elif isinstance(element, QtWidgets.QLineEdit):
                    
                    # Handle the case where an individual QLineEdit is present
                    name = element.text().strip()
                    if name:
                        all_names.append(name)
    
        #extract the quantities and quantity units from the UI
        for section, items in self.quantity_unit_dict.items():
            for item in items: 
                if section == 'mould':
                    if isinstance(item, tuple):
                        line_edit_2, combo_box  = item
                        if line_edit_2.text().strip() is not None:
                            quantity = str(float(line_edit_2.text().strip())/float(self.mould_reuse_window.moldreuse_factor))
                            
                            if quantity:
                                quantities.append(quantity)
                                units.append(unit)   
                        else:
                            continue
                    
                    elif isinstance(item, QtWidgets.QLineEdit):
                        if item.text().strip() != "":
                            quantity = str(float(item.text().strip())/float(self.mould_reuse_window.moldreuse_factor))
                            if quantity:
                                quantities.append(quantity)
                        else:
                            continue
                    elif isinstance(item, QtWidgets.QComboBox):
                            unit = item.currentText().strip()
                            if unit:
                                units.append(unit)   
                
                elif isinstance(item, tuple):
                    line_edit_2, combo_box  = item
                    quantity = line_edit_2.text().strip()
                    unit = combo_box.currentText().strip()
                    
                    if quantity:
                        quantities.append(quantity)
                        units.append(unit)
                elif isinstance(item, QtWidgets.QLineEdit):
                    quantity = item.text().strip()
                    if quantity:
                        quantities.append(quantity)
                elif isinstance(item, QtWidgets.QComboBox):
                    unit = item.currentText().strip()
                    if unit:
                        units.append(unit)
        #combine names, quantities and units
        combined_data = zip(all_names, quantities, units)
             
        # Create a list of dictionaries 
        result_combined_list = []
        for name, quantity, unit in combined_data:
            material_data = {'name': name, 'quantity': quantity, 'unit': unit}
            result_combined_list.append(material_data)
        #set the parameters required for the search_by_keyword_data function --> into a settings menu in the future
        for material_data in result_combined_list:
            print_url = 'yes'
            print_data = 'no'
            print_ep_data = 'no'
            target_module = ['A1-A3', 'A1', 'A2', 'A3']
            name_2 = material_data['name']
            
            #check if the name is present in the list containing the manually added names and change the varaibles accordingly
            if any(name_2.strip() == imported_name.strip() for imported_name in self.imported_names):
                index = next(i for i, imported_name in enumerate(self.imported_names) if imported_name.strip() == name_2.strip())
                combined_list = self.imported_env_data[index]
                FU_node = self.imported_FU[index]
                quantity = float(material_data['quantity'])
                unit = material_data['unit']
            
            #if the name is not present in the list containing the manually added names, the EPD database is searched for the data based on the entered name
            else:
                name_list_2, FU_node, combined_list, unit_list = search_by_keyword_data(name_2, self.data_node_1, target_module, print_url, print_data, self.headers, self.params_2, print_ep_data)
                quantity = float(material_data['quantity'])
                unit = material_data['unit']
            
            #check for the unit of the quanties and calls the correct function accordingly; appends the resulting data to the final dictionairy
            if unit == 'm3':
                multiplied_volume = multiply_volume(combined_list, FU_node, quantity)
                for entry in multiplied_volume:
                    entry['value'] = float(entry['value'])
                self.LCA_result_dict = append_final_dict(LCA_dict, stage, name_2, multiplied_volume)
            elif unit == 'm2':
                multiplied_area = multiply_volume(combined_list, FU_node, quantity)
                for entry in multiplied_area:
                    entry['value'] = float(entry['value'])
                self.LCA_result_dict = append_final_dict(LCA_dict, stage, name_2, multiplied_area)
            elif unit == 'kg':
                multiplied_weight = multiply_weight(combined_list, FU_node, quantity)
                for entry in multiplied_weight:
                    entry['value'] = float(entry['value'])
                self.LCA_result_dict = append_final_dict(LCA_dict, stage, name_2, multiplied_weight)
            else:
                print('no unit found')
        
        
        #Filter out the data attached to impact catagories that don't occur for every material
        
        #Replace GWP with GWP-total for the materials that only contain GWP --> for future merging and overall consistency
        self.LCA_result_dict = replace_GWP_GWPtotal(self.LCA_result_dict)
        
        self.LCA_result_dict = filter_impact_categories(self.LCA_result_dict)

        #Divide the values in the LCA results dictionairy by the entered surface area of the sandwich element
        self.LCA_result_dict = divide_values_by_surface(self.LCA_result_dict, stage, self.surface_setting_window.square_meters)
        
        abr = 'GWP-total'
        plot_material_impact_stage_bar_chart(abr, stage, self.LCA_result_dict)
        return all_names
    
    #Function that opens the hopper capacity window for A3
    def show_hopper_capacity_window(self):
        self.hoppercapacity = HopperCapacityWindow()
        self.hoppercapacity.show()
    
    #Function that opens the mold reuse factor window
    def show_mould_reuse_window(self):
        self.mould_reuse_window = MouldReuseWindow()
        self.mould_reuse_window.show()

    #Function that opens the surface and lifespanc selection window
    def show_surface_settings_window(self):
        self.surface_setting_window = SquareMeterWindow()
        self.surface_setting_window.show()

    #Function that open the emission factor window for A2
    def show_transport_emission_window(self):
        self.transport_emission_window = EmissionFactorsWindow()
        self.transport_emission_window.show()

    #Function that opens the emission factor window for A3
    def show_process_emission_window(self):
        self.processFactors = EmissionFactorsWindow_A3()
        self.processFactors.show()
        
    #Function that opens the Import selection window        
    def show_import_selection_window(self): 
        # Pass self.selected_file to the ImportSelectionWindow constructor
        self.import_selection_window = ImportSelectionWindow(self.selected_file)
        self.import_selection_window.show()
        self.import_selection_window.dataProcessed.connect(self.handle_IFC_data)
    
    #Function that allows for the importing of and excel file and the extraction of the data in the correct format 
    def import_and_process_excel(self): 
        # Open file dialog for Excel files
        file_dialog = QFileDialog(self, "Open Excel Files", "", "Excel Files (*.xlsx;*.xls);;All Files (*)")
        #Ensure that selection of multiple files is enabled
        file_dialog.setFileMode(QFileDialog.ExistingFiles)  # Allow selecting multiple files
        if file_dialog.exec_() == QFileDialog.Accepted:
            file_paths = file_dialog.selectedFiles()
            print(f"Importing Excel files: {file_paths}")

            for file_path in file_paths:
                df = pd.read_excel(file_path)
                environmental_data_manual, material_name_manual, functional_unit_manual = import_excel_data(df) 
                self.imported_names.append(material_name_manual)
                self.imported_env_data.append(environmental_data_manual)
                self.imported_FU.append(functional_unit_manual)
 
    #Function that opens the dialog box in which the valid_year for the API connection can be set manually
    def show_eco_settings_dialog(self): 
        
        dialog = Eco_settingsDialog()
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            self.valid_until = dialog.valid_until_spinbox.value()
            print(f"Valid until year set to: {self.valid_until}")

            self.data_node_1 = connect_node_1(self.headers, self.params, self.valid_until)
    
    #Function that places the data extracted from the .ifc file into the line edit boxes
    def handle_IFC_data(self, result_ifc_ins, result_ifc_inner_con, result_ifc_inner_rebar, result_ifc_outer_con, result_ifc_outer_rebar): 
        if result_ifc_ins is not None:
            self.lineEdit_quantity_ins.setText(str(result_ifc_ins))
            self.lineEdit_matpro_ins.setText('Insulation material --> use EPD search to define')
            self.comboBox_unit_ins.setCurrentIndex(0)
        if result_ifc_inner_con is not None:
            self.lineEdit_quantity_inner.setText(str(result_ifc_inner_con))
            self.lineEdit_matpro_inner.setText('Concrete --> use EPD search to define')
            self.comboBox_unit_inner.setCurrentIndex(0)
        if result_ifc_inner_rebar is not None:
            self.add_line_inner()
            self.lineEdit_quantity_inner.setText(str(result_ifc_inner_rebar))
            self.lineEdit_matpro_inner.setText('Rebar --> use EPD search to define')
            self.comboBox_unit_inner.setCurrentIndex(1)
        if result_ifc_outer_con is not None:
            self.lineEdit_quantity_outer.setText(str(result_ifc_outer_con))
            self.lineEdit_matpro_outer.setText('Concrete --> use EPD search to define')
            self.comboBox_unit_outer.setCurrentIndex(0)
        if result_ifc_outer_rebar is not None:
            self.add_line_outer()
            self.lineEdit_quantity_outer.setText(str(result_ifc_outer_rebar))
            self.lineEdit_matpro_outer.setText('Rebar --> use EPD search to define')
            self.comboBox_unit_outer.setCurrentIndex(1)

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    icon = QIcon
    MainWindow.setWindowIcon(icon)
    MainWindow.show()
    app.exec_()

