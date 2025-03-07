import streamlit as st
import plotly.express as px
import pandas as pd
from utils import  prepare_geojson, get_individual_activities, treat_distance_and_time, adjust_pace, parse_coordinates, treat_date, to_float, process_strava_data
import pydeck as pdk
import numpy as np

def show():
    df = get_individual_activities()
    df = treat_distance_and_time(df)
    df['pace'] = np.round((df['time_min'] / df['distance_km']),2)
    df['pace_adjusted'] = df.pace.apply(adjust_pace)
    df.drop(columns=['pace'], inplace=True)
    df.rename(columns={'pace_adjusted': 'pace'}, inplace=True)

    df = parse_coordinates(df)
    df = treat_date(df)
    df = to_float(df)

    geojson = prepare_geojson(df)

    all_activities = pd.read_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/activities.csv')
    all_activities = process_strava_data(all_activities)
    all_activities = all_activities[all_activities['type_run'] == 'Outdoor']

    with st.container():
        st.markdown("## 🏃‍♂️ Individual Activities")
        st.markdown("This map shows the path of each individual activity.")

        #  filtro de data
        unique_dates = geojson['date'].dt.date.unique()
        selected_date = st.date_input("Select a date (optional)", value=None, min_value=min(unique_dates), max_value=max(unique_dates))

        col1, col2, col3 = st.columns([1, 1, 1])
        #  filtrando o geojson pela data selecionada
        if selected_date:
            geojson_filtered = geojson[geojson['date'].dt.date == selected_date]
            selected_date_activities = all_activities[all_activities['start_date'].dt.date == selected_date]
            if not selected_date_activities.empty:
                with col1:
                    # filtrando o df all_activities pela data selecionada e puxando a distância percorrida
                    total_distance = selected_date_activities['distance_km'].sum()
                    st.metric(label="🏃‍♂️ Distance", value=f"{total_distance} km")
                with col2:
                    # filtrando o df all_activities pela data selecionada e puxando o pace
                    average_pace = adjust_pace(selected_date_activities['pace'].mean())
                    st.metric(label="📏 Average Pace", value=f"{average_pace} min/km")
                with col3:
                    # filtrando o df all_activities pela data selecionada e puxando o tempo total
                    total_time = selected_date_activities['time_min'].sum()
                    st.metric(label="⏱️ Total Time", value=f"{total_time} min")
            else:
                st.warning("No activities found for the selected date.")
                geojson_filtered = geojson

        else:
            with col1:
                #  faz a soma da distancia total percorrida de todas as atividades
                total_distance = all_activities['distance_km'].sum()
                st.metric(label="🏃‍♂️ Distance", value=f"{np.round(total_distance,2)} km")
            with col2:
                #  faz a média do pace de todas as atividades
                average_pace = adjust_pace(all_activities['pace'].mean())
                st.metric(label="📏 Average Pace", value=f"{average_pace} min/km")
            with col3:
                #  faz a soma do tempo total de todas as atividades
                total_time = all_activities['time_min'].sum()
                st.metric(label="⏱️ Total Time", value=f"{total_time} min")
            geojson_filtered = geojson

        
        if len(geojson.path) > 0:
            init_lon, init_lat = geojson.path[0][0]
        else:
            init_lon, init_lat = -40.0, -20.0

        view_state = pdk.ViewState(
            latitude = init_lat,
            longitude=init_lon,
            zoom=5,
            pitch=10,
        )

        path_layer = pdk.Layer(
            "PathLayer",
            data=geojson_filtered,
            get_path='path',
            get_color='color',
            get_width=15,
            width_min_pixels=2,
            auto_highlight=True,
            highlight_color=[255, 255, 0, 200],
        )

        st.pydeck_chart(pdk.Deck(layers=[path_layer], initial_view_state=view_state))
