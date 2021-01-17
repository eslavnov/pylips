# REST API Method: POST input/key
Sends a key to the TV.
## URL
**Android TVs**:

https://ip-address:1926/6/input/key

**Non-Android TVs:**

http://ip-address:1925/6/input/key

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.
### Keys
* key (string): One of the following:
  * Standby
  * Back
  * Find
  * RedColour
  * GreenColour
  * YellowColour
  * BlueColour
  * Home
  * VolumeUp
  * VolumeDown
  * Mute
  * Options
  * Dot
  * Digit0
  * Digit1
  * Digit2
  * Digit3
  * Digit4
  * Digit5
  * Digit6
  * Digit7
  * Digit8
  * Digit9
  * Info
  * CursorUp
  * CursorDown
  * CursorLeft
  * CursorRight
  * Confirm
  * Next
  * Previous
  * Adjust
  * WatchTV
  * Viewmode
  * Teletext
  * Subtitle
  * ChannelStepUp
  * ChannelStepDown
  * Source
  * AmbilightOnOff
  * PlayPause
  * Play
  * Pause
  * FastForward
  * Stop
  * Rewind
  * Record
  * Online
### JSON example
`{"key": "Home"}`
