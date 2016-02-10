import requests
from bottle import route, run, redirect, request

CLIENT_ID = '77giusd8moiwk9'
CLIENT_SECRET = 'MIXScG7cnvkixyCn'

linkedin_auth_url = 'https://www.linkedin.com/uas/oauth2/authorization'
linkedin_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
callback_url = 'http://localhost:8080/auth/callback'
state_const = 'qweqwe1111'

access_token = 'AQXwDhAGTuC1XU9iQFPq_PZz039K7jxutsASxPpIyosVixcofm3orsPCT5goB5wVxzXQ5ZDiLJrBFwjqwjeGK7rKE8GnKdI1fnOTP2K9KY2nS-2M_mOS9gFJpizMVUdrvx0jWDmy7BHTKsENDKrdN-WCdGaVBxuEWeTuSzBhzEOBt1KDRHw'


@route('/auth')
def auth():
    return redirect(linkedin_auth_url +
                    '?response_type=code' +
                    '&client_id=' + CLIENT_ID +
                    '&redirect_uri=' + callback_url +
                    '&state=' + state_const)


@route('/auth/callback')
def auth_callback():
    global access_token

    if 'error' in request.query:
        return 'Error!<br>' + request.query.error \
               + '<br>' + request.query.error_description
    elif 'state' in request.query:
        code = request.query.code
        r = requests.post(linkedin_token_url, params={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': callback_url,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET})
        data = r.json()
        access_token = data['access_token']
        return 'token: ' + access_token


@route('/search')
def search():
    global access_token

    r = requests.get('https://api.linkedin.com/v1/people-search', params={
        'oauth2_access_token': access_token,
        'keywords': 'princess'})
    return r.text


run(host='localhost', port=8080, debug=True)
