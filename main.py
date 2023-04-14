import PySimpleGUI as sg
import os.path
import json
from services.gui.config_gui import gui_config_loop


def main():
    board = gui_config_loop()
    # TODO:
    # 1. Create a new window with the board
    # 2. create a window with the statistics


main()
