# REST API Method: GET ambilight/topology
Returns TV's ambilight topology.

## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/topology

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/topology

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* layers (integer): The number of layers.
* left (integer): The number of pixels on the left.
* top (integer): The number of pixels on the top.
* right (integer): The number of pixels on the right.
* bottom (integer): The number of pixels on the bottom.

### JSON example
`{"layers": 2, "left": 4, "top": 6, "right": 4, "bottom": 0}`                                                            