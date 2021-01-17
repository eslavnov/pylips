# REST API Method: POST audio/volume
Changes the TV volume.
## URL
**Android TVs**:

https://ip-address:1926/6/audio/volume

**Non-Android TVs:**

http://ip-address:1925/6/audio/volume

# Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.
### Keys
* muted (boolean): Set to true to mute the sound or false to unmute the sound.
* current (integer number): The new volume setting. This should be between the min and max as returned by [Audio (GET)](Audio-(GET).md).
### JSON example
`{"muted": false,
     "current": 18}`
