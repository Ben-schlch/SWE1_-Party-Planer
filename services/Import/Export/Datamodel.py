class Person():
    def __init__(self, id_person: int, name: str,  wunschabstaende: list[float], startposition: tuple[int, int], panikfaktor: float = 0):    #wunschabstaende: list[float], 
        self.id = id_person
        self.name = name
        self.wunschabstaende = wunschabstaende
        self.position = startposition
        self.panikfaktor = panikfaktor


    def move_person(self, newposition: tuple[int, int]):
        self.position = newposition

    def save_panicfaktor(self, panikfaktor: float):
        self.panikfaktor = panikfaktor


class Raum():
    def __init__(self, groesse: tuple[int, int], personen: list[Person], tisch: list[tuple[int, int]]):
        self.groesse = groesse
        self.personen = personen
        self.tisch = tisch
