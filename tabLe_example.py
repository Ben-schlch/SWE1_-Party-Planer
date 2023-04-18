class Personen:
    def __init__(self, id_person: int, name: str, wunschabstaende: list[float],  # index of list is id of a person
                 startposition: tuple[int, int], panikfaktor: float):
        self.id = id_person
        self.name = name
        self.wunschabstaende = wunschabstaende
        self.startposition = startposition
        self.panikfaktor = panikfaktor


class Raum:
    def __init__(self, groesse: tuple[int, int], personen: list[Personen], tisch: list[tuple[int, int]]):
        self.groesse = groesse
        self.personen = personen
        self.tisch = tisch
