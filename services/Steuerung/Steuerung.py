# Autor: Alwin Zomotor
from time import sleep

from services.Import.Datamodel import Person, Statistik, Raum


class Steuerung:

    def __init__(self, raum: Raum):
        self.states = {"running": 0, "paused": 1, "stopped": 2}
        self.raum = raum
        self.state = self.states["paused"]
        self.personen = raum.personen
        self.tisch = raum.tisch
        self.current_guest = 0
        self.guest_list_size = len(self.personen)

    def one_guest(self, simulation=False):
        """
        Bewegt die nächste Person
        :param simulation: True, wenn die Funktion aus der Simulation aufgerufen wird.
        False, wenn die Funktion aus der GUI aufgerufen wird.
        Die Funktion darf nicht aus der GUI aufgerufen werden, während die Simulation läuft.
        """
        if not simulation and self.state is self.states["running"]:
            return
        if self.current_guest == self.guest_list_size:
            self.current_guest = 0
        person = self.personen[self.current_guest]
        self.current_guest += 1
        positions = self.__get_adjacent_positions(person)
        position, panikfaktor = self.__get_best_position(person, positions)
        person.save_panicfaktor(panikfaktor)
        person.move_person(position)

    def all_guests(self, simulation=False):
        """
        Bewegt alle Personen.
        :param simulation: True, wenn die Funktion aus der Simulation aufgerufen wird.
        False, wenn die Funktion aus der GUI aufgerufen wird.
        Die Funktion darf nicht aus der GUI aufgerufen werden, während die Simulation läuft.
        """
        if not simulation and self.state is self.states["running"]:
            return
        for p in self.personen:
            self.one_guest()
        pass

    def start_simulation(self):
        """
        Startet die Simulation.
        """
        self.state = self.states["running"]
        while self.state is self.states["running"]:
            self.all_guests(True)
            sleep(0.5)

    def pause_simulation(self):
        """
        Pausiert die Simulation
        """
        self.state = self.states["paused"]

    def stop_simulation(self):
        """
        Stoppt die Simulation
        """
        self.state = self.states["stopped"]
        statistic = Statistik(self.personen)
        return statistic

    def __calculate_panic_factor(self, person: Person, position: tuple[int, int]) -> float:
        """
        Berechnet den Panikfaktor einer Person anhand des Abstandes zu anderen Personen und dem Wunschabstand
        :param person: Person, deren Panikfaktor berechnet werden soll.
        :return: Panikfaktor der Person
        """
        panikfaktor = 0.0
        abstand = 0.0
        for p in self.personen:
            if p == person:
                continue
            wunschabstand = person.wunschabstaende[p.id]
            abstand = self.__calc_distance(position, p.position)
            panikfaktor += self.__panikfaktor_metrik(abstand, wunschabstand)
        for t in self.tisch:
            temp_abstand = self.__calc_distance(position, t)
            abstand = temp_abstand if temp_abstand < abstand else abstand
        panikfaktor += self.__panikfaktor_metrik(abstand, 0)
        return panikfaktor

    @staticmethod
    def __panikfaktor_metrik(abstand: float, wunschabstand: float) -> float:
        """
        Berechnet den Panikfaktor einer Person anhand des Abstandes zu anderen Personen und dem Wunschabstand
        mit beschränktem Wachstum.
        :param abstand: aktueller Abstand zu einer anderen Person
        :param wunschabstand: Wunschabstand zu einer anderen Person
        :return: Panikfaktor (min 0; max 10)
        """
        obere_schranke = 10
        untere_schranke = 0
        return obere_schranke - ((obere_schranke - untere_schranke) / (1 + (abstand - wunschabstand) ** 2))

    @staticmethod
    def __calc_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
        """
        Berechnet den Abstand zwischen zwei Punkten.
        :param pos1: Position 1
        :param pos2: Position 2
        :return: Abstand zwischen den beiden Punkten
        """
        # wurzel a quadrat + b quadrat = c quadrat --> Pythagoras
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def __check_collision(self, person: Person) -> bool:
        """
        Prüft, ob eine Person mit einer anderen Person oder einem Tisch kollidiert.
        :param person: Person, die geprüft werden soll
        :return: True, wenn Kollision vorliegt, sonst False
        """
        for p in self.personen:
            if p == person:
                continue
            if person.position == p.position:
                return True
        if person.position in self.tisch:
            return True
        return False

    def __get_adjacent_positions(self, person: Person) -> list[tuple[int, int]]:
        """
        Gibt alle Positionen zurück, die direkt an einer Person liegen.
        :return: Liste mit allen Positionen, die direkt an einer Person liegen
        """
        adjacent_positions = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.__check_collision(person):
                    continue
                adjacent_positions.append((person.position[0] + i, person.position[1] + j))
        return adjacent_positions

    def __get_best_position(self, person: Person, positions: list[tuple[int, int]]) -> tuple[tuple[int, int], float]:
        """
        Gibt die beste Position zurück, die eine Person einnehmen kann.
        :param person: Person, die eine Position einnehmen soll.
        :param positions: Liste mit allen Positionen, die die Person einnehmen kann.
        :return: Beste Position, die die Person einnehmen kann und der Panikfaktor.
        """
        panikfaktor = 10.0
        position = (0, 0)
        for pos in positions:
            panikfaktor_temp = self.__calculate_panic_factor(person, pos)
            panikfaktor, position = panikfaktor_temp, pos if panikfaktor_temp < panikfaktor else panikfaktor
        return position, panikfaktor
