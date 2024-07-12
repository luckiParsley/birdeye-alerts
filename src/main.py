import os
import json
from dotenv import load_dotenv
import requests
import pygame
import time


def load_config():
    config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config = os.path.join(config_dir, 'config.json')
    try:
        with open(config, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("!!FILE NOT FOUND!!")

def make_request(address, api):
    url = "https://public-api.birdeye.so/defi/price"
    params = {
        "check_liquidity": "1000.25",
        "include_liquidity": "true",
        "address": address
    }
    headers = {
        "accept": "application/json",
        "x-chain": "solana",
        "X-API-Key": api
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        price = round(data.get('data', {}).get('value'), 2)
        if price:
            print(price)
        else:
            print('an error has occured')
            # make some sort of noise/ alert 
    # going to want to make auditory alerts for this was well
    # Finish up the exceptions
    except requests.exceptions.HTTPError as err:
        print("HTTP Error", err)
    except Exception as err:
        print("HTTP Error:", err)
    return price

def check_price(price, upper, lower, is_above, is_below):

    if price > upper:
        print("price is above")
        is_above = True
    if price < lower:
        print("price is below")
        is_below = True
    return is_above, is_below
    
def send_alert(sound, sound_config):
    print('sending alert')
    sound_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sound = os.path.join(sound_dir, sound)
    print(sound)

    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound)
    if not pygame.mixer.get_busy():
        while sound_config == True:
            sound_channel = sound.play()
            time.sleep(20)

def main():
    config = load_config()
    sound_config = bool(config.get('Sound-Alerts'))
    alert_config = bool(config.get('Alerts'))

    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)
    BIRDEYE_API = os.getenv('BIRDEYE_API')

    while True:
        price = make_request(config.get('address'), BIRDEYE_API)
        is_above = False
        is_below = False
        is_above, is_below = check_price(price, config.get('Upper-bound'), config.get('Lower-bound'), is_above, is_below)

        if is_above == True:
            send_alert('elephant.wav', sound_config)
        elif is_below == True:
            send_alert('putt.wav', sound_config)
        time.sleep(15)

if __name__ == "__main__":
    main()