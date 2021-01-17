# REST API Method: GET system/storage
Returns TV's power state.
## URL
**Android TVs**:

https://ip-address:1926/6/system/storage

**Non-Android TVs:**

http://ip-address:1925/6/system/storage

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* status (string): TV's storage status (?). Needs further investigating with a USB thumb drive, for example.
 
### JSON example
`{"status":"removed"}`