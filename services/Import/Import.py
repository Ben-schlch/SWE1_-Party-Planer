import json
import sys, os
from services.Import.Datamodel import Raum, Person


def importJson(data):
    #create persons
    personlist = []
    for p in data['Personen']:
        wunschabstaede = {}

        for l in data['Wunschabstaende']:
            if(l['person1_id'] == p['id']):
                wunschabstaede[l['person2_id']] = float(l['wunschabstand'])
        position = (int(p['startposition'][0]), int(p['startposition'][1]))
        tmp = Person(p['id'], p['name'], wunschabstaede, position)
        #print(p['id'], p['name'], wunschabstaede, p['startposition'])
        personlist.append(tmp)


    #create room
    raum = data['Spielfeld']
    raumgroesse = (int(raum['raum_breite']), int(raum['raum_hoehe']))

    tisch = []

    for i in range(int(raum['tisch_breite'])):
        for j in range(int(raum['tisch_hoehe'])):
           tisch.append((int(raum['tisch_x'])+i, int(raum['tisch_y'])+j))
    #print(raumgroesse, tisch)
    return Raum(raumgroesse, personlist, tisch)
