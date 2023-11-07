import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import warnings
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import seaborn as sns

def main():
    data_original = pd.read_csv("Traffic_Crashes_-_Crashes.csv")
    warnings.filterwarnings("ignore")
    
    # Asegúrate de que la columna 'CRASH_DATE' esté en formato de fecha
    data_original['CRASH_DATE'] = pd.to_datetime(data_original['CRASH_DATE'])

    # Filtra los datos para el año 2022
    data_original = data_original[data_original['CRASH_DATE'].dt.year == 2022]
    data_original = data_original[data_original['CRASH_DATE'].dt.month == 12]

    
    crashes_hour_cause_speed = data_original[['CRASH_HOUR', 'POSTED_SPEED_LIMIT', 'WEATHER_CONDITION']]
    
    print(crashes_hour_cause_speed)
    
    crashes_hour_cause_speed = crashes_hour_cause_speed[crashes_hour_cause_speed['WEATHER_CONDITION'].isin(['RAIN', # Ignorar luz roja
                                                                        'CLOUDY/OVERCAST', # Primerizo
                                                                        'SNOW', # escribir texto
                                                                        'FOG/SMOKE/HAZE' ])]

    print(crashes_hour_cause_speed)
    
    count_df = crashes_hour_cause_speed.groupby(['CRASH_HOUR', 'POSTED_SPEED_LIMIT', 'WEATHER_CONDITION']).size().reset_index(name='COUNT')

    # Crear un gráfico de dispersión
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=count_df, x='CRASH_HOUR', y='POSTED_SPEED_LIMIT', hue='WEATHER_CONDITION', palette='coolwarm', size='COUNT', sizes=(20, 200), alpha=0.6)

    plt.title('Choque por cada hora y el limite de velocidad del y tipo de clima 2022 diciembre')
    plt.xlabel('Hora del choque')
    plt.ylabel('longitud')

    # Personalizar la leyenda
    plt.legend(title='Causa del Choque')

    plt.savefig("images/crash_hour_posted_limit_tiempo_2022_dic.png")
    plt.close()

    

    
    """
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=crashes_hour_cause_speed, x='CRASH_HOUR', y='POSTED_SPEED_LIMIT', palette='coolwarm')
    plt.title('Choque por cada hora y el limite de velocidad publicado')
    plt.xlabel('Hora del choque')
    plt.ylabel('Limite de velocidad mostrado')
    plt.savefig("images/crash_hour_posted_speed_limit.png")
    plt.close()
    """
    
if __name__ == "__main__":
    main()