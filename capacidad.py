from modelo import TopeAprendices

import os.path
import json
class Capacidad:
    def __init__(self, tipo_competencia = "TEC", vinculacion = "Planta"):
        self._tope = 0
        with open(os.path.join('json', 'capacidad.json'), 'r') as conex:
            arc = json.load(conex)
            try:
                ta = TopeAprendices(tipo_competencia=tipo_competencia, vinculacion=vinculacion, tope=arc[tipo_competencia][vinculacion])
            except:
                print("Error, no existe el tipo de competencia o la vinculacion, cargaremos el tope para TECNICOS DE PLANTA")
                ta = TopeAprendices(tipo_competencia="TEC",vinculacion="Planta", tope=arc["TEC"]["Planta"])
            self._tope = ta.tope
    
    def getTope(self):
        return self._tope

if __name__ == '__main__':
    cap = Capacidad(tipo_competencia="TRA", vinculacion="Contrat")
    print(cap.getTope())
