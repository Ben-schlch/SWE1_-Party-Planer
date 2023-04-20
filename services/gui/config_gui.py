import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QWidget, QPushButton, QHBoxLayout, QHeaderView, QMessageBox
from PyQt5.QtCore import *

from services.gui.simulation_gui import SimulationWindow
from services.Import.Import import importJson

# noinspection PyUnresolvedReferences
class ConfigWindow(QMainWindow):
    json_ready = pyqtSignal(str)

    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        # Set the window title
        self.setWindowTitle("JSON Viewer")

        # Set up the main widget and layout
        self.centralWidget = QWidget()
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        # Create a file selection button
        self.fileButton = QPushButton("Select JSON File")
        self.fileButton.clicked.connect(self.loadJsonFile)
        self.layout.addWidget(self.fileButton)

        self.jsonbuttons = QHBoxLayout()
        self.layout.addLayout(self.jsonbuttons)

        # Create a button to load the JSON file
        self.loadButton = QPushButton("Load JSON File", self)
        self.loadButton.clicked.connect(self.loadJsonData)
        self.jsonbuttons.addWidget(self.loadButton)

        self.exportButton = QPushButton("Export Data to JSON File", self)
        self.exportButton.clicked.connect(self.exportJson)
        self.jsonbuttons.addWidget(self.exportButton)

        # Create a layout to hold the tables for Personen and Wunschabstaende
        self.tablesLayout = QHBoxLayout()
        self.layout.addLayout(self.tablesLayout)

        # Create three tables for the Personen, Wunschabstaende, and Einstellungen
        # Create the Personen table
        self.personenTable = QTableWidget()
        self.personenTable.setColumnCount(4)
        self.personenTable.setHorizontalHeaderLabels(["ID", "Name", "Startposition x", "Startposition y"])
        self.personenTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tablesLayout.addWidget(self.personenTable)

        # Create the Wunschabstaende table
        self.wunschabstaendeTable = QTableWidget()
        self.wunschabstaendeTable.setColumnCount(3)
        self.wunschabstaendeTable.setHorizontalHeaderLabels(["Person 1 ID", "Person 2 ID", "Wunschabstand"])
        self.wunschabstaendeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablesLayout.addWidget(self.wunschabstaendeTable)

        self.addrowLayout = QHBoxLayout()
        self.layout.addLayout(self.addrowLayout)

        # Create a button to add a row to the Personen table
        self.addRowPersonenButton = QPushButton("Add Row to Personen Table")
        self.addRowPersonenButton.clicked.connect(self.addRowPersonen)
        self.addrowLayout.addWidget(self.addRowPersonenButton)

        # Create a button to add a row to the Wunschabstaende table
        self.addRowWunschabstaendeButton = QPushButton("Add Row to Wunschabstaende Table")
        self.addRowWunschabstaendeButton.clicked.connect(self.addRowWunschabstaende)
        self.addrowLayout.addWidget(self.addRowWunschabstaendeButton)

        self.einstellungenTable = QTableWidget()
        self.einstellungenTable.setColumnCount(2)
        self.einstellungenTable.setHorizontalHeaderLabels(["Setting", "Value"])
        self.einstellungenTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.einstellungenTable)

        self.startSimulationButton = QPushButton("Starte die Simulation")
        self.startSimulationButton.clicked.connect(self.startSimulation)
        self.layout.addWidget(self.startSimulationButton)

    def loadJsonFile(self):
        # Open a file dialog to select a JSON file
        filename, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")

        if filename:
            self.json_filename = filename

    def loadJsonData(self):
        # Load the JSON data from the file
        try:
            with open(self.json_filename, "r") as file:
                data = json.load(file)

            # Populate the Personen table
            self.personenTable.setRowCount(len(data["Personen"]))
            for i, person in enumerate(data["Personen"]):
                self.personenTable.setItem(i, 0, QTableWidgetItem(str(person["id"])))
                self.personenTable.setItem(i, 1, QTableWidgetItem(person["name"]))
                x_y = person["startposition"]
                self.personenTable.setItem(i, 2, QTableWidgetItem(str(x_y[0])))
                self.personenTable.setItem(i, 3, QTableWidgetItem(str(x_y[1])))
            # Populate the Wunschabstaende table
            self.wunschabstaendeTable.setRowCount(len(data["Wunschabstaende"]))
            for i, wunsch in enumerate(data["Wunschabstaende"]):
                self.wunschabstaendeTable.setItem(i, 0, QTableWidgetItem(str(wunsch["person1_id"])))
                self.wunschabstaendeTable.setItem(i, 1, QTableWidgetItem(str(wunsch["person2_id"])))
                self.wunschabstaendeTable.setItem(i, 2, QTableWidgetItem(str(wunsch["wunschabstand"])))

            # Populate the Einstellungen table
            self.einstellungenTable.setRowCount(len(data["Spielfeld"]) + 1)
            self.einstellungenTable.setItem(0, 0, QTableWidgetItem("Iterationen"))
            self.einstellungenTable.setItem(0, 1, QTableWidgetItem(str(data["Spielfeld"]["Iterationen"])))
            for i, (setting, value) in enumerate(data["Spielfeld"].items()):
                self.einstellungenTable.setItem(i + 1, 0, QTableWidgetItem(setting))
                self.einstellungenTable.setItem(i + 1, 1, QTableWidgetItem(str(value)))
        except:
            print("Error loading JSON file")
            error_message_box = QMessageBox()
            error_message_box.setIcon(QMessageBox.Critical)
            error_message_box.setWindowTitle("Error")
            error_message_box.setText("An error occurred while loading JSON. Try again!")
            error_message_box.exec_()

    def exportJson(self):
        try:
            # Create a dictionary to store the config data
            config = self.createjson()

            # Write the config dictionary to a file
            filename, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "", "JSON Files (*.json)")
            if filename:
                with open(filename, "w") as file:
                    json.dump(config, file, indent=4)
        except:
            print("Error storing JSON file")
            error_message_box = QMessageBox()
            error_message_box.setIcon(QMessageBox.Critical)
            error_message_box.setWindowTitle("Error")
            error_message_box.setText("An error occurred while loading JSON. Try again!")
            error_message_box.exec_()

    def createjson(self):
        config = {}

        # Add the Personen table data to the config dictionary
        personen_data = []
        for row in range(self.personenTable.rowCount()):
            id_item = self.personenTable.item(row, 0)
            name_item = self.personenTable.item(row, 1)
            x_item = self.personenTable.item(row, 2)
            y_item = self.personenTable.item(row, 3)
            if id_item is not None and name_item is not None and x_item is not None and y_item is not None:
                person = {
                    "id": id_item.text(),
                    "name": name_item.text(),
                    "startposition": [x_item.text(), y_item.text()]
                }
                personen_data.append(person)
        config["Personen"] = personen_data

        # Add the Wunschabstaende table data to the config dictionary
        wunschabstaende_data = []
        for row in range(self.wunschabstaendeTable.rowCount()):
            person1_id_item = self.wunschabstaendeTable.item(row, 0)
            person2_id_item = self.wunschabstaendeTable.item(row, 1)
            wunschabstand_item = self.wunschabstaendeTable.item(row, 2)
            if person1_id_item is not None and person2_id_item is not None and wunschabstand_item is not None:
                wunschabstand = {
                    "person1_id": person1_id_item.text(),
                    "person2_id": person2_id_item.text(),
                    "wunschabstand": wunschabstand_item.text()
                }
                wunschabstaende_data.append(wunschabstand)
        config["Wunschabstaende"] = wunschabstaende_data

        # Add the Einstellungen table data to the config dictionary
        spielfeld_data = {}
        for row in range(self.einstellungenTable.rowCount()):
            setting_item = self.einstellungenTable.item(row, 0)
            value_item = self.einstellungenTable.item(row, 1)
            if setting_item is not None and value_item is not None:
                spielfeld_data[setting_item.text()] = value_item.text()
        config["Spielfeld"] = spielfeld_data

        return config


    def addRowWunschabstaende(self):
        # Get the current row count of the table
        rowCount = self.wunschabstaendeTable.rowCount()
        # Add a new row to the table
        self.wunschabstaendeTable.insertRow(rowCount)

        # Set default values for the new row
        self.wunschabstaendeTable.setItem(rowCount, 0, QTableWidgetItem(""))
        self.wunschabstaendeTable.setItem(rowCount, 1, QTableWidgetItem(""))
        self.wunschabstaendeTable.setItem(rowCount, 2, QTableWidgetItem(""))

    def addRowPersonen(self):
        # Get the current row count and add a new row
        currentRowCount = self.personenTable.rowCount()
        self.personenTable.insertRow(currentRowCount)

        # Set default values for the new row
        self.personenTable.setItem(currentRowCount, 0, QTableWidgetItem(str(currentRowCount + 1)))
        self.personenTable.setItem(currentRowCount, 1, QTableWidgetItem(""))
        self.personenTable.setItem(currentRowCount, 2, QTableWidgetItem("0"))
        self.personenTable.setItem(currentRowCount, 3, QTableWidgetItem("0"))

    def startSimulation(self):

        data = self.get_json()
        raum = importJson(data)
        simulation_window = SimulationWindow(raum, self.stack, self)
        self.stack.addWidget(simulation_window)
        self.stack.setCurrentWidget(simulation_window)

    def get_json(self):
        jsondata = self.createjson()
        return jsondata

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ConfigWindow()
#     window.show()
#     window = ConfigWindow()
#     window.show()
#     sys.exit(app.exec_())
