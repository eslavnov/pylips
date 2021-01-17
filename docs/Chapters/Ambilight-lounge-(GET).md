# REST API Method: GET ambilight/lounge
Returns the ambilight color settings for LOUNGE mode - no idea what this is.
## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/lounge

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/lounge

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* color (object): An object containing color settings:
  * hue (integer)
  * saturation (integer)
  * brightness (integer)
* colordelta (object): An object containing color delta (?) settings:
  * hue (integer number)
  * saturation (integer)
  * brightness (integer)
* speed (integer): Unknown (?)
* mode (string): Unknown (?)
### JSON example
`{"color":{"hue":155,"saturation":240,"brightness":180},"colordelta":{"hue":20,"saturation":25,"brightness":100},"speed":45,"mode":"Default"}`