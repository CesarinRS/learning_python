import datetime
from datetime import date

mi_hora = datetime.time(9, 30)

mi_fecha = datetime.date.today()

print(mi_hora)
print(mi_fecha)

nacimiento = date(2004, 2, 23)

death = date(2100, 12, 31)

vida = death - nacimiento
print(vida)

minutos = datetime.date.today()
print(minutos)

minutos = datetime.datetime.now().minute
print(minutos)