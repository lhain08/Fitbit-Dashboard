# Get the requested type and date
import sys
import os

# Used for Fitbit client API
import fitbit
from Fitbit_API import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
import time

# Read in credentials
def get_credentials(file='credentials.txt'):
    try:
        creds = open(file, 'r')
        CLIENT_ID = creds.readline().strip()
        CLIENT_SECRET = creds.readline().strip()
        creds.close()
    except:
        print("ERROR: credentials.txt does not exist or has invalid format")
        print("\tShould contain CLIENT_ID and CLIENT_SECRET on first and second lines respectively")
        raise("Bad File")
    return CLIENT_ID, CLIENT_SECRET

# Authorize the user
def authorize_user(CLIENT_ID, CLIENT_SECRET, recursive=False):
    try:
        file = open("tokens.txt", 'r')
        ACCESS_TOKEN = file.readline().strip()
        REFRESH_TOKEN = file.readline().strip()
        file.close()
    except:
        # Create server and run browser authorization
        try:
            server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
            server.browser_authorize()
        except:
            raise ("Authorization Failed")
        # Get tokens and client
        ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
        # Cache the tokens
        file = open("tokens.txt", 'w')
        file.write(ACCESS_TOKEN + '\n' + REFRESH_TOKEN)
        file.close()

    CLIENT = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN,\
                           redirect_uri="http://127.0.0.1:8080/")

    return CLIENT

def clear_tokens():
    os.remove('tokens.txt')
