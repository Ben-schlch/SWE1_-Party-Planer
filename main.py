import sys

from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication, QMessageBox, QStackedWidget

from services.gui.config_gui import ConfigWindow
from services.gui.simulation_gui import SimulationWindow
from services.Import.Import import importJson

def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()

    config_window = ConfigWindow()
    stack.addWidget(config_window)
    stack.show()

    while True:
        # Create a QEventLoop to wait for the signal to be emitted
        loop = QEventLoop()
        config_window.json_ready.connect(loop.quit)
        # Start the event loop and wait for the signal to be emitted
        try:
            loop.exec_()

            data = config_window.get_json()
            raum = importJson(data)
            # If the importJson call succeeds without raising any errors,
            # break out of the loop and continue with the rest of the program
            break
        except Exception as e:
            # If an error is raised during the importJson call, display the error
            # message and retry the loop
            print(f"Error starting JSON")
            error_message_box = QMessageBox()
            error_message_box.setIcon(QMessageBox.Critical)
            error_message_box.setWindowTitle("Error")
            error_message_box.setText("An error occurred while importing JSON. Try again!")
            error_message_box.exec_()

    simulation_window = SimulationWindow(raum)
    stack.addWidget(simulation_window)

    # Switch to the simulation window
    stack.setCurrentWidget(simulation_window)

    stack.show()
    sys.exit(app.exec_())


main()
