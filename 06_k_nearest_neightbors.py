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
    
    #Precisión del modelo k-NN: 61.08%
    #Se clasificara cada tipo de condicion del ambiente en los choques y su tipo de costo
    #Clasificacion de choques: CLEAR, RAIN, SNOW, CLOUDY/OVERCAST, FREEZING RAIN/DRIZZLE, 
    #                          FOG/SMOKE/HAZE,* SLEET/HAIL,* SEVERE CROSS WIND GATE*
    #                          (BLOWING SAND, SOIL, DIRT)*
    #Clasifiacion de costo en daños: 1, 2, 3, 
    
    
    crashes_weather_condition_damage = data_original[['WEATHER_CONDITION', 'DAMAGE']]
    
    mapping = {
        '$500 OR LESS': 1,
        '$501 - $1,500': 2,
        'OVER $1,500': 3
    }
    
    crashes_weather_condition_damage['DAMAGE'] = crashes_weather_condition_damage['DAMAGE'].replace(mapping)
    
    # Filtra los registros en los que 'WEATHER_CONDITION' no sea 'UNKNOWN' ni 'OTHER'
    crashes_weather_condition_damage = crashes_weather_condition_damage[~crashes_weather_condition_damage['WEATHER_CONDITION'].isin(['UNKNOWN', 'OTHER', 'BLOWING SAND, SOIL, DIRT', 'FOG/SMOKE/HAZE', 'SLEET/HAIL', 'SEVERE CROSS WIND GATE'])]
    
    print(crashes_weather_condition_damage)
    
    # Codificar la columna 'WEATHER_CONDITION' a valores numéricos
    le = LabelEncoder()
    crashes_weather_condition_damage['WEATHER_CONDITION'] = le.fit_transform(crashes_weather_condition_damage['WEATHER_CONDITION'])
    
    
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=crashes_weather_condition_damage, x='WEATHER_CONDITION', y='DAMAGE', hue='WEATHER_CONDITION', palette='coolwarm')
    plt.title('Relación entre DAMAGE y Condición Meteorológica')
    plt.xlabel('Condición Meteorológica')
    plt.ylabel('DAMAGE')
    plt.legend(title='Condición Meteorológica', loc='upper right', bbox_to_anchor=(1.25, 1))
    plt.savefig("images/clasiffication_WEATHER_CONDITION_DAMAGE_COST.png")
    plt.close()

    
    # Dividir los datos en conjunto de entrenamiento y prueba
    X = crashes_weather_condition_damage[['WEATHER_CONDITION']]
    y = crashes_weather_condition_damage['DAMAGE']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    # Crear y entrenar el modelo k-NN
    k = 3  # Puedes ajustar el valor de k según tus necesidades
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)

    # Realizar predicciones en el conjunto de prueba
    y_pred = knn.predict(X_test)

    # Calcular la precisión del modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo k-NN: {accuracy * 100:.2f}%")
    
if __name__ == "__main__":
    main()