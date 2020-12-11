# Pylips
Pylips is a Python tool to control Philips TVs (2015+) through their reverse-engineered API. 

1. Supports both Android and non-Android TVs
1. 80+ built-in commands + support for custom "GET" and "POST" requests to the API
1. All commands work on TVs with API version 6, most of them also work for API version 5
1. Full control of Ambilight including color, brightness, mode and 'Ambilight + Hue'
1. Allows sending TV status updates and receiving commands over MQTT

The current version of the API does not allow switching input sources anymore (?), use [this tool](https://github.com/eslavnov/android-tv-remote) instead (Android TVs only).

## Table of contents ##
1. [Prerequisites](#prerequisites)
1. [Setting up Pylips](#setting-up-pylips)
    1. [New users](#new-users)
    1. [Migrating from older versions](#migrating-from-older-versions)
1. [Controlling the TV (manual mode)](#controlling-the-tv-manual-mode)
    1. [Built-in commands](#built-in-commands)
    1. [Custom commands](#custom-commands)
1. [Controlling the TV (MQTT mode)](#controlling-the-tv-mqtt-mode)
1. [API reference](#api-reference)
1. [Change log](#change-log)
1. [TO-DO](#to-do)
1. [Acknowledgements](#acknowledgements)
1. [Contact details](#contact-details)

## Prerequisites

Provided that you have python (version 3+) on your system, install all the dependencies first:

```
pip3 install -r requirements.txt
```

You may have to use `pip` and `python` instead of `pip3` and `python3` depending on how these tools are installed on your system.

## Setting up Pylips

### New users ###

To begin using Pylips you first need to add the ip adress of your TV to the [TV] section in the `settings.ini` file. If you want to use MQTT, you will also need to fill in the [MQTT] section and set the required flags in the [DEFAULT] section:
```
[DEFAULT]
verbose = True          # show various debug output
MQTT_listen = False     # listen for MQTT commands. Requires correct [MQTT] settings
MQTT_update = False     # publish status updates over MQTT. Requires correct [MQTT] settings
num_retries = 3         # number of retries when sending requests. No need to change it unless your network sucks.
update_interval = 3     # interval between updates in seconds (used if MQTT_update = True). Your TV might not appreciate lower values.
[TV]
host =                  # TV's ip address
port =                  # will be discovered automatically, but you can override it here
apiv =                  # will be discovered automatically, but you can override it here
user =                  # will be discovered automatically (if required for your TV model), but you can override it here
pass =                  # will be discovered automatically (if required for your TV model), but you can override it here
protocol =              # will be discovered automatically, but you can override it here
[MQTT]
host =                  # your MQTT broker's ip address
port =                  # your MQTT broker's port
user =                  # your MQTT username
pass =                  # your MQTT password
TLS = False             # use TLS  
cert_path =             # full path to your custom certificate if you are using one, otherwise leave it blank            
topic_pylips =          # Pylips will listen for commands to this topic
topic_status =          # Pylips will send status updates to this topic
```

Now turn your TV on and run Pylips without any arguments to complete setting it up (it will discover your TV's API version, port and protocol + pair and save the credentials if required):

`python3 pylips.py`

Once it's done, you are ready to use Pylips!

**Security note:**

To pair with the Android TVs we need to create a HMAC signature using an 88-character (?) key. As far as I can tell the key is used for pairing only. With that in mind and to make this tool as user-friendly as possible, the key is hardcoded. I see no security issues with this but if you are extremely paranoid you can change it: look for a `secret_key` in the beginning of the code.

**Custom config path:**

You can load a custom config by specifying its **absolute** path with a `--config` parameter:

`python pylips.py --config '/home/eslavnov/repos/Pylips/some_settings.ini'`

### Migrating from older versions ###

The new version of Pylips is 100% backwards-compatible with the old arguments and commands, so you don't have to change anything to keep using it, but every call will take slightly longer to identify the API version. Follow the instructions for the new users to save your API version in `settings.ini`, then it will run faster. If you want to override the API version check you can also use the `--apiv` parameter (manual mode only). Finally, you still need to follow the instructions for the new users to take advantage of MQTT. 

## Controlling the TV (manual mode) ##
You can take advantage of some of the built-in commands or send your own custom commands.

### Built-in commands ###
```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command %command%
```

Any passed arguments will override the settings in `settings.ini` without overwriting them. If you have already run the discovery for new users, you don't have to specify `--host`, `--user` and `-pass` parameters. Also skip the `--user` and `--pass` parameters if your TV does not have Android. Add `--verbose False` to any command if you don't want to see the feedback in your terminal (useful for command line sensors). 


**Available built-in commands:**

&nbsp; &nbsp; &nbsp; &nbsp; **TV status:**
1. `powerstate` - Returns current power state of the TV ('On' or 'Off')
1. `volume` - Returns current volume and mute status
1. `current_channel` - Returns current channel (if in TV mode)
1. `current_app` - Returns current app (Android TVs only)

   **TV remote keys:**
1. `standby` - Sends Standby key
1. `mute` - Sends Mute key
1. `volume_up` - Sends VolumeUp key
1. `volume_down` - Sends VolumeDown key
1. `channel_up` - Sends ChannelStepUp key
1. `channel_down` - Sends ChannelStepDown key
1. `play` - Sends Play key
1. `pause` - Sends Pause key
1. `play_pause` - Sends PlayPause key
1. `stop` - Sends Stop key
1. `fast_forward` - Sends FastForward key
1. `rewind` - Sends Rewind key
1. `next` - Sends Next key
1. `previous` - Sends Previous key
1. `cursor_up` - Sends CursorUp key
1. `cursor_down` - Sends CursorDown key
1. `cursor_left` - Sends CursorLeft key
1. `cursor_right` - Sends CursorRight key
1. `confirm` - Sends Confirm key
1. `back` - Sends Back key
1. `home` - Sends Home key
1. `options` - Sends Options key
1. `info` - Sends Info key
1. `find` - Sends Find key
1. `adjust` - Sends Adjust key
1. `watch_tv` - Sends WatchTV key
1. `viewmode` - Sends Viewmode key
1. `teletext` - Sends Teletext key
1. `subtitle` - Sends Subtitle key
1. `record` - Sends Record key
1. `online` - Sends Online key
1. `source` - Sends Source key
1. `ambilight_onoff` - Sends AmbilightOnOff key
1. `red` - Sends RedColour key
1. `green` - Sends GreenColour key
1. `yellow` - Sends YellowColour key
1. `blue` - Sends BlueColour key
1. `dot` - Sends Dot key
1. `digit_0` - Sends Digit0 key
1. `digit_1` - Sends Digit1 key
1. `digit_2` - Sends Digit2 key
1. `digit_3` - Sends Digit3 key
1. `digit_4` - Sends Digit4 key
1. `digit_5` - Sends Digit5 key
1. `digit_6` - Sends Digit6 key
1. `digit_7` - Sends Digit7 key
1. `digit_8` - Sends Digit8 key
1. `digit_9` - Sends Digit9 key

   **TV channels:**
1. `set_channel` - Turns a specified channel on. Requires a valid `--body` argument, see [API reference](https://github.com/eslavnov/pylips/wiki/Activities-TV-(GET)/) to get it.
1. `list_channels` - Returns channel list
1. `list_favorite` - Returns favorite list

   **Ambilight:**
1. `ambilight_on` - Turns ambilight on
1. `ambilight_off` - Turns ambilight off
1. `ambihue_status` - Returns the current status of 'Ambilight + Hue'
1. `ambihue_on` - Turns 'Ambilight + Hue' on
1. `ambihue_off` - Turns 'Ambilight + Hue' off
1. `ambilight_color` - Sets ambilight color (in HSB format). Requires a valid `--body` argument: `{"hue": 360, "saturation": 100, "brightness": 255}`
1. `ambilight_brightness` - Sets ambilight brightness. Requires a valid `--body` argument: `{"value": 10}`
1. `ambilight_video_immersive` - Sets Ambilight to 'Follow video' (Immersive)
1. `ambilight_video_standard` - Sets Ambilight to 'Follow video' (Standard)
1. `ambilight_video_natural` - Sets Ambilight to 'Follow video' (Natural)
1. `ambilight_video_vivid` - Sets Ambilight to 'Follow video' (Vivid)
1. `ambilight_video_game` - Sets Ambilight to 'Follow video' (Game)
1. `ambilight_video_comfort` - Sets Ambilight to 'Follow video' (Comfort)
1. `ambilight_video_relax` - Sets Ambilight to 'Follow video' (Relax)
1. `ambilight_color_hot_lava` - Sets Ambilight to 'Follow color' (Hot lava)
1. `ambilight_color_warm_white` - Sets Ambilight to 'Follow color' (Warm white)
1. `ambilight_color_cool_white` - Sets Ambilight to 'Follow color' (Cool white)
1. `ambilight_color_fresh_nature` - Sets Ambilight to 'Follow color' (Fresh nature)
1. `ambilight_deep_water` - Sets Ambilight to 'Follow color' (Deep water)
1. `ambilight_audio_adapt_brightness` - Sets Ambilight to 'Follow audio' (Energy Adaptive Brightness)
1. `ambilight_audio_adapt_colors` - Sets Ambilight to 'Follow audio' (Energy Adaptive Colors)
1. `ambilight_audio_vu_meter` - Sets Ambilight to 'Follow audio' (VU Meter)
1. `ambilight_audio_spectrum` - Sets Ambilight to 'Follow audio' (Spectrum Analyzer)
1. `ambilight_audio_knight_rider_1` - Sets Ambilight to 'Follow audio' (Knight Rider Clockwise)
1. `ambilight_audio_knight_rider_2` - Sets Ambilight to 'Follow audio' (Knight Rider Alternating)
1. `ambilight_audio_flash` - Sets Ambilight to 'Follow audio' (Random Pixel Flash)
1. `ambilight_audio_strobo` - Sets Ambilight to 'Follow audio' (Stroboscope)
1. `ambilight_audio_party` - Sets Ambilight to 'Follow audio' (Party)
1. `ambilight_audio_random` - Sets Ambilight to 'Follow audio' (Random Mode)

   **Other:**
1. `launch_app` - Launches an app (Android TVs only). Requires a valid `--body` argument. See [API reference](https://github.com/eslavnov/pylips/wiki/Applications-(GET)) to get a list of installed apps, find your app in this list and use it as a `--body` argument.
1. `power_on` - Turns on the TV even if it's in a deep sleep mode. You might need to run `allow_power_on` first, although it was not needed for me.
1. `allow_power_on` - Allows to remotely power on the TV via chromecast requests.

**Examples of using the built-in commands:**

Send Stop key:
```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command stop
```

Turn Ambilight on:
```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command ambilight_on
```

Launch YouTube:
```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command launch_app --body '{"id":"com.google.android.apps.youtube.tv.activity.ShellActivity-com.google.android.youtube.tv","order":0,"intent":{"action":"Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 pkg=com.google.android.youtube.tv cmp=com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity }","component":{"packageName":"com.google.android.youtube.tv","className":"com.google.android.apps.youtube.tv.activity.ShellActivity"}},"label":"YouTube"}'
```

Launch Netflix:
```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command launch_app --body '{"label":"Netflix","intent":{"component":{"packageName":"com.netflix.ninja","className":"com.netflix.ninja.MainActivity"},"action":"Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 pkg=com.netflix.ninja cmp=com.netflix.ninja/.MainActivity }"},"order":0,"id":"com.netflix.ninja.MainActivity-com.netflix.ninja","type":"app"}'
```

Launch Amazon Prime Video:
```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command launch_app --body '{"id":"com.amazon.amazonvideo.livingroom","order":0,"intent":{"action":"Intent{act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 pkg=com.amazon.amazonvideo.livingroom }","component":{"packageName":"com.amazon.amazonvideo.livingroom","className":"com.amazon.ignition.IgnitionActivity"}},"label":"Prime Video"}'
```

Launch Kodi:
```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command launch_app --body '{"id":"org.xbmc.kodi","order":0,"intent":{"action":"Intent{act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 pkg=org.xbmc.kodi }","component":{"packageName":"org.xbmc.kodi","className":"org.xbmc.kodi.Splash"}},"label":"Kodi"}'
```

### Custom commands ###
The tools exposes two general commands to talk to the TV's API: `get` (sends GET request and *gets* back some data like ambilight mode) and `post` (sends POST request that *posts* some data and changes something in the TV - like turning the ambilight off). You can also add custom commands to `available_commands.json`.

Read the API reference first to understand available endpoints and how to use them. There are some unexpected things like:
* Pairing process returns objects like '{"error_id":"SUCCESS"}' (why, Philips?!)
* Using strings like 'On'/'Off' for boolean variables (really, Philips?!)
* API returns 'Nodeid' for some GET requests, while expecting 'nodeid' for POST requests (come on, Philips has to do it all on purpose, right? Right?)

**Get method:**

To use the `get` method you need to provide a path to the required endpoint with a `--path` argument. For example, this will send a get request to the `system` endpoint (https://yourIP:1926/6/system):

```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command get --path system
```

**Post method:**

To use the `post` method you need to provide a path to the required endpoint with a `--path` argument and the body of your POST request with a `--body` argument. For example, this will send a post request to the `menuitems/settings/current` endpoint with a body that will get back the status of 'Ambilight + Hue' (notice that the `--body` argument **needs to come inside the quotes for UNIX systems**):

```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command post --path menuitems/settings/current --body '{"nodes":[{"nodeid":2131230774}]}'
```

**For Windows systems**:

```
python3 pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command post --path menuitems/settings/current --body ^"{^"^"nodes^"^":[{^"^"nodeid^"^":2131230774}]}^"
```

## Controlling the TV (MQTT mode) ##
Pylips can connect to your MQTT broker to listen for commands and to publish TV status updates.

Edit the `settings.ini` according to your config and simply run `python3 pylips.py` without any arguments to run in MQTT mode.

Enabling `MQTT_listen` in `settings.ini` will allow you to send commands to a topic specified in `topic_pylips` by posting a JSON message. This works pretty much the same as sending manual commands: your arguments become keys and their values - values of these keys. You can send any commands (POST, GET and built-in), but you won't get anything in return since you are just publishing a message over MQTT. Useful for POST commands that change the state of your TV, but for general GET requests you are better off using the manual mode.

See examples:

```
# Let's say we want to change the brightness of ambilight to max (10):

# BUILT-IN COMMANDS

# Manual mode: 
python3 pylips.py --command ambilight_brightness --body '{"value":10}'

# MQTT mode: 
{"command":"ambilight_brightness", "body":{"value":10} 


# POST REQUESTS

# Manual mode: 
python3 pylips.py --command post --path 'menuitems/settings/update' --body '{"values":[{"value":{"Nodeid":2131230769,"Controllable":"true", "Available":"true", "string_id":"Brightness", "data":{"value":10}}}]}'

# MQTT mode: 
{"command":"post", "path": "menuitems/settings/update", "body": {"values":[{"value":{"Nodeid":2131230769,"Controllable":"true", "Available":"true","string_id":"Brightness", "data":{"value":10}}}]}}
 
```

Enabling `MQTT_update` in `settings.ini` will publish status updates to `topic_status` like these:
```
{"powerstate": "On", "volume": 28, "muted": false, "cur_app": "org.droidtv.settings", "ambilight": {"styleName": "FOLLOW_VIDEO", "isExpert": false, "menuSetting": "IMMERSIVE"}, "ambihue": false}
```
```
{"powerstate": "On", "volume": 28, "muted": false, "cur_app": {"app": "TV", "channel": {"channel": {"ccid": 644, "preset": "15", "name": "Comedy Central HD"}, "channelList": {"id": "allcab", "version": "19"}}}, "ambilight": {"styleName": "OFF", "isExpert": false}, "ambihue": false}
```

## API reference
The TV's API is roughly based on [JointSpace](http://jointspace.sourceforge.net/) with a current version of 6.2. The only available official documentation that I was able to find is for JointSpace version 1, which is incredibly outdated. 

Since no official API documentation is available, I've decided to collect and document to the best of my knowledge all endpoints that are working in API version 6+ (Philips TVs 2016-2018). Most of them should also work for API version 5 (2015 TVs). This API reference is based on:
* [Official JointSpace documentation](http://jointspace.sourceforge.net/projectdata/documentation/jasonApi/1/doc/API.html)
* Community endpoints (various endpoints discovered by the community over the years)
* Endpoints discovered by using a man-in-the-middle attack on an iPhone running an official Philips TV remote app (this finally allowed to discover an endpoint responsible for toggling 'Ambilight + Hue' mode among other things)

All endpoints in API reference are tested and fully working unless explicitly marked otherwise. Any comments, new endpoints and fixes to the API reference are incredibly welcome.

[The API reference](https://github.com/eslavnov/Pylips/wiki).

## Change log

### 1.2.0 - 2020-02-28
**Added**
- `ambilight_color_hot_lava`, `ambilight_color_warm_white`, `ambilight_color_cool_white`, `ambilight_color_fresh_nature`, `ambilight_color_deep_water` commands

### 1.1.1 - 2020-02-20
**Fixed**
- MQTT payload encoded with utf8 is now correctly decoded. Thx @popy2k14!

### 1.1.0 - 2020-01-12
**Added**
- Remote `power_on` command that works even from sleep mode. Should work for all Android TVs, not sure about other models. Thx [@neophob](https://github.com/neophob)!

**Fixed**
- Paths issue when running outside Pylips folder on Windows systems

**Changed**
- SSL session is now being reused to help with API stoping to respond
- Pycryptodome instead of the outdated pycrypto dependency

### 1.0.11 - 2019-11-27
**Added**
- Custom settings file support

### 1.0.10 - 2019-10-27
**Changed**
- Improved response handling in MQTT

### 1.0.9 - 2019-07-30
**Fixed**
- Fixed a bug in MQTT loop

### 1.0.8 - 2019-06-11
**Fixed**
- Fixed an edge case when a combination of certain parameters broke the tool (`MQTT_listen = True` + `MQTT_update = False`)

**Added**
- Add support for custom certificates (MQTT mode)

### 1.0.7 - 2019-05-22
**Fixed**
- Got my hands on some non-android TVs, fixed some small bugs in pairing/sending commands

### 1.0.6 - 2019-05-12
**Fixed**
- Fixed `ambilight_brightness` command (manual mode)

### 1.0.5 - 2019-05-05
**Fixed**
- Fixed `launch_app` command

### 1.0.4 - 2019-04-29
**Fixed**
- Fixed a broken check for `path` and `body` arguments in MQTT mode

### 1.0.3 - 2019-04-28
**Fixed**
- Fixed a bug that broke some POST requests

### 1.0.2 - 2019-04-27
**Changed**
- Relative paths => absolute paths so it plays nice with tools like crontab

### 1.0.1 - 2019-04-25
**Changed**
- Fixed a bug in pairing (Android TVs)
- Changed `power_on` to `powerstate` in TV status, so now we support "Standby" and possibly other modes (MQTT-only)

### 1.0.0 - 2019-04-21
**Changed**
- Most of the app was rewritten, but it's backward-compatible with previous versions.
- Pylips is now a Python class so you can potentially integrate it with your other projects

**Added**
- Config file so you don't have to pass the same parameters every time
- Automatic discovery of your TV's API version, port and protocol
- Automatic pairing for Android TVs
- Support for API version 5 + any newer versions should also work (unless Philips breaks something in the future versions of the API)
- MQTT listener: send commands to Pylips over MQTT
- MQTT updater: Pylips can listen for TV status updates and send them over MQTT
- Extend built-in commands (set ambilight color, set ambilight brightness, get current volume, get current app)
- Move built-in commands to a separate JSON file

### 0.4 - 2019-01-28
**Added**
- Expand built-in commands (set/get TV channel and launch apps)
- Add `--verbose` option

### 0.3 - 2018-12-31
**Added**
- Non-Android Philips TVs are now also supported

### 0.2 - 2018-12-30
**Added**
- All TV remote key commands are now built-in
- Add change log to README

### 0.1 - 2018-12-26
Initial release

## TO-DO
~1. Finish documenting and testing all available API endpoints (January 2019)~ DONE

~2. Increase number of built-in commands~ DONE

~3. Improve error handling when sending requests~ DONE

~4. User-friendly way of changing Ambilight colors~ DONE

~5. Move settings to a config file~ DONE

~6. MQTT server support~ DONE

~7. Home assistant integration~ CANCELLED: not needed since you can now integrate it with MQTT sensors/switches.

At this point I consider the tool to be completed. No new functionality is planned, but I will fix any reported bugs and add any missing API endpoints/commands. [Open an issue](https://github.com/eslavnov/pylips/issues) with your problem/suggestions.

## Acknowledgements
1. TV pairing mechanism as well as the inspiration for this tool come from [@suborb](https://github.com/suborb)'s brilliant [repo](https://github.com/suborb/philips_android_tv).
2. This tool was also inspired by [@arzzen](https://github.com/arzzen)'s CLI [tool](https://github.com/arzzen/philips-tv).
3. [@jomwells](https://github.com/jomwells) did a pretty good job of collecting various [ambilight endpoints](https://github.com/jomwells/ambilights).
4. [Some good info](https://gist.github.com/marcelrv/ee9a7cf97c227d069e4ee88d26691019) from [@marcelrv](https://gist.github.com/marcelrv).

## Contact details
Email: eslavnov@gmail.com; LinkedIn: https://www.linkedin.com/in/evgeny-slavnov/
