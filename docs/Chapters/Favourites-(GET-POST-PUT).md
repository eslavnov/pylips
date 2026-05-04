# REST API Methods: Favourites (GET/POST/PUT)
Endpoints for reading, modifying, and reordering favourite channel lists. These write endpoints were previously undocumented and were discovered by decompiling the TV's `xtv.apk` (specifically `xtvRequestHandler.java` and `FavouritesManager.java`) using [jadx](https://github.com/skylot/jadx).

**Tested on:** Philips 2019 Android TV (MSAF_2019_P, API v6.4.0)

**Important constraint:** The TV must be actively watching a channel (WatchTv, WatchSatellite, or WatchVirtualSource context) for write operations to succeed. If the TV is on the home screen or in an app, the API returns HTTP 503. This is enforced by `FavouritesManager.isValidContext()` in the TV firmware.

---

## 1. Read a favourite list (GET)

### URL
**Android TVs**:

https://ip-address:1926/6/channeldb/tv/favoriteLists/{list_id}

### Format
json
### HTTP Method
GET
### Response
This resource returns a JSON object with the favourite list metadata and its channels.

#### Keys
* id (string): The favourite list id (1-8).
* version (string): List version, incremented on each modification.
* type (string): Source type, e.g. "MixedSources".
* medium (string): Medium type, e.g. "mixed".
* name (string): Display name of the list, e.g. "Favourites 1".
* channels (list): Ordered list of channel objects in this favourite list.
  * ccid (integer): Channel's id (matches ccid from the channel list).
  * preset (string): Channel's TV preset number.

#### JSON example
`{"id":"1","version":"241","type":"MixedSources","medium":"mixed","name":"Favourites 1","channels":[{"ccid":22,"preset":"1"},{"ccid":23,"preset":"2"}]}`

---

## 2. Add or remove channels from a favourite list (POST)

### URL
**Android TVs**:

https://ip-address:1926/6/channeldb/tv/modifyfavourite/{list_id}

Where `list_id` is 1-8.

### Format
json
### HTTP Method
POST
### Upload data
This resource accepts a JSON object specifying channels to add and/or remove. The `add` and `remove` fields are objects containing an `id` array of ccid integers (not flat arrays). The `name` field sets the display name of the favourite list. You can include only `add`, only `remove`, or both in a single request.

#### Keys
* add (object): Channels to add to the list.
  * id (list of integers): Array of ccid values to add.
* remove (object): Channels to remove from the list.
  * id (list of integers): Array of ccid values to remove.
* name (string): Display name for the favourite list.

#### JSON examples
Add channels 22 and 23, remove channel 45:

`{"add":{"id":[22,23]},"remove":{"id":[45]},"name":"Favourites 1"}`

Add channels only:

`{"add":{"id":[22,23]},"name":"Favourites 1"}`

Remove channels only:

`{"remove":{"id":[10]},"name":"Favourites 1"}`

---

## 3. Reorder or replace an entire favourite list (PUT)

### URL
**Android TVs**:

https://ip-address:1926/6/channeldb/tv/favoriteLists/{list_id}

Where `list_id` is 1-8.

### Format
json
### HTTP Method
PUT

**Note:** This endpoint requires PUT. Sending a POST returns HTTP 405 (Method Not Allowed).

### Upload data
This resource accepts a JSON object with the complete ordered list of channel ccid values. The existing list is replaced entirely with the provided channels in the specified order.

#### Keys
* channels (list of integers): Ordered array of ccid values representing the new favourite list contents.

#### JSON example
`{"channels":[22,23,24]}`

---

## 4. Switch TV to a favourites context (POST)

To make the TV use a specific favourite list as the active channel list (affecting channel up/down navigation), POST to the activities/tv endpoint with the favourite list id instead of "all". See [Activities TV (POST)](Activities-TV-(POST).md) for the full endpoint reference.

### URL
**Android TVs**:

https://ip-address:1926/6/activities/tv

### HTTP Method
POST

### JSON example
Switch to favourite list 1 (channels will cycle through this list):

`{"channelList":{"id":"1"}}`

Switch back to the full channel list:

`{"channelList":{"id":"all"}}`

---

## Discovery method
These endpoints were found by pulling `/system/priv-app/xtv/xtv.apk` via ADB from a Philips 2019 Android TV, then decompiling it with [jadx](https://github.com/skylot/jadx). The relevant source files are `xtvRequestHandler.java` (route registration) and `FavouritesManager.java` (validation logic and request handling). To the best of our knowledge, no open-source project has previously documented the write endpoints (`modifyfavourite` and PUT `favoriteLists`).
