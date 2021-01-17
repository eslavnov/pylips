# REST API Method: GET powerstate
Returns TV's power state.
## URL
**Android TVs**:

https://ip-address:1926/6/powerstate

**Non-Android TVs:**

http://ip-address:1925/6/powerstate

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* powerstate (string): TV's power state ('On'/'Off')
 
### JSON example
`{"powerstate":"On"}`