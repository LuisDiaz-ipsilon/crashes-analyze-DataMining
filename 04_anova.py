import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import warnings
import plotly.graph_objects as go


def main():
    df = pd.read_csv("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
    #Se dividira el mapa 

    # Definir los intervalos de las zonas
    bins = [41.644670, 41.739197, 41.833725, 41.928252, 42.022780]

    # Usar la función cut para determinar a qué zona pertenece cada valor de LATITUDE
    df['ZONE'] = pd.cut(df['LATITUDE'], bins=bins, labels=[1,2,3,4], right=False)

    # Filtrar el dataframe original para obtener solo aquellos registros que tienen un valor ZONE
    crashes_four_zones = pd.DataFrame() 
    crashes_four_zones = df[['ZONE', 'CRASH_DATE']]
    
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
    
    # Convertir la columna CRASH_DATE a datetime
    crashes_four_zones['CRASH_DATE'] = pd.to_datetime(crashes_four_zones['CRASH_DATE'])

    # Extraer el año de la fecha y crear una nueva columna 'YEAR'
    crashes_four_zones['YEAR'] = crashes_four_zones['CRASH_DATE'].dt.year

    # Agrupar por ZONE y YEAR y contar el número de registros para cada combinación
    sum_crashes_by_year_zone = crashes_four_zones.groupby(['ZONE', 'YEAR']).size().reset_index(name='SUM_CRASHES')

    print(sum_crashes_by_year_zone)


    # Ajuste del modelo
    model = ols('SUM_CRASHES ~ ZONE', data=sum_crashes_by_year_zone).fit()

    # ANOVA
    anova_table = sm.stats.anova_lm(model, typ=2)

    print(anova_table)
    
        
    # Definición de las zonas
    zonas = [
        41.644670,
        41.739197,
        41.833725,
        41.928252,
        42.022780
    ]

    # Crear datos para las líneas horizontales
    data = {
        'latitude': [],
        'longitude_start': [],
        'longitude_end': []
    }

    for zona in zonas:
        data['latitude'].append(zona)
        data['longitude_start'].append(-87.9)
        data['longitude_end'].append(-87.6)

    # Crear un DataFrame vacío solo para inicializar el mapa
    lines_map = pd.DataFrame({
        'lat': [],
        'lon': []
    })

    # Inicializar el mapa
    fig = px.scatter_mapbox(lines_map, lat='lat', lon='lon', zoom=10, center=dict(lat=41.833725, lon=-87.75), title="Prueba anova 4 zonas por choques", color=sum_crashes_by_year_zone['SUM_CRASHES'])

    # Normalización de la columna SUM_CRASHES para obtener colores
    norm = plt.Normalize(sum_crashes_by_year_zone['SUM_CRASHES'].min(), sum_crashes_by_year_zone['SUM_CRASHES'].max())
    colors = plt.cm.plasma_r(norm(sum_crashes_by_year_zone['SUM_CRASHES']))

    for i in range(len(zonas) - 1):
        lat_center = (zonas[i] + zonas[i+1]) / 2
        fig.add_trace(go.Scattermapbox(
            lat=[zonas[i], zonas[i], zonas[i+1], zonas[i+1], zonas[i]],
            lon=[-87.9, -87.6, -87.6, -87.9, -87.9],
            mode='lines+text',
            fill='toself',
            fillcolor=f'rgba({int(colors[i][0]*255)}, {int(colors[i][1]*255)}, {int(colors[i][2]*255)}, 0.5)',  #Color con transparencia
            text=str(i+1),
            textposition="middle center",
            textfont=dict(size=18, color='white'),
            hoverinfo='text',
            hovertext=f"ZONE {sum_crashes_by_year_zone['ZONE'][i]}: {sum_crashes_by_year_zone['SUM_CRASHES'][i]} crashes"
        ))

    fig.update_layout(mapbox_style="open-street-map")
    fig.show()
        
    
    

if __name__ == "__main__":
    main()