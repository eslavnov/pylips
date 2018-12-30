# version 0.2
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

    # Built-in GET commands (basically wrappers around common API calls)
    available_commands_get={
        "list_channels": {
            "path": "channeldb/tv/channelLists/all"
        },
        "powerstate": {
            "path": "powerstate"
        }
    }

    # Built-in POST commands (basically wrappers around common API calls)
    available_commands_post ={
        "ambilight_on": {
            "path": "ambilight/power",
            "body": {
                "power": "On"
            }
        },
        "ambilight_off": {
            "path": "ambilight/power",
            "body": {
            "power": "Off"
            }
        },
        "ambilight_video_immersive": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_VIDEO",
                "isExpert": "false",
                "menuSetting": "IMMERSIVE"
            }
        },
        "ambilight_video_standard": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_VIDEO",
                "isExpert": "false",
                "menuSetting": "STANDARD"
            }
        },
        "ambilight_video_natural": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_VIDEO",
                "isExpert": "false",
                "menuSetting": "NATURAL"
            }
        },
        "ambilight_video_vivid": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_VIDEO",
                "isExpert": "false",
                "menuSetting": "VIVID"
            }
        },
        "ambilight_video_game": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_VIDEO",
                "isExpert": "false",
                "menuSetting": "GAME"
            }
        },
        "ambilight_video_comfort": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_VIDEO",
                "isExpert": "false",
                "menuSetting": "COMFORT"
            }
        },
        "ambilight_video_relax": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_VIDEO",
                "isExpert": "false",
                "menuSetting": "RELAX"
            }
        },
        "ambilight_audio_adapt_brightness": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "ENERGY_ADAPTIVE_BRIGHTNESS"
            }
        },
        "ambilight_audio_adapt_colors": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "ENERGY_ADAPTIVE_COLORS"
            }
        },
        "ambilight_audio_vu_meter": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "VU_METER"
            }
        },
        "ambilight_audio_spectrum": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "SPECTRUM_ANALYZER"
            }
        },
        "ambilight_audio_knight_rider_1": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "KNIGHT_RIDER_CLOCKWISE"
            }
        },
        "ambilight_audio_knight_rider_2": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "KNIGHT_RIDER_ALTERNATING"
            }
        },
        "ambilight_audio_flash": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "RANDOM_PIXEL_FLASH"
            }
        },
        "ambilight_audio_strobo": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "STROBO"
            }
        },
        "ambilight_audio_party": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "PARTY"
            }
        },
        "ambilight_audio_random": {
            "path": "ambilight/currentconfiguration",
            "body": {
                "styleName": "FOLLOW_AUDIO",
                "isExpert": "false",
                "menuSetting": "MODE_RANDOM"
            }
        },
        "ambihue_status": {
            "path": "menuitems/settings/current",
            "body": {
                "nodes": [
                    {
                        "nodeid": 2131230774
                    }
                ]
            }
        },
        "ambihue_on": {
            "path": "menuitems/settings/update",
            "body": {
                "values": [
                    {
                        "value": {
                            "Nodeid": 2131230774,
                            "Controllable": "true",
                            "Available": "true",
                            "data": {
                                "value": "true"
                            }
                        }
                    }
                ]
            }
        },
        "ambihue_off": {
            "path": "menuitems/settings/update",
            "body": {
                "values": [
                    {
                        "value": {
                            "Nodeid": 2131230774,
                            "Controllable": "true",
                            "Available": "true",
                            "data": {
                                "value": "false"
                            }
                        }
                    }
                ]
            }
        },
        "standby": {
            "path": "input/key",
            "body": {
                "key": "Standby"
            }
        },
        "mute": {
            "path": "input/key",
            "body": {
                "key": "Mute"
            }
        },
        "volume_up": {
            "path": "input/key",
            "body": {
                "key": "VolumeUp"
            }
        },
        "volume_down": {
            "path": "input/key",
            "body": {
                "key": "VolumeDown"
            }
        },
        "channel_up": {
            "path": "input/key",
            "body": {
                "key": "ChannelStepUp"
            }
        },
        "channel_down": {
            "path": "input/key",
            "body": {
                "key": "ChannelStepDown"
            }
        },
        "play": {
            "path": "input/key",
            "body": {
                "key": "Play"
            }
        },
        "pause": {
            "path": "input/key",
            "body": {
                "key": "Pause"
            }
        },
        "play_pause": {
            "path": "input/key",
            "body": {
                "key": "PlayPause"
            }
        },
        "stop": {
            "path": "input/key",
            "body": {
                "key": "Stop"
            }
        },
        "fast_forward": {
            "path": "input/key",
            "body": {
                "key": "FastForward"
            }
        },
        "rewind": {
            "path": "input/key",
            "body": {
                "key": "Rewind"
            }
        },
        "next": {
            "path": "input/key",
            "body": {
                "key": "Next"
            }
        },
        "previous": {
            "path": "input/key",
            "body": {
                "key": "Previous"
            }
        },
        "cursor_up": {
            "path": "input/key",
            "body": {
                "key": "CursorUp"
            }
        },
        "cursor_down": {
            "path": "input/key",
            "body": {
                "key": "CursorDown"
            }
        },
        "cursor_left": {
            "path": "input/key",
            "body": {
                "key": "CursorLeft"
            }
        },
        "cursor_right": {
            "path": "input/key",
            "body": {
                "key": "CursorRight"
            }
        },
        "confirm": {
            "path": "input/key",
            "body": {
                "key": "Confirm"
            }
        },
        "back": {
            "path": "input/key",
            "body": {
                "key": "Back"
            }
        },
        "find": {
            "path": "input/key",
            "body": {
                "key": "Find"
            }
        },
        "red": {
            "path": "input/key",
            "body": {
                "key": "RedColour"
            }
        },
        "green": {
            "path": "input/key",
            "body": {
                "key": "GreenColour"
            }
        },
        "yellow": {
            "path": "input/key",
            "body": {
                "key": "YellowColour"
            }
        },
        "blue": {
            "path": "input/key",
            "body": {
                "key": "BlueColour"
            }
        },
        "home": {
            "path": "input/key",
            "body": {
                "key": "Home"
            }
        },
        "options": {
            "path": "input/key",
            "body": {
                "key": "Options"
            }
        },
        "dot": {
            "path": "input/key",
            "body": {
                "key": "Dot"
            }
        },
        "digit_0": {
            "path": "input/key",
            "body": {
                "key": "Digit0"
            }
        },
        "digit_1": {
            "path": "input/key",
            "body": {
                "key": "Digit1"
            }
        },
        "digit_2": {
            "path": "input/key",
            "body": {
                "key": "Digit2"
            }
        },
        "digit_3": {
            "path": "input/key",
            "body": {
                "key": "Digit3"
            }
        },
        "digit_4": {
            "path": "input/key",
            "body": {
                "key": "Digit4"
            }
        },
        "digit_5": {
            "path": "input/key",
            "body": {
                "key": "Digit5"
            }
        },
        "digit_6": {
            "path": "input/key",
            "body": {
                "key": "Digit6"
            }
        },
        "digit_7": {
            "path": "input/key",
            "body": {
                "key": "Digit7"
            }
        },
        "digit_8": {
            "path": "input/key",
            "body": {
                "key": "Digit8"
            }
        },
        "digit_9": {
            "path": "input/key",
            "body": {
                "key": "Digit9"
            }
        },
        "info": {
            "path": "input/key",
            "body": {
                "key": "Info"
            }
        },
        "adjust": {
            "path": "input/key",
            "body": {
                "key": "Adjust"
            }
        },
        "watch_tv": {
            "path": "input/key",
            "body": {
                "key": "WatchTV"
            }
        },
        "viewmode": {
            "path": "input/key",
            "body": {
                "key": "Viewmode"
            }
        },
        "teletext": {
            "path": "input/key",
            "body": {
                "key": "Teletext"
            }
        },
        "subtitle": {
            "path": "input/key",
            "body": {
                "key": "Subtitle"
            }
        },
        "source": {
            "path": "input/key",
            "body": {
                "key": "Source"
            }
        },
        "ambilight_onoff": {
            "path": "input/key",
            "body": {
                "key": "AmbilightOnOff"
            }
        },
        "record": {
            "path": "input/key",
            "body": {
                "key": "Record"
            }
        },
        "online": {
            "path": "input/key",
            "body": {
                "key": "Online"
            }
        }
    }

    if args.command in available_commands_post:
        config['path'] = available_commands_post[args.command]['path']
        config['body'] = available_commands_post[args.command]['body']
        post(config)

    elif args.command in available_commands_get:
        config['path'] = available_commands_get[args.command]['path']
        get(config)

    # a general GET request for custom commands
    elif args.command == "get":
        if args.path:
            config['path'] = args.path
            get(config)
        else:
            print("For general GET requests --path is required") 
            
    # a general POST request for custom commands
    elif args.command == "post":
        if args.body and args.path:
            config['path'] = args.path
            config['body'] = json.loads(args.body)
            post(config)
        else:
            print("For general POST requests --path and --body are required") 

    else:
        print("Unknown command", args.command)

if __name__ == '__main__':
    main()
