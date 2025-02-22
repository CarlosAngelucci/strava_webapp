# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import adjust_pace, treat_date, treat_distance_and_time, parse_coordinates
# import seaborn as sns
# %%
def process_strava_data(df: pd.DataFrame) -> pd.DataFrame:
    df = treat_date(df)
    df = treat_distance_and_time(df)
    df = parse_coordinates(df)

    #  filter only runs
    df_run = df[df['type'] == 'Run']
    df_run.reset_index(drop=True, inplace=True)
    df_run.rename(columns={'average_speed': 'average_speed_meter_sec'}, inplace=True)

    df_run['start_latitude'] = df_run['start_latitude'].replace('', 0)
    df_run['start_longitude'] = df_run['start_longitude'].fillna(0)
    df_run['end_latitude'] = df_run['end_latitude'].replace('', 0)
    df_run['end_longitude'] = df_run['end_longitude'].fillna(0)
    df_run['type_run'] = df_run['start_latitude'].apply(lambda x: 'Indoor' if x == 0 else 'Outdoor')

    #  PROCESS PACE INFORMATION
    # calculate pace dividing time by distance so we have pace in minutes per kilometer 
    df_run['pace'] = np.round((df_run['time_min'] / df_run['distance_km']),2)
    # convert pace from centesimal of minute to minutes and seconds
    df_run['pace_adjusted'] = df_run.pace.apply(adjust_pace)
    df_run.drop(columns=['pace'], inplace=True)
    df_run.rename(columns={'pace_adjusted': 'pace'}, inplace=True)
    df_run = df_run[['id','type_run', 'start_date', 'start_time', 'distance_km', 'time_min', 'pace',  'weekday_name', 'average_heartrate', 'max_heartrate', 'rest_during_run_min', 'kudos_count', 'start_latitude', 'start_longitude', 'end_latitude', 'end_longitude']]

    # convert numeric columns to float
    df_run['distance_km'] = df_run['distance_km'].astype(float)
    df_run['time_min'] = df_run['time_min'].astype(float)
    df_run['pace'] = df_run['pace'].replace(':', '.', regex=True).astype(float)
    df_run['average_heartrate'] = df_run['average_heartrate'].astype(float)
    df_run['max_heartrate'] = df_run['max_heartrate'].astype(float)
    df_run['rest_during_run_min'] = df_run['rest_during_run_min'].astype(float)
    df_run['kudos_count'] = df_run['kudos_count'].astype(int)

    return df_run
# %%
df = pd.read_csv('data/activities.csv', index_col=False)
df = process_strava_data(df)
df

# %%
