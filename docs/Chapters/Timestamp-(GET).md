# REST API Method: GET system/timestamp
Returns a current timestamp
## URL
**Android TVs**:

https://ip-address:1926/6/system/timestamp

**Non-Android TVs:**

http://ip-address:1925/6/system/timestamp

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* timestamp (integer): Timestamp (seconds since midnight?).
 
### JSON example
`{"timestamp":"58439"}`