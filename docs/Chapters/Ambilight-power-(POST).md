# REST API Method: POST ambilight/power
Turns ambilight on and off.
## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/power

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/power

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.
### Keys
* power (string): 'On' or 'Off'.
### JSON example
`{"power":"On"}`

