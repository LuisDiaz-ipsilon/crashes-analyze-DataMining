import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import warnings
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.cluster import KMeans

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import seaborn as sns

def main():
    data = pd.read_csv("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    warnings.filterwarnings("ignore")
    
    # Selecciona las columnas LATITUDE y LONGITUDE
    coordinates = data[['LATITUDE', 'LONGITUDE']]

    # Especifica el número de clústeres que deseas
    n_clusters = 5  # Puedes ajustar este valor según tus necesidades

    # Aplica K-means para agrupar las ubicaciones geográficas
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    data['cluster'] = kmeans.fit_predict(coordinates)

    
    fig = px.scatter_mapbox(data, lat='LATITUDE', lon='LONGITUDE', 
                        title="K-means de los choques",
                        color='cluster',  # Colorea los puntos por el clúster asignado
                        size_max=71,  # Tamaño máximo de los puntos
                        zoom=9, mapbox_style='open-street-map')
    
    fig.show()


    
if __name__ == "__main__":
    main()