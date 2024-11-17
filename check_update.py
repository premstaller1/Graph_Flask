import requests
import datetime

def makeApiCall(url, endpointParams, debug='no'):
    data = requests.get(url, endpointParams)
    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['json_data'] = data.json()

    return response
def getLongLivedAccessToken(params):
    url = params['graph_domain'] + '/oauth/access_token'
    endpointParams = dict()
    endpointParams['grant_type'] = 'fb_exchange_token'
    endpointParams['client_id'] = params['client_id']
    endpointParams['client_secret'] = params['client_secret']
    endpointParams['fb_exchange_token'] = params['access_token']
    return makeApiCall(url, endpointParams, params['debug'])

def debugAccessToken(params):
    endpointParams = dict()
    endpointParams['input_token'] = params['access_token']
    endpointParams['access_token'] = params['access_token']
    url = params['graph_domain'] + '/debug_token'
    return makeApiCall(url, endpointParams, params['debug'])

def printTokenExpiration(creds):
    response = debugAccessToken(creds)
    expiration = datetime.datetime.fromtimestamp(response['json_data']['data']['expires_at'])
    profile = creds.get('profile_name', 'Unknown')
    print(f"\n{profile.capitalize()}: Token Expires at: {expiration}")

def updateAccessToken(creds):
    response = getLongLivedAccessToken(creds)
    new_access_token = response['json_data'].get('access_token', None)
    profile = creds.get('profile_name', 'Unknown')
    if new_access_token:
        creds['access_token'] = new_access_token
        print(f"\n ---- {profile.capitalize()} ACCESS TOKEN INFO ----\n")
        print(f"{profile.capitalize()} Access Token:")
        print(new_access_token)
    return creds

def getCreds(profile='productminimal'):
    creds = dict()  # dictionary to hold everything
    creds['profile_name'] = profile

    # Default credentials for productminimal
    if profile == 'productminimal':
        creds['access_token'] = 'EAAG24jaJaYIBO41JyeHF6XGw3gIv0ZB3HY0WT9EebvZBWmGZBrCeZANUMVTqB2nVI2qCGaqBtFDmO0EvDtDtRaDIoOzr7hc0JbKiKW3UyZChQZCOnNv1MMsih0Y7AEOhFnXRbPazwP3rlNod1FsbabwTQbDDIcmm7AVaKDYtL3Q2iLzT7Gc7Kl3RnS1mI1pie1Fts8U1H9'
        creds['client_id'] = '482557670549890'
        creds['client_secret'] = 'd62937e7f31973871d86b8242430b73e'
        creds['graph_domain'] = 'https://graph.facebook.com'
        creds['graph_version'] = 'v20.0'
        creds['endpoint_base'] = creds['graph_domain'] + '/' + creds['graph_version'] + '/'
        creds['page_id'] = '482557670549890'
        creds['instagram_account_id'] = '17841447229527043'
        creds['ig_username'] = 'productminimal'

    # Credentials for productsdesign
    elif profile == 'productsdesign':
        creds['access_token'] = 'EAAG24jaJaYIBO41JyeHF6XGw3gIv0ZB3HY0WT9EebvZBWmGZBrCeZANUMVTqB2nVI2qCGaqBtFDmO0EvDtDtRaDIoOzr7hc0JbKiKW3UyZChQZCOnNv1MMsih0Y7AEOhFnXRbPazwP3rlNod1FsbabwTQbDDIcmm7AVaKDYtL3Q2iLzT7Gc7Kl3RnS1mI1pie1Fts8U1H9'
        creds['client_id'] = '482557670549890'
        creds['client_secret'] = 'd62937e7f31973871d86b8242430b73e'
        creds['graph_domain'] = 'https://graph.facebook.com'
        creds['graph_version'] = 'v20.0'
        creds['endpoint_base'] = creds['graph_domain'] + '/' + creds['graph_version'] + '/'
        creds['page_id'] = '482557670549890'
        creds['instagram_account_id'] = '17841419699397187'
        creds['ig_username'] = 'productsdesign'

    else:
        raise ValueError("Invalid profile name. Use 'productminimal' or 'productsdesign'.")

    creds['debug'] = 'yes'  # Enable debug mode

    return creds

# Example usage
creds_minimal = getCreds('productminimal')
creds_design = getCreds('productsdesign')

# Separately call the printTokenExpiration and updateAccessToken functions
printTokenExpiration(creds_minimal)
printTokenExpiration(creds_design)
