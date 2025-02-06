#Librerias para poder leer excel, alamenar poligonos y para formato wkt de coordenadas
import pandas as pd 
from shapely import wkt
from shapely.geometry import Polygon, Point

#Ruta especifica del archivo con las coordendas
df = pd.read_csv("C:/Users/DATA ANALYST MD/Documents/CUADRANTES RUTAS MD.csv")

print(df.head)

poligonos = []

for index, row in df.iterrows():
    #funion para obtener el poligono on wkt
    wkt_poligono = row['WKT']
    nombre_poligono = row['Nombre']

    poligono = wkt.loads(wkt_poligono)

    poligonos.append({
        'Nombre': nombre_poligono,
        'Wkt': poligono
    })



getCoordenadas = pd.read_excel("C:/Users/DATA ANALYST MD/Documents/ClientesDB.xlsx" )
print(getCoordenadas.head)
negocios = []
for index, row in getCoordenadas.iterrows():
    #obtenemos las filas de las columans que nos interesan
    Nombre = row['Nombre']
    Latitud = row['Latitud']
    Longitud = row['Longitud']

   

    punto = Point(Longitud,Latitud)

    poligono_encontrado = None
    for i, poligono in enumerate(poligonos, start=1):
       if poligono['Wkt'].contains(punto): 
            poligono_encontrado = poligono['Nombre']
            break
       
    negocios.append({
        'Nombre': Nombre,
        'Latitud': Latitud,
        'Longitud': Longitud,
        'Poligono': poligono_encontrado
    })
df_negociosPoligonos = pd.DataFrame(negocios)
df_negociosPoligonos.to_csv("NegociosPoligonos.csv", index=False)

# Verificar si el número de filas es igual en ambos DataFrames
if len(getCoordenadas) == len(df_negociosPoligonos):
    getCoordenadas['Poligono'] = df_negociosPoligonos['Poligono']
    getCoordenadas.to_excel('ClientesBD.xlsx')
    print("Las longitudes de los índices coinciden. Columna 'Poligono' agregada exitosamente.")
else:
    print(f"¡Error! Los índices no coinciden: {len(getCoordenadas)} filas en getCoordenadas y {len(df_negociosPoligonos)} filas en df_negociosPoligonos.")



# for negocio in negocios:
#  if negocio['Poligono']:
#     print(f"Nombre: {negocio['Nombre']}, Coordenadas LonLat: ({negocio['Longitud']}, {negocio['Latitud']}), Dentro del poligino: {negocio['Poligono']}")
#  else:
#     print(f"Nombre: {negocio['Nombre']}, Coordendas LonLat: ({negocio['Longitud']}, {negocio['Latitud']}), No esta dentro de ningun poligono")