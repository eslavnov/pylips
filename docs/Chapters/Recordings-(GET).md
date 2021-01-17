# REST API Method: GET recordings/list
Returns a list of recordings. Needs additional testing in January 2019.
## URL
**Android TVs**:

https://ip-address:1926/6/recordings/list

**Non-Android TVs:**

http://ip-address:1925/6/recordings/list

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* recordings (list): A list of recordings (?)
 
### JSON example
`{"recordings":[]}`