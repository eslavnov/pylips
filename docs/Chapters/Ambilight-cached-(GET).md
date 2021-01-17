# REST API Method: GET ambilight/cached
Returns the ambilight colours stored in the cache.
## URL
**Android TVs**:

https://ip-address:1926/6/ambilight/cached

**Non-Android TVs:**

http://ip-address:1925/6/ambilight/cached

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
* layerx (object): An object containing all pixels in layer i.
* left (object): An object containing all pixels on the left side in the containing layer.
* top (object): An object containing all pixels on the top side in the containing layer.
* right (object): An object containing all pixels on the right side in the containing layer.
* bottom (object): An object containing all pixels on the bottom side in the containing layer.
* pixelnr (object): An object containing RGB value for one pixel. The pixel nr is relative within the side containing the pixel. Pixels within a side are numbered clockwise (from the viewer perspective) starting from "0".
* r (integer): The red value for a pixel, between 0 and 255.
* g (integer): The green value for a pixel, between 0 and 255.
* b (integer): The blue value for a pixel, between 0 and 255.
### JSON example
`{"layer1":
    {
        "left":
        {
            "0":
            {
                "r": 100,
                "g": 210,
                "b": 30
            },
            "1":
            {
                "r": 110,
                "g": 220,
                "b": 25
            },
            "2":
            {
                "r": 115,
                "g": 230,
                "b": 20
            },
            "3":
            {
                "r": 125,
                "g": 235,
                "b": 15
            }
        },
        "top":
        {
            "0":
            {
                "r": 140,
                "g": 250,
                "b": 10
            },
            "1":
            {
                "r": 140,
                "g": 250,
                "b": 10
            },
            "2":
            {
                "r": 140,
                "g": 250,
                "b": 10
            },
            "3":
            {
                "r": 140,
                "g": 250,
                "b": 10
            },
            "4":
            {
                "r": 140,
                "g": 250,
                "b": 10
            },
            "5":
            {
                "r": 140,
                "g": 250,
                "b": 10
            }
        },
        "right":
        {
            "0":
            {
                "r": 125,
                "g": 235,
                "b": 15
            },
            "1":
            {
                "r": 115,
                "g": 230,
                "b": 20
            },
            "2":
            {
                "r": 110,
                "g": 220,
                "b": 25
            },
            "3":
            {
                "r": 100,
                "g": 210,
                "b": 30
            }
        },
        "bottom":
        {
        }
    },
    "layer2":
    {
        etc.
    }}` 