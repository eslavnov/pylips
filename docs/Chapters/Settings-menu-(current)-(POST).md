# REST API Method: POST menuitems/settings/current
Send a POST request with a list of menu's node ids to get their current status.
## URL
**Android TVs**:

https://ip-address:1926/6/menuitems/settings/current

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. See the JSON example for how these key/value pairs are passed.
### Keys
* nodes (list): A list of objects:
  * nodeid (integer number): An id of the node
### JSON example
`{"nodes":[{"nodeid":2131230774}]}`
## Response example
`{"values":[{"value":{"Nodeid":2131230774,"Controllable":true,"Available":true,"string_id":"Switch on","data":{"value":false}}}],"version":0}`

