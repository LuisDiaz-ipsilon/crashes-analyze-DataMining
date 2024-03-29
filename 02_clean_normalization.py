import pandas as pd


def main():

    #Obtenemos el .csv para pandas

    df = pd.read_csv("Traffic_Crashes_-_Crashes.csv")


    #Solo requeriremos de las siguientes columnas:
    selec_col = [
        'CRASH_DATE',
        'HIT_AND_RUN_I',
        'PRIM_CONTRIBUTORY_CAUSE',
        'SEC_CONTRIBUTORY_CAUSE',
        'INJURIES_TOTAL',
        'INJURIES_FATAL',
        'INJURIES_INCAPACITATING',
        'INJURIES_NON_INCAPACITATING',
        'CRASH_HOUR',
        'CRASH_DAY_OF_WEEK',
        'CRASH_MONTH',
        'LATITUDE',
        'LONGITUDE'
    ]

    df = df[selec_col]

    #Limpieza
    #primero retiramos la hora del campo CRASH_DATE, ya que la tenemos redundante con el campo CRASH_HOUR
    df['CRASH_DATE'] = df['CRASH_DATE'].str.split(' ').str[0]

    #En la columna HIT_AND_RUN_I tenemos 2 tipos de valores "Y" y NaN, por lo que vamos a rellenar con "N"
    #Indicando que NO hubo huida 
    df['HIT_AND_RUN_I'] = df['HIT_AND_RUN_I'].fillna(0)

    df['HIT_AND_RUN_I'] = df['HIT_AND_RUN_I'].replace('Y', '1')

    #Tenemos dos columnas de causas y para nuestros efectos requerimos que esten unidas en una nueva CAUSES
    df['CAUSES'] = df['PRIM_CONTRIBUTORY_CAUSE'] + ', ' + df['SEC_CONTRIBUTORY_CAUSE']

    df = df.drop('PRIM_CONTRIBUTORY_CAUSE', axis=1)
    df = df.drop('SEC_CONTRIBUTORY_CAUSE', axis=1)


    #Vemos que las injurias son varios campos, nos interesan solo 2 cosas, si es necesario una ambulancia
    #y si hay muertos(FATAL). Por lo que unificaremos todo tipo de injurias en AMBULANCE_REQUIRED
    #y si hubo una accidente fatal tendremos FATAL_ACCIDENT

    df['AMBULANCE_REQUIRED'] = df['INJURIES_TOTAL'].apply(lambda x: 'Y' if x > 0 else 'N')
    df['AMBULANCE_REQUIRED'] = df['INJURIES_TOTAL'].replace('Y', '1')
    df['AMBULANCE_REQUIRED'] = df['INJURIES_TOTAL'].replace('N', '0')

    df['FATAL_ACCIDENT'] = df['INJURIES_FATAL'].apply(lambda x: 'Y' if x > 0 else 'N')
    df['FATAL_ACCIDENT'] = df['INJURIES_FATAL'].replace('Y', '1')
    df['FATAL_ACCIDENT'] = df['INJURIES_FATAL'].replace('N', '0')

    df = df.drop('INJURIES_TOTAL', axis=1)
    df = df.drop('INJURIES_INCAPACITATING', axis=1)
    df = df.drop('INJURIES_NON_INCAPACITATING', axis=1)

    #limpiemos la LATITUDE y LONGITUDE ya que algunos valores son cero y en nuestro caso nos interesan los puntos geograficos.
    mask = (df['LATITUDE'] == 0) | (pd.isna(df['LATITUDE']))
    df = df[~mask]

    mask = (df['LONGITUDE'] == 0) | (pd.isna(df['LONGITUDE']))
    df = df[~mask]

    #Ordenamos el dataframe
    order_col = [
        'CRASH_DATE',
        'HIT_AND_RUN_I',
        'CAUSES',
        'AMBULANCE_REQUIRED',
        'FATAL_ACCIDENT',
        'CRASH_HOUR',
        'CRASH_DAY_OF_WEEK',
        'CRASH_MONTH',
        'LATITUDE',
        'LONGITUDE'
    ]

    df = df[order_col]

    #Comprobamos resultados
    print(df.head(10))

    #Creamos un nuevo .csv con los cambios
    try:
        df.to_csv('Traffic_Crashes_-_Crashes_cleaned_normalized.csv', index=False)
        print("Traffic_Crashes_-_Crashes_cleaned_normalized.csv creado correctamente")
    except Exception as e:
        print(e)

    


if __name__ == "__main__":
    main()