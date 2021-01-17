# PHILIPS TV (2015+) UNOFFICIAL API REFERENCE

**Update 2020-30-12:** Two years into this project and I have finally thought of looking deeper into my Android TV. I was able to extract and decode the API and now I have its full source code in a fully readable format. I did not spend too much time researching it since I feel like all the endpoints have already been discovered, but it's certainly an interesting read for anybody curious about how this API works/who developed it for Philips. You can see all the endpoints, parameters they take and the exact logic for any part of the API - anything you want. You'll need to grab `/system/priv-app/xtv/oat/arm/xtv.odex`, then use [vdexExtractor](https://github.com/anestisb/vdexExtractor) and [jadx](https://github.com/skylot/jadx) to see the Java code.


***

The TV's API is roughly based on [JointSpace](http://jointspace.sourceforge.net/) with a current version of 6.2. The only available official documentation that I was able to find is for JointSpace version 1, which is incredibly outdated. 

Since no official API documentation is available, I've decided to collect and document to the best of my knowledge all endpoints that are working in API version 6+ (Philips TVs 2016-2018). Most of these endpoints should work for API version 5 as well (2015 Philips TVs), but your mileage may vary. This API reference is based on:
* [Official JointSpace documentation](http://jointspace.sourceforge.net/projectdata/documentation/jasonApi/1/doc/API.html)
* Community endpoints (various endpoints discovered by the community over the years)
* Endpoints discovered by using a man-in-the-middle attack on an iPhone running an official Philips TV remote app (this finally allowed to discover an endpoint responsible for toggling 'Ambilight + Hue' mode among other things)

All endpoints in API reference are tested and fully working unless explicitly marked otherwise. Any comments, new endpoints and fixes to the API reference are incredibly welcome.

**Differences between Android TVs and non-Android TVs**
1) Android TVs require pairing, non-Android do not need it
2) Android TVs need to send username/password with the requests, non-Android do not need it
3) Android TVs use `https://`, non-Android TV use `http://`
4) Android TVs primarily use port 1926, non-Android TV use port 1925 only

**General endpoint format**

`%protocol% + %ip_address% + ":" + %port% + "/" + %api_version% + "/" + %endpoint%`

**Sending requests**

Send requests with the tool's `get` or `post` commands or use cURL:

```curl -X GET --digest --insecure -u %username%:%password% https://%ip_address%:1926/6/%endpoint%```

```curl -X POST --digest --insecure -u %username%:%password% https://%ip_address%:1926/6/%endpoint% -d '%body%'```

## TABLE OF CONTENTS
&nbsp; &nbsp; &nbsp; &nbsp; **Ambilight:**
1. [Ambilight power (GET)](Chapters/Ambilight-power-(GET).md)
1. [Ambilight power (POST)](Chapters/Ambilight-power-(POST).md)
1. [Ambilight supported styles (GET)](Chapters/Ambilight-supported-styles-(GET).md)
1. [Ambilight config (GET)](Chapters/Ambilight-config-(GET).md)
1. [Ambilight config (POST)](Chapters/Ambilight-config-(POST).md)
1. [Ambilight cached (GET)](Chapters/Ambilight-cached-(GET).md)
1. [Ambilight cached (POST)](Chapters/Ambilight-cached-(POST).md)
1. [Ambilight mode (GET)](Chapters/Ambilight-mode-(GET).md)
1. [Ambilight mode (POST)](Chapters/Ambilight-mode-(POST).md)
1. [Ambilight lounge (GET)](Chapters/Ambilight-lounge-(GET).md)
1. [Ambilight lounge (POST)](Chapters/Ambilight-lounge-(POST).md)
1. [Ambilight proccesed (GET)](Chapters/Ambilight-proccesed-(GET).md)
1. [Ambilight measured (GET)](Chapters/Ambilight-measured-(GET).md)
1. [Ambilight topology (GET)](Chapters/Ambilight-topology-(GET).md)

   **Applications:**
1. [Applications (GET)](Chapters/Applications-(GET).md)
1. [Activities current (GET)](Chapters/Activities-current-(GET).md)
1. [Activities launch (POST)](Chapters/Activities-launch-(POST).md)

   **Audio:**
1. [Audio (GET)](Chapters/Audio-(GET).md)
1. [Audio (POST)](Chapters/Audio-(POST).md)

   **TV channels:** 
1. [Channel list (GET)](Chapters/Channel-list-(GET).md)
1. [EPG source (GET)](Chapters/EPG-source-(GET).md)
1. [Recordings (GET)](Chapters/Recordings-(GET).md)

   **TV settings:**
1. [Settings menu (current) (POST)](Chapters/Settings-menu-(current)-(POST).md)
1. [Settings menu structure (GET)](Chapters/Settings-menu-structure-(GET).md)
1. [Settings menu update (POST)](Chapters/Settings-menu-update-(POST).md)

   **TV remote control:**
1. [Input key (POST)](Chapters/Input-key-(POST).md)
1. [Power state (GET)](Chapters/Power-state-(GET).md)

   **Other:**
1. [System (GET)](Chapters/System-(GET).md)
1. [Storage (GET)](Chapters/Storage-(GET).md)
1. [Timestamp (GET)](Chapters/Timestamp-(GET).md)
1. [Notifychange (POST)](Chapters/Notify-change-(POST).md)