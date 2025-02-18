# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import adjust_pace, treat_date, treat_distance_and_time, parse_coordinates, process_strava_data

import plotly.express as px
import plotly.graph_objs as go

# column chart for distance and line chart for pace
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def distance_pace_chart(df):
    fig = px.line(df, x=df.index, y='pace',  
              markers=True, 
              labels={'pace': 'Pace (min/km)'})

    fig.update_traces(
        textposition='top center', 
        textfont_size=10, 
        showlegend=True, 
        name='Pace (min/km)',  # Corrigindo a string do nome
        line=dict(color='#FFA500', width=2),
        marker=dict(size=8, opacity=0.6),
        hovertemplate='<b>Pace</b>: %{y:.2f} min/km<extra></extra>'
    )

    bar_trace = go.Bar(
        x=df.index, 
        y=df['distance_km'], 
        marker=dict(color='#2E8B57'), 
        text=df['distance_km'].astype(str) + "km\n" + df['start_date'].dt.strftime('%b %Y'),  # Formato "Jan 2024"
        textposition='inside',  # Mantendo dentro, mas podemos mudar para 'outside'
        textfont=dict(size=12, color='white'),  # Aumentando tamanho e garantindo contraste
        name='Distance (km)',
        hovertext=df['start_date'].dt.strftime('%d/%m/%Y'),  # Formato "01/01/2024"
        hovertemplate='<b>Distance</b>: %{y:.2f} km<br><b>Date</b>: %{hovertext}<extra></extra>'
    )

    pace_mean_line = go.Scatter(
        x=df.index, 
        y=[df['pace'].mean()]*len(df.index), 
        mode='lines', 
        name='Mean Pace (min/km)', 
        line=dict(color='#A9A9A9', dash='dashdot', width=2),
        hovertemplate='<b>Mean Pace</b>: %{y:.2f} min/km<extra></extra>',
    )

    fig.add_trace(pace_mean_line)
    fig.add_trace(bar_trace)

    # Layout e melhorias visuais
    fig.update_layout(
        barmode='overlay', 
        width=1000, 
        height=500,
        legend=dict(
            yanchor="top",
            y=-0.01,
            xanchor="center",
            x=0.5,
            orientation='h',
            font=dict(size=18, color='white')
        ),
        xaxis_title='', 
        yaxis_title='Distance (km)<br>Pace (min/km)',
        yaxis=dict(
            range=[0, max(df['distance_km'])+1], 
            tickvals=np.arange(0, max(df['distance_km'])+1, 1),
            title='Distance (km) <br> Pace (min/km)', 
            tickfont=dict(color='#81C784'),
            title_font=dict(color='white', size=20),
        ),
        title_text='Distance and Pace',
        title_x=0.5,
        title_font_family="Roboto",
        title_font_color="white",
        title_font_size=20,
        font_family="Roboto",
        font_color="white",
        paper_bgcolor='#1a1a1a',
        plot_bgcolor='#1a1a1a',
        hovermode='x unified',
    )

    fig.add_annotation(x=0, 
                       y=df['pace'].mean()+6, 
                       text=f'Mean Pace: {df["pace"].mean():.2f}min/km', 
                       showarrow=False, 
                       yshift=10, 
                       font=dict(size=16, color='#FFD54F'))
    
    fig.add_annotation(x=0, 
                       y=df['distance_km'].mean()+5.5, 
                       text=f'Mean Distance: {df["distance_km"].mean():.2f}km', 
                       showarrow=False, 
                       yshift=10,
                       font=dict(size=16, color='#81C784'))

    fig.add_annotation(
        text='Half Marathon Training',
        xref='paper', yref='paper',
        x=0.52, y=1.07,
        font=dict(family='Arial', size=13, color='#B0BEC5'),
        showarrow=False
    )

    fig.update_yaxes(showgrid=False, showline=True, linewidth=1, linecolor='black', mirror=False)
    fig.update_xaxes(showgrid=False, showline=True, linewidth=1, linecolor='black', mirror=False, showticklabels=False)
    
    # Grid mais sutil
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')
    
    return fig
