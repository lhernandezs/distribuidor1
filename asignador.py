##  autor: Leonardo Hernández Silva
##  email: leo66@hotmail.com
##  fecha: 9 - feb - 2024

from auxiliar       import calcularInstructorPorCompetencia
from salida         import Salida
from distribuidor   import Distribuidor
from entradaSalida  import EntradaSalida
from modelo         import Ficha, Instructor

class Asginador:

    ENCABEZADOS = ["NOMBRE"         , 
                   "NIVEL"          , 
                   "PROGRAMA"       , 
                   "NFICHA"         , 
                   "FECHA_INICIO"   , 
                   "APRENDICES"     , 
                   "INS_TECNICO"    , 
                   "COMPETENCIA"]

    def __init__(self):
        self._fichas                = []    # contiene las fichas que se van a asignar
        self._instructores          = []    # contiene los destalle de los instructores
        self._nInsXCompetencias     = {}    # calculara el numero de instructores totales y de planta por competencia
        self._fichasXCompetencia    = {}    # calculara las fichas por competencia

    # carga los datos de las fichas a asignar desde el archivo consolidado.xlsx
    def getFichas(self):
        self._fichas = EntradaSalida().getData('consolidado.xlsx', 'fichasD', Ficha)

    # carga los datos los instructores  desde el archivo consolidado.xlsx y llena la variable de instancioa self._nInsXCompetencias
    def getInstructores(self):
        self._instructores = EntradaSalida().getData('consolidado.xlsx', 'instructores', Instructor)
        self._nInsXCompetencias = calcularInstructorPorCompetencia(self._instructores)

        print("Numero de instructores por competencia ----------------------")
        print(self._nInsXCompetencias)

    # consigue un objeto ficha por el nficha, si no existe retorna None
    def getFichaXnficha(self, nficha):
        for ficha in self._fichas:
            if ficha.nficha == nficha:
                return ficha
        return None

    # consigue un objeto instructor por el nombre, si no existe retorna None
    def getInstructorXNombre(self, nombre):
        for instructor in self._instructores:
            if instructor.nombre == nombre:
                return instructor
        return None

    # carga la variable de instancia self._fichasXCompetencia (diccionario) con las competencias y luego las fichas (desde self._fichas)
    def setFichasXCompetencia(self): 
        for competencia in self._nInsXCompetencias.keys():
            self._fichasXCompetencia[competencia] = []

        for competencia in self._nInsXCompetencias:
            for ficha in self._fichas:
                if ficha.competencias[0:3] == competencia:
                    self._fichasXCompetencia[competencia].append((ficha.nficha,ficha.aprendices))
                if len(ficha.competencias) == 9 and ficha.competencias[6:9] == competencia:
                    self._fichasXCompetencia[competencia].append((ficha.nficha,ficha.aprendices))

        print("Fichas por competencia --------------------------------------")
        for competencia in self._fichasXCompetencia:
            print(competencia, ": ", self._fichasXCompetencia[competencia])


    # prepara los datos para llamar al Distribuidor
    def getDatosXDistribuidor(self, competencia):
        numInstructores = self._nInsXCompetencias[competencia][0]       # numero de instructores por competencia  
        numInsPlanta    = self._nInsXCompetencias[competencia][1]       # numero de instructores de planta por competencia
        fichas = {}                                                     # diccionario de listas de tuplas (nficha, aprendices) por competencia
        for tficha in self._fichasXCompetencia[competencia]:
            fichas[tficha[0]] = tficha[1]
        if fichas != {}:
            return (numInstructores, numInsPlanta, fichas)
        else:
            return (None, None, None)
    
    # escribe la hoja salida del archivo consolidado.xlsx
    def escribirSalida(self, indice, nFichas):
        instructor = self._instructores[indice]
        filas =[]
        for nficha in nFichas:
            ficha = self.getFichaXnficha(nficha)
            filas.append([
                            instructor.nombre            ,
                            ficha.nivel                  ,
                            ficha.programa               ,
                            str(ficha.nficha)            ,
                            str(ficha.fecha_inicio)      ,
                            str(ficha.aprendices)        ,
                            ficha.ins_tecnico            ,
                            instructor.competencia
                        ])
        EntradaSalida().writeSheet(nameArchivo="consolidado.xlsx", nameHoja="salida", encabezados=Asginador.ENCABEZADOS, filas = filas)

    # coloca las fichas para la salida
    def asignarFichas(self):
        self.getFichas()
        self.getInstructores()
        self.setFichasXCompetencia()

        for competencia in self._nInsXCompetencias.keys():
            (numInstructores, numInsPlanta, fichas) = self.getDatosXDistribuidor(competencia) 
            if fichas is not None:
                    indice = 0
                    indicesInstructoresPlanta   = [] 
                    indicesInstructoresContrato = []
                    for instructor in self._instructores:
                        if instructor.competencia == competencia:
                            if instructor.vinculacion == "Planta":
                                indicesInstructoresPlanta.append(indice)       # adiciona el indice a la lista de instructores de planta
                            else:
                                indicesInstructoresContrato.append(indice)     # adiciona el indice a la lista de instructores de contrato
                        indice += 1

                    distribucion = Distribuidor(numInstructores, numInsPlanta, fichas).distribuirFichasEntreInstructores()

                    keysInstructoresDePlanta  = []                             # se llenara con las claves en la distribucion de instructores que tienen fichas > 9999000
                    for keyInstructor in distribucion.keys():                  # recorremos la distribucion de fichas entre los indices de los instructores
                        for tFicha in distribucion[keyInstructor]:             
                            if tFicha[0] > 9999000:
                                keysInstructoresDePlanta.append(keyInstructor) # incluye la clave en la distribucion de los instructores de planta en una lista 
                                distribucion[keyInstructor].remove(tFicha)     # remueve de la distribucion las tuplas de las fichas > 9999000

                    for keyInstructor in distribucion.keys():
                        if keyInstructor in keysInstructoresDePlanta:
                            indice = indicesInstructoresPlanta.pop(0)          # selecciona y remueve el siguiente indice de la lista de instructores de planta
                        else:
                            indice = indicesInstructoresContrato.pop(0)        # selecciona y remueve el siguiente indice de la lista de instructores de contrato
                        nFichas = [nficha for (nficha, aprendices) in distribucion[keyInstructor]]    
                        self.escribirSalida(indice, nFichas)
            else:
                Salida("No hay fichas para la competencia" + competencia)

if __name__ == "__main__":
    Asginador().asignarFichas()