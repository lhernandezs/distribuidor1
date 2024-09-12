# from functools      import reduce
# from entradaSalida  import EntradaSalida
# from modelo         import Instructor

# recibe una lista de instructores y retorna su clasificacion por competencia y vinculacion
def calcularInstructorPorCompetencia(instructores: list) -> dict:
    nInsXCompetencias = {}
    for instructor in instructores:
        planta = 1 if instructor.vinculacion == "Planta" else 0
        if instructor.competencia not in nInsXCompetencias:
            nInsXCompetencias[instructor.competencia] = [1, planta]
        else:
            [numIns, numInsPlanta] = nInsXCompetencias[instructor.competencia]
            nInsXCompetencias[instructor.competencia] = [(numIns + 1), (numInsPlanta + planta)]
    return nInsXCompetencias

# OJO:   carga el diccionario {nficha : (listaCompetenciasFaltan, aprendices)}
# def getListaCompetenciasXFicha(self):
#     dictCompetenciasXFicha = {}
#     for ficha in self._fichas:
#         competenciasFaltan = (ficha.competencias_faltan).split()
#         if len(competenciasFaltan) > 0:
#             dictCompetenciasXFicha[ficha.nficha] = (competenciasFaltan, ficha.aprendices)
#     return dictCompetenciasXFicha

# if __name__ == "__main__":    
#     instructores = EntradaSalida().getData('consolidado.xlsx', 'instructores', Instructor)
#     print(calcularInstructorPorCompetencia(instructores))
