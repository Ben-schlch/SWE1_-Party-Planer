from math import floor

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, \
    QSplitter

from services.Import.Datamodel import Raum, Statistik, Person
from services.gui.statistik_widget import StatistikWidget


class RoomWidget(QWidget):

    def __init__(self, raum: Raum):
        super().__init__()
        self.setContentsMargins(5, 5, 5, 5)
        self.raum = raum

        #connect to the object and change widget on object changes
        self.raum.signalRaum.connect(self.updateWidget)


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
        qp.setPen(QPen(Qt.black, max(tile_size / 20, 2), Qt.SolidLine))
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
            color = QColor(person.color[0], person.color[1], person.color[2])
            opposite_color = QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())
            qp.setBrush(color)
            qp.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            x, y = person.position
            qp.drawEllipse(x * tile_size + 3, y * tile_size + 3, tile_size - 6, tile_size - 6)
            qp.setFont(QFont('Decorative', floor(tile_size * 2 / 7)))
            qp.setPen(QPen(opposite_color, 2, Qt.SolidLine))
            qp.drawText(x * tile_size + floor(tile_size / 5),
                        y * tile_size + floor(tile_size / 2) + floor(tile_size / 5),
                        person.name[0].upper() + str(person.id))

    def resizeEvent(self, event):
        size = self.size()
        height = size.height()
        width = size.width()
        if height - 10 < width:
            new_size = QSize(height, height)
            self.resize(new_size)
        elif width - 10 < height:
            new_size = QSize(width, width)
            self.resize(new_size)
        self.update()

    def updateWidget(self):
        self.update()


class SimulationWindow(QMainWindow):

    def __init__(self, raum, stack, config_window):
        super().__init__()
        self.stack = stack
        self.config_window = config_window
        self.centralWidget = QWidget()
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Party Simulation:")

        # add a new widget to contain the splitter
        splitter_widget = QWidget(self.centralWidget)
        splitter_layout = QVBoxLayout(splitter_widget)
        self.layout.addWidget(splitter_widget)

        self.splitter = QSplitter(Qt.Horizontal)

        # add left and right to splitter
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        self.splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        self.splitter.addWidget(right_widget)

        # add frame with vertical line between left and right widgets
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet("QSplitter::handle {background-color: #000000;}")
        splitter_layout.addWidget(self.splitter)

        self.splitter.setSizes([self.width() // 2, self.width() // 2])

        # Create RoomWidget and add to left side
        # put the room_widget in the middle of the left widget
        self.room_widget = RoomWidget(raum)
        left_layout.addWidget(self.room_widget)
        self.statistik_widget = StatistikWidget(statisitk)  # todo: replace with real statistik object you get
        right_layout.addWidget(self.statistik_widget)


        # Add a spacer to center the widget

        # Create buttons
        self.simulationbuttons = QHBoxLayout()
        left_layout.addLayout(self.simulationbuttons)
        button_heigth = self.height() // 20
        self.play_button = QPushButton(QIcon(r'C:\Users\bensc\Projects\swe\SWE1_-Party-Planer\data\play.png'), "Play",
                                       self)
        self.play_button.setMinimumHeight(button_heigth)
        self.simulationbuttons.addWidget(self.play_button)
        self.pause_button = QPushButton(QIcon(r'C:\Users\bensc\Projects\swe\SWE1_-Party-Planer\data\pause.png'),
                                        "Pause", self)
        self.pause_button.setMinimumHeight(button_heigth)
        self.simulationbuttons.addWidget(self.pause_button)
        self.iterate_button = QPushButton(QIcon(r'C:\Users\bensc\Projects\swe\SWE1_-Party-Planer\data\iterate.png'),
                                          "Iterate", self)
        self.iterate_button.setMinimumHeight(button_heigth)
        self.simulationbuttons.addWidget(self.iterate_button)
        self.guestiterate_button = QPushButton(
            QIcon(r'C:\Users\bensc\Projects\swe\SWE1_-Party-Planer\data\guestiterate.png'), "Guestiterate", self)
        self.guestiterate_button.setMinimumHeight(button_heigth)
        self.simulationbuttons.addWidget(self.guestiterate_button)

        # Return to config button on right side
        self.return_to_config = QPushButton("Zurück zur Config", self)
        self.return_to_config.setMinimumHeight(button_heigth)

        self.return_to_config.clicked.connect(self.show_config_window)
        right_layout.addWidget(self.return_to_config)

    def show_config_window(self):
        self.stack.setCurrentWidget(self.config_window)

        def resizeEvent(event):
            self.splitter.setSizes([self.width() // 2, self.width() // 2])
            self.room_widget.resizeEvent(event)
            new_button_height = self.parent().height() // 10
            self.play_button.setMinimumHeight(new_button_height)
            self.pause_button.setMinimumHeight(new_button_height)
            self.iterate_button.setMinimumHeight(new_button_height)
            self.guestiterate_button.setMinimumHeight(new_button_height)
            self.return_to_config.setMinimumHeight(new_button_height)

        self.resizeEvent = resizeEvent


personen = [Person(1, "Max", [1.5, 1.5, 1.5], (0, 0), 0), Person(2, "Moritz", [1.5, 1.5, 1.5], (1, 1), 0),
            Person(3, "Maximilian", [1.5, 1.5, 1.5], (9, 9), 0)]
# raum = Raum((10, 10), personen, [(5, 5), (5, 6), (6, 5), (6, 6)])
#
# app = QApplication([])
# window = SimulationWindow(raum)
# window.show()
# app.exec_()

statisitk = Statistik(personen)
statisitk.save_panicfaktor(1, 1)
statisitk.save_panicfaktor(2, 2)
statisitk.save_panicfaktor(3, 3)
statisitk.save_panicfaktor(1, 4)
statisitk.save_panicfaktor(2, 5)
statisitk.save_panicfaktor(3, 6)
statisitk.save_panicfaktor(1, 7)
statisitk.save_panicfaktor(2, 2)
statisitk.save_panicfaktor(3, 3)
statisitk.save_panicfaktor(1, 4)
