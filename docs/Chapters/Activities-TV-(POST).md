# REST API Method: GET activities/tv
Allows to turn a specified TV channel on. See [Activities TV (GET)](Activities-TV-(GET).md) to get the required values for a specific channel.
## URL
**Android TVs**:

https://ip-address:1926/6/activities/tv

## Format
json
## HTTP Method
POST
## Response
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.

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