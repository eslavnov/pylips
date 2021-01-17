# REST API Method: GET activities/tv
Returns current TV channel info.
## URL
**Android TVs**:

https://ip-address:1926/6/activities/tv

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* channel (object): Channel object
  * ccid (integer): Channel's id.
  * preset (integer): Channel's TV preset (e.g. channel's number)
  * name (string): Channel's name.
* channelList (object): Channel list object
  * id (string): Channel list id.
  * version (string): Channel list version.

### JSON example
`{"channel":{"ccid":338,"preset":"3","name":"NPO 3 HD"},"channelList":{"id":"allcab","version":"13"}}`