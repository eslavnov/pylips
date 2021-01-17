# REST API Method: POST activities/launch
Launches an application on the TV.
## URL
**Android TVs**:

https://ip-address:1926/6/activities/launch

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. It is allowed to send an object containing only the key/value pairs that need to be changed. See the JSON example for how these key/value pairs are passed.
### Keys
* id (string): An app's id.
* order (integer): Unknown (?)
* intent (object): An object with an app's intent:
  * action (string): Android's app action.
  * component (object): An object with a packageName and className
* label (string)

### JSON example
`{"id":"com.google.android.apps.youtube.tv.activity.ShellActivity-com.google.android.youtube.tv","order":0,"intent":{"action":"Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 pkg=com.google.android.youtube.tv cmp=com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity }","component":{"packageName":"com.google.android.youtube.tv","className":"com.google.android.apps.youtube.tv.activity.ShellActivity"}},"label":"YouTube"}`
