# REST API Method: GET ambilight/mode
Returns TV's ambilight mode.

## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/mode

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/mode

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* current (string): One of following values:
  * internal: The internal ambilight algorithm is used to calculate the ambilight colours.
  * manual: The cached ambilight colours are shown.
  * expert: The cached ambilight colours are used as input for the internal ambilight algorithm.

### JSON example
`{"current": "internal"}`                                                            