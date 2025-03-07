# # %%
# import pandas as pd
# import polyline
# import numpy as np
# import os 
# from pathlib import Path
# parent_dir = Path(os.getcwd()).resolve().parent
# os.chdir(parent_dir)
# from utils import adjust_pace, treat_date, treat_distance_and_time, parse_coordinates, decode_polyline
# import pydeck as pdk 

# def get_individual_activities():
#     df = pd.read_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/individual_activity.csv')
#     return df

# df = get_individual_activities()
# pd.set_option('display.max_columns', None)


# df = treat_distance_and_time(df)
# df['pace'] = np.round((df['time_min'] / df['distance_km']),2)
# df['pace_adjusted'] = df.pace.apply(adjust_pace)
# df.drop(columns=['pace'], inplace=True)
# df.rename(columns={'pace_adjusted': 'pace'}, inplace=True)

# df = parse_coordinates(df)

# df = treat_date(df)

# df['distance_km'] = df['distance_km'].astype(float)
# df['time_min'] = df['time_min'].astype(float)
# df['pace'] = df['pace'].replace(':', '.', regex=True).astype(float)
# df['average_heartrate'] = df['average_heartrate'].astype(float)
# df['max_heartrate'] = df['max_heartrate'].astype(float)
# df['rest_during_run_min'] = df['rest_during_run_min'].astype(float)
# df['kudos_count'] = df['kudos_count'].astype(int)

# #  decoding polyline
# df = decode_polyline(df)

# #  documentation: https://deckgl.readthedocs.io/en/latest/gallery/path_layer.html

# # %%

# from utils import prepare_geojson

# geojson = prepare_geojson(df)

# if len(geojson.path) > 0:
#     init_lon, init_lat = geojson.path[0][0]
# else:
#     init_lon, init_lat = -40.0, -20.0

# view_state = pdk.ViewState(
#     latitude = init_lat,
#     longitude=init_lon,
#     zoom=7,
#     pitch=10,
# )

# layer = pdk.Layer(
#     "PathLayer",
#     data=geojson,
#     get_path="path",
#     get_color='color',  
#     get_width=15,           
#     width_min_pixels=2
# )

# r = pdk.Deck(layers=[layer], initial_view_state=view_state)
# r.show()

# %%import streamlit as st
import plotly.express as px
import pandas as pd
import os 
from pathlib import Path
parent_dir = Path(os.getcwd()).resolve().parent
os.chdir(parent_dir)
from utils import  prepare_geojson, get_individual_activities, treat_distance_and_time, adjust_pace, parse_coordinates, treat_date, to_float, random_rgb, decode_polyline
import pydeck as pdk
import numpy as np


# %%
df = get_individual_activities()
df = treat_distance_and_time(df)
df['pace'] = np.round((df['time_min'] / df['distance_km']),2)
df['pace_adjusted'] = df.pace.apply(adjust_pace)
df.drop(columns=['pace'], inplace=True)
df.rename(columns={'pace_adjusted': 'pace'}, inplace=True)

df = parse_coordinates(df)
df = treat_date(df)
df = to_float(df)
# %%
geojson = pd.DataFrame({
"date": df["start_date"],  # Data da atividade
"name": [f"Rota {i+1}" for i in range(len(df))],  # Nome da atividade
"color": "#ed1c24",  # Cor fixa, pode personalizar
"path": df["map_polyline"]  # Lista de listas de coordenadas
})

geojson["color"] = geojson["color"].apply(lambda x: random_rgb())

geojson = geojson[geojson['path'].notnull()]
decode_polyline(df)
def swap_coords(coord_list):
    return [[i[1], i[0]] for i in coord_list]

geojson['path'] = geojson['path'].apply(swap_coords)
geojson.reset_index(drop=True, inplace=True)