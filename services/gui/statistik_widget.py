import sys

from services.Import.Datamodel import Raum, Statistik, Person
from PyQt5.QtGui import QColor, QFont
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from typing import List
from collections import defaultdict


class StatistikWidget(QWidget):
    def __init__(self, statistik):
        super().__init__()
        self.statistik = statistik

        # Set up the graph
        self.graph = pg.PlotWidget()
        self.graph.setBackground('w')
        self.graph.showGrid(x=True, y=True)
        self.graph.setLabel('left', 'Panikfaktor')
        self.graph.setLabel('bottom', 'Iterationen')
        self.graph.setLimits(xMin=0, xMax=1000, yMin=0, yMax=100)
        self.graph.addLegend()

        x_ticks = [(i, str(i)) for i in range(0, 1001, 1)]
        self.graph.getAxis('bottom').setTicks([x_ticks])

        pen_width = round(self.width() / 150)

        self.avg_line = self.graph.plot(statistik.panik_history_avg, name="Average",
                                        pen=pg.mkPen(QColor(0, 0, 0), width=pen_width * 3))

        # Create a line for each person's panik factors
        for person_id, (name, color, panik_history) in self.statistik.statistik.items():
            pen = pg.mkPen(color, width=pen_width)
            self.graph.plot(panik_history, name=f"{id}  {name}", pen=pen)

        # Panik value
        self.value_label = QLabel()
        self.value_label.setText(f"Aktueller Panik average: {self.statistik.panik_history_avg[-1]}")
        self.font = QFont()
        self.font.setPointSize(round(self.height() / 75))
        self.value_label.setFont(self.font)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.graph)
        layout.addWidget(self.value_label)

        self.setLayout(layout)

        # Connect signal to update graph
        self.statistik.signalPanicfactor.connect(self.update_graph)

    def update_graph(self):
        # Update average line data
        self.avg_line.setData(self.statistik.panik_history_avg)

        # Update person lines data
        for person_id, (name, color, panik_history) in self.statistik.statistik.items():
            self.data[person_id].setData(panik_history)

        # Rescale the graph to fit the new data
        self.graph.autoRange()

    def resizeEvent(self, event):
        self.font.setPointSize(round(self.height() / 75))
        self.value_label.setFont(self.font)
        self.update()
