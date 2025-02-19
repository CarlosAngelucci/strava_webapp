# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import adjust_pace, treat_date, treat_distance_and_time, parse_coordinates, process_strava_data, prepare_df_for_week_analysis

import plotly.express as px
import plotly.graph_objs as go

# column chart for distance and line chart for pace
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

strava_orange = '#FC4C02'  # Cor principal de energia da Strava
strava_green = '#242C04'
strava_secondary_green = '#81C784'

def distance_pace_chart(df):
    fig = px.line(df, x=df.index, y='pace',  
              markers=True, 
              labels={'pace': 'Pace (min/km)'})

    fig.update_traces(
        textposition='top center', 
        textfont_size=10, 
        showlegend=True, 
        name='Pace (min/km)',  # Corrigindo a string do nome
        line=dict(color=strava_orange, width=2),
        marker=dict(size=8, opacity=0.6),
        hovertemplate='<b>Pace</b>: %{y:.2f} min/km<extra></extra>'
    )

    bar_trace = go.Bar(
        x=df.index, 
        y=df['distance_km'], 
        marker=dict(color=strava_secondary_green), 
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
            tickfont=dict(color=strava_secondary_green),
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
                       font=dict(size=16, color=strava_orange))
    
    fig.add_annotation(x=0, 
                       y=df['distance_km'].mean()+5.5, 
                       text=f'Mean Distance: {df["distance_km"].mean():.2f}km', 
                       showarrow=False, 
                       yshift=10,
                       font=dict(size=16, color=strava_secondary_green))

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
    fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')
    
    return fig


def week_analysis_chart(df):
    df = prepare_df_for_week_analysis(df)
    fig1 = make_subplots(rows=1, cols=1, shared_xaxes=False, vertical_spacing=0.2, subplot_titles=('', 'Pace (min/km)'))

    bar_trace = go.Bar(x=df.week_year, y=df['distance_km'], 
                marker=dict(color='#4CAF50'), 
                text=df['distance_km'].astype(str) + 'km ' + '<br>Week: ' + df['week_year'].dt.strftime('%d/%m/%Y'), 
                textposition='outside',
                textfont=dict(color='white', size=18),
                name='',
                hovertext=df['week_year'].astype(str),
                hovertemplate='<b>Distance</b>: %{y:.2f} km<br><b>Week</b>: %{hovertext}<extra></extra>')


    fig1.add_trace(bar_trace, row=1, col=1)
    fig1.update_layout(
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
    yaxis=dict(
        range=[0, max(df['distance_km'])+5], 
        tickvals=np.arange(0, max(df['distance_km'])+5, 5),
        title='', 
        tickfont=dict(color=strava_secondary_green),
        title_font=dict(color='white', size=20),
    ),
    title_text='Distance per Week',
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

    fig1.update_yaxes(showgrid=False, showline=True, linewidth=1, linecolor='white', mirror=False)
    fig1.update_xaxes(showgrid=False, showline=True, linewidth=1, linecolor='white', mirror=False, showticklabels=False)
    # Grid mais sutil
    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')

    #  ======================== WATERFALL CHART
    #  calculando a variação semanal
    df['time_diff'] = df['time_min'].diff().fillna(df['time_min'].iloc[0])

#  definindo se a medida é relativa ou total
    df['measure'] = ['relative'] * len(df)

#  ajustando a primeira medida para ser total para começar do zero
    df.loc[0, 'measure'] = 'total'

    fig2 = make_subplots(rows=1, cols=1, shared_xaxes=False)
    waterfall_chart = go.Waterfall(
    name = "Accumulated Time (min)", 
    orientation = "v",
    measure = df['measure'],
    x = df.week_year,
    y = df['time_diff'],
    textposition = "outside",
    text = df['time_min'].astype(str) + ' min',
    hovertext = df.week_year.astype(str),
    hoverinfo = "x+text+name",
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
    decreasing = {"marker":{"color":"#FB4E05"}},
    increasing = {"marker":{"color":"#7AAD74"}},
)
    fig2.add_trace(waterfall_chart, row=1, col=1)

    fig2.update_layout(
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
    xaxis=dict(
        showticklabels=True,  
    ), 
    yaxis=dict(
        showticklabels=False,  # Esconde os labels dos ticks
        showgrid=False,        # Esconde a grade
        zeroline=False,        # Esconde a linha do zero
        showline=True,        # Esconde a linha do eixo
        title='',              # Remove o título
        visible=False          # Esconde completamente o eixo Y
    ),
    title_text='Accumulated Time per Week <br> Half Marathon Training',
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

    fig2.update_yaxes(showgrid=False, showline=True, linewidth=1, linecolor='white', mirror=False)
    fig2.update_xaxes(showgrid=False, showline=True, linewidth=1, linecolor='white', mirror=False, showticklabels=True)

    last_week = df['week_year'].iloc[-1]
    fig2.add_annotation(
    x=last_week,
    y = df['time_min'].iloc[-1]+10,
    text="Current Week",
    showarrow=True,
    arrowhead=2,
    ax=80,
    ay=-20,
    font=dict(size=16, color=strava_secondary_green),
    bgcolor='#1a1a1a',
    bordercolor='#1a1a1a',
    borderwidth=2,
    opacity=0.8,
    arrowcolor=strava_secondary_green,
    arrowwidth=2
)
    
    return fig1,fig2

