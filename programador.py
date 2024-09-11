from functools      import reduce
from modelo         import Instructor, Ficha
from entradaSalida  import EntradaSalida
from capacidad      import Capacidad
from auxiliar       import calcularInstructorPorCompetencia

class Programador:

    def __init__(self, numeroPeriodos = 1):
        self._numeroDePeriodos                  = numeroPeriodos    # entero que representa el numero de periodos
        self._fichas                            = []                # lista que tiena los registros de las fichas
        self._instructores                      = []                # lista que tiene los registros de los instructores
        self._nInsXCompetencias                 = {}                # diccionario que tiene el numero de instructores Totales y de Planta clasificados por competencias
        self._capacidadAprendicesXCompetencia   = {}                # diccionario {competencia: capacidadToral} contiene la cantidad de aprendices que pueden atender los instructores en cada competencia
        self._fichasXCompetencia                = {}                # diccionario que tiene las tuplas (ficha, aprendices) por cada competencia

    # calcula la cantidad de aprendices que pueden atender los instructores disponibles por cada competencia
    def capacidadAprendicesXCompetencia(self):
        self._fichas = EntradaSalida().getData('consolidado.xlsx', 'fichasD', Ficha)
        self._instructores = EntradaSalida().getData('consolidado.xlsx', 'instructores', Instructor)
        self._nInsXCompetencias = calcularInstructorPorCompetencia(self._instructores)
        print("capacidad aprendices por competencia -----------------------") 
        for competencia in self._nInsXCompetencias:
            tipo = "TRA" # OJO: se programa solo para competencias TRANSVERSALES; ampliar a todo tipo de competencias
            insPlanta   = self._nInsXCompetencias[competencia][1]
            insContrato = self._nInsXCompetencias[competencia][0] - insPlanta
            capContrato = Capacidad(tipo_competencia=tipo, vinculacion="Contrato").getTope() * insContrato
            capPlanta   = Capacidad(tipo_competencia=tipo, vinculacion="Planta"  ).getTope() * insPlanta
            capTotal    = capContrato + capPlanta
            self._capacidadAprendicesXCompetencia[competencia] = capTotal
            print(competencia, " :", capTotal, end=", ")
        print("")

    # carga el diccionario self._fichasXCompetencia con las competencias y luego las fichas (desde self._fichas)
    def setFichasXCompetencia(self): 
        self._fichasXCompetencia = {competencia : [] for competencia in self._nInsXCompetencias.keys()} # crea el diccionario, las claves son las competencias en donde hay instructores
        competenciasSinInstructor = []
        for ficha in self._fichas:
            competenciasFaltan = [] if ficha.competencias_faltan is None else (ficha.competencias_faltan).split()
            if len(competenciasFaltan) > 0:
                for competenciaFalta in competenciasFaltan:
                    if competenciaFalta in self._fichasXCompetencia.keys(): 
                        self._fichasXCompetencia[competenciaFalta].append((ficha.nficha, ficha.aprendices))
                    else:
                        if competenciaFalta not in competenciasSinInstructor:
                            competenciasSinInstructor.append(competenciaFalta)

        print("Fichas por competencia --------------------------------------")
        for competencia in self._fichasXCompetencia:
            print(competencia, ": ", [tFicha[0] for tFicha in self._fichasXCompetencia[competencia]])
            print("------------------------------------------------------------")

        for competencia in competenciasSinInstructor:
            print("No hay instructores para la competencia ", competencia)

    # es el metodo principal; carga en un diccionario de dos dimensiones (periodo y competencia) las fichas que se programaran
    def programarPeriodos(self):
        self.capacidadAprendicesXCompetencia()
        self.setFichasXCompetencia()
        competencias = self._capacidadAprendicesXCompetencia.keys() # es la lista de competencias para las que hay instructores
        programacion = {periodo : {competencia :[] for competencia in competencias} for periodo in range(self._numeroDePeriodos)}
        for periodo in range(self._numeroDePeriodos):
            for competencia in competencias:
                capacidad = self._capacidadAprendicesXCompetencia[competencia]
                for ficha in self._fichasXCompetencia[competencia]:
                    aprendicesAsginados = 0 if len(programacion[periodo][competencia]) == 0 else reduce(lambda x, y: x+y, map(lambda a: a[1], programacion[periodo][competencia]))
                    # si hay capacidad de atender a los aprendices de la ficha y no esta programada en este periodo
                    if capacidad >= (aprendicesAsginados + ficha[1]) and len(list(filter(lambda comp: (ficha in programacion[periodo][comp]), programacion[periodo]))) == 0 : 
                        programacion[periodo][competencia].append(ficha)

                for ficha in programacion[periodo][competencia]:
                    self._fichasXCompetencia[competencia].remove(ficha) # remueva de las fichas que faltan por competencia las ya asignadas

        for p in range(self._numeroDePeriodos):
            for com in competencias:
                if len(programacion[p][com])> 0:
                    print("p: ", p, " comp: ", com, " fichas: ", [ficha for (ficha, aprendices) in programacion[p][com]])

        for competencia in self._fichasXCompetencia:
            if len(self._fichasXCompetencia[competencia]) > 0:
                print("en la competencia ", competencia, " estas fichas no se asignaron :", self._fichasXCompetencia[competencia] )
        
        # OJO: afinar el algoritmo para que pueda asginar hasta dos competencias si los periodos son inferiores a la cantidad de competencas por ver..
         

if __name__ == "__main__":
    Programador(8).programarPeriodos()