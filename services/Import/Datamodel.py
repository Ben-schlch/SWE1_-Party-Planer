import random

from PyQt5.QtCore import pyqtSignal, QObject


class Person:
    def __init__(self, id_person: int, name: str, wunschabstaende: list[float], startposition: tuple[int, int],
                 panikfaktor: float = 0):  # wunschabstaende: list[float],
        self.id = id_person
        self.name = name
        self.wunschabstaende = wunschabstaende
        self.position = startposition
        self.panikfaktor = panikfaktor
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def move_person(self, newposition: tuple[int, int]):
        self.position = newposition

    def save_panicfaktor(self, panikfaktor: float):
        self.panikfaktor = panikfaktor


class Raum(QObject):
    signalRaum = pyqtSignal()
    def __init__(self, groesse: tuple[int, int], personen: list[Person], tisch: list[tuple[int, int]]):
        super().__init__()

        self.groesse = groesse
        self.personen = personen
        self.tisch = tisch

    def change_position(self, id_person: int, newposition: tuple[int, int]):
        for person in self.personen:
            if person.id == id_person:
                person.position = newposition
                return
        self.signalRaum.emit()


class Statistik(QObject):
    '''
    Klasse zur Speicherung der Statistiken mit Array aus [(Name, color, [Panikfaktor1, Panikfaktor2,...])]
    '''
    signalPanicfactor = pyqtSignal()

    def __init__(self, personen: list[Person]):
        super().__init__()
        self.statistik = {}
        for person in personen:
            self.statistik[person.id] = (person.name, person.color, [])
        self.panik_history_avg = []

    def get_person_id_with_certain_panik_history_length(self, length: int) -> list[int]:
        return [person[0] for person in self.statistik.items() if len(person[1][2]) == length]

    def save_panicfaktor(self, id_person: int, panikfaktor: float):
        self.statistik[id_person][2].append(panikfaktor)
        amount_panik_history = len(self.statistik[id_person][2])
        part_of_average = self.get_person_id_with_certain_panik_history_length(amount_panik_history)

        avg = sum([self.statistik.get(p)[2][amount_panik_history - 1] for p in part_of_average]) / len(part_of_average)
        try:
            self.panik_history_avg[amount_panik_history - 1] = avg
        except IndexError:
            self.panik_history_avg.append(avg)

        self.signalPanicfactor.emit()
