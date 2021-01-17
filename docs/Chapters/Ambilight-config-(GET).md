# REST API Method: GET ambilight/currentconfiguration
Returns TV's ambilight configuration.

## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/currentconfiguration

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/currentconfiguration

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* styleName (string): Current ambilight style.
* isExpert (boolean): Expert mode (?).
* menuSetting (string): Current ambilight mode.

### JSON example
`{"styleName":"FOLLOW_VIDEO","isExpert":false,"menuSetting":"IMMERSIVE"}`                                                            