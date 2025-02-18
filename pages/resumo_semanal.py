import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from utils import process_strava_data, prepare_df_for_week_analysis
from charts import distance_pace_chart, week_analysis_chart


def show():
    st.markdown("<h3 style='text-align: center; color: white;'>Weekly Summary Analysis</h3>", unsafe_allow_html=True)
    st.write('---')
    # Simulação de carregamento dos dados
    df = pd.read_csv("data/activities.csv")
    df = process_strava_data(df)
    # Criar gráfico de distance vs pace
    fig1, fig2 = week_analysis_chart(df)
    st.plotly_chart(fig1, use_container_width=True, height=2000)
    st.plotly_chart(fig2, use_container_width=True, height=2000)

    col4, col5, col6 = st.columns([1, 3, 1])
    df = prepare_df_for_week_analysis(df)
    with col5:
        col7, col8, col9 = st.columns(3)
        with col7:
            st.metric(label="🏃‍♂️ Week Number", value=len(df))

        with col8:
            st.metric(label="📏 Average Distance", value=f"{df['distance_km'].mean():.2f} km")

        with col9:
            st.metric(label="⏱️ Average Pace", value=f"{df['pace'].mean():.2f} min/km")