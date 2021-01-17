# REST API Method: GET ambilight/supportedstyles
Returns the styles supported by the ambilight.
## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/supportedstyles

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/supportedstyles

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* supportedStyles (array): Array of all supported styles and parameters.

### JSON example
`{"supportedStyles":[{"styleName":"OFF"},{"styleName":"FOLLOW_VIDEO"},{"styleName":"FOLLOW_AUDIO","algorithms":["ENERGY_ADAPTIVE_BRIGHTNESS","ENERGY_ADAPTIVE_COLORS","VU_METER","SPECTRUM_ANALYZER","KNIGHT_RIDER_CLOCKWISE","KNIGHT_RIDER_ALTERNATING","RANDOM_PIXEL_FLASH","STROBO","PARTY"],"maxTuning":2},{"styleName":"FOLLOW_COLOR","algorithms":["MANUAL_HUE","AUTOMATIC_HUE"],"maxSpeed":255},{"styleName":"LOUNGE"},{"styleName":"MANUAL"},{"styleName":"EXPERT"},{"styleName":"GRID"}]`                                                            