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
    st.title("🏃 Distance & Pace Analysis")
    
    # Simulação de carregamento dos dados
    df = pd.read_csv("data/activities.csv")
    df = process_strava_data(df)

    
    # Criar gráfico de distance vs pace
    fig = distance_pace_chart(df)
    st.plotly_chart(fig, use_container_width=True, height=2000)