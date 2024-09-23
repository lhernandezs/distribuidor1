##  autor: Leonardo Hernández Silva
##  email: leo66@hotmail.com
##  fecha: 9 - feb - 2024

import os.path
import csv

from correo         import Correo
from modelo         import Instructor, Ficha, DatosCorreo, Competencia
from entradaSalida  import EntradaSalida

class Robot:
    # constructor de la clase
    def __init__(self):
        self._competencias       = []     # contiene las competencias y sus descripciones
        self._instructores          = []      # contiene los registros de los instructores
        self._salida                    = []      # contiene los registros de las asignaciones de fichas TRANSVESALES
        self._fichasD                 = []      # contiene los registros de las asignaciones de fichas diferentes a TRANSVERSALES

    # obtiene las Competencias del archivo consolidado.xlsx
    def getCompetencias(self):
        self._competencias = EntradaSalida().getData('consolidado.xlsx', 'competencias', Competencia)

    # obtiene los Instructores del archivo consolidado.xlsx
    def getInstructores(self):
        self._instructores = EntradaSalida().getData('consolidado.xlsx', 'instructores', Instructor)

    # obtiene la Salida con la asignacion de fichas por instructor del archivo consolidado.xlsx
    def getSalida(self):
        self._salida = EntradaSalida().getData('consolidado.xlsx', 'salida', Ficha)

    # obtiene la hoja fichasDSalida con la asignacion de fichas (diferentes a transversales) por instructor del archivo consolidado.xlsx
    # def getSalida(self):
    #     self._fichasD = EntradaSalida().getData('consolidado.xlsx', 'fichasD', Ficha)

    # es el metodo principal; envia los correos para todos los instructores segun el tipo
    def sendCorreos(self, tipo: str):
        self.getCompetencias()
        self.getSalida()
        self.getInstructores()

        for instructor in self._instructores: 
            if instructor.nombre in [
                                    'CLAUDIA ALICIA HERNANDEZ MESA', 
                                    'NUBIA STELLA CARRENO AMAYA', 
                                    'CLAUDIA YAMILE MORALES CASTRO', 
                                    'SONIA PATRICIA CASTAÑEDA CAYCEDO', 
                                    'CARLOS ALBERTO HERNANDEZ ARCILA', 
                                    'ANGELICA JANETH RODRIGUEZ ALONSO', 
                                    'MARITZABEL MONTEALEGRE RAMIREZ'
                                     ]:
                fechaInicioPeriodo = '30-sep-2024'
                fechaFinPeriodo    = '31-oct-2024'
            else:
                fechaInicioPeriodo = '30-sep-2024'
                fechaFinPeriodo    = '31-oct-2024'
                
            if tipo == "TRANS":
                descripcionCompetencia = ""
                for competencia in self._competencias:
                    if competencia.competencia == instructor.competencia:
                        descripcionCompetencia = competencia.descripcion_competencia
                        break
            elif tipo == "TECNI":
                descripcionCompetencia = "COMPETENCIAS TECNICAS DEL PROGRAMA"
            elif tipo == "PRODU":
                descripcionCompetencia = "RESULTADOS DE APRENDIZAJE ETAPA PRACTICA"
            elif tipo == "BILIN":
                descripcionCompetencia = "INTERACTUAR EN LENGUA INGLESA DE FORMA ORAL Y ESCRITA DENTRO DE CONTEXTOS SOCIALES Y LABORALES SEGÚN LOS CRITERIOS ESTABLECIDOS POR EL MARCO COMÚN EUROPEO DE REFERENCIA PARA LAS LENGUAS"

            fichas = []

            if tipo in ["TRANS", "BILIN"]:
                listSalida = list(filter(lambda fichaSalida: fichaSalida.nombre == instructor.nombre, self._salida))
            else:
                listSalida = list(filter(lambda fichasD: fichasD.ins_tecnico == instructor.nombre, self._fichasD))

            for fichaSalida in listSalida:
                fichas.append([ fichaSalida.nivel          ,
                                fichaSalida.programa       ,
                                fichaSalida.nficha         ,
                                fichaSalida.fecha_inicio   ,
                                fichaSalida.aprendices     ,
                                fichaSalida.ins_tecnico    ,
                                fechaInicioPeriodo         ,
                                fechaFinPeriodo])

            datosCorreo = DatosCorreo(
                                            instructor                         = instructor          ,
                                        fichas                                = fichas                 ,
                                        descripcion_competencia = descripcionCompetencia)
            
            correo = Correo(tipo,'lhernandezs', 'sena.edu.co', 'LeonardoSENA', datosCorreo)   # destino correo Leonardo
            # correo = Correo(tipo,'formacionvirtualcsf', 'sena.edu.co', 'Coordinacion Formacion Virtual', datosCorreo)   # destino correo formacionvirtualcsf
            # correo = Correo(tipo,'jpulgarin', 'sena.edu.co', 'Juan Camilo Pulgarin Vanegas', datosCorreo)   # destino correo Juan Camilo
            correo.send_email() 

if __name__ == '__main__':
    robot = Robot()
    while True:
        print("1. TRANSVERSAL")
        print("2. TECNICO")
        print("3. BILINGUISMO")
        print("4. PRODUCTIVA")
        print("5. SALIR (q)")
        opcion = input("Digita tu opcion: ")
        if opcion in ["1", "2", "3", "4", "5", "Q", "q"]:
            if opcion == "1":
                robot.sendCorreos("TRANS")
            elif opcion == "2":
                robot.sendCorreos("TECNI")            
            elif opcion == "3":
                robot.sendCorreos("BILIN")    
            elif opcion == "4":
                robot.sendCorreos("PRODU")    
            elif opcion in ["5", "Q", "q"]:
                print("Terminó.......")
                break
        else:
            print("Equivocado - Digite una opción correcta: ")
    