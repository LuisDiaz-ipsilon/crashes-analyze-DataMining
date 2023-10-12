import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import geopandas as gpd
from datetime import datetime
import numpy as np


def timeSeries_sum_ambulances_by_year(url:str):
    df = pd.read_csv(url)

	#Veamos por año cuantas ambulancias son requeridas 
	#Cantidad de choques que requieren de ambulancia por fecha
	#Para esto es necesario eliminar todos los registros que no requirieron ambulancia 
	#Y todos los que si solo colocarles 1 y no 2, 3, 4 ....



    df['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATE'], format='%m/%d/%Y')
    

    data_crash_ambulance_year = pd.DataFrame({'CRASH_DATE': df['CRASH_DATE'].dt.year, 
											'AMBULANCE_REQUIRED': df['AMBULANCE_REQUIRED']})
    
    mask = (data_crash_ambulance_year['AMBULANCE_REQUIRED'] == 0)
    data_crash_ambulance_year = data_crash_ambulance_year[~mask]
    data_crash_ambulance_year['AMBULANCE_REQUIRED'] = 1
    sum_by_year = data_crash_ambulance_year.groupby('CRASH_DATE')['AMBULANCE_REQUIRED'].sum().reset_index()
    
    print(sum_by_year)
    plt.plot(sum_by_year.CRASH_DATE, sum_by_year.AMBULANCE_REQUIRED)
    plt.title('Ambulancias requeridas en accidentes de tráfico en Chicago.')
    plt.xlabel('YEAR')
    plt.ylabel('AMBULANCES')
    plt.savefig("images/timeSeries_sum_ambulances_by_year.png")
    plt.close()


#Cantidad de choques que requieren de ambulancia por 12 meses del año
def timeSeries_sum_ambulances_by_month(url:str):
    df = pd.read_csv(url)
    
    data_crash_ambulance_date = pd.DataFrame()
    
    data_crash_ambulance_date['CRASH_DATE'] = df['CRASH_DATE']
    
    data_crash_ambulance_date['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATE'], format='%m/%d/%Y')
    
    data_crash_ambulance_date['YEAR'] = data_crash_ambulance_date['CRASH_DATE'].dt.year
    data_crash_ambulance_date['MONTH'] = data_crash_ambulance_date['CRASH_DATE'].dt.month
    
    anio_meses = data_crash_ambulance_date.groupby(['YEAR', 'MONTH']).size().reset_index(name='COUNT')
    
    unique_years = data_crash_ambulance_date['YEAR'].unique()
    for y in unique_years:
        data_year = anio_meses[anio_meses['YEAR'] == y]
        
        plt.figure(figsize=(10, 6))
        plt.plot(data_year['MONTH'], data_year['COUNT'])
        plt.title(f'Ambulancias requeridas en accidentes de tráfico en Chicago año {y}.')
        plt.xlabel('Month')
        plt.ylabel('AMBULANCES')
        try:
            plt.savefig(f"images/timeSeries_sum_ambulances_by_year_month {y}.png")
            print("Imagen creada exitosamente")
        except Exception as e:
            print(e)
        plt.close()

def map_sum_crashes_all_time(url : str):
    df = pd.read_csv(url)
    
    data_crashes_all = df[['LATITUDE', 'LONGITUDE']]
    
    lat_min = 41.7
    lat_max = 42.1
    lon_min = -88.0
    lon_max = -87.7
    num_zonas = 4
    
    # Divide el rango de latitud y longitud en 10 partes iguales
    lat_step = (lat_max - lat_min) / num_zonas
    lon_step = (lon_max - lon_min) / num_zonas

    #Ignoramos los warnings
    pd.options.mode.chained_assignment = None
    # cálculos de la división del área geográfica en zonas de tamaño uniforme.
    data_crashes_all.loc[:, 'ZONE_LAT'] = ((data_crashes_all['LATITUDE'] - lat_min) // lat_step) * lat_step + lat_min + lat_step / 2
    data_crashes_all.loc[:, 'ZONE_LON'] = ((data_crashes_all['LONGITUDE'] - lon_min) // lon_step) * lon_step + lon_min + lon_step / 2

    # Creamos un nuevo
    crashesh_by_zone = data_crashes_all.groupby(['ZONE_LAT', 'ZONE_LON']).size().reset_index(name='CRASHES')

    fig = px.scatter_mapbox(crashesh_by_zone, lat = 'ZONE_LAT', lon = 'ZONE_LON', 
                        title = "Choques que hubo de 2016 a parte del 2023 Chicago",
                        size = 'CRASHES', color= 'CRASHES',
                        zoom = 4, mapbox_style = 'open-street-map')
                        
    fig.show()
    
def csv_sum_crashes_by_year(url: str, year: int):
    df = pd.read_csv(url)
    year_min = df['CRASH_DATE'].min()
    year_max= df['CRASH_DATE'].max()
        
    year_min = datetime.strptime(year_min, "%m/%d/%Y")
    year_max = datetime.strptime(year_max, "%m/%d/%Y")

    if year > year_max.year or year < year_min.year:
        print((f'El año {year} no esta dispoible.'))
        
    data_crashes_all = df[['CRASH_DATE', 'LATITUDE', 'LONGITUDE']]
    
    #Ignoramos los warnings
    pd.options.mode.chained_assignment = None
    
    #Obtenermos solo el year
    data_crashes_all['CRASH_DATE'] = pd.to_datetime(data_crashes_all['CRASH_DATE'], format="%m/%d/%Y")

    data_crashes_all['YEAR'] = data_crashes_all['CRASH_DATE'].dt.year
    data_crashes_all= data_crashes_all.drop('CRASH_DATE', axis=1)

    data_crashes_all = data_crashes_all[['YEAR', 'LATITUDE', 'LONGITUDE']]
    
    print(data_crashes_all)
    
    # Se obtienen los 4 puntos mas alejados como si de un cuadrado se tratase para obtener 
    # Los centros de estos para despues agrupar por zona y año
    lat_norte = data_crashes_all['LATITUDE'].max()
    lon_norte = data_crashes_all[data_crashes_all['LATITUDE'] == lat_norte]['LONGITUDE'].values[0]
    lat_sur = data_crashes_all['LATITUDE'].min()
    lon_sur = data_crashes_all[data_crashes_all['LATITUDE'] == lat_sur]['LONGITUDE'].values[0]
    lon_este = data_crashes_all['LONGITUDE'].max()
    lat_este = data_crashes_all[data_crashes_all['LONGITUDE'] == lon_este]['LATITUDE'].values[0]
    lon_oeste = data_crashes_all['LONGITUDE'].min()
    lat_oeste = data_crashes_all[data_crashes_all['LONGITUDE'] == lon_oeste]['LATITUDE'].values[0]

    print("Norte:", (lat_norte, lon_norte))
    print("Sur:", (lat_sur, lon_sur))
    print("Este:", (lat_este, lon_este))
    print("Oeste:", (lat_oeste, lon_oeste))
    
    # puntos extremos
    norte = (lat_norte, lon_norte)
    sur = (lat_sur, lon_sur)
    este = (lat_este, lon_este)
    oeste = (lat_oeste, lon_oeste)

    delta_lat = (norte[0] - sur[0]) / 4
    delta_lon = (este[1] - oeste[1]) / 5

    centros = []

    # Itera sobre la cuadrícula y calcula el centro de cada celda
    for i in range(4):  # para las 4 filas
        for j in range(5):  # para las 5 columnas
            lat_centro = sur[0] + (i + 0.5) * delta_lat
            lon_centro = oeste[1] + (j + 0.5) * delta_lon
            centros.append((lat_centro, lon_centro))
                    
    LATITUDE = [centro[0] for centro in centros]
    LONGITUDE = [centro[1] for centro in centros]
    
    point_centers = pd.DataFrame(centros, columns=["LATITUDE", "LONGITUDE"])
    
    print(point_centers)


    """fig = px.scatter_mapbox(point_centers,
                    lat="LATITUDE",
                    lon="LONGITUDE",
                    title = "Puntos centrales de 20 zonas en chicago",
                    zoom = 4, mapbox_style = 'open-street-map'
                    )

    
    fig.show()"""
    
    # Función para calcular la distancia euclidiana
    def compute_distance(lat1, lon1, lat2, lon2):
        return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    # Para cada choque indicarle cual es la zona que le corresponde
    zones = []
    for index, crash in data_crashes_all.iterrows():
        distances = point_centers.apply(lambda row: compute_distance(crash['LATITUDE'], crash['LONGITUDE'], row['LATITUDE'], row['LONGITUDE']), axis=1)
        closest_zone = distances.idxmin() + 1  # +1 porque las zonas van de 1 a 20
        zones.append(closest_zone)

    data_crashes_all['ZONE'] = zones

    # Creando nuevo data frame
    result_df = data_crashes_all[['YEAR', 'ZONE', 'LATITUDE', 'LONGITUDE']]

    print(result_df)
    
    SUM_CRASHES_BY_YEAR_AND_ZONE = result_df.groupby(['YEAR', 'ZONE']).size().reset_index(name='SUM_CRASHES')

    SUM_CRASHES_BY_YEAR_AND_ZONE.to_csv('Traffic_Crashes_-_SUM_CRASHES_BY_YEAR_AND_ZONE.csv', index=False)
    print(SUM_CRASHES_BY_YEAR_AND_ZONE)
        
def map_sum_crashes_by_year_and_zone(url: str):
    SUM_CRASHES_BY_YEAR_AND_ZONE = pd.read_csv(url)
    
    #Estos puntos los obtuvimos del anterior metodo.
    point_centers_data = {
        'LATITUDE': [
            41.691934, 41.691934, 41.691934, 41.691934, 41.691934,
            41.786461, 41.786461, 41.786461, 41.786461, 41.786461,
            41.880989, 41.880989, 41.880989, 41.880989, 41.880989,
            41.975516, 41.975516, 41.975516, 41.975516, 41.975516
        ],
        'LONGITUDE': [
            -87.895032, -87.812711, -87.730390, -87.648069, -87.565748,
            -87.895032, -87.812711, -87.730390, -87.648069, -87.565748,
            -87.895032, -87.812711, -87.730390, -87.648069, -87.565748,
            -87.895032, -87.812711, -87.730390, -87.648069, -87.565748
        ]
    }
    
    point_centers = pd.DataFrame(point_centers_data)
    
    # Establecer el índice de point_centers para que coincida con la columna ZONE (recordando que la indexación en Python comienza desde 0)
    point_centers['ZONE'] = point_centers.index + 1

    # Fusionar dataframes
    crashes_by_zone_and_year = pd.merge(SUM_CRASHES_BY_YEAR_AND_ZONE, point_centers, on='ZONE', how='left')

    # Seleccionar las columnas deseadas y renombrarlas si es necesario
    crashes_by_zone_and_year = crashes_by_zone_and_year[['YEAR', 'LATITUDE', 'LONGITUDE', 'SUM_CRASHES']]
    
    fig = px.scatter_mapbox(crashes_by_zone_and_year, lat = 'LATITUDE', lon = 'LONGITUDE', 
                        title = "sumatoria de choques por zona (20)  que hubo de año a año en Chicago",
                        size = 'SUM_CRASHES', color= 'SUM_CRASHES',
                        zoom = 9, mapbox_style = 'open-street-map',
                        animation_frame='YEAR',)
    
    fig.show()
    

#Contruccion
def csv_sum_crashes_by_month_and_zone(url: str):
    df = pd.read_csv(url)
        
    data_crashes_all = df[['CRASH_DATE', 'LATITUDE', 'LONGITUDE']]
    
    #Ignoramos los warnings
    pd.options.mode.chained_assignment = None
    
    #Obtenermos solo el MONTH
    data_crashes_all['CRASH_DATE'] = pd.to_datetime(data_crashes_all['CRASH_DATE'], format="%m/%d/%Y")

    data_crashes_all['MONTH'] = data_crashes_all['CRASH_DATE'].dt.month
    data_crashes_all= data_crashes_all.drop('CRASH_DATE', axis=1)
    
    data_crashes_all = data_crashes_all[['MONTH', 'LATITUDE', 'LONGITUDE']]
    

    
    # Se obtienen los 4 puntos mas alejados como si de un cuadrado se tratase para obtener 
    # Los centros de estos para despues agrupar por zona y año
    lat_norte = data_crashes_all['LATITUDE'].max()
    lon_norte = data_crashes_all[data_crashes_all['LATITUDE'] == lat_norte]['LONGITUDE'].values[0]
    lat_sur = data_crashes_all['LATITUDE'].min()
    lon_sur = data_crashes_all[data_crashes_all['LATITUDE'] == lat_sur]['LONGITUDE'].values[0]
    lon_este = data_crashes_all['LONGITUDE'].max()
    lat_este = data_crashes_all[data_crashes_all['LONGITUDE'] == lon_este]['LATITUDE'].values[0]
    lon_oeste = data_crashes_all['LONGITUDE'].min()
    lat_oeste = data_crashes_all[data_crashes_all['LONGITUDE'] == lon_oeste]['LATITUDE'].values[0]
    
    # puntos extremos
    norte = (lat_norte, lon_norte)
    sur = (lat_sur, lon_sur)
    este = (lat_este, lon_este)
    oeste = (lat_oeste, lon_oeste)

    delta_lat = (norte[0] - sur[0]) / 4
    delta_lon = (este[1] - oeste[1]) / 5

    centros = []

    # Itera sobre la cuadrícula y calcula el centro de cada celda
    for i in range(4):  # para las 4 filas
        for j in range(5):  # para las 5 columnas
            lat_centro = sur[0] + (i + 0.5) * delta_lat
            lon_centro = oeste[1] + (j + 0.5) * delta_lon
            centros.append((lat_centro, lon_centro))
                    
    LATITUDE = [centro[0] for centro in centros]
    LONGITUDE = [centro[1] for centro in centros]
    
    point_centers = pd.DataFrame(centros, columns=["LATITUDE", "LONGITUDE"])
    

    """
    fig = px.scatter_mapbox(point_centers,
                    lat="LATITUDE",
                    lon="LONGITUDE",
                    title = "Puntos centrales de 20 zonas en chicago",
                    zoom = 4, mapbox_style = 'open-street-map'
                    )

    
    fig.show()"""
    
    # Función para calcular la distancia euclidiana
    def compute_distance(lat1, lon1, lat2, lon2):
        return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    # Para cada choque indicarle cual es la zona que le corresponde
    zones = []
    for index, crash in data_crashes_all.iterrows():
        distances = point_centers.apply(lambda row: compute_distance(crash['LATITUDE'], crash['LONGITUDE'], row['LATITUDE'], row['LONGITUDE']), axis=1)
        closest_zone = distances.idxmin() + 1  # +1 porque las zonas van de 1 a 20
        zones.append(closest_zone)

    data_crashes_all['ZONE'] = zones

    # Creando nuevo data frame
    result_df = data_crashes_all[['MONTH', 'ZONE', 'LATITUDE', 'LONGITUDE']]
    
    SUM_CRASHES_BY_MONTH_AND_ZONE = result_df.groupby(['MONTH', 'ZONE']).size().reset_index(name='SUM_CRASHES')

    SUM_CRASHES_BY_MONTH_AND_ZONE.to_csv('Traffic_Crashes_-_SUM_CRASHES_BY_MONTH_AND_ZONE.csv', index=False)
    print(SUM_CRASHES_BY_MONTH_AND_ZONE)

def map_sum_crashes_by_month_and_zone(url: str):
    SUM_CRASHES_BY_MONTH_AND_ZONE = pd.read_csv(url)
    
    #Estos puntos los obtuvimos del anterior metodo.
    point_centers_data = {
        'LATITUDE': [
            41.691934, 41.691934, 41.691934, 41.691934, 41.691934,
            41.786461, 41.786461, 41.786461, 41.786461, 41.786461,
            41.880989, 41.880989, 41.880989, 41.880989, 41.880989,
            41.975516, 41.975516, 41.975516, 41.975516, 41.975516
        ],
        'LONGITUDE': [
            -87.895032, -87.812711, -87.730390, -87.648069, -87.565748,
            -87.895032, -87.812711, -87.730390, -87.648069, -87.565748,
            -87.895032, -87.812711, -87.730390, -87.648069, -87.565748,
            -87.895032, -87.812711, -87.730390, -87.648069, -87.565748
        ]
    }
    
    point_centers = pd.DataFrame(point_centers_data)
    
    # Establecer el índice de point_centers para que coincida con la columna ZONE (recordando que la indexación en Python comienza desde 0)
    point_centers['ZONE'] = point_centers.index + 1

    # Fusionar dataframes
    crashes_by_zone_and_month = pd.merge(SUM_CRASHES_BY_MONTH_AND_ZONE, point_centers, on='ZONE', how='left')

    # Seleccionar las columnas deseadas y renombrarlas si es necesario
    crashes_by_zone_and_month = crashes_by_zone_and_month[['MONTH', 'LATITUDE', 'LONGITUDE', 'SUM_CRASHES']]
    
    fig = px.scatter_mapbox(crashes_by_zone_and_month, lat = 'LATITUDE', lon = 'LONGITUDE', 
                        title = "sumatoria de choques por zona (20) mes a mes sumando todos los años",
                        size = 'SUM_CRASHES', color= 'SUM_CRASHES',
                        zoom = 9, mapbox_style = 'open-street-map',
                        animation_frame='MONTH',)
    
    fig.show()   
    
    
    


def main():

	#timeSeries_sum_ambulances_by_year("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
    #timeSeries_sum_ambulances_by_month("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
    #map_sum_crashes_all_time("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
    #csv_sum_crashes_by_year_and_zone("Traffic_Crashes_-_Crashes_cleaned_normalized.csv", 2017)
    
    #map_sum_crashes_by_year_and_zone("Traffic_Crashes_-_SUM_CRASHES_BY_YEAR_AND_ZONE.csv")
    
    #csv_sum_crashes_by_month_and_zone("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
	
    map_sum_crashes_by_month_and_zone("Traffic_Crashes_-_SUM_CRASHES_BY_MONTH_AND_ZONE.csv")
    

if __name__ == "__main__":
    main()