# REST API Method: GET applications
Returns a list of available applications.
## URL
**Android TVs**:

https://ip-address:1926/6/applications

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* version (integer): API version?
* applications (list): A list of objects (applications) with Android intents and actions
 
### JSON example
`{"version": 6,
  "applications": [{"label": "Help",
      "intent": {
        "component": {
          "packageName": "org.droidtv.eum",
          "className": "org.droidtv.eum.onehelp.HowToTutorials.HowToVideosActivity"
        },
        "action": "Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 pkg=org.droidtv.eum cmp=org.droidtv.eum/.onehelp.HowToTutorials.HowToVideosActivity }"
      },
      "order": 0,
      "id": "org.droidtv.eum.onehelp.HowToTutorials.HowToVideosActivity-org.droidtv.eum",
      "type": "app"
    },{...}]}`