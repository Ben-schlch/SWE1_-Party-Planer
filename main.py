import sys

from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication, QMessageBox, QStackedWidget

from services.gui.config_gui import ConfigWindow
from services.gui.simulation_gui import SimulationWindow
from services.Import.Import import importJson

def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()

    config_window = ConfigWindow(stack)
    stack.addWidget(config_window)
    stack.show()

    sys.exit(app.exec_())


main()
