# REST API Method: GET audio/volume
Returns the TV volume.

## URL
**Android TVs**:

https://ip-address:1926/6/audio/volume

**Non-Android TVs:**

http://ip-address:1925/6/audio/volume

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* muted (boolean): Set to true if the sound is muted, false if not.
* current (integer number): The actual volume.
* min (integer number): The minimum volume.
* max (integer number): The maximum volume.

### JSON example

`{"muted": false,
     "current": 18,
     "min": 0,
     "max": 60}`
