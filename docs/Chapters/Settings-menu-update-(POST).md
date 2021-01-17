# REST API Method: POST menuitems/settings/update
Allows modyfing menu items and settings. Read [this](Settings-menu-structure-(GET).md) first.
## URL
**Android TVs**:

https://ip-address:1926/6/menuitems/settings/update

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.
### Keys
* values (list): A list of objects:
  * value (object):
    * Nodeid (integer number): An id of the node
    * data (object): An object holding node's data
### JSON example
`{"values":[{"value":{"Nodeid":2131230774,"Controllable":true,"Available":true,"data":{"value":false}}}]}`

