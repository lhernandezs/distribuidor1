##  autor: Leonardo Hernández Silva
##  email: leo66@hotmail.com
##  fecha: 9 - feb - 2024

from functools import reduce
class Distribuidor: 
    # constructor que recibe un entero con el numero de instructores, un entero con el numero de instructores planta y un diccionario {ficha: numero_de_aprendices} 
    def __init__(self, numInstructores: int, numInsPlanta: int, fichas: dict):
        self._fichas            = fichas                                    # diccionario con las fichas y aprendices
        self._numInstructores   = numInstructores                           # valor entero representa el numero total de instructores
        self._numInsPlanta      = numInsPlanta                              # valor entero representa el numero de instructores de planta
        self._distribucion      = {n:[] for n in range(numInstructores)}    # diccionario que almacenara el resultado

    # ingresa una lista de tuplas de (fichas, aprendices) y un boooleano que representa el orden; retorna un diccionario ordenado
    def ordenarFichasPorAprendices(self, listaDeTuplas, ordenContrario = True):
        return {key:value for key, value in sorted(listaDeTuplas, key=lambda item:item[1], reverse = ordenContrario)}
    
    # ingresa una lista de tuplas de (nficha, aprendices); retorna un entero con la suma de aprendices
    def sumaDeAprendices(self, listaDeTuplas):
        return 0 if listaDeTuplas is None or len(listaDeTuplas) == 0 else reduce(lambda x, y: x+y, map(lambda a: a[1], listaDeTuplas))

    # retorna una lista de tuplas (instructor, suma_de_aprendices) ordenada con todos los instructores de menos a mas aprendices asignados en la distribucion
    def ordenarInstructoresPorAprendices(self, ordenContrario=True):
        listaDeTuplas = list(map(lambda instructor: (instructor, self.sumaDeAprendices(self._distribucion[instructor])), range(self._numInstructores)))
        return sorted(listaDeTuplas, key = lambda t: (t[1]), reverse = ordenContrario)

    # retorna una tupla con el instructor que tiene la ficha con mayor aprendices y el instructor que tiene la ficha con menos aprendices (optimas para el intercambio)
    def fichasOptimas(self):
        listaDeTuplas = self.ordenarInstructoresPorAprendices(ordenContrario=False)
        tMax, tMin = listaDeTuplas[self._numInstructores -1], listaDeTuplas[0]
        insMax, aprendicesInsMax, insMin, aprendicesInsMin = tMax[0], tMax[1], tMin[0], tMin[1]

        diferenciaTotal = aprendicesInsMax - aprendicesInsMin
        lisTuplasInsMax = list(self.ordenarFichasPorAprendices(self._distribucion[insMax],False).items())
        lisTuplasInsMin = list(self.ordenarFichasPorAprendices(self._distribucion[insMin],False).items())
        
        (fichaMax, aprendicesFichaMax) = lisTuplasInsMax.pop()
        (fichaMin, aprendicesFichaMin) = lisTuplasInsMin.pop(0)
        
        diferenciaFichas = aprendicesFichaMax - aprendicesFichaMin
        mejorDistancia = abs(diferenciaTotal - diferenciaFichas)
        
        for tuplaFichaInsMax in self._distribucion[insMax]:
            for tuplaFichaInsMin in self._distribucion[insMin]:
                diferenciaFichas = tuplaFichaInsMax[1] - tuplaFichaInsMin[1]
                distancia = abs(diferenciaTotal - diferenciaFichas)
                if distancia < mejorDistancia:
                    fichaMax = tuplaFichaInsMax[0]
                    fichaMin = tuplaFichaInsMin[0]
                    mejorDistancia = distancia 
        
        return (insMax, (fichaMax, self._fichas[fichaMax]), insMin, (fichaMin, self._fichas[fichaMin]))

    # intercambia las fichas entre los instructores para hacer mejor el equilibrio; retorna las tuplas (ficha, aprendices) intercambiadas
    def intercambioDeFichas(self, insX, tfichaX, insY, tfichaY):
        self._distribucion[insX].remove(tfichaX)
        self._distribucion[insX].append(tfichaY)
        self._distribucion[insY].remove(tfichaY)
        self._distribucion[insY].append(tfichaX)

    # verifica si las fichas a intercambiar son diferentes a las intercambiadas en la iteraricion anterior, si son iguales retorna False
    def sigueIntercambioDeFichas(self, tfichaX, tfichaY, ultimatFichaX, ultimatFichaY):
        if  ultimatFichaX       is not None         and \
            ultimatFichaY       is not None         and \
            tfichaX             is not None         and \
            tfichaY             is not None         and \
            tfichaX == ultimatFichaX                and \
            tfichaY == ultimatFichaY                  :
            return False
        else:
            return True

    # retorna la clave del instructor que tiene asignada la ficha, sino retorna None
    def getKeyInstructorEnDistribucion(self, nFicha):
        for keyInstructor in self._distribucion.keys():
            if nFicha in [nFicha for (nFicha, aprendices) in self._distribucion[keyInstructor]]:
                return keyInstructor
        return None
    
    # retorna True si la ficha esta asignada a una lista de instructores
    def fichaAsignadaAInstructores(self, tFicha, instructores):
        for instructor in instructores:
            if tFicha in self._distribucion[instructor]: 
                return True
        return False

    # intercambia las fichas de los instructores de Planta que tienen mas de una ficha 9999XXX
    def intercambiarFichas9999(self, instructoresPorMejorar, instructoresPlanta):
        while len(instructoresPorMejorar) > 0:
            siguienteInstructor = instructoresPorMejorar.pop(0)
            listaFichas9999 = list(filter(lambda tFichas: tFichas[0] > 9999000, self._distribucion[siguienteInstructor]))
            listaFichas9999.pop(0)  
            for tFicha9999 in listaFichas9999:
                menorDistancia = 999
                for tFicha in list(filter(lambda tFicha: not self.fichaAsignadaAInstructores(tFicha, instructoresPlanta), self._fichas.items())):
                    distancia = abs(tFicha9999[1] - tFicha[1])
                    if distancia < menorDistancia:
                        menorDistancia = distancia
                        mejorTFicha = tFicha

                keyInstructor2 = self.getKeyInstructorEnDistribucion(mejorTFicha[0])
                self.intercambioDeFichas(siguienteInstructor, tFicha9999, keyInstructor2, mejorTFicha)
        
    # distribuye las fichas 9999XXX para que cada instructor de planta quede con solo 1 ficha
    def distribuirFichas9999(self):
        if self._numInsPlanta > 1:
            instructoresPlanta = [] 
            instructoresPorMejorar = [] 

            for keyInstructor in self._distribucion.keys():
                listaFichas9999 = list(filter(lambda nficha: nficha > 9999000,[nficha for (nficha, aprendices) in self._distribucion[keyInstructor]]))
                if len(listaFichas9999) > 0:
                    instructoresPlanta.append(keyInstructor)
                if len(listaFichas9999) > 1:
                    instructoresPorMejorar.append(keyInstructor)

            if len(instructoresPorMejorar) > 0:
                    self.intercambiarFichas9999(instructoresPorMejorar, instructoresPlanta)
     
    # es el metodo principal de la clase; devuelve un diccionario con los indices de los instructores como clave y las tuplas (nFicha, aprendices) como valores
    def distribuirFichasEntreInstructores(self):
        # se revisa si hay instructores de planta y si es así crea una ficha 9999999 por cada instructor para asignarles y luego descontarla
        if self._numInsPlanta > 0:
            sumAprendices = self.sumaDeAprendices(self._fichas.items())
            aprendicesPorInstructor = sumAprendices // self._numInstructores
            for num in (range(self._numInsPlanta)):
                self._fichas[9999001+num] = int(aprendicesPorInstructor * 0.25)

        # carga en la variable de instancia (diccionario) self._distribucion las fichas -- 1ra distribucion
        for ficha in self.ordenarFichasPorAprendices(self._fichas.items()):
            instructor = self.ordenarInstructoresPorAprendices(ordenContrario=False)[0][0]
            self._distribucion[instructor].append((ficha, self._fichas[ficha]))

        # Mejora la distribucion de aprendices intercambiando fichas entre los instructores extremos
        tfichaX = tfichaY = ultimatFichaX = ultimatFichaY = None
        while self.sigueIntercambioDeFichas(tfichaX, tfichaY, ultimatFichaX, ultimatFichaY):
            insMax, tfichaX, insMin, tfichaY = self.fichasOptimas()
            self.intercambioDeFichas(insMax, tfichaX, insMin, tfichaY)
            ultimatFichaX = tfichaX
            ultimatFichaY = tfichaY
        
        self.distribuirFichas9999()

        return self._distribucion

if __name__ == "__main__":
    fichas = {
                2626895:23, 2626896:32, 2626898:30, 2626899:33, 2626900:34, 2626901:29, 2626902:21, 2626937:36, 2626938:39, 2626939:36, 2626940:21,
                2626941:40, 2626942:35, 2626943:39, 2626944:15, 2626955:20, 2626956:18, 2626957:17, 2626958:24, 2627060:26, 2627061:20, 2627062:22, 
                2627063:25, 2627064:29, 2627065:12, 2627066:8,  2627067:17, 2627068:10, 2627069:12, 2627070:23, 2627071:20, 2627072:17, 2627073:40,
                2627201:33, 2627202:39, 2627203:43, 2627204:34, 2627205:36, 2627206:41, 2675717:32, 2675744:23, 2675745:24, 2675746:30, 2675747:31,
                2675758:28, 2675759:27, 2675791:36, 2675815:34, 2675816:33, 2675817:33, 2675818:40, 2675819:36, 2675820:36, 2675821:45, 2675822:34, 
                2675823:41, 2675824:33, 2675825:42, 2675826:44, 2675827:44, 2675828:37, 2675829:37, 2675830:45, 2675831:40, 2675832:40, 2675911:40, 
    }

    distribuidor = Distribuidor(numInstructores= 6, numInsPlanta= 1, fichas = fichas)

    distribucion = distribuidor.distribuirFichasEntreInstructores()
    for instructor in distribucion.keys():
        print(instructor, distribucion[instructor], " aprendices: ", distribuidor.sumaDeAprendices(distribucion[instructor]))
