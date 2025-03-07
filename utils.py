import os
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv

def adjust_pace(pace: pd.Series) -> pd.Series:
    """
    Ajusta o valor de pace de centésimos de minuto (base 100) para minutos e segundos (base 60).

    No DataFrame, o valor de pace está representado em minutos com uma parte decimal que indica
    centésimos de minuto (base 100). Por exemplo, um pace de 6.11 significa 6 minutos e 11 centésimos
    de minuto. No entanto, o pace real (como no Strava) é representado em minutos e segundos (base 60),
    onde 6:07 significa 6 minutos e 7 segundos.

    Esta função converte a parte decimal (centésimos de minuto) para segundos, multiplicando por 60,
    e formata o resultado no formato MM:SS.

    Parâmetros:
    -----------
    pace : pd.Series
        O valor de pace em minutos com centésimos de minuto (ex: 6.11).

    Retorna:
    --------
    pd.Series
        O pace formatado no padrão MM:SS (ex: "6:07").

    Exemplo:
    --------
    >>> adjust_pace(6.11)
    '6:07'

    Explicação matemática:
    ----------------------
    1. A parte inteira do valor representa os minutos.
    2. A parte decimal representa centésimos de minuto (base 100).
    3. Para converter a parte decimal em segundos (base 60):
       segundos = parte_decimal * 60
    4. Arredonda-se os segundos para o valor inteiro mais próximo.
    5. Formata-se o resultado como MM:SS.

    Exemplo numérico:
    -----------------
    Para pace = 6.11:
    - Minutos = 6
    - Parte decimal = 0.11
    - Segundos = 0.11 * 60 = 6.66 → arredondado para 7
    - Pace real = 6:07
    """
    minutes = int(pace)
    decimal_part = pace - minutes
    seconds = round(decimal_part * 60)

    if seconds >= 60:
        minutes += 1
        seconds -= 60
    return f"{minutes:02d}:{seconds:02d}"

def treat_date(df: pd.DataFrame) -> pd.DataFrame:
    df['start_date'] = pd.to_datetime(df['start_date'], format='%Y-%m-%dT%H:%M:%SZ')
    df['start_date'] = df['start_date'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
    df['start_time'] = df['start_date'].dt.time
    df['start_date'] = df['start_date'].dt.date
    df['start_date'] = pd.to_datetime(df['start_date'], format='%Y-%m-%d')
    df['weekday_name'] = pd.to_datetime(df['start_date']).dt.day_name()
    df = df[df['start_date'].dt.year >= 2024] 
    return df

def treat_distance_and_time(df: pd.DataFrame) -> pd.DataFrame:
    df['distance_km'] = np.round((df.distance / 1000), 2)
    df['time_min'] = np.round((df['moving_time'] / 60), 2)
    df['rest_during_run_min'] = np.round(((df['elapsed_time'] - df['moving_time']) / 60),2)

    #  delete distances smaller than 1km
    df = df[df['distance_km'] > 1]

    return df

def parse_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    df['start_latlng'] = df['start_latlng'].str.extract(r'\[(.*?)\]')
    df['end_latlng'] = df['end_latlng'].str.extract(r'\[(.*?)\]')
    df['start_latlng'] = df['start_latlng'].str.split(', ')
    df['end_latlng'] = df['end_latlng'].str.split(', ')

    df['start_latitude'] = df['start_latlng'].apply(lambda x: x[0] if len(x) > 0 else None)
    df['start_longitude'] = df['start_latlng'].apply(lambda x: x[1] if len(x) > 1 else None)

    df['end_latitude'] = df['end_latlng'].apply(lambda x: x[0] if len(x) > 0 else None)
    df['end_longitude'] = df['end_latlng'].apply(lambda x: x[1] if len(x) > 1 else None)

    return df

def process_strava_data(df: pd.DataFrame) -> pd.DataFrame:
    df = treat_date(df)
    df = treat_distance_and_time(df)
    df = parse_coordinates(df)

    #  filter only runs
    df_run = df[df['type'] == 'Run']
    df_run = df_run.sort_values(by='start_date', ascending=True)
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

def prepare_df_for_week_analysis(df):
    df['week_year'] = df['start_date'].dt.strftime('%Y-%U')
    #  to datetime
    df['week_year'] = pd.to_datetime(df['week_year'] + '-0', format='%Y-%U-%w')
    # df['week_number'] = df['start_date'].dt.isocalendar().week
    # df['year'] = df['start_date'].dt.year

#  groupby year and week number columns sum distance, mean pace and sum time
    df = df.groupby(['week_year']).agg({'distance_km': 'sum', 'pace': 'mean', 'time_min': 'sum'}).reset_index()
    df['pace'] = df['pace'].round(2)
    df['distance_km'] = df['distance_km'].round(2)

# join year and week number columns
    # df['week'] = df['year'].astype(str) + '-' + df['week_number'].astype(str)
    # df.drop(columns=['year', 'week_number'], inplace=True)
    # df.set_index('week', inplace=True)
    return df


#def get_latest_runs():
    load_dotenv()
    client_secret = os.getenv('client_secret')
    refresh_token = os.getenv('refresh_token')
    auth_url = "https://www.strava.com/oauth/token"
    authorization_token = '916939aec74f385d61bff7fd8a04d14db52ec819'

    payload = {
    'client_id': "148656",
    'client_secret': client_secret,
    'refresh_token': refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    res_json = res.json()
    if 'access_token' not in res_json:
        raise KeyError("Access token not found in the response")
    access_token = res_json['access_token']
    # print("Access Token = {}\n".format(access_token))


    # Initialize the dataframe

    col_names = ['id','type', 'name', 'distance', 'moving_time', 'elapsed_time', 'total_elevation_gain', 'start_date',  'start_latlng', 'end_latlng', 'average_heartrate', 'max_heartrate', 'elev_high', 'elev_low', 'average_speed', 'max_speed', 'kudos_count']
    activities = pd.DataFrame(columns=col_names)

    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}

    page = 1
    per_page = 50

    while True:
    # get page of activities from Strava
        param = {'per_page': per_page, 'page': page}
        r = requests.get(activites_url, headers=header, params=param).json()

    # if no results then exit loop
        if (not r):
            break
    
    # otherwise add new data to dataframe
        for x in range(len(r)):
          for c in col_names:
            try:
              activities.loc[x + (page-1)*50, c] = r[x][c]
            except:
              activities.loc[x + (page-1)*50, c] = 'null'

    # increment page
        page += 1

    print("Activites imported")
    print(activities)

    activities.to_csv('data/activities.csv')
