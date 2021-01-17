# REST API Method: POST ambilight/lounge
Controls ambilight LOUNGE settings (does not seem to work for me).
## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/lounge

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/lounge

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.
### Keys
* color (object): An object containing color settings:
  * hue (integer)
  * saturation (integer)
  * brightness (integer)
* colordelta (object): An object containing color delta (?) settings:
  * hue (integer)
  * saturation (integer)
  * brightness (integer)
* speed (integer): Unknown (?)
* mode (string): Unknown (?)
### JSON example
`{"color":{"hue":155,"saturation":240,"brightness":180},"colordelta":{"hue":20,"saturation":25,"brightness":100},"speed":45,"mode":"Default"}`

