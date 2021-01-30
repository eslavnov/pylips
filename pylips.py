# version 1.3.2
import platform    
import subprocess
import configparser
import requests
import json
import string
import time
import argparse
import sys
import random
from base64 import b64encode,b64decode
from Crypto.Hash import SHA, HMAC
from requests.auth import HTTPDigestAuth
import paho.mqtt.client as mqttc
import os 

# Suppress "Unverified HTTPS request is being made" error message
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
session.verify = False
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=1))

# Key used for generated the HMAC signature
secret_key="JCqdN5AcnAHgJYseUn7ER5k3qgtemfUvMRghQpTfTZq7Cvv8EPQPqfz6dDxPQPSu4gKFPWkJGw32zyASgJkHwCjU"

parser = argparse.ArgumentParser(description="Control Philips TV API (versions 5 and 6)")
parser.add_argument("--host", dest="host", help="TV's ip address")
parser.add_argument("--user", dest="user", help="Username")
parser.add_argument("--pass", dest="password", help="Password")
parser.add_argument("--command", help="Command to run", default="")
parser.add_argument("--path", dest="path", help="API's endpoint path")
parser.add_argument("--body", dest="body", help="Body for post requests")
parser.add_argument("--verbose", dest="verbose", help="Display feedback")
parser.add_argument("--apiv", dest="apiv", help="Api version", default="")
parser.add_argument("--config", dest="config", help="Path to config file", default=os.path.dirname(os.path.realpath(__file__))+os.path.sep+"settings.ini")

args = parser.parse_args()

class Pylips:
    def __init__(self, ini_file):
        # read config file
        self.config = configparser.ConfigParser()

        if os.path.isfile(ini_file) == False:
            return print("Config file", ini_file, "not found")

        try:
            self.config.read(ini_file)
        except:
            return print("Config file", ini_file, "found, but cannot be read")

        if args.host is None and self.config["TV"]["host"]=="":
            return print("Please set your TV's IP-address with a --host parameter or in [TV] section in settings.ini")
            
        # check verbose option
        if self.config["DEFAULT"]["verbose"] == "True":
            self.verbose = True
        else:
            self.verbose = False

        # override config with passed args
        if len(sys.argv)>1:
            if args.verbose is not None:
                if args.verbose.lower()=="true":
                  self.verbose = True
                else:
                  self.verbose = False
            if args.host:
                self.config["TV"]["host"] = args.host
            if args.user and args.password:
                self.config["TV"]["user"] = args.user
                self.config["TV"]["pass"] = args.password
                self.config["TV"]["port"] = "1926"
                self.config["TV"]["protocol"] = "https://"
            elif (len(self.config["TV"]["user"])==0 or len(self.config["TV"]["pass"])==0) and self.config["TV"]["port"] == 1926:
                return print ("If you have an Android TV, please provide both a username and a password (--user and --pass)")
            if len(args.apiv) != 0:
                self.config["TV"]["apiv"]=args.apiv

        # check API version
        if len(self.config["TV"]["apiv"])==0:
            if self.find_api_version(self.verbose):
                if self.check_if_paired() is False:
                    print("No valid credentials found, starting pairing process...")
                    self.pair()
                with open("settings.ini", "w") as configfile:
                    self.config.write(configfile)
            else:
                if self.is_online(self.config["TV"]["host"]):
                    return print("IP", self.config["TV"]["host"], "is online, but no known API is found. Exiting...")
                else:
                    return print("IP", self.config["TV"]["host"], "seems to be offline. Exiting...")

        # load API commands
        with open(os.path.dirname(os.path.realpath(__file__))+"/available_commands.json") as json_file:  
            self.available_commands = json.load(json_file)

        # start MQTT listener and updater if required
        if (len(sys.argv)==1 or (len(sys.argv)==3 and sys.argv[1] == "--config")) and self.config["DEFAULT"]["mqtt_listen"] == "True":
                if len(self.config["MQTT"]["host"])>0:
                    # listen for MQTT messages to run commands
                    self.start_mqtt_listener()
                    if self.config["DEFAULT"]["mqtt_update"] == "True":
                        # Update TV status and publish any changes
                        self.last_status = {"powerstate": None, "volume":None, "muted":False, "cur_app":None, "ambilight":None, "ambihue":False}
                        self.start_mqtt_updater(self.verbose)
                else:
                    print("Please specify host in MQTT section in settings.ini to use MQTT")
        elif len(sys.argv)>1:
            # parse the passed args and run required command
            body=args.body
            path=args.path
            if args.command == "get":
                self.get(path,self.verbose)
            elif args.command == "post":
                self.post(path, body, self.verbose)
            elif len(args.command)>0:
                self.run_command(args.command,body, self.verbose)
            else:
                print("Please provide a valid command with a '--command' argument")
        else:
            print("Please enable mqtt_listen in settings.ini or provide a valid command with a '--command' argument")
               
    def is_online(self, host):
        """
        Returns True if host (str) responds to a ping request.
        """
        # Option for the number of packets as a function of
        param = "-n" if platform.system().lower()=="windows" else "-c"

        # Building the command. Ex: "ping -c 1 google.com"
        command = ["ping", param, "1", host]

        return subprocess.call(command) == 0

    # finds API version, saves it to settings.ini (["TV"]["apiv"]) and returns True if successful.
    def find_api_version(self, verbose=True, possible_ports=[1925], possible_api_versions=[6,5,1]):
        if verbose:
            print ("Checking API version and port...")
        protocol="http://"
        for port in possible_ports:
            for api_version in possible_api_versions:
                try:
                    if verbose:
                        print("Trying", str(protocol) + str(self.config["TV"]["host"]) + ":" + str(port)+"/" + str(api_version)+"/system")
                    r = session.get(str(protocol) + str(self.config["TV"]["host"]) + ":" + str(port)+"/" + str(api_version)+"/system", verify=False, timeout=2)
                except requests.exceptions.ConnectionError:
                    print("Connection refused")
                    continue
                if r.status_code == 200:
                    if "api_version" in r.json():
                        self.config["TV"]["apiv"] = str(r.json()["api_version"]["Major"])
                    else:
                        print("Could not find a valid API version! Pylips will try to use '", api_version, "'" )
                        self.config["TV"]["apiv"] = str(api_version)
                    if "featuring" in r.json() and "systemfeatures" in r.json()["featuring"] and "pairing_type" in r.json()["featuring"]["systemfeatures"] and r.json()["featuring"]["systemfeatures"]["pairing_type"] == "digest_auth_pairing":
                        self.config["TV"]["protocol"] = "https://"
                        self.config["TV"]["port"] = "1926"
                    else:
                        self.config["TV"]["protocol"] = "http://"
                        self.config["TV"]["port"] = "1925"
                    return True
        return False

    # returns True if already paired or using non-Android TVs.
    def check_if_paired(self):
        if str(self.config["TV"]["protocol"])=="https://" and (len(str(self.config["TV"]["user"]))==0 or len(str(self.config["TV"]["pass"]))==0):
            return False
        else:
            return True
        
    # creates random device id
    def createDeviceId(self):
        return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))

    # creates signature
    def create_signature(self, secret_key, to_sign):
        sign = HMAC.new(secret_key, to_sign, SHA)
        return str(b64encode(sign.hexdigest().encode()))

    # creates device spec JSON
    def getDeviceSpecJson(self, config):
        device_spec =  { "device_name" : "heliotrope", "device_os" : "Android", "app_name" : "Pylips", "type" : "native"}
        device_spec["app_id"] = config["application_id"]
        device_spec["id"] = config["device_id"]
        return device_spec

    # initiates pairing with a TV
    def pair(self, err_count=0):
        payload = {}
        payload["application_id"] = "app.id"
        payload["device_id"] = self.createDeviceId()
        self.config["TV"]["user"] = payload["device_id"]
        data = { "scope" :  [ "read", "write", "control"] }
        data["device"]  = self.getDeviceSpecJson(payload)
        print("Sending pairing request")
        self.pair_request(data)

    # pairs with a TV
    def pair_request(self, data, err_count=0):
        print("https://" + str(self.config["TV"]["host"]) + ":1926/"+str(self.config["TV"]["apiv"])+"/pair/request")
        response={}
        r = session.post("https://" + str(self.config["TV"]["host"]) + ":1926/"+str(self.config["TV"]["apiv"])+"/pair/request", json=data, verify=False, timeout=2)
        if r.json() is not None:
            if r.json()["error_id"] == "SUCCESS":
                response=r.json()
            else:
                return print("Error", r.json())
        else:
            return print("Can not reach the API")

        auth_Timestamp = response["timestamp"]
        self.config["TV"]["pass"] = response["auth_key"]
        data["device"]["auth_key"] = response["auth_key"]
        pin = input("Enter onscreen passcode: ")

        auth = { "auth_AppId" : "1"}
        auth["pin"] = str(pin)
        auth["auth_timestamp"] = auth_Timestamp
        auth["auth_signature"] = self.create_signature(b64decode(secret_key), str(auth_Timestamp).encode() + str(pin).encode())

        grant_request = {}
        grant_request["auth"] = auth
        data["application_id"]="app.id"
        data["device_id"]=self.config["TV"]["user"]
        grant_request["device"]  = self.getDeviceSpecJson(data)

        print("Attempting to pair")
        self.pair_confirm(grant_request)

    # confirms pairing with a TV
    def pair_confirm(self, data, err_count=0):
        while err_count < 10:
            if err_count > 0:
                print("Resending pair confirm request")
            try:
                r = session.post("https://" + str(self.config["TV"]["host"]) +":1926/"+str(self.config["TV"]["apiv"])+"/pair/grant", json=data, verify=False, auth=HTTPDigestAuth(self.config["TV"]["user"], self.config["TV"]["pass"]),timeout=2)
                print("Username for subsequent calls is: " + str(self.config["TV"]["user"]))
                print("Password for subsequent calls is: " + str(self.config["TV"]["pass"]))
                return print("The credentials are saved in the settings.ini file.")
            except Exception:
                # try again
                err_count += 1
                continue
        else:
            return print("The API is unreachable. Try restarting your TV and pairing again")

    # sends a general GET request
    def get(self, path, verbose=True, err_count=0, print_response=True):
        while err_count < int(self.config["DEFAULT"]["num_retries"]):
            if verbose:
                print("Sending GET request to", str(self.config["TV"]["protocol"]) + str(self.config["TV"]["host"]) + ":" + str(self.config["TV"]["port"]) + "/" + str(self.config["TV"]["apiv"]) + "/" + str(path))
            try:
                r = session.get(str(self.config["TV"]["protocol"]) + str(self.config["TV"]["host"]) + ":" + str(self.config["TV"]["port"]) + "/" + str(self.config["TV"]["apiv"]) + "/" + str(path), verify=False, auth=HTTPDigestAuth(str(self.config["TV"]["user"]), str(self.config["TV"]["pass"])), timeout=2)
            except Exception:
                err_count += 1
                continue
            if verbose:
                print("Request sent!")
            if len(r.text) > 0:
                if print_response:
                  print(r.text)
                return r.text
        else:
            if self.config["DEFAULT"]["mqtt_listen"].lower()=="true":
                self.mqtt_update_status({"powerstate":"Off", "volume":None, "muted":False, "cur_app":None, "ambilight":None, "ambihue":False})
            return json.dumps({"error":"Can not reach the API"})

    # sends a general POST request
    def post(self, path, body, verbose=True, callback=True, err_count=0):
        while err_count < int(self.config["DEFAULT"]["num_retries"]):
            if type(body) is str:
                body = json.loads(body)
            if verbose:
                print("Sending POST request to", str(self.config["TV"]["protocol"]) + str(self.config["TV"]["host"]) + ":" + str(self.config["TV"]["port"]) + "/" + str(self.config["TV"]["apiv"]) + "/" + str(path)) 
            try:
                r = session.post(str(self.config["TV"]["protocol"]) + str(self.config["TV"]["host"]) + ":" + str(self.config["TV"]["port"]) + "/" + str(self.config["TV"]["apiv"]) + "/" + str(path), json=body, verify=False, auth=HTTPDigestAuth(str(self.config["TV"]["user"]), str(self.config["TV"]["pass"])), timeout=2)
            except Exception:
                err_count += 1
                continue
            if verbose:
                print("Request sent!")
            if callback and self.config["DEFAULT"]["mqtt_listen"].lower()=="true" and len(sys.argv)==1:
                # run mqtt callback to update the status (only in MQTT mode)
                self.mqtt_callback(path)
            if len(r.text) > 0:
                print(r.text)
                return r.text
            elif r.status_code == 200:
                print(json.dumps({"response":"OK"}))
                return json.dumps({"response":"OK"})
        else:
            if self.config["DEFAULT"]["mqtt_listen"].lower()=="true" and len(sys.argv)==1:
                self.mqtt_update_status({"powerstate":"Off", "volume":None, "muted":False, "cur_app":None, "ambilight":None, "ambihue":False})
            print(json.dumps({"error":"Can not reach the API"}))
            return json.dumps({"error":"Can not reach the API"})

    # runs a command
    def run_command(self, command, body=None, verbose=True, callback=True, print_response=True):
        if command in self.available_commands["get"]:
            return self.get(self.available_commands["get"][command]["path"],verbose, 0, print_response)
        elif command in self.available_commands["post"]:
            if "body" in self.available_commands["post"][command] and body is None:
                if "input_" in command:
                    body = self.available_commands["post"]["google_assistant"]["body"]
                    path = self.available_commands["post"]["google_assistant"]["path"]
                    body["intent"]["extras"]["query"] = self.available_commands["post"][command]["body"]["query"]
                else:
                  body = self.available_commands["post"][command]["body"]
                  path = self.available_commands["post"][command]["path"]
                return self.post(path,body,verbose, callback)
            if "body" in self.available_commands["post"][command] and body is not None:
                if type(body) is str:
                    body = json.loads(body)
                new_body = self.available_commands["post"][command]["body"]
                if command == "ambilight_brightness":
                    new_body["values"][0]["value"]["data"] = body
                elif command == "ambilight_color":
                    new_body["colorSettings"]["color"]["hue"] = int(body["hue"]*(255/360))
                    new_body["colorSettings"]["color"]["saturation"]=int(body["saturation"]*(255/100))
                    new_body["colorSettings"]["color"]["brightness"]=int(body["brightness"])
                elif command == "google_assistant":
                    new_body["intent"]["extras"]["query"] = body["query"]
                elif "input_" in command:
                    new_body = self.available_commands["google_assistant"][command]
                    new_body["intent"]["extras"]["query"] = self.available_commands["post"][command]["body"]["query"]
                return self.post(self.available_commands["post"][command]["path"], new_body, verbose, callback)
            else:
                return self.post(self.available_commands["post"][command]["path"], body,verbose, callback)
        elif command in self.available_commands["power"]:
            return session.post("http://" + str(self.config["TV"]["host"]) +":8008/"+self.available_commands["power"][command]["path"], verify=False, timeout=2)
        else:
            print("Unknown command")

    # updates status immediately after sending a POST request. Currently works only for ambilight and ambihue.        
    def mqtt_callback(self, path):
        if "ambilight" or "ambihue" in path:
            self.mqtt_update_ambilight()
            self.mqtt_update_ambihue()

    # starts MQTT listener that accepts Pylips commands               
    def start_mqtt_listener(self):
        def on_connect(client, userdata, flags, rc):
            print("Connected to MQTT broker at", self.config["MQTT"]["host"])
            client.subscribe(self.config["MQTT"]["topic_pylips"])
        def on_message(client, userdata, msg):
                if str(msg.topic)==self.config["MQTT"]["topic_pylips"]:
                  try:
                    message = json.loads(msg.payload.decode('utf-8'))
                  except:
                    return print("Invalid JSON in mqtt message:", msg.payload.decode('utf-8'))
                if "status" in message:
                    self.mqtt_update_status(message["status"])
                if "command" in message:
                    body=None
                    path=""
                    if "body" in message:
                        body = message["body"]
                    if "path" in message:
                        path = message["path"]
                    if message["command"] == "get":
                        if len(path)==0:
                            return print("Please provide a 'path' argument")
                        self.get(path,self.verbose,0,False)
                    elif message["command"] == "post":
                        if len(path)==0:
                            return print("Please provide a 'path' argument")
                        self.post(path, body, self.verbose)
                    elif message["command"] != "post" and message["command"] != "get":
                        self.run_command(message["command"],body, self.verbose)

        self.mqtt = mqttc.Client()
        self.mqtt.on_connect = on_connect
        self.mqtt.on_message = on_message

        if len(self.config["MQTT"]["user"])>0 and len(self.config["MQTT"]["pass"])>0:
            self.mqtt.username_pw_set(self.config["MQTT"]["user"], self.config["MQTT"]["pass"])
        if self.config["MQTT"]["TLS"].lower()=="true":
            if len(self.config["MQTT"]["cert_path"].strip())>0:
                self.mqtt.tls_set(self.config["MQTT"]["cert_path"])
            else:
                self.mqtt.tls_set()
        self.mqtt.connect(str(self.config["MQTT"]["host"]), int(self.config["MQTT"]["port"]), 60)
        if self.config["DEFAULT"]["mqtt_listen"] == "True" and self.config["DEFAULT"]["mqtt_update"] == "False":
            self.mqtt.loop_forever()
        else:
            self.mqtt.loop_start()

    # publishes an update with TV status over MQTT
    def mqtt_update_status(self, update):
        new_status = dict(self.last_status, **update)
        if json.dumps(new_status) != json.dumps(self.last_status):
            self.last_status = new_status
            self.mqtt.publish(str(self.config["MQTT"]["topic_status"]), json.dumps(self.last_status), retain = True)
    
    # updates powerstate for MQTT status and returns True if TV is on
    def mqtt_update_powerstate(self):
        powerstate_status = self.get("powerstate",self.verbose,0, False)
        if powerstate_status is not None and powerstate_status[0]=='{':
            powerstate_status = json.loads(powerstate_status)
            if "powerstate" in powerstate_status:
                if "powerstate" in self.last_status and self.last_status["powerstate"] != powerstate_status['powerstate']:
                    self.mqtt.publish(str(self.config["MQTT"]["topic_pylips"]), json.dumps({"status":{"powerstate":powerstate_status['powerstate']}}), retain = False)
                if powerstate_status['powerstate'].lower()=="on":
                    return True
            else:
                self.mqtt_update_status({"powerstate":"Off", "volume":None, "muted":False, "cur_app":None, "ambilight":None, "ambihue":False})
        else:
                self.mqtt_update_status({"powerstate":"Off", "volume":None, "muted":False, "cur_app":None, "ambilight":None, "ambihue":False})
        return False

    # updates ambilight for MQTT status
    def mqtt_update_ambilight(self):
        ambilight_status = self.get("ambilight/currentconfiguration",self.verbose,0,False)
        if ambilight_status is not None and ambilight_status[0]=='{':
            ambilight_status = json.loads(ambilight_status)
            if "styleName" in ambilight_status:
                ambilight = ambilight_status
                if json.dumps(self.last_status["ambilight"]) != json.dumps(ambilight):
                    self.mqtt.publish(str(self.config["MQTT"]["topic_pylips"]), json.dumps({"status":{"ambilight":ambilight}}), retain = False)
    
    # updates ambihue for MQTT status
    def mqtt_update_ambihue(self):
        ambihue_status = self.run_command("ambihue_status",None,self.verbose, False, False)
        if ambihue_status is not None and ambihue_status[0]=='{':
            ambihue_status = json.loads(ambihue_status)
            if "power" in ambihue_status:
                ambihue = ambihue_status["power"]
                if self.last_status["ambihue"] != ambihue:
                    self.mqtt.publish(str(self.config["MQTT"]["topic_pylips"]), json.dumps({"status":{"ambihue":ambihue}}), retain = False)

    # updates current app for MQTT status
    def mqtt_update_app(self):
        actv_status = self.run_command("current_app",None,self.verbose, False, False)
        if actv_status is not None and actv_status[0]=='{':
            actv_status=json.loads(actv_status)
            if "component" in actv_status:
                if actv_status["component"]["packageName"] == "org.droidtv.zapster" or actv_status["component"]["packageName"] =="NA":
                    self.mqtt_update_channel()
                else:
                    if self.last_status["cur_app"] is None or self.last_status["cur_app"] != actv_status["component"]["packageName"]:
                        self.mqtt.publish(str(self.config["MQTT"]["topic_pylips"]), json.dumps({"status":{"cur_app":actv_status["component"]["packageName"]}}), retain = False)

    # updates current channel for MQTT status
    def mqtt_update_channel(self):
        channel = self.run_command("current_channel",None,self.verbose, False)
        if channel is not None and channel[0]=='{':
            channel=json.loads(channel)
            if "channel" in channel:
                if json.dumps(self.last_status["cur_app"]) != json.dumps({"app":"TV","channel":channel}):
                    self.mqtt.publish(str(self.config["MQTT"]["topic_pylips"]), json.dumps({"status":{"cur_app":{"app":"TV","channel":channel}}}), retain = False)
    
    # updates volume and mute state for MQTT status
    def mqtt_update_volume(self):
        vol_status = self.run_command("volume",None,self.verbose, False, False)
        if vol_status is not None:
            vol_status = json.loads(vol_status)
            if "muted" in vol_status:
                muted = vol_status["muted"]
                volume = vol_status["current"]
                if self.last_status["muted"] != muted or self.last_status["volume"] != volume:
                    self.mqtt.publish(str(self.config["MQTT"]["topic_pylips"]), json.dumps({"status":{"muted":muted, "volume":volume}}), retain = False)

    # runs MQTT update functions with a specified update interval
    def start_mqtt_updater(self, verbose=True):
        print("Started MQTT status updater")
        while True:
            if self.mqtt_update_powerstate():
                self.mqtt_update_volume()
                self.mqtt_update_app()
                self.mqtt_update_ambilight()
                self.mqtt_update_ambihue()
            time.sleep(int(self.config["DEFAULT"]["update_interval"]))

if __name__ == '__main__':
    pylips = Pylips(args.config)
