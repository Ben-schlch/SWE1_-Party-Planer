from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, \
    QSizePolicy, QSplitter, QFrame, QSpacerItem
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from typing import List, Tuple
from random import randint
from math import floor


class RoomWidget(QWidget):

    def __init__(self, raum):
        super().__init__()
        self.setContentsMargins(5, 5, 5, 5)
        self.raum = raum
        self.person_colors = {}

    def calculate_tile_size(self):
        widget_width = self.width()
        number_of_tiles_x = self.raum.groesse[0]
        widget_width = widget_width - 20
        width_per_tile = round(widget_width / number_of_tiles_x)
        return width_per_tile

    def paintEvent(self, event):
        qp = QPainter(self)
        tile_size = self.calculate_tile_size()
        self.drawGrid(qp, tile_size)
        self.drawTables(qp, tile_size)
        self.drawPersons(qp, tile_size)

    def drawGrid(self, qp, tile_size):
        qp.setPen(QPen(Qt.black, max(tile_size/20, 2), Qt.SolidLine))
        for i in range(self.raum.groesse[0] + 1):
            qp.drawLine(i * tile_size, 0, round(i * tile_size), round(self.raum.groesse[1] * tile_size))
        for i in range(self.raum.groesse[1] + 1):
            qp.drawLine(0, i * tile_size, self.raum.groesse[0] * tile_size, i * tile_size)

    def drawTables(self, qp, tile_size):
        for x, y in self.raum.tisch:
            qp.setBrush(QColor(255, 200, 0))
            qp.drawRect(x * tile_size, y * tile_size, tile_size, tile_size)

    def drawPersons(self, qp, tile_size):
        for person in self.raum.personen:
            if person.id not in self.person_colors:
                color = QColor(randint(0, 255), randint(0, 255), randint(0, 255))
                self.person_colors[person.id] = color
            else:
                color = self.person_colors[person.id]
            opposite_color = QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())
            qp.setBrush(color)
            qp.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            x, y = person.position
            qp.drawEllipse(x * tile_size + 3, y * tile_size + 3, tile_size - 6, tile_size - 6)
            qp.setFont(QFont('Decorative', floor(tile_size * 2 / 7)))
            qp.setPen(QPen(opposite_color, 2, Qt.SolidLine))
            qp.drawText(x * tile_size + floor(tile_size / 5),
                        y * tile_size + floor(tile_size / 2) + floor(tile_size / 5),
                        person.name[0].upper()+str(person.id))

    def resizeEvent(self, event):
        size = self.size()
        height = size.height()
        width = size.width()
        if height -10 < width:
            new_size = QSize(height, height)
            self.resize(new_size)
        elif width -10 < height:
            new_size = QSize(width, width)
            self.resize(new_size)
        self.update()


class SimulationWindow(QMainWindow):

    def __init__(self, raum):
        super().__init__()
        self.centralWidget = QWidget()
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Party Simulation:")

        # add a new widget to contain the splitter
        splitter_widget = QWidget(self.centralWidget)
        splitter_layout = QVBoxLayout(splitter_widget)
        self.layout.addWidget(splitter_widget)

        splitter = QSplitter(Qt.Horizontal)

        # add left and right to splitter
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)

        # add frame with vertical line between left and right widgets
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle {background-color: #000000;}")
        splitter_layout.addWidget(splitter)

        splitter.setSizes([self.width() // 2, self.width() // 2])

        # Create RoomWidget and add to left side
        #put the room_widget in the middle of the left widget
        self.room_widget = RoomWidget(raum)
        left_layout.addWidget(self.room_widget)


        # Add a spacer to center the widget

        # Create buttons
        self.simulationbuttons = QHBoxLayout()
        left_layout.addLayout(self.simulationbuttons)
        button_heigth = self.height() // 20
        self.play_button = QPushButton(QIcon(r'C:\Users\bensc\Projects\swe\SWE1_-Party-Planer\data\play.png'), "", self)
        self.play_button.setMinimumHeight(button_heigth)
        self.simulationbuttons.addWidget(self.play_button)
        self.pause_button = QPushButton(QIcon(r'C:\Users\bensc\Projects\swe\SWE1_-Party-Planer\data\pause.png'), "", self)
        self.pause_button.setMinimumHeight(button_heigth)
        self.simulationbuttons.addWidget(self.pause_button)
        self.iterate_button = QPushButton(QIcon(r'C:\Users\bensc\Projects\swe\SWE1_-Party-Planer\data\iterate.png'), "", self)
        self.iterate_button.setMinimumHeight(button_heigth)
        self.simulationbuttons.addWidget(self.iterate_button)
        self.guestiterate_button = QPushButton(QIcon(r'C:\Users\bensc\Projects\swe\SWE1_-Party-Planer\data\guestiterate.png'), "", self)
        self.guestiterate_button.setMinimumHeight(button_heigth)
        self.simulationbuttons.addWidget(self.guestiterate_button)

        def resizeEvent(event):
            splitter.setSizes([self.width() // 2, self.width() // 2])
            self.room_widget.resizeEvent(event)
            new_button_height = self.height() // 10
            self.play_button.setMinimumHeight(new_button_height)
            self.pause_button.setMinimumHeight(new_button_height)
            self.iterate_button.setMinimumHeight(new_button_height)
            self.guestiterate_button.setMinimumHeight(new_button_height)

        self.resizeEvent = resizeEvent


class Person:
    def __init__(self, id_person: int, name: str, wunschabstaende: list[float],  # index of list is id of a person
                 startposition: tuple[int, int], panikfaktor: float = 0):
        self.id = id_person
        self.name = name
        self.wunschabstaende = wunschabstaende
        self.position = startposition
        self.panikfaktor = panikfaktor


class Raum:
    def __init__(self, groesse: tuple[int, int], personen: list[Person], tisch: list[tuple[int, int]]):
        self.groesse = groesse
        self.personen = personen
        self.tisch = tisch


personen = [Person(1, "Max", [1.5, 1.5, 1.5], (0, 0), 0), Person(2, "Moritz", [1.5, 1.5, 1.5], (1, 1), 0),
            Person(3, "Maximilian", [1.5, 1.5, 1.5], (9, 9), 0)]
raum = Raum((10, 10), personen, [(5, 5), (5, 6), (6, 5), (6, 6)])

app = QApplication([])
window = SimulationWindow(raum)
window.show()
app.exec_()
