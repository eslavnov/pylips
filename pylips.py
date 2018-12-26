import requests
import json
import random
import string
import argparse
import sys

from base64 import b64encode,b64decode
from Crypto.Hash import SHA, HMAC
from requests.auth import HTTPDigestAuth
from datetime import datetime

# Suppress "Unverified HTTPS request is being made" error message
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Key used for generated the HMAC signature
secret_key="JCqdN5AcnAHgJYseUn7ER5k3qgtemfUvMRghQpTfTZq7Cvv8EPQPqfz6dDxPQPSu4gKFPWkJGw32zyASgJkHwCjU"

# creates random device id
def createDeviceId():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))

# creates signature
def create_signature(secret_key, to_sign):
    sign = HMAC.new(secret_key, to_sign, SHA)
    return str(b64encode(sign.hexdigest().encode()))

# creates device spec JSON
def getDeviceSpecJson(config):
    device_spec =  { "device_name" : "heliotrope", "device_os" : "Android", "app_name" : "Pylips", "type" : "native"}
    device_spec['app_id'] = config['application_id']
    device_spec['id'] = config['device_id']
    return device_spec

# pairs with a TV
def pair_request(config, data, errCount=0):
    if errCount < 10:
        if errCount > 0:
            print("resending pair request")
        response={}
        try:
            r = requests.post("https://" + "172.168.201.11" + ":1926/6/pair/request", json=data, verify=False, timeout=2)
            if r.json() is not None:
                if r.json()['error_id'] == 'SUCCESS':
                    response=r.json()
                else:
                    return print('Error', r.json())
            else:
                return print('Can not reach the API')
        except Exception:
            # try again
            errCount += 1
            return pair_request(config, data, errCount)

        auth_Timestamp = response["timestamp"]
        config['auth_key'] = response["auth_key"]

        pin = input("Enter onscreen passcode: ")

        auth = { "auth_AppId" : "1"}
        auth['pin'] = str(pin)
        auth['auth_timestamp'] = auth_Timestamp
        auth['auth_signature'] = create_signature(b64decode(secret_key), str(auth_Timestamp).encode() + str(pin).encode())

        grant_request = {}
        grant_request['auth'] = auth
        grant_request['device']  = getDeviceSpecJson(config)

        print("Attempting to pair")
        pair_confirm(config,grant_request)
        
    else:
        print("The API is unreachable. Try restarting your TV and pairing again")
        return 

# confirms pairing with a TV
def pair_confirm(config, data, errCount=0):
    if errCount < 10:
        if errCount > 0:
            print("Resending pair confirm request")
        try:
            requests.post("https://" + config['address'] +":1926/6/pair/grant", json=data, verify=False, auth=HTTPDigestAuth(config['device_id'], config['auth_key']),timeout=2)
            print("Username for subsequent calls is: " + config['device_id'])
            print("Password for subsequent calls is: " + config['auth_key'])
            print("Use these credentials with --user and --pass parameters")
        except Exception:
            # try again
            errCount += 1
            pair_confirm(config, data, errCount)
    else:
        print("The API is unreachable. Try restarting your TV and pairing again")

# initiates pairing with a TV
def pair(config, errCount=0):
    config['application_id'] = "app.id"
    config['device_id'] = createDeviceId()
    data = { 'scope' :  [ "read", "write", "control"] }
    data['device']  = getDeviceSpecJson(config)
    print("Starting pairing request")
    pair_request(config,data)
    
# a general GET request
def get(config, errCount=0):
    if errCount < 10:
        try:
            print("Sending GET request")
            r = requests.get("https://" + config['address'] + ":1926/6/" + config['path'], verify=False,auth=HTTPDigestAuth(config['device_id'], config['auth_key']), timeout=2)
        except Exception:
            # try again
            errCount += 1
            return get(config, errCount)
        if len(r.text) > 0:
            print(r.text)
        print("Request sent!")
    else:
        print("Can not reach the API")

# a general POST request
def post(config, errCount=0):
    if errCount < 10:
        try:
            print("Sending POST request")
            r = requests.post("https://" + config['address'] + ":1926/" + config['path'], json=config['body'], verify=False,auth=HTTPDigestAuth(config['device_id'], config['auth_key']), timeout=2)
        except Exception:
            # try again
            errCount += 1
            return post(config, errCount)
        if len(r.text) > 0:
            print(r.text)
        print("Request sent!")

def main():
    config={}
    parser = argparse.ArgumentParser(description='Control Philips TV API (version 6)')
    parser.add_argument("--host", dest='host', help="TV's ip address")
    parser.add_argument("--user", dest='user', help="Username")
    parser.add_argument("--pass", dest='password', help="Password")
    parser.add_argument("--command", help="Command to run", default="pair")
    parser.add_argument("--path", dest='path', help="API's endpoint path")
    parser.add_argument("--body", dest='body', help="Body for post requests")

    args = parser.parse_args()

    if args.host is None:
        return print("Please set your TV's IP-address with a --host parameter")

    config['address'] = args.host
 
    if args.command == "pair":
        choice=""
        while choice != "exit":
            choice = input('Would you like to pair with your TV? [Y/n]').lower()
            yes = {'yes','y', 'ye', ''}
            no = {'no','n'}
            if choice in yes:
                pair(config)
                return
            elif choice in no:
                return print ("Please provide username and password (--user and --pass)")
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' \n")

    if args.user is None or args.password is None:
        return print("Please provide username and password (--user and --pass) or run --pair to get them")

    config['device_id'] = args.user
    config['auth_key'] = args.password

    # ambilight power
    if args.command == "ambilight_on":
        config['path'] = "ambilight/power"
        config['body'] = { "power":"On"}
        post(config)

    if args.command == "ambilight_off":
        config['path'] = "ambilight/power"
        config['body'] = { "power":"Off"}
        post(config)

    # ambilight video modes
    if args.command == "ambilight_video_immersive":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_VIDEO","isExpert":"false","menuSetting":"IMMERSIVE"}
        post(config)

    elif args.command == "ambilight_video_standard":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_VIDEO","isExpert":"false","menuSetting":"STANDARD"}
        post(config)

    elif args.command == "ambilight_video_natural":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_VIDEO","isExpert":"false","menuSetting":"NATURAL"}
        post(config)

    elif args.command == "ambilight_video_vivid":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_VIDEO","isExpert":"false","menuSetting":"VIVID"}
        post(config)

    elif args.command == "ambilight_video_game":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_VIDEO","isExpert":"false","menuSetting":"GAME"}
        post(config)

    elif args.command == "ambilight_video_comfort":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_VIDEO","isExpert":"false","menuSetting":"COMFORT"}
        post(config)

    elif args.command == "ambilight_video_relax":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_VIDEO","isExpert":"false","menuSetting":"RELAX"}
        post(config)

    # ambilight audio modes
    elif args.command == "ambilight_audio_adapt_brightness":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"ENERGY_ADAPTIVE_BRIGHTNESS"}
        post(config)

    elif args.command == "ambilight_audio_adapt_colors":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"ENERGY_ADAPTIVE_COLORS"}
        post(config)

    elif args.command == "ambilight_audio_vu_meter":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"VU_METER"}
        post(config)

    elif args.command == "ambilight_audio_spectrum":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"SPECTRUM_ANALYZER"}
        post(config)

    elif args.command == "ambilight_audio_knight_rider_1":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"KNIGHT_RIDER_CLOCKWISE"}
        post(config)

    elif args.command == "ambilight_audio_knight_rider_2":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"KNIGHT_RIDER_ALTERNATING"}
        post(config)

    elif args.command == "ambilight_audio_flash":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"RANDOM_PIXEL_FLASH"}
        post(config)

    elif args.command == "ambilight_audio_strobo":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"STROBO"}
        post(config)

    elif args.command == "ambilight_audio_party":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"PARTY"}
        post(config)

    elif args.command == "ambilight_audio_random":
        config['path'] = "ambilight/currentconfiguration"
        config['body'] = {"styleName":"FOLLOW_AUDIO","isExpert":"false","menuSetting":"MODE_RANDOM"}
        post(config)

    #ambilight + hue controls
    elif args.command == "ambihue_status":
        config['path'] = "menuitems/settings/current"
        config['body'] = {"nodes":[{"nodeid":2131230774}]}
        post(config)

    elif args.command == "ambihue_on":
        config['path'] = "menuitems/settings/update"
        config['body'] = {"values":[{"value":{"Nodeid":2131230774,"Controllable":"true","Available":"true","data":{"value":"true"}}}]}
        post(config)

    elif args.command == "ambihue_off":
        config['path'] = "menuitems/settings/update"
        config['body'] = {"values":[{"value":{"Nodeid":2131230774,"Controllable":"true","Available":"true","data":{"value":"false"}}}]}
        post(config)

    # get channels list
    elif args.command == "list_channels":
        config['path'] = "channeldb/tv/channelLists/all"
        get(config)

    # basic TV controls
    elif args.command == "standby":
        config['path'] = "input/key"
        config['body'] = {"key":"Standby"}
        post(config)
    
    elif args.command == "mute":
        config['path'] = "input/key"
        config['body'] = {"key":"Mute"}
        post(config)

    elif args.command == "volume_up":
        config['path'] = "input/key"
        config['body'] = {"key":"VolumeUp"}
        post(config)

    elif args.command == "volume_down":
        config['path'] = "input/key"
        config['body'] = {"key":"VolumeDown"}
        post(config)

    elif args.command == "channel_up":
        config['path'] = "input/key"
        config['body'] = {"key":"ChannelStepUp"}
        post(config)

    elif args.command == "channel_down":
        config['path'] = "input/key"
        config['body'] = {"key":"ChannelStepDown"}
        post(config)

    elif args.command == "play":
        config['path'] = "input/key"
        config['body'] = {"key":"Play"}
        post(config)

    elif args.command == "pause":
        config['path'] = "input/key"
        config['body'] = {"key":"Pause"}
        post(config)

    elif args.command == "play_pause":
        config['path'] = "input/key"
        config['body'] = {"key":"PlayPause"}
        post(config)

    elif args.command == "stop":
        config['path'] = "input/key"
        config['body'] = {"key":"Stop"}
        post(config)

    elif args.command == "fast_forward":
        config['path'] = "input/key"
        config['body'] = {"key":"FastForward"}
        post(config)

    elif args.command == "rewind":
        config['path'] = "input/key"
        config['body'] = {"key":"Rewind"}
        post(config)

    elif args.command == "next":
        config['path'] = "input/key"
        config['body'] = {"key":"Next"}
        post(config)

    elif args.command == "previous":
        config['path'] = "input/key"
        config['body'] = {"key":"Previous"}
        post(config)

    elif args.command == "cursor_up":
        config['path'] = "input/key"
        config['body'] = {"key":"CursorUp"}
        post(config)

    elif args.command == "cursor_down":
        config['path'] = "input/key"
        config['body'] = {"key":"CursorDown"}
        post(config)

    elif args.command == "cursor_left":
        config['path'] = "input/key"
        config['body'] = {"key":"CursorLeft"}
        post(config)

    elif args.command == "cursor_right":
        config['path'] = "input/key"
        config['body'] = {"key":"CursorRight"}
        post(config)

    elif args.command == "confirm":
        config['path'] = "input/key"
        config['body'] = {"key":"Confirm"}
        post(config)

    # a general POST request
    elif args.command == "post":
        if args.body and args.path:
            config['path'] = args.path
            config['body'] = json.loads(args.body)
            post(config)
        else:
            print("For general POST requests --path and --body are required") 

    # a general GET request
    elif args.command == "get":
        if args.path:
            config['path'] = args.path
            get(config)
        else:
            print("For general GET requests --path is required") 

if __name__ == '__main__':
    main()