from module.base.button import Button

# Coordinates calibrated from EN ship detail page screenshots (1280x720).
# CN/JP/TW coordinates are set to match EN and may need adjustment.

# Ship name text area on the detail page.
# White text below the hull type icon, e.g. "Helena (Retrofit)", "Fritz Rumey".
DETAIL_SHIP_NAME = Button(
    area={'cn': (210, 70, 425, 100), 'en': (210, 70, 425, 100), 'jp': (210, 70, 425, 100), 'tw': (210, 70, 425, 100)},
    color={'cn': (0, 0, 0), 'en': (0, 0, 0), 'jp': (0, 0, 0), 'tw': (0, 0, 0)},
    button={'cn': (210, 70, 425, 100), 'en': (210, 70, 425, 100), 'jp': (210, 70, 425, 100), 'tw': (210, 70, 425, 100)},
    file={'cn': './assets/cn/dockscan/DETAIL_SHIP_NAME.png', 'en': './assets/en/dockscan/DETAIL_SHIP_NAME.png', 'jp': './assets/jp/dockscan/DETAIL_SHIP_NAME.png', 'tw': './assets/tw/dockscan/DETAIL_SHIP_NAME.png'},
)

# Ship level text area in the Stats section of the detail page.
# White text "Level:125" right below the Stats header bar.
DETAIL_SHIP_LEVEL = Button(
    area={'cn': (490, 148, 615, 178), 'en': (490, 148, 615, 178), 'jp': (490, 148, 615, 178), 'tw': (490, 148, 615, 178)},
    color={'cn': (0, 0, 0), 'en': (0, 0, 0), 'jp': (0, 0, 0), 'tw': (0, 0, 0)},
    button={'cn': (490, 148, 615, 178), 'en': (490, 148, 615, 178), 'jp': (490, 148, 615, 178), 'tw': (490, 148, 615, 178)},
    file={'cn': './assets/cn/dockscan/DETAIL_SHIP_LEVEL.png', 'en': './assets/en/dockscan/DETAIL_SHIP_LEVEL.png', 'jp': './assets/jp/dockscan/DETAIL_SHIP_LEVEL.png', 'tw': './assets/tw/dockscan/DETAIL_SHIP_LEVEL.png'},
)

# Limit break stars area on the detail page.
# Gold star icons above the ship name. Up to 6 stars for UR ships.
DETAIL_STAR_AREA = Button(
    area={'cn': (200, 52, 395, 80), 'en': (200, 52, 395, 80), 'jp': (200, 52, 395, 80), 'tw': (200, 52, 395, 80)},
    color={'cn': (0, 0, 0), 'en': (0, 0, 0), 'jp': (0, 0, 0), 'tw': (0, 0, 0)},
    button={'cn': (200, 52, 395, 80), 'en': (200, 52, 395, 80), 'jp': (200, 52, 395, 80), 'tw': (200, 52, 395, 80)},
    file={'cn': './assets/cn/dockscan/DETAIL_STAR_AREA.png', 'en': './assets/en/dockscan/DETAIL_STAR_AREA.png', 'jp': './assets/jp/dockscan/DETAIL_STAR_AREA.png', 'tw': './assets/tw/dockscan/DETAIL_STAR_AREA.png'},
)
