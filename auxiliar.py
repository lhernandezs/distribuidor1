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

