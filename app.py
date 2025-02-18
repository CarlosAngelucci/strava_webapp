import streamlit as st
import pandas as pd
from charts import distance_pace_chart
from utils import process_strava_data
from pages import distance_pace

st.set_page_config(page_title='Half Marathon Training Analysis', layout='wide')

# Sidebar para navegação
st.sidebar.title("📊 Running Metrics Dashboard")
page = st.sidebar.radio("Selecione a análise", ["🏃 Distância & Pace", "📆 Resumo Semanal", "📈 Tendências"])

st.title('Half Marathon Training Analysis!')
st.write('This is a simple dashboard to analyze my half marathon training data.')

# Carregar a página selecionada
if page == "🏃 Distância & Pace":
    distance_pace.show()
# elif page == "📆 Resumo Semanal":
#     weekly_summary.show()
# elif page == "📈 Tendências":
#     trends.show()

