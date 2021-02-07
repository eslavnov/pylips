# REST API Method: POST notifychange
Sending the current values of other endpoints to the endpoint will block the response from the endpoint until either the request times out, or one of the fields have changed. If a field is different from supplied value, the endpoint will directly return with it's current values. It will only return the fields that is different from the supplied values.

Also notice that it runs on port 1925 on a http protocol on ALL Philips TVs regardless of Android support. It also seem available on 1926 on https protocol.

Noticed issues:
 * The "audio/volume" endpoint doesn't seem to work.

## URL
**Android TVs**:

http://ip-address:1925/6/notifychange

**Non-Android TVs**:

http://ip-address:1925/6/notifychange

## Format
json
## HTTP Method
POST
## Upload data
This resource accepts a JSON object with key/value pairs. 

### Request example
`{"notification": {"context": {},"network/devices": [],"input/textentry": { "textentry": "requested", "initialstring": "" },"input\/pointer":{"status":"enabled"},"channeldb/tv":{},"activities/tv":{},"applications/version":"","system/epgsource": {},"powerstate": { "powerstate": "Standby" },"system/nettvversion": "4.6.0","system/storage/status":"","recordings/list":{"version":""},"activities/current":{},"companionlauncher":{"device_id":"C03ADF98-5956-40DA-ADA1-9C876FB94ABB","msg_id":""}}}`

### Response example
`{"input/textentry":{"textentry":"not requested","initialstring":""},"context":{"level1":"WatchExtension","level2":"NA","level3":"NA","data":"NA"},"input/pointer":{"pointerstatus":"disabled"},"powerstate":{"powerstate":"On"},"network/devices":[{"mac":"70:C9:4E:47:8D:82","ip":"192.168.1.28","type":"Wifi","wake-on-lan":"Enabled"}],"channeldb/tv":{},"activities/tv":{"channel":{"ccid":"@","preset":0,"name":"@"},"channelList":{"id":"allsat","version":"1"}},"system/epgsource":{"epgsource":"ip"},"system/storage/status":"removed"}`
