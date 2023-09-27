# Se usara la API de Kaggle para hacer la descarga del dataset. 
# La funcion es  get_csv_from_url que guarda el csv.

import requests
import shutil
from bs4 import BeautifulSoup
import pandas as pd
import io
import re
import os
import json
import kaggle

def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def get_username_and_datasetname(soup):

    atributos_target = {
        "property": "og:url"
    }

    meta_tag = soup.find("meta", attrs = atributos_target)

    data = meta_tag.get('content')

    return data

def get_version_download(soup):
    
    atributos_target= {
        "type": "application/ld+json"
    }

    _meta_tag = soup.find("script", attrs = atributos_target).string
    json_data = json.loads(_meta_tag)

    version = None
    
    if 'version' in json_data:
        version = json_data['version']
    else:
        print("No se encontro la version.")

    return version

def concat_link_download(username_datasetname : str, version: str):
    return 'https://www.kaggle.com'+username_datasetname+'/download?datasetVersionNumber='+version

def get_csv_from_url(url:str) -> pd.DataFrame:

    ruta_kaggle_json = 'C:/Users/luisdev/Desktop/kaggle.json'
    os.environ['KAGGLE_CONFIG_DIR'] = os.path.dirname(ruta_kaggle_json)
    kaggle.api.authenticate()

    dataset_name = "nathaniellybrand/chicago-car-crash-dataset/"
    destination_path = 'C:/Users/luisdev/Documents/FCFM/07 Mineria de Datos/downloadpy'

    try:
        kaggle.api.dataset_download_files(dataset_name, path=destination_path, unzip=True)
    except Exception as e:
        print(e)
        print("Hubo en error al descargar el dataset.")
    else:
        return None
    


def main():
    url = 'https://www.kaggle.com/datasets/nathaniellybrand/chicago-car-crash-dataset'

    #soup = get_soup(url)

    #username_datasetname = get_username_and_datasetname(soup)

    #version = get_version_download(soup)

    #link_download = concat_link_download(username_datasetname, str(version))


    get_csv_from_url(link_download)

if __name__ == "__main__":
    main()
