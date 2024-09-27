lista = [3, 1, 4, 7, 2, 8, 9, 11, 10] 

filtrada = [ elemento for elemento in lista if (lambda elemento: elemento % 2) ].pop(0)

print(filtrada)

