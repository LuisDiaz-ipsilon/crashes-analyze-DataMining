import pandas as pd
from scipy.stats import f_oneway

def main():
    """
    Probar si la hora gris en chicago es causa de mayores choques durante el 2022 
    Se toma hora gris 
    """
    
    
    df = pd.read_csv("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    data = df[['CRASH_DATE', 'CRASH_HOUR', 'CAUSES']].copy()
    
    #Filtrar para año 2022    
    data['CRASH_DATE'] = pd.to_datetime(data['CRASH_DATE'])
    data = data[data['CRASH_DATE'].dt.year == 2021]
    # Filtra por el mes deseado
    #data = data[data['CRASH_DATE'].dt.month == 6]
    
    #Filtrar por causas
    causas = ['VISION OBSCURED', 'EXCEEDING SAFE SPEED FOR CONDITIONS']
    # Filtra las filas que contienen alguna de las frases en la columna "CAUSES"
    data = data[data['CAUSES'].str.contains('|'.join(causas))]
    
    print(data)
        
    # Crea una nueva columna para clasificar las horas en periodos del día.
    #data['PERIODO_DEL_DIA'] = pd.cut(data['CRASH_HOUR'], bins=[0, 5, 7, 16, 19, 24], labels=['Noche', 'Amanecer', 'Dia', 'Atardecer', 'N'])
    data['PERIODO_DEL_DIA'] = pd.cut(data['CRASH_HOUR'], bins=[0,1,2, 3, 4, 5, 7,8,9,10,11,12,13,14,15, 16, 19,20,21,22,23, 24], labels=['Noche1', 'Noche2', 'Noche3', 'Noche4', 'Noche5', 'Amanecer', 'Dia8', 'Dia9', 'Dia10', 'Dia11', 'Dia12', 'Dia13', 'Dia14', 'Dia15', 'Dia16', 'Atardecer', 'Noche20', 'Noche21', 'Noche22', 'Noche23', 'Noche24'])


    # Mapea los valores 'Amanecer', 'Tarde' y 'Otros'.
    #data['PERIODO_DEL_DIA'] = data['PERIODO_DEL_DIA'].map({'Amanecer': 'Amanecer', 'Atardecer': 'Atardecer', 'Noche': 'Dia/Noche', 'Dia': 'Dia/Noche', 'N': 'Dia/Noche'})

    # Realiza el análisis de varianza (ANOVA).
    #grupos = [data[data['PERIODO_DEL_DIA'] == periodo]['CRASH_HOUR'] for periodo in ['Amanecer', 'Atardecer', 'Dia/Noche']]
    grupos = [data[data['PERIODO_DEL_DIA'] == periodo]['CRASH_HOUR'] for periodo in ['Amanecer', 'Atardecer', 'Noche1', 'Noche2', 'Noche3', 'Noche4', 'Noche5', 'Dia8', 'Dia9', 'Dia10', 'Dia11', 'Dia12', 'Dia13', 'Dia14', 'Dia15', 'Dia16', 'Noche20', 'Noche21', 'Noche22', 'Noche23']]
    resultado_anova = f_oneway(*grupos)
    
    # Imprime los resultados.
    print(resultado_anova)
    
    # Cuenta la cantidad de choques en cada periodo del día.
    counts_por_periodo = data['PERIODO_DEL_DIA'].value_counts()

    # Muestra los resultados.
    print(counts_por_periodo)

if __name__ == "__main__":
    main()