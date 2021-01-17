# REST API Method: GET ambilight/power
Returns ambilight power status (on/off).
## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/power

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/power

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.
### Keys
* power (string): Ambilight power status ("On" or "Off")
### JSON example
`{"power":"On"}`
