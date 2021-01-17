# REST API Method: GET activities/current
Returns the app that is currently open on the TV.
## URL
**Android TVs**:

https://ip-address:1926/6/activities/current

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* component (object): App object
  * packageName (string): Android app package name.
  * className (string): Android app class name.

### JSON example
`{"component":{"packageName":"org.droidtv.nettv.market","className":"org.droidtv.nettv.market.MarketMainActivity"}}`