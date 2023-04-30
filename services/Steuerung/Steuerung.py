# Autor: Alwin Zomotor

from services.Import.Datamodel import Person, Statistik, Raum


class Steuerung:

    def __init__(self, raum: Raum):
        self.states = {"running": 0, "paused": 1, "stopped": 2}
        self.raum = raum
        self.state = self.states["paused"]
        self.personen = raum.personen
        self.tisch = raum.tisch
        self.current_guest = self.personen[0]

    def one_guest(self):
        pass

    def all_guests(self):
        pass

    def start_simulation(self):
        self.state = self.states["running"]
        while self.state is self.states["running"]:
            for person in self.personen:
                panikfaktor = self.__calculate_panic_factor(person, self.personen, self.tisch)
                person.set_panikfaktor(panikfaktor)
                person.move()
            self.__check_collision()
            self.raum.update()
        pass

    def pause_simulation(self):
        self.state = self.states["paused"]
        pass

    def __calculate_panic_factor(self, person: Person, personen: [Person], tisch: [tuple[int, int]]) -> float:
        panikfaktor = 0.0
        abstand = 0.0
        for p in personen:
            if p in personen:
                continue
            wunschabstand = person.wunschabstaende[p.id]
            abstand = self.__calc_distance(person.position, p.position)
            panikfaktor += self.__panikfaktor_metrik(abstand, wunschabstand)
        for t in tisch:
            temp_abstand = self.__calc_distance(person.position, t)
            abstand = temp_abstand if temp_abstand < abstand else abstand
        panikfaktor += self.__panikfaktor_metrik(abstand, 0)
        return panikfaktor

    def __panikfaktor_metrik(self, abstand: float, wunschabstand: float) -> float:
        return 0.0

    def __calc_distance(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
        # wurzel a quadrat + b quadrat = c quadrat --> Pythagoras
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def __check_collision(self):
        pass
