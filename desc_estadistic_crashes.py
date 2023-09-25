import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


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

def timeSeries_sum_ambulances_by_day_month_allyears(url : str):
    df = pd.read_csv(url)
    
    print(df['LATITUDE'].describe())
    print(df['LONGITUDE'].describe())
    


def main():

	#timeSeries_sum_ambulances_by_year("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
    #timeSeries_sum_ambulances_by_month("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
    timeSeries_sum_ambulances_by_day_month_allyears("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    
	

if __name__ == "__main__":
    main()