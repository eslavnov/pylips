# REST API Method: POST notifychange
As far as I can tell, sending a list of API endpoints with their current status to this endpoint should return an object with the updated status of these endpoints. The problem is that I could not get this endpoint to work despite trying various settings, timeouts, etc. Moreover, looking at the captured traffic from the official Philips TV remote, I can see that this endpoint is failing most of the time even for Philips. Either I completely misunderstand how it should be used or it is broken.

Also notice that it runs on port 1925 on a http protocol on ALL Philips TVs regardless of Android support.

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
