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
        self._instructores          = []    # contiene los destalles de los instructores
        self._nInsXCompetencias     = {}    # calculara el numero de instructores totales y de planta por competencia
        self._fichasXCompetencia    = {}    # calculara las fichas por competencia

    def getDatos(self, hoja, modelo):
        return EntradaSalida().getData('consolidado.xlsx', hoja, modelo)

    # consigue un objeto ficha por el nficha, si no existe retorna None
    def getFichaXnficha(self, nficha):
        try:
            return [ficha for ficha in self._fichas if ficha.nficha == nficha].pop()
        except:
            return None

    # consigue un objeto instructor por el nombre, si no existe retorna None
    def getInstructorXNombre(self, nombre):
        try:
            return [instructor for instructor in self._instructores if instructor.nombre == nombre].pop()
        except:
            return None

    # carga la variable de instancia self._fichasXCompetencia (diccionario) con las competencias y luego las fichas (desde self._fichas)
    def setFichasXCompetencia(self): 
        self._fichasXCompetencia ={competencia : [] for competencia in self._nInsXCompetencias.keys()}
        for competencia in self._nInsXCompetencias:
            for ficha in self._fichas:
                [self._fichasXCompetencia[competencia].append((ficha.nficha,ficha.aprendices)) for comp in ficha.competencias.split() if comp == competencia]

        [print(competencia, ": ", self._fichasXCompetencia[competencia]) for competencia in self._fichasXCompetencia]

    # prepara los datos para llamar al Distribuidor
    def getDatosXDistribuidor(self, competencia):
        numInstructores = self._nInsXCompetencias[competencia][0]                                       # numero de instructores por competencia  
        numInsPlanta    = self._nInsXCompetencias[competencia][1]                                       # numero de instructores de planta por competencia
        fichas = {nFicha: aprendices for (nFicha, aprendices) in self._fichasXCompetencia[competencia]} # diccionario de fichas a distribuir
        return (numInstructores, numInsPlanta, fichas) if fichas != {} else (None, None, None)
    
    # escribe la hoja salida del archivo consolidado.xlsx
    def escribirSalida(self, indice, nFichas):
        instructor = self._instructores[indice]
        filas = []
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
        self._fichas = self.getDatos('fichasD', Ficha)
        self._instructores = self.getDatos('instructores', Instructor)
        self._nInsXCompetencias = calcularInstructorPorCompetencia(self._instructores)
        self.setFichasXCompetencia()

        # para cada una de las competencias donde hay instructores
        for competencia in self._nInsXCompetencias.keys():
            (numInstructores, numInsPlanta, fichas) = self.getDatosXDistribuidor(competencia) 
            if fichas is not None:
                distribucion = Distribuidor(numInstructores, numInsPlanta, fichas).distribuirFichasEntreInstructores()

                indice = 0
                indicesInstructoresPlanta   = [] 
                indicesInstructoresContrato = []
                for instructor in self._instructores:
                    if instructor.competencia == competencia:
                        indicesInstructoresPlanta.append(indice) if instructor.vinculacion == "Planta" else indicesInstructoresContrato.append(indice)
                    indice += 1

                keysInstructoresDePlanta  = []                             # se llenara con las claves en la distribucion de instructores que tienen fichas > 9999000
                for keyInstructor in distribucion.keys():                  # recorremos la distribucion de fichas entre los indices de los instructores
                    for tFicha in distribucion[keyInstructor]:             
                        if tFicha[0] > 9999000:
                            keysInstructoresDePlanta.append(keyInstructor) # incluye la clave en la distribucion de los instructores de planta en una lista 
                            distribucion[keyInstructor].remove(tFicha)     # remueve de la distribucion las tuplas de las fichas > 9999000

                for keyInstructor in distribucion.keys():
                    indice = indicesInstructoresPlanta.pop(0) if keyInstructor in keysInstructoresDePlanta else indicesInstructoresContrato.pop(0)
                    self.escribirSalida(indice, [nficha for (nficha, aprendices) in distribucion[keyInstructor]])
            else:
                Salida("No hay fichas para la competencia" + competencia)

if __name__ == "__main__":
    Asginador().asignarFichas()