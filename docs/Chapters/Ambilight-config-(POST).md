# REST API Method: POST ambilight/currentconfiguration
Sets TV's ambilight configuration. See [available options](Ambilight-supported-styles-(GET).md).

## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/currentconfiguration

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/currentconfiguration

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.
### Keys
* styleName (string): Ambilight style. Possible values: 
* isExpert (boolean): Expert mode (?).
* menuSetting (string): Ambilight mode.

### JSON example
`{"styleName":"FOLLOW_VIDEO","isExpert":false,"menuSetting":"IMMERSIVE"}`           
                                                 