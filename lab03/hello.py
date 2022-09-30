#!/usr/bin/env python3

import os
import json
from templates import login_page

def get_env():
    # empty dict of environment variables
    env = {}

    # q1
    # get each environment variable
    # source: https://www.techiedelight.com/check-environment-variables-python 
    #           and lab d01 videos on eclass
    for env_key, env_variable in os.environ.items():
        env[env_key] = env_variable
        #print((env_variable, os.getenv(env_variable)))

    return env

env = get_env()

## SERVE AS JSON
# print("Content-Type: application/json")
# print()
# print(json.dumps(env)) # print environment as json

## PRINT BROWSER AND QUERY STRING
# print("Content-Type: text/html")
#print(f"<p>Query string: = env['QUERY_STRING']</p>") # q2
#print("Browsers information: " + env["HTTP_USER_AGENT"]) #q3
#print(f"<p>Browsers information: env['HTTP_USER_AGENT']</p>") #q3