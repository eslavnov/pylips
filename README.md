# Pylips
Pylips is a Python tool to control Philips TVs (2016+) through their reverse-engineered API.

There are some similar modules available, but they lack documentation, miss some API methods and sometimes have outdated code. This module is the most complete one in terms of both functionality and documentation. It supports both Android and non-Android Philips TVs.

**It is also the only module that allows toggling 'Ambilight + Hue' setting.**

The current version of the API does not allow switching input sources anymore (?), use [this tool](https://github.com/eslavnov/android-tv-remote) instead (Android TVs only).

## Table of contents ##
1. [Prerequisites](#prerequisites)
1. [Pairing with the TV (Android TVs only)](#pairing-with-the-tv-android-tvs-only)
1. [Controlling the TV](#controlling-the-tv)
    1. [Built-in commands](#built-in-commands)
    1. [Custom commands](#custom-commands)
1. [API reference](#api-reference)
1. [Change log](#change-log)
1. [TO-DO](#to-do)
1. [Acknowledgements](#acknowledgements)
1. [Contact details](#contact-details)

## Prerequisites

Provided that you have python (version 3+) on your system, install all the dependencies first:

```
pip install -r requirements.txt
```

You may have to use `pip3` and `python3` instead of `pip` and `python` depending on how these tools are installed on your system.

**If your TV has Android, you have to pair with the TV first to get a username/password which you will need to provide with `--user` and `--pass` parameters for all future calls.**

**If your TV does not have Android, you do NOT need to pair with the TV. You should also NEVER use `--user` and `--pass` parameters - they are required for Android TVs only.**

## Pairing with the TV (Android TVs only)

To use this tool with your Philips Android TV you will need a username and a password, which you can get by running the tool with a `-- host` parameter (your TV's ip address):

```
python pylips.py --host 192.168.201.10
```
The TV will display a 4-digit pin-code that you need to input to get a username and password. 

**Write down the username and password since they are required for all future calls!**

**Security note:**

To pair with the TV we need to create a HMAC signature using an 88-character (?) key. As far as I can tell the key is used for pairing only. With that in mind and to make this tool as user-friendly as possible, the key is hardcoded. I see no security issues with this but if you are extremely paranoid you can change it: look for a `secret_key` in the beginning of the code.

## Controlling the TV ##
You can take advantage of some of the built-in commands (to be extended) or send your own custom commands.

Add `--verbose 0` to any command if you don't want to see the feedback in your terminal (useful for command line sensors).

### Built-in commands ###
```
python pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command %command%
```

Skip the `--user` and `--pass` parameters if your TV does not have Android.

**Available built-in commands:**

&nbsp; &nbsp; &nbsp; &nbsp; **TV power:**
1. `powerstate` - Returns the current power state of the TV ('On' or 'Off')

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
1. `current_channel` - Returns current channel (if in TV mode)
1. `set_channel` - Turns a specified channel on. Requires a valid `--body` argument, see [API reference](https://github.com/eslavnov/pylips/wiki/Activities-TV-(GET)/) to get it.
1. `list_channels` - Returns channel list
1. `list_favorite` - Returns favorite list

   **Ambilight:**
1. `ambilight_on` - Turns ambilight on
1. `ambilight_off` - Turns ambilight off
1. `ambihue_status` - Returns the current status of 'Ambilight + Hue'
1. `ambihue_on` - Turns 'Ambilight + Hue' on
1. `ambihue_off` - Turns 'Ambilight + Hue' off
1. `ambilight_video_immersive` - Sets Ambilight to 'Follow video' (Immersive)
1. `ambilight_video_standard` - Sets Ambilight to 'Follow video' (Standard)
1. `ambilight_video_natural` - Sets Ambilight to 'Follow video' (Natural)
1. `ambilight_video_vivid` - Sets Ambilight to 'Follow video' (Vivid)
1. `ambilight_video_game` - Sets Ambilight to 'Follow video' (Game)
1. `ambilight_video_comfort` - Sets Ambilight to 'Follow video' (Comfort)
1. `ambilight_video_relax` - Sets Ambilight to 'Follow video' (Relax)
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
1. `launch_app` - Launches an app (Android TVs only). Requires a valid `--body` argument, see [API reference](https://github.com/eslavnov/pylips/wiki/Activities-current-(GET)) to get it.

**Examples of using the built-in commands:**

Send Stop key:
```
python pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command stop
```

Turn Ambilight on:
```
python pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command ambilight_on
```

Launch YouTube:
```
python pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command launch_app --body '{"id":"com.google.android.apps.youtube.tv.activity.ShellActivity-com.google.android.youtube.tv","order":0,"intent":{"action":"Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 pkg=com.google.android.youtube.tv cmp=com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity }","component":{"packageName":"com.google.android.youtube.tv","className":"com.google.android.apps.youtube.tv.activity.ShellActivity"}},"label":"YouTube"}'
```

### Custom commands ###
The tools exposes two general commands to talk to the TV's API: `get` (sends GET request and *gets* back some data like ambilight mode) and `post` (sends POST request that *posts* some data and changes something in the TV - like turning the ambilight off).

Read the API reference first to understand available endpoints and how to use them. There are some unexpected things like:
* Pairing process returns objects like '{"error_id":"SUCCESS"}' (why, Philips?!)
* Using strings like 'On'/'Off' for boolean variables (really, Philips?!)
* API returns 'Nodeid' for some GET requests, while expecting 'nodeid' for POST requests (come on, Philips has to do it all on purpose, right? Right?)

**Get method:**

To use the `get` method you need to provide a path to the required endpoint with a `--path` argument. For example, this will send a get request to the `system` endpoint (https://yourIP:1926/6/system):

```
python pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command get --path system
```

**Post method:**

To use the `post` method you need to provide a path to the required endpoint with a `--path` argument and the body of your POST request with a `--body` argument. For example, this will send a post request to the `menuitems/settings/current` endpoint with a body that will get back the status of 'Ambilight + Hue' (notice that the `--body` argument **needs to come inside the quotes**):

```
python pylips.py --host %TV's_ip_address% --user %username% --pass %password% --command get --path menuitems/settings/current --body '{"nodes":[{"nodeid":2131230774}]}'
```
## API reference
The TV's API is roughly based on [JointSpace](http://jointspace.sourceforge.net/) with a current version of 6.2. The only available official documentation that I was able to find is for JointSpace version 1, which is incredibly outdated. 

Since no official API documentation is available, I've decided to collect and document to the best of my knowledge all endpoints that are working in API version 6+ (Philips TVs 2016-2018). This API reference is based on:
* [Official JointSpace documentation](http://jointspace.sourceforge.net/projectdata/documentation/jasonApi/1/doc/API.html)
* Community endpoints (various endpoints discovered by the community over the years)
* Endpoints discovered by using a man-in-the-middle attack on an iPhone running an official Philips TV remote app (this finally allowed to discover an endpoint responsible for toggling 'Ambilight + Hue' mode among other things)

All endpoints in API reference are tested and fully working unless explicitly marked otherwise. Some channel endpoints are missing since I can not test them until January 2019. Any comments, new endpoints and fixes to the API reference are incredibly welcome.

[The API reference (work in progress)](https://github.com/eslavnov/Pylips/wiki).

## Change log


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
1. Finish documenting and testing all available API endpoints (January 2019)
2. Increase number of built-in commands
3. Improve error handling when sending requests
4. User-friendly way of changing Ambilight colors
5. Move settings to a config file
6. MQTT server support
7. Home assistant integration

## Acknowledgements
1. TV pairing mechanism as well as the inspiration for this tool come from [@suborb](https://github.com/suborb)'s brilliant [repo](https://github.com/suborb/philips_android_tv).
2. This tool was also inspired by [@arzzen](https://github.com/arzzen)'s CLI [tool](https://github.com/arzzen/philips-tv).
3. [@jomwells](https://github.com/jomwells) did a pretty good job of collecting various [ambilight endpoints](https://github.com/jomwells/ambilights).
4. [Some good info](https://gist.github.com/marcelrv/ee9a7cf97c227d069e4ee88d26691019) from [@marcelrv](https://gist.github.com/marcelrv).

## Contact details
Email: eslavnov@gmail.com; LinkedIn: https://www.linkedin.com/in/evgeny-slavnov/
