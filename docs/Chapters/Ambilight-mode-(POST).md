# REST API Method: POST ambilight/mode
Changes the ambilight mode.
## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/mode

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/mode

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.
### Keys
* current (string): One of following values:
  * internal: The internal ambilight alorithm is used to calculate the ambilight colours.
  * manual: The cached ambilight colours are shown.
  * expert: The cached ambilight colours are used as input for the internal ambilight algorithm.
### JSON example
`{"current": "manual"}`
