import pandas as pd
import plotly.express as px




def main():
	dt = pd.read_csv("Traffic_Crashes_-_Crashes_1.04_cleaned_normalized.csv")

	px.set_mapbox_access_token(open("mining_crashes.mapbox_token").read())
	fig = px.scatter_mapbox(dt, lat="LATITUDE", lon="LONGITUDE")
	fig.update_layout(mapbox_style="open-street-map")
	fig.show()

	

if __name__ == "__main__":
   main()