# %%
import requests
import urllib3
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import ast  # Para conversão segura de strings de dicionário

auth_url = "https://www.strava.com/oauth/token"
authorization_token = '916939aec74f385d61bff7fd8a04d14db52ec819'

# tutorial video here for info on how: https://www.youtube.com/watch?v=sgscChKfGyg&list=PLO6KswO64zVvcRyk0G0MAzh5oKMLb6rTW

payload = {
    'client_id': "148656",
    'client_secret': 'c8f778c91799bbe763df44f0a8a7eb678892b329',
    'refresh_token': 'fe2447df89c69bcb0fda2f22f3f4a453e11be078',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))


activity_url = "https://www.strava.com/api/v3/activities"
activities_list = []

header = {'Authorization': 'Bearer ' + access_token}

#  read csv for individual activities, if does not exist, create one
try:
    individual_activities = pd.read_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/individual_activities.csv')
except:
    individual_activities = pd.DataFrame()
    individual_activities.to_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/individual_activities.csv')

all_activities = pd.read_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/activities.csv')
for id in all_activities['id']:
    r = requests.get(activity_url + '/' + str(id), headers=header).json()
    print(r)
    activities_list.append(r)

activities_df = pd.DataFrame(activities_list)
activities_df.to_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/individual_activities.csv')

df = pd.read_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/individual_activities.csv')
nested_columns = ["athlete", "map", "splits_metric", "splits_standard", "best_efforts", "laps"]

def safe_convert(x):
    if pd.isna(x):  # Ignorar valores NaN
        return None
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)  # Converte string para dicionário (corrige aspas)
        except (ValueError, SyntaxError):
            print(f"Erro ao converter: {x}")  # Depuração
            return None
    return x  # Se já for dicionário, mantém

nested_columns = ["athlete", "map", "splits_metric", "splits_standard", "best_efforts", "laps"]

for column in nested_columns:
    df[column] = df[column].apply(safe_convert)
    df_nested = pd.json_normalize(df[column])
    df = df.drop(columns=column).join(df_nested.add_prefix(column + "_"))
# %%
columns_to_drop = ['Unnamed: 0','type','workout_type', 'location_city', 'location_country','photo_count', 'commute', 'manual', 'private', 'visibility', 'flagged', 'has_heartrate', 'heartrate_opt_out', 'display_hide_heartrate_option','from_accepted_tag','total_photo_count', 'has_kudoed', 'perceived_exertion', 'prefer_perceived_exertion', 'photos', 'stats_visibility', 'hide_from_home', 'similar_activities']


df = df.drop(columns=columns_to_drop)
# %%
df = df[df['sport_type'] == 'Run']

df.to_csv('/Users/kaduangelucci/Documents/Projetos/Strava Analysis/data/individual_activity.csv')



