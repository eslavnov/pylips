# REST API Method: GET system/epgsource
Returns TV's EPG source.
## URL
**Android TVs**:

https://ip-address:1926/6/system/epgsource

**Non-Android TVs:**

http://ip-address:1925/6/system/epgsource

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* epgsource (string): TV's EPG (Electronic Program Guide) source.
 
### JSON example
`{"epgsource":"one"}`