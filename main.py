import sys

from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication

from services.gui.config_gui import ConfigWindow
from services.gui.simulation_gui import SimulationWindow

def main():
    app = QApplication(sys.argv)
    config_window = ConfigWindow()
    config_window.show()

    # Create a QEventLoop to wait for the signal to be emitted
    loop = QEventLoop()
    config_window.json_ready.connect(loop.quit)
    # Start the event loop and wait for the signal to be emitted
    loop.exec_()

    data = config_window.get_json()
    print(data)

    simulation_window = SimulationWindow(data)
    simulation_window.show()
    # TODO:
    # 1. Create a new window with the room (simulation)
    # 2. create a window with the statistics


main()
