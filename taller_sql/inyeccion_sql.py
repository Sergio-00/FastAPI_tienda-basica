import sqlite3

conexion = sqlite3.connect("taller.db")
cursor = conexion.cursor()

# Valor malicioso
dato = "' OR '1'='1"

#
# CONSULTA INSEGURA
#
consulta_insegura = f"SELECT * FROM estudiantes WHERE nombre = '{dato}'"

print("CONSULTA INSEGURA")
print(consulta_insegura)

cursor.execute(consulta_insegura)

resultado_inseguro = cursor.fetchall()

print("Resultado del ataque:")
print(resultado_inseguro)

#
# CONSULTA SEGURA
#
print("\nCONSULTA SEGURA")

cursor.execute(
    "SELECT * FROM estudiantes WHERE nombre = ?",
    (dato,),
)

resultado_seguro = cursor.fetchall()

print("Resultado protegido:")
print(resultado_seguro)

conexion.close()
