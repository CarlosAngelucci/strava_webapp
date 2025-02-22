import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from utils import adjust_pace, treat_date, treat_distance_and_time, parse_coordinates, process_strava_data
from charts import distance_pace_chart

def show():
    st.markdown("<h3 style='text-align: center; color: white;'>Distance and Pace Analysis</h3>", unsafe_allow_html=True)
    st.write('---')
    # Simulação de carregamento dos dados
    df = pd.read_csv("data/activities.csv")
    df = process_strava_data(df)

    # st.markdown("<h4 style='text-align: center; color: #FC4C02;'>Select the type of run</h4>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    options = ['All', 'Outdoor', 'Indoor']
    with col1:
        st.markdown("""
            <style>
            .stRadio > label {
                font-size: 40px; /* Ajuste este valor para o tamanho desejado */
            }
            </style>
            """, unsafe_allow_html=True)
        selection = st.radio("Select the type of run:", options, horizontal=True, index=0, key='type_run')

    if selection != "All":
        df = df[df['type_run'] == selection]
    else:
        df = df
    

    # Criar gráfico de distance vs pace
    fig = distance_pace_chart(df)
    st.plotly_chart(fig, use_container_width=True, height=2000)

    col4, col5, col6 = st.columns([1, 3, 1])
    with col2:
        col7, col8, col9 = st.columns(3)
        with col7:
            st.metric(label="🏃‍♂️ Train", value=len(df))

        with col8:
            st.metric(label="📏 Average Distance", value=f"{df['distance_km'].mean():.2f} km")

        with col9:
            average_pace = adjust_pace(df['pace'].mean())
            st.metric(label="📏 Average Distance", value=f"{average_pace} km")