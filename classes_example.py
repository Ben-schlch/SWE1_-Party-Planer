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


Personen = [Person(1, "Max", [1.5, 1.5, 1.5], (0, 0), 0), Person(2, "Moritz", [1.5, 1.5, 1.5], (1, 1), 0),
            Person(3, "Maximilian", [1.5, 1.5, 1.5], (5, 5), 0)]
Raum = Raum((10, 10), Personen, [(5, 5), (5, 6), (6, 5), (6, 6)])
