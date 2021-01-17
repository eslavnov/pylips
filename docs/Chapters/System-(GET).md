# REST API Method: GET system
Returns all system settings. See individual system resources for details.
## URL
**Android TVs**:

https://ip-address:1926/6/system

**Non-Android TVs:**

http://ip-address:1925/6/system

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.
### Keys
* menulanguage (string): The current menu language.
* name (string): The name of the TV.
* country (string): The installation country.
* serialnumber_encrypted (string): The encrypted serial number.
* softwareversion_encrypted (string): The encrypted software version.
* model_encrypted (string): The encrypted model.
* deviceid_encrypted (string): The encrypted device id.
* api_version (object): Object holding API version data ("Major", "Minor" and "Patch").
* nettvversion (string): Nettv (?) version.
* epgsource (string): Unknown (?)
* notifyChange (string): Unknown (?)
* featuring (object): Available features (?)
* systemfeatures (object): Additional features (?)

### JSON example
`{'notifyChange': 'http', 'menulanguage': 'English', 'name': 'TV', 'country': 'Netherlands', 'serialnumber_encrypted': 'vcC3/EVebazJf9RRWc9tXIuWJ7D/KZB1Z6BIg0SCMyY=\n', 'softwareversion_encrypted': 'S6LXbGZt8xKN6cjGXnsChHjEyQbsooVQ1n85YeSpqOg=\n', 'model_encrypted': 'Jgfax43NM5lAqgXv9Ofdd727XjxWG6bQ+tipIIu/rhM=\n', 'deviceid_encrypted': '1Esm9ua/YoNc/4Mdo89knUbee4O4LJSAS/dnjAAO940=\n', 'nettvversion': '8.1.0', 'epgsource': 'one', 'api_version': {'Major': 6, 'Minor': 2, 'Patch': 0}, 'featuring': {'jsonfeatures': {'editfavorites': ['TVChannels', 'SatChannels'], 'recordings': ['List', 'Schedule', 'Manage'], 'ambilight': ['LoungeLight', 'Hue', 'Ambilight'], 'menuitems': ['Setup_Menu'], 'textentry': ['context_based', 'initial_string_available', 'editor_info_available'], 'applications': ['TV_Apps', 'TV_Games', 'TV_Settings'], 'pointer': ['not_available'], 'inputkey': ['key'], 'activities': ['intent'], 'channels': ['preset_string'], 'mappings': ['server_mapping']}, 'systemfeatures': {'tvtype': 'consumer', 'content': ['dmr', 'dms_tad'], 'tvsearch': 'intent', 'pairing_type': 'digest_auth_pairing', 'secured_transport': 'true'}}}`
