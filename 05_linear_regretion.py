import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import warnings
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression



def main():
    df = pd.read_csv("Traffic_Crashes_-_Crashes.csv")
    
    #Regresion lineal para conocer si la hora del choque podria ser un indice de cantidad de lesiones en un choque
    #*************************************************************IMPORANTE********************** 
    # LA HORA 1 SON LAS 6 PM y la hora 24 son las 5 AM, esto para saber si 
    # la noche hace que sea mas posible una lesion
    
    #Coeficiente (pendiente): -0.0036586476147908143
    #Intercepto: 0.242187892070799
    
    crashes_hour_and_injuries = df[['CRASH_HOUR', 'INJURIES_TOTAL']]
    
    crashes_hour_and_injuries['CRASH_HOUR'] = crashes_hour_and_injuries['CRASH_HOUR'].apply(lambda x: x if 0 <= x <= 23 else np.nan)        
    
    # Mapeo de horas antiguas a nuevas
    hour_mapping = {
        #hora nueva: hora anterior 
        1: 6, #6AM
        2: 7,
        3: 8,
        4: 9,
        5: 10,
        6: 11,
        7: 12,
        8: 13,
        9: 14,
        10: 15,
        11: 16,
        12: 17, # 5PM
        13: 18,
        14: 19,
        15: 20,
        16: 21,
        17: 22,
        18: 23,
        19: 0,
        20: 1,
        21: 2,
        22: 3,
        23: 4,
        24: 5
    }

    
    # Reemplazo de horas
    crashes_hour_and_injuries['CRASH_HOUR'] = crashes_hour_and_injuries['CRASH_HOUR'].replace(hour_mapping)
        
    # Calcula el promedio de INJURIES_TOTAL para cada hora
    crashes_by_hour_prom = crashes_hour_and_injuries.groupby('CRASH_HOUR')['INJURIES_TOTAL'].mean().reset_index()

    crashes_by_hour_prom = crashes_by_hour_prom.rename(columns={'INJURIES_TOTAL': 'INJURIES_PROM'})
    print(crashes_by_hour_prom)

    plt.scatter(crashes_by_hour_prom['CRASH_HOUR'], crashes_by_hour_prom['INJURIES_PROM'])
    plt.xlabel('Hora del Accidente')
    plt.ylabel('Promedio de Lesiones')
    plt.title('Dispersión del promedio de Lesiones por Hora del Accidente HORA 1: 6 AM, HORA 6: 11 AM, HORA 17: 10 PM')
    #plt.savefig("images/dispersion_crashes_injuries_by_hour_prom_.png")
    plt.close()
    
    
    # Separar las características (X) y la variable objetivo (y)
    X = crashes_by_hour_prom[['CRASH_HOUR']]
    y = crashes_by_hour_prom['INJURIES_PROM']

    model = LinearRegression()
    model.fit(X, y)

    # Hacer predicciones para las mismas horas
    y_pred = model.predict(X)
    
    plt.figure(figsize=(20, 6))

    # Visualizar los resultados
    plt.scatter(X, y, label='Datos reales')
    plt.plot(X, y_pred, color='red', label='Regresión lineal')
    plt.xlabel('Hora del accidente')
    plt.ylabel('Promedio de personas heridas')
    plt.title('Regresion lineal hora a hora y promedio de personas lesionadas 2015-2023\n HORA 1: 6 AM, HORA 6: 11 AM, HORA 17: 10 PM')
    plt.legend()
    #plt.savefig("images/linear_regression_mean_injuries_in_crashes_chicago.png")
    plt.close()

    # Coeficientes de la regresión
    print(f'Coeficiente (pendiente): {model.coef_[0]}')
    print(f'Intercepto: {model.intercept_}')
    
    

if __name__ == "__main__":
    main()