
1. Paste this link in your webbrowser: https://www.strava.com/oauth/authorize?client_id=148656&redirect_uri=http://localhost&response_type=code&scope=activity:read_all 
include the client_id. This will request the user to authorize the app to access their data, and after that, the user will be redirected to the redirect_uri with a code in the query string like this: http://localhost/?state=&code=ae97497d582060086c58eee7a4093094416e8f84&scope=read,activity:read_all this code is used to get the access token.

2. Now that we have this code, we can make a POST to:
https://www.strava.com/oauth/token?client_id=148656&client_secret=c8f778c91799bbe763df44f0a8a7eb678892b329&code=916939aec74f385d61bff7fd8a04d14db52ec819&grant_type=authorization_code
where you need to include the client_id, client_secret and the code. This will return a JSON object with the access token and the refresh token.

3. Now that you have access token, make a GET request to: https://www.strava.com/api/v3/athlete/activities?access_token=287673a322e1d8de0550ebc29df135bb716b2f9d where you need to include the access token. This will return a JSON object with the activities of the user.

4. Since this acess token expires, we need to use our refresh token to get a new access token. Make a POST request to: https://www.strava.com/oauth/token?client_id=148656&client_secret=c8f778c91799bbe763df44f0a8a7eb678892b329&refresh_token=fe2447df89c69bcb0fda2f22f3f4a453e11be078&grant_type=refresh_token
and this will return a new access token so you can keep making requests to the API in your application

4. After you did this for the first time, you just need to send a post to auth_url with client_id, client_secret and refresh_token to get a new access token, and this new access_token will be used to send a request to activities_url to get the activities of the user.