# %%
import pandas as pd
import polyline
import numpy as np
import os 
from pathlib import Path
parent_dir = Path(os.getcwd()).resolve().parent
os.chdir(parent_dir)
from utils import adjust_pace, treat_date, treat_distance_and_time, parse_coordinates

def get_individual_activities():
    df = pd.read_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/individual_activity.csv')
    return df

df = get_individual_activities()
pd.set_option('display.max_columns', None)


df = treat_distance_and_time(df)
df['pace'] = np.round((df['time_min'] / df['distance_km']),2)
df['pace_adjusted'] = df.pace.apply(adjust_pace)
df.drop(columns=['pace'], inplace=True)
df.rename(columns={'pace_adjusted': 'pace'}, inplace=True)

df = parse_coordinates(df)

df = treat_date(df)

df['distance_km'] = df['distance_km'].astype(float)
df['time_min'] = df['time_min'].astype(float)
df['pace'] = df['pace'].replace(':', '.', regex=True).astype(float)
df['average_heartrate'] = df['average_heartrate'].astype(float)
df['max_heartrate'] = df['max_heartrate'].astype(float)
df['rest_during_run_min'] = df['rest_during_run_min'].astype(float)
df['kudos_count'] = df['kudos_count'].astype(int)

# %%
#  decoding polyline
df['map_polyline'] = df['map_polyline'].apply(lambda x: polyline.decode(x) if isinstance(x, str) else None)
df['map_summary_polyline'] = df['map_summary_polyline'].apply(lambda x: polyline.decode(x) if isinstance(x, str) else None)

df['map_polyline'] = df['map_polyline'].apply(lambda x: [list(i) for i in x] if isinstance(x, list) else None)
df['map_summary_polyline'] = df['map_summary_polyline'].apply(lambda x: [list(i) for i in x] if isinstance(x, list) else None)

# %%
import json
import pydeck as pdk 
import random 

geojson = pd.DataFrame({
    "name": [f"Rota {i+1}" for i in range(len(df))],  # Nome da atividade
    "color": "#ed1c24",  # Cor fixa, pode personalizar
    "path": df["map_polyline"]  # Lista de listas de coordenadas
})

#  generate a function that creates random rgbs for each route
def random_rgb():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

geojson["color"] = geojson["color"].apply(lambda x: random_rgb())

geojson = geojson[geojson['path'].notnull()]
def swap_coords(coord_list):
    return [[i[1], i[0]] for i in coord_list]

geojson['path'] = geojson['path'].apply(swap_coords)
geojson.reset_index(drop=True, inplace=True)


if len(geojson.path) > 0:
    init_lon, init_lat = geojson.path[0][0]
else:
    init_lon, init_lat = -40.0, -20.0  # Algum fallback

# %%
view_state = pdk.ViewState(
    latitude = init_lat,
    longitude=init_lon,
    zoom=7,
    pitch=10,
)

layer = pdk.Layer(
    "PathLayer",
    data=geojson,
    get_path="path",
    get_color='color',  
    get_width=15,           
    width_min_pixels=2
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.show()

#  documentation: https://deckgl.readthedocs.io/en/latest/gallery/path_layer.html