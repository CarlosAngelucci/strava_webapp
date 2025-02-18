# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from utils import adjust_pace, treat_date, treat_distance_and_time, parse_coordinates, process_strava_data


# %%
df = pd.read_csv('../data/activities.csv', index_col=False)
df = process_strava_data(df)
df.sort_values(by='start_date', inplace=True, ascending=True)
df.reset_index(drop=True, inplace=True)

# %%
#  plot pace distribution
fig, ax = plt.subplots(figsize=(12,6))
ax.set_frame_on(False)
ax.tick_params(axis='both', length=0)
# ax.yaxis.set_ticklabels([])
ax.legend(['Pace\n(min/km)'])
n, bins, patches = ax.hist([df[df['type_run']=='Outdoor'].pace, df[df['type_run']=='Indoor'].pace], bins=15, color=['skyblue', 'lightgreen'], edgecolor='black', stacked=True, label=['Outdoor', 'Indoor'])
plt.title('Distribution of Pace')
plt.xlabel('Pace (min/km)')
plt.ylabel('Frequency')

# Adicionando rótulos de dados
for i in range(len(n[0])):
    freq_outdoor = n[0][i]
    freq_indoor = n[1][i]
    total_freq = freq_outdoor + freq_indoor
    if total_freq > 0:
        # Posição x do rótulo (centro do bin)
        x_pos = bins[i] + (bins[i+1] - bins[i])/2
        # Posição y do rótulo (topo da barra)
        y_pos = n[1][i] + 0.2
        # Texto do rótulo
        label_text = f'Qty:{int(total_freq)}\nOutdoor: {freq_outdoor}\nTreadmill: {freq_indoor}\n({bins[i]:.2f}-{bins[i+1]:.2f})'
        plt.text(x=x_pos, y=y_pos, s=label_text, ha='center', va='bottom', fontdict={'fontsize': 6})

plt.show()

 # %%
#  plot distance distribution
fig, ax = plt.subplots(figsize=(12,6))
ax.set_frame_on(False)
ax.tick_params(axis='both', length=0)
ax.yaxis.set_ticklabels([])
ax.legend(['Distance\n(km)'])
n, bins, patches = ax.hist(df['distance_km'], bins=5, color=['skyblue'], edgecolor='black')
plt.title('Distribution of Distance')
plt.xlabel('Distance (km)')
plt.ylabel('Frequency')

# Adicionando rótulos de dados
for i in range(len(n)):
    if n[i] > 0:
        freq = n[i]
        # Posição x do rótulo (centro do bin)
        x_pos = bins[i] + (bins[i+1] - bins[i])/2
        # Posição y do rótulo (topo da barra)
        y_pos = n[i] + 0.2
        #  texto
        text = f'Qty:{int(freq)}\n({bins[i]:.0f}-{bins[i+1]:.0f})km'
        # Texto do rótulo
        label_text = f'Qty:{int(freq)}\n({bins[i]:.2f}-{bins[i+1]:.2f})'
        plt.text(x=x_pos, y=y_pos, s=text, ha='center', va='bottom', fontdict={'fontsize': 9})
# %%
#  a chart with a line representing pace and bars representing distance for each run
fig, ax = plt.subplots(figsize=(12,6))
df.sort_values(by='start_date', inplace=True, ascending=True)
df.reset_index(drop=True, inplace=True)
ax.set_frame_on(False)
ax.tick_params(axis='both', length=0)
ax.grid(axis='y', linestyle='--', alpha=0.1)
# ax.yaxis.set_ticklabels([])
ax.legend(['Distance\n(km)', 'Pace\n(min/km)'])



# plot day by day distance and pace disconsidering days without data
ax.bar(df.index, df['distance_km'], color='skyblue', edgecolor='black', label='Distance')
ax.plot(df.index, df['pace'], color='lightgreen', label='Pace', marker='o', markersize=5, markerfacecolor='black')
ax.axhline(y=df['pace'].mean(), xmin=0, xmax=len(df.index), color='darkgreen', linestyle='--', label='Mean Pace', alpha=0.4)

#  rotate x labels
plt.xticks(rotation=90)
plt.title('Distance and Pace')
plt.xlabel('Run')
plt.ylabel('Distance (km) / \nPace (min/km)')

ax.set_ylim(0, max(df['distance_km'])+1)
ax.set_yticks(np.arange(0, max(df['distance_km'])+1, 1))
ax.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)

for i, value in enumerate(df['distance_km']):
    y = value
    x = i
    if value >= 3:
        ax.annotate(xy=(x, y), xytext=(x, y),
                    text=f'{value:.1f}km {df['start_date'].dt.month[i]}/{df['start_date'].dt.year[i]}', color='white', fontweight='bold', fontsize=8,
                    va='top', ha='center', rotation=270)

#  ANNOTATE MEAN PACE
ax.annotate(xy=(0, df['pace'].mean()+5), xytext=(2, df['distance_km'].max()),
            text=f' Mean Pace: \n{df['pace'].mean():.2f}min/km', color='lightgreen', fontweight='bold', fontsize=12,
            va='top', ha='center', rotation=0)

# ANNOTATE MEAN DISTANCE
ax.annotate(xy=(0, df['distance_km'].mean()), xytext=(2, df['distance_km'].max()-2),
            text=f' Mean Distance: \n{df['distance_km'].mean():.2f}km', color='skyblue', fontweight='bold', fontsize=12,
            va='top', ha='center', rotation=0)

plt.show()

# %%
import plotly.express as px
import plotly.graph_objs as go

fig = px.line(df, x=df.index, y='pace',  
            markers=True, 
            labels={'pace': 'Pace (min/km)'}, 
            hover_data={'start_date': True, 'pace': ':.2f'})

fig.update_traces(textposition='top center', textfont_size=5, showlegend=True, name='Pace (min/km)', 
                line=dict(color='#FF9800', width=2),
                marker=dict(size=8, opacity=0.6), 
                hovertemplate='<b>Pace</b>: %{y:.2f} min/km<extra></extra>')

bar_trace = go.Bar(x=df.index, y=df['distance_km'], 
                marker=dict(color='#4CAF50'), 
                text=df['distance_km'].astype(str) + df['start_date'].dt.strftime(' %m/%Y'), 
                textposition='inside',
                name='Distance (km)',
                hovertext=df['start_date'].dt.strftime('%d/%m/%Y'),
                hovertemplate='<b>Distance</b>: %{y:.2f} km<br><b>Date</b>: %{hovertext}<extra></extra>')

pace_mean_line = go.Scatter(x=df.index, y=[df['pace'].mean()]*len(df.index), 
                        mode='lines', 
                        name='Mean Pace (min/km)', 
                        line=dict(color='#2196F3', dash='dashdot', width=2),
                        hovertemplate='<b>Mean Pace</b>: %{y:.2f} min/km<extra></extra>')

fig.add_trace(pace_mean_line)
fig.add_trace(bar_trace)

fig.update_layout(barmode='overlay',
                width=1000, 
                height=500,
                legend=dict(
                    yanchor="top",
                    y=-0.01,
                    xanchor="center",
                    x=0.5,
                    orientation='h',
                ),
                xaxis_title='', 
                yaxis=dict(range=[0, max(df['distance_km'])+1], 
                            tickvals=np.arange(0, max(df['distance_km'])+1, 1),
                            title='Distance (km) <br> Pace (min/km)',
                            tickfont=dict(color='#81C784'),
                        )
)

fig.add_annotation(x=0.1, y=df['pace'].mean()+4, text=f'Mean Pace: {df["pace"].mean():.2f}min/km', showarrow=False, yshift=10, font=dict(color='#FFD54F'))
fig.add_annotation(x=0, y=df['distance_km'].mean()+3.5, text=f'Mean Distance: {df["distance_km"].mean():.2f}km', showarrow=False, yshift=10, font=dict(color='#81C784'))

# TITLE
fig.update_layout(
title_text='Distance and Pace',
title_x=0.5,
title_font_family="Roboto",
title_font_color="white",
title_font_size=20,
font_family="Roboto",
font_color="white",
)
fig.add_annotation(
text='Half Marathon Training',
xref='paper', yref='paper',
x=0.5, y=1.07,
font=dict(family='Arial', size=13, color='#B0BEC5'),
showarrow=False
)

fig.update_layout(
paper_bgcolor='#1a1a1a',
plot_bgcolor="#1a1a1a",
hovermode='x',
)

fig.update_yaxes(showgrid=False, showline=True, linewidth=1, linecolor='white', mirror=False)
fig.update_xaxes(showgrid=False, showline=True, linewidth=1, linecolor='white', mirror=False, 
showticklabels=False)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')
# %%
