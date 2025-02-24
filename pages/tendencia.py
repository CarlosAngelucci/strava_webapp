import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os
from utils import process_strava_data, prepare_df_for_week_analysis
import pydeck as pdk


def show():
    df = pd.read_csv("data/activities.csv")
    df = process_strava_data(df)
    df['start_latitude'] = df['start_latitude'].astype(float)
    df['start_longitude'] = df['start_longitude'].astype(float)
    df['end_latitude'] = df['end_latitude'].astype(float)
    df['end_longitude'] = df['end_longitude'].astype(float)
    df = df[df['type_run'] == 'Outdoor']
    df = df[['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude']]
    data_dict = df.to_dict(orient='records')

    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude = -20.3478,
                longitude=-40.2949,
                zoom=13,
                pitch=90,
            ),
            layers = [
                pdk.Layer(
                    "HexagonLayer",
                    data = data_dict,
                    get_position = ['start_longitude', 'start_latitude'],
                    radius = 50,
                    elevation_scale = 4,
                    elevation_range = [0, 200],
                    pickable = True,
                    extruded = True
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data = data_dict,
                    get_position = ['end_longitude', 'end_latitude'],
                    radius = 500,
                    elevation_scale = 4,
                    elevation_range = [0, 500],
                    pickable = True,
                    extruded = True
                )
            ]
        )
        )
    