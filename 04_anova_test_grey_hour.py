import pandas as pd
from scipy.stats import f_oneway
from sklearn.cluster import KMeans
import warnings

def main():
    warnings.filterwarnings("ignore")
    """
    Probar si la hora gris en chicago es causa de mayores choques en los años registrados 2017-2022
    La hora gris en el amancer y el anochecer en chicago alrededor de 07:18:11 AM y 06:31:42 PM respectivamente
    Tambien se verifico la zona donde se igualan las condiciones mostradas en el video donde son carreteras que en nuestro caso es el cluster 3
    Video: https://youtu.be/Wvf9DDtIgT4?si=s4ShpmKT9QIiBH8R
    """
    
    df = pd.read_csv("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    data = df[['CRASH_DATE', 'CRASH_HOUR', 'CAUSES', 'LATITUDE', 'LONGITUDE']].copy()
    
    # Selecciona las columnas LATITUDE y LONGITUDE
    coordinates = data[['LATITUDE', 'LONGITUDE']]
    # Especifica el número de clústeres que deseas
    n_clusters = 5 
    # Aplica K-means para agrupar las ubicaciones geográficas
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    data['CLUSTER'] = kmeans.fit_predict(coordinates)
    
    #Filtrar por cluster 3
    data_c3 = data[data['CLUSTER'] == 3]
    
    #Filtrar por causas
    causas = ['VISION OBSCURED', 'EXCEEDING SAFE SPEED FOR CONDITIONS']
    # Filtra las filas que contienen alguna de las frases en la columna "CAUSES"
    data_c3 = data_c3[data_c3['CAUSES'].str.contains('|'.join(causas))]
            
    # Crea una nueva columna para clasificar las horas en periodos del día.
    data_c3['PERIODO_DEL_DIA'] = pd.cut(data_c3['CRASH_HOUR'], bins=[0,1,2,3,4,5, 7,8,9,10,11,12,13,14,15,16, 19,20,21,22,23,24], labels=['Noche1', 'Noche2', 'Noche3', 'Noche4', 'Noche5', 'Amanecer', 'Dia8', 'Dia9', 'Dia10', 'Dia11', 'Dia12', 'Dia13', 'Dia14', 'Dia15', 'Dia16', 'Atardecer', 'Noche20', 'Noche21', 'Noche22', 'Noche23', 'Noche24'])

    #ANOVAs
    grupos = [data_c3[data_c3['PERIODO_DEL_DIA'] == periodo]['CRASH_HOUR'] for periodo in ['Amanecer', 'Atardecer', 'Noche1', 'Noche2', 'Noche3', 'Noche4', 'Noche5', 'Dia8', 'Dia9', 'Dia10', 'Dia11', 'Dia12', 'Dia13', 'Dia14', 'Dia15', 'Dia16', 'Noche20', 'Noche21', 'Noche22', 'Noche23']]
    resultado_anova = f_oneway(*grupos)
    
    
    print(f"\nProbar si la hora gris en chicago es causa de mayores choques en los años registrados 2017-2022\nLa hora gris en el amancer y el anochecer en chicago alrededor de 07:18:11 AM y 06:31:42 PM respectivamente\nTambien se verifico la zona donde se igualan las condiciones mostradas en el video donde son carreteras que en nuestro caso es el cluster 3\nVideo: https://youtu.be/Wvf9DDtIgT4?si=s4ShpmKT9QIiBH8R \n")
    #Impresion del anova
    print(resultado_anova)
    print("\nEn nuestro caso se tomo una prueba anova F con una donde F dio un resultado muy grande en comparacion de los diferentes horas por lo que si se indica una diferencia")
    print("\nY como el valor de p es 0 o muy cercano a cero lo que sugiere que hay diferencias significativas")
    
    # Cuenta la cantidad de choques en cada periodo del día.
    crashes_by_hour = data_c3['PERIODO_DEL_DIA'].value_counts()
    print(crashes_by_hour)

if __name__ == "__main__":
    main()