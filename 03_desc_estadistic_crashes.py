import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


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
    print(df['CRASH_DATE'].min())
    print(df['CRASH_DATE'].max())
    
    
    data_crashes_all = df[['LATITUDE', 'LONGITUDE']]
    
    lat_min = 41.7
    lat_max = 42.1
    lon_min = -88.0
    lon_max = -87.7
    num_zonas = 4
    
    # Divide el rango de latitud y longitud en 10 partes iguales
    lat_step = (lat_max - lat_min) / num_zonas
    lon_step = (lon_max - lon_min) / num_zonas

    # cálculos de la división del área geográfica en zonas de tamaño uniforme.
    data_crashes_all['ZONE_LAT'] = ((data_crashes_all['LATITUDE'] - lat_min) // lat_step) * lat_step + lat_min + lat_step / 2
    data_crashes_all['ZONE_LON'] = ((data_crashes_all['LONGITUDE'] - lon_min) // lon_step) * lon_step + lon_min + lon_step / 2

    # Creamos un nuevo
    crashesh_by_zone = data_crashes_all.groupby(['ZONE_LAT', 'ZONE_LON']).size().reset_index(name='CRASHES')


    # Carga los datos geoespaciales de los municipios de Chicago
    limits_chicago = gpd.read_file("./util/rows.json")
    
    # Crea un mapa de Chicago y agrega los límites de los municipios
    fig = px.choropleth_mapbox(limits_chicago, geojson=limits_chicago.geometry, locations=limits_chicago.index, 
                        hover_data={"name": limits_chicago["nombre"]}, color=limits_chicago.index,
                        color_continuous_scale="Viridis", range_color=(0, len(limits_chicago)),
                        labels={"name": "Municipio"})

    # Agrega las burbujas de choques
    fig.add_trace(px.scatter_geo(crashesh_by_zone, lat='ZONE_LAT', lon='ZONE_LON', text='CRASHES', size='CRASHES').data[0])

    # Define los límites del mapa
    fig.update_geos(
        center={"lat": 41.85, "lon": -87.7},
        projection_scale=15,
        visible=False
    )

    # Muestra el mapa
    fig.show()

    
    


def main():

	#timeSeries_sum_ambulances_by_year("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
    #timeSeries_sum_ambulances_by_month("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
    map_sum_crashes_all_time("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
	

if __name__ == "__main__":
    main()