import requests
import urllib3
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
authorization_token = '916939aec74f385d61bff7fd8a04d14db52ec819'
refresh_token = 'fe2447df89c69bcb0fda2f22f3f4a453e11be078'
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
# access_token = res.json()['access_token']
# print("Access Token = {}\n".format(access_token))


# Initialize the dataframe
# access_token = '1a58132b1ca008187af2ee08c13149af03f040c1'
access_token = '287673a322e1d8de0550ebc29df135bb716b2f9d'
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

activities.to_csv('activities.csv')

