# REST API Method: GET channeldb/tv
Returns various channel lists.
## URL
**Android TVs**:

https://ip-address:1926/6/channeldb/tv

You can also specify a list:

https://ip-address:1926/6/channeldb/tv/channelLists/all

https://ip-address:1926/6/channeldb/tv/favoritelLists/all


## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* channelLists (list): A list of channels (?)
  * id (string): Id (?) but it's value does not make sense.
  * version (string)
  * listType (string): Type of the channel list (?)
  * medium (string): Channel list medium (?)
  * active (boolean)
  * virtual (boolean): (?)
  * modifiable: false
* favoritelLists (list): A list of favourite channel lists (?)
  * id (string)
  * version (integer)
  * parentId (sting)
  * listType (string): Type of the channel list (?)
  * medium (string): Channel list medium (?)
  * virtual (boolean): (?)
  * modifiable (boolean): false
  * name (string)

### JSON example
`{"channelLists":[{"id":"all","version":10,"listType":"MixedSources","medium":"mixed","active":true,"virtual":true,"modifiable":false}],"favoriteLists":[{"id":"com.google.android.videos%2F.tv.usecase.tvinput.playback.TvInputService","version":1545826184134,"parentId":"all","listType":"MixedSources","medium":"mixed","virtual":false,"modifiable":false,"name":"Google Play Movies & TV"},{"id":"1","version":"0","listType":"MixedSources","medium":"mixed","name":"Favourites  1","parentId":"all","virtual":false,"modifiable":true},{"id":"2","version":"0","listType":"MixedSources","medium":"mixed","name":"Favourites  2","parentId":"all","virtual":false,"modifiable":true},{"id":"3","version":"0","listType":"MixedSources","medium":"mixed","name":"Favourites  3","parentId":"all","virtual":false,"modifiable":true},{"id":"4","version":"0","listType":"MixedSources","medium":"mixed","name":"Favourites  4","parentId":"all","virtual":false,"modifiable":true},{"id":"5","version":"0","listType":"MixedSources","medium":"mixed","name":"Favourites  5","parentId":"all","virtual":false,"modifiable":true},{"id":"6","version":"0","listType":"MixedSources","medium":"mixed","name":"Favourites  6","parentId":"all","virtual":false,"modifiable":true},{"id":"7","version":"0","listType":"MixedSources","medium":"mixed","name":"Favourites  7","parentId":"all","virtual":false,"modifiable":true},{"id":"8","version":"0","listType":"MixedSources","medium":"mixed","name":"Favourites  8","parentId":"all","virtual":false,"modifiable":true}]}`