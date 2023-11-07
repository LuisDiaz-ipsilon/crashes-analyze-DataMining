import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import warnings
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import seaborn as sns

def main():
    data_original = pd.read_csv("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    warnings.filterwarnings("ignore")
    
    #se hara una serie de tiempo de los choques que han sido por 
    # texto, alcohol y se hara la prediccion en tiempo
    
    data_original['CRASH_DATE'] = pd.to_datetime(data_original['CRASH_DATE'])
    data_original = data_original[data_original['CRASH_DATE'].dt.year == 2022]
    crashes_by_date_cause_texting_2022 = data_original[['CRASH_DATE', 'CAUSES']]
    
    crashes_by_date_cause_texting_2022 = crashes_by_date_cause_texting_2022[crashes_by_date_cause_texting_2022['CAUSES'].str.contains("TEXT")]   
    # Asegúrate de que 'CRASH_DATE' esté en formato de fecha
    crashes_by_date_cause_texting_2022['CRASH_DATE'] = pd.to_datetime(crashes_by_date_cause_texting_2022['CRASH_DATE'])
    
    # Agrupa los registros por semana y cuenta la cantidad de registros en cada semana
    weekly_counts = crashes_by_date_cause_texting_2022.resample('W', on='CRASH_DATE').size()

    # Crea un nuevo DataFrame con las semanas como índice y la suma de registros como columna
    crashes_sum_by_week_cause_texting_2022 = pd.DataFrame(weekly_counts, columns=['Total_Registros'])

    # Esto dará como resultado un DataFrame 'crashes_sum_by_week_cause_texting_2022' con las semanas como índice
    # y la columna 'Total_Registros' que contiene la suma de registros en cada semana.

    # Si deseas un DataFrame con exactamente 52 semanas, puedes rellenar las semanas faltantes con ceros.
    # Esto asegurará que tengas 52 registros en total.
    all_weeks = pd.date_range(start=crashes_by_date_cause_texting_2022['CRASH_DATE'].min(),
                            end=crashes_by_date_cause_texting_2022['CRASH_DATE'].max(),
                            freq='W')

    crashes_sum_by_week_cause_texting_2022 = crashes_sum_by_week_cause_texting_2022.reindex(all_weeks, fill_value=0)
    
    print(crashes_sum_by_week_cause_texting_2022)
    

    plt.figure(figsize=(12, 6))
    crashes_sum_by_week_cause_texting_2022['Total_Registros'].plot()
    plt.title('Choques con causados por textear 2022 con prediccion.')
    plt.xlabel('Fecha')
    plt.ylabel('Total de Registros')
    plt.grid(True)

    plt.savefig("images/timeSeries_forecasting_crashesh_texting.png")
    plt.close()
    
    # Ajustar un modelo ARIMA a tus datos
    p, d, q = 1, 1, 1  # Ajusta los órdenes ARIMA según tus datos
    model = sm.tsa.ARIMA(crashes_sum_by_week_cause_texting_2022['Total_Registros'], order=(p, d, q))
    results = model.fit()

    # Obtener los valores pronosticados
    n = 26  # Número de semanas hacia el futuro que deseas pronosticar
    forecast = results.get_forecast(steps=n)

    # Obtener intervalos de confianza
    forecast_mean = forecast.predicted_mean
    forecast_conf_int = forecast.conf_int(alpha=0.25)  # Establece el nivel de confianza deseado

    # Generar las fechas para el pronóstico
    last_date = crashes_sum_by_week_cause_texting_2022.index[-1]
    forecast_dates = [last_date + pd.DateOffset(weeks=i) for i in range(1, n+1)]

    # Graficar la serie de tiempo y los intervalos de confianza
    plt.figure(figsize=(12, 6))
    plt.plot(crashes_sum_by_week_cause_texting_2022['Total_Registros'], label='Serie de Tiempo', color='blue')
    plt.plot(forecast_dates, forecast_mean, label='Pronóstico', color='red')
    plt.fill_between(forecast_dates, forecast_conf_int['lower Total_Registros'], forecast_conf_int['upper Total_Registros'], color='pink', alpha=0.6, label='Intervalo de Confianza')
    plt.legend()
    plt.xlabel('Semana')
    plt.ylabel('Total de Registros')
    plt.title('Pronóstico con Intervalos de Confianza para choques provocados por texting')
    
    plt.savefig("images/timeSeries_forecasting_crashesh_texting_forecasting.png")
    plt.close()

    
if __name__ == "__main__":
    main()