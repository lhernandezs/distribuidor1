##  autor: Leonardo Hernández Silva
##  email: leo66@hotmail.com
##  fecha: 9 - feb - 2024

from correo         import Correo
from modelo         import Competencia, Instructor, Ficha, DatosCorreo 
from entradaSalida  import EntradaSalida

class Robot:
    # constructor de la clase
    def __init__(self):
        self._competencias = EntradaSalida().getData('consolidado.xlsx', 'competencias', Competencia) # contiene las competencias y sus descripciones
        self._instructores = EntradaSalida().getData('consolidado.xlsx', 'instructores', Instructor)  # contiene los registros de los instructores
        self._salida       = EntradaSalida().getData('consolidado.xlsx', 'salida', Ficha)             # contiene los registros de las asignaciones de fichas 

    # es el metodo principal; envia los correos para todos los instructores segun el tipo
    def sendCorreos(self, tipo: str):
        insDiferentePeriodo = [
                                'CLAUDIA ALICIA HERNANDEZ MESA'     , 
                                'NUBIA STELLA CARRENO AMAYA'        , 
                                'CLAUDIA YAMILE MORALES CASTRO'     , 
                                'SONIA PATRICIA CASTAÑEDA CAYCEDO'  , 
                                'CARLOS ALBERTO HERNANDEZ ARCILA'   , 
                                'ANGELICA JANETH RODRIGUEZ ALONSO'  , 
                                'MARITZABEL MONTEALEGRE RAMIREZ'
                              ]

        for instructor in self._instructores: 
            if instructor.nombre in insDiferentePeriodo:
                fecIniPeriodo = '30-sep-2024'
                fecFinPeriodo = '31-oct-2024'
            else:
                fecIniPeriodo = '30-sep-2024'
                fecFinPeriodo = '31-oct-2024'

            if tipo == "TRANS":
                descripcionCompetencia = list(filter(lambda comp: comp.competencia == instructor.competencia, self._competencias))[0].descripcion_competencia
            elif tipo == "TECNI":
                descripcionCompetencia = "COMPETENCIAS TECNICAS DEL PROGRAMA"
            elif tipo == "PRODU":
                descripcionCompetencia = "RESULTADOS DE APRENDIZAJE ETAPA PRACTICA"
            elif tipo == "BILIN":
                descripcionCompetencia = "INTERACTUAR EN LENGUA INGLESA DE FORMA ORAL Y ESCRITA DENTRO DE CONTEXTOS SOCIALES Y LABORALES SEGÚN LOS CRITERIOS ESTABLECIDOS POR EL MARCO COMÚN EUROPEO DE REFERENCIA PARA LAS LENGUAS"

            fichas = []
            listSalida = list(filter(lambda fichaSalida: fichaSalida.nombre == instructor.nombre, self._salida))

            for fichaSalida in listSalida:
                fichas.append([ 
                                fichaSalida.nivel          ,
                                fichaSalida.programa       ,
                                fichaSalida.nficha         ,
                                fichaSalida.fecha_inicio   ,
                                fichaSalida.aprendices     ,
                                fichaSalida.ins_tecnico    ,
                                fecIniPeriodo              ,
                                fecFinPeriodo
                             ])

            datosCorreo = DatosCorreo(
                                        instructor              = instructor          ,
                                        fichas                  = fichas              ,
                                        descripcion_competencia = descripcionCompetencia
                                     )
            
            correo = Correo(tipo,'lhernandezs', 'sena.edu.co', 'LeonardoSENA', datosCorreo)   # destino correo Leonardo
            # correo = Correo(tipo,'formacionvirtualcsf', 'sena.edu.co', 'Coordinacion Formacion Virtual', datosCorreo)   # destino correo formacionvirtualcsf
            # correo = Correo(tipo,'jpulgarin', 'sena.edu.co', 'Juan Camilo Pulgarin Vanegas', datosCorreo)   # destino correo Juan Camilo
            correo.send_email() 

if __name__ == '__main__':
    robot = Robot()
    while True:
        opciones = ['TRANSVERSAL', 'TECNICO', 'BILIGUISMO', 'PRODUCTIVA', 'SALIR (q)']
        i = 0
        for opcion in opciones:
            i += 1
            print(f'{i}. {opcion}')
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
    