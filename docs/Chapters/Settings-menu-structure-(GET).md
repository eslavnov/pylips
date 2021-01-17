# REST API Method: GET menuitems/settings/structure
Returns the menu items and options. Lots of values to explore here: for example, one of the nodes turns on/off Ambilight + hue.

```
1 picture
1.0 picture_style
1.1 picture_style
1.2 colour
1.3 contrast
1.4 sharpness
1.5 brightness
1.6 3d
1.7 advanced_picture
1.8 picture_format
1.9 quick_picture_settings
2 sound
2.0 sound_style
2.1 bass
2.2 treble
2.3 headphones_volume
2.4 auto_surround_3d
2.5 surround_mode
2.6 subwoofer_level
2.7 tv_placement
2.8 advanced_sound
3 ambilight
3.0 ambilight_style
3.1 ambilight_halo_size
3.2 ambilight_brightness
3.3 ambilight_brightness_bottom_side
3.4 ambilight_saturation
3.5 ambilight_hue_menu
3.6 ambilight_advanced
4 eco_settings
4.0 energy_saving
4.1 energy_saving
4.2 screen_off
4.3 eco_settings_light_sensor
4.4 switch_off_timer
5 general_settings
5.0 usb_storage
5.1 usb_keyboard_settings
5.2 philips_wordmark
5.3 location
5.4 shop_setup
5.5 easylink_menu
5.6 hdmi_ultra_hd
5.7 hdmi_ultra_hd
5.8 advanced_general_settings
5.9 factory_settings
5.10 reinstall_tv
6 region_languages
6.0 languages
6.1 clock
6.2 rc_keyboard
6.3 rc_keyboard
7 android_settings
7.0 MAIN_DEVICE
7.1 MAIN_PREFERENCES
7.2 MAIN_PERSONAL
8 accessibility
8.0 universal_access
8.1 key_beep
8.2 voice_guidance
8.3 hearing_impaired
8.4 audio_description_menu
9 child_lock
9.0 parental_rating
9.1 parental_rating
9.2 parential_locking
9.3 app_locking
9.4 change_code
10 wireless_networks
10.0 network
10.1 bluetooth
11 channels
11.0 channel_installation
11.1 satellite_installation
11.2 channel_list_copy
12 update_software
12.0 search_for_update
12.1 current_software_info
12.2 announcement
12.3 clear_announcement
12.4 automatic_update
```

## URL
**Android TVs**:

http://ip-address:1926/6/menuitems/settings/structure

## Format
json
## HTTP Method
GET
## Response
This resource returns a JSON object with key/value pairs. See the JSON example for how these key/value pairs are returned.

### Keys
No official documentation is available. 
* node_id (integer number) is important since we can get additional info by referencing this id [here](Settings-menu-(current)-(POST).md) and change some settings [here](Settings-menu-update-(POST).md).
### JSON example
`{"node":{"node_id":2131230748,
      "type":"PARENT_NODE",
      "string_id":"org.droidtv.ui.strings.R.string.MAIN_VB_SETUP",
      "context":"Setup_Menu",
      "data":{"nodes":[{ "node_id":2131230774,
                                 "context":"ambilight_hue_off",
                                 "data":{},
                                 "type":"TOGGLE_NODE"},{...}]}}}`                                               