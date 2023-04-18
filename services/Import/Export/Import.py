import json
import sys, os
from Datamodel import Raum, Person


def importJson(jsonPath):
    with open(jsonPath) as f:
        data = json.load(f)
    
    #create persons
    personlist = []
    for p in data['Personen']:
        wunschabstaede = {}

        for l in data['Wunschabstaende']:
            if(l['person1_id'] == p['id']):
                wunschabstaede[l['person2_id']] = l['wunschabstand']
        tmp = Person(p['id'], p['name'], wunschabstaede, p['startposition'])
        #print(p['id'], p['name'], wunschabstaede, p['startposition'])
        personlist.append(tmp)
   

    #create room
    raum = data['Spielfeld']
    raumgroesse = tuple[raum['raum_breite'], raum['raum_hoehe']]

    tisch = [tuple]

    for i in range(raum['tisch_hoehe']):
        for j in range(raum['tisch_breite']):
           tisch.append(tuple[raum['tisch_x']+i, raum['tisch_y']+j])
    #print(raumgroesse, tisch)
    Raum(raumgroesse, personlist, tisch)   
