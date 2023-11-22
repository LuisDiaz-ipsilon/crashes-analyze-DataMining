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

from wordcloud import WordCloud

def main():
    data = pd.read_csv("Traffic_Crashes_-_Crashes_cleaned_normalized.csv")
    warnings.filterwarnings("ignore")
    
    # Concatenar todas las causas en una sola cadena
    all_causes = ' '.join(data['CAUSES'].astype(str).values)

    # Crear la word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_causes)

    # Mostrar la word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig("images/09_world_cloud_causes_crashes.png")
    plt.close()
    
if __name__ == "__main__":
    main()