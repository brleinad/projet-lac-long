from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import csv
import requests


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get('/')
# async def ping():
#     return {"message": "Yo"}

def is_valid_send(tick: dict):
    is_valid_lead_send = tick.get('Lead Style', '').lower() in ['onsight', 'flash', 'redpoint']
    is_valid_boulder_send = tick.get('Style', '').lower() in 'send'

    is_lead = tick.get('Style').lower() in 'lead'
    is_boulder = tick.get('Route Type').lower() in 'boulder'

    is_valid = False

    if is_lead:
        is_valid = is_valid_lead_send
    elif is_boulder:
        is_valid = is_valid_boulder_send

    return is_valid


def is_in_lac_long(route: dict):
    lac_long_location = 'International > North America > Canada > Quebec > 03. Quebec City, Charlevoix, Portneuf > Lac Long '
    return lac_long_location.lower() in route.get('Location').lower()



@app.get('/sends/{user_id}/{username}')
async def get_user_sends(user_id, username):
    url = f'https://www.mountainproject.com/user/{user_id}/{username}/tick-export'
    response = requests.get(url)

    ticks = csv.DictReader(response.text.splitlines())

    total_sends = 0
    for tick in ticks:
        if is_in_lac_long(tick) and is_valid_send(tick):
            print(tick.get('Route'), tick.get('Style'), tick.get('Lead Style'))
            total_sends += 1

    return {'sends': total_sends}

app.mount("/", StaticFiles(directory="site", html=True), name="site")
