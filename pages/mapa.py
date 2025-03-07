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

    with st.container():
        st.markdown("## 🛤️ Conexões Entre Início e Fim das Corridas")
        st.markdown("Este mapa exibe a relação entre os pontos de início e fim das corridas, destacando padrões de deslocamento.")
        
        GREEN_RGB = [0, 255, 0, 200] #  start point
        RED_RGB = [240, 100, 0, 200] # end point

        arc_layer = pdk.Layer(
            "ArcLayer",
            data=df,
            get_source_position = ["start_longitude", 'start_latitude'],
            get_target_position = ['end_longitude','end_latitude'],
            get_source_color = GREEN_RGB,
            get_target_color = RED_RGB,
            get_width = 5,
            pickable = True,
            auto_highlight = True,
        )

        view_state = pdk.ViewState(
            latitude = -20.3478,
            longitude=-40.2949,
            zoom=12,
            pitch=90,
        )

        st.pydeck_chart(pdk.Deck(layers=[arc_layer], initial_view_state=view_state))

    with st.container():
        st.markdown("## 📍 Heatmap das Corridas")
        st.markdown("Este mapa mostra a densidade das corridas realizadas com base nos pontos de início.")

        hex_layer = pdk.Layer("HexagonLayer",
                data = data_dict,
                get_position = ['start_longitude', 'start_latitude'],
                radius = 50,
                elevation_scale = 4,
                elevation_range = [0, 200],
                pickable = True,
                extruded = True)
        hex_view_state = pdk.ViewState(
            latitude = -20.3478,
            longitude=-40.2949,
            zoom=12,
            pitch=90,
        )
        st.pydeck_chart(pdk.Deck(layers = [hex_layer], initial_view_state=hex_view_state))
    



#  pydeck documentation: https://deckgl.readthedocs.io/en/latest/