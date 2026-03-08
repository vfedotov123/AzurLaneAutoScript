from module.base.button import Button

# Coordinates calibrated from EN ship detail page screenshots (1280x720).
# CN/JP/TW coordinates are set to match EN and may need adjustment.

# Ship name text area on the detail page.
# White text below the hull type icon, e.g. "Helena (Retrofit)", "Fritz Rumey".
DETAIL_SHIP_NAME = Button(
    area={'cn': (205, 88, 465, 120), 'en': (205, 88, 465, 120), 'jp': (205, 88, 465, 120), 'tw': (205, 88, 465, 120)},
    color={'cn': (0, 0, 0), 'en': (0, 0, 0), 'jp': (0, 0, 0), 'tw': (0, 0, 0)},
    button={'cn': (205, 88, 465, 120), 'en': (205, 88, 465, 120), 'jp': (205, 88, 465, 120), 'tw': (205, 88, 465, 120)},
    file={'cn': './assets/cn/dockscan/DETAIL_SHIP_NAME.png', 'en': './assets/en/dockscan/DETAIL_SHIP_NAME.png', 'jp': './assets/jp/dockscan/DETAIL_SHIP_NAME.png', 'tw': './assets/tw/dockscan/DETAIL_SHIP_NAME.png'},
)

# Ship level text area in the Stats section of the detail page.
# White text "Level:125" right below the Stats header bar.
DETAIL_SHIP_LEVEL = Button(
    area={'cn': (688, 288, 845, 325), 'en': (688, 288, 845, 325), 'jp': (688, 288, 845, 325), 'tw': (688, 288, 845, 325)},
    color={'cn': (0, 0, 0), 'en': (0, 0, 0), 'jp': (0, 0, 0), 'tw': (0, 0, 0)},
    button={'cn': (688, 288, 845, 325), 'en': (688, 288, 845, 325), 'jp': (688, 288, 845, 325), 'tw': (688, 288, 845, 325)},
    file={'cn': './assets/cn/dockscan/DETAIL_SHIP_LEVEL.png', 'en': './assets/en/dockscan/DETAIL_SHIP_LEVEL.png', 'jp': './assets/jp/dockscan/DETAIL_SHIP_LEVEL.png', 'tw': './assets/tw/dockscan/DETAIL_SHIP_LEVEL.png'},
)

# Limit break stars area on the detail page.
# Gold star icons above the ship name. Up to 6 stars for UR ships.
DETAIL_STAR_AREA = Button(
    area={'cn': (212, 68, 350, 93), 'en': (212, 68, 350, 93), 'jp': (212, 68, 350, 93), 'tw': (212, 68, 350, 93)},
    color={'cn': (0, 0, 0), 'en': (0, 0, 0), 'jp': (0, 0, 0), 'tw': (0, 0, 0)},
    button={'cn': (212, 68, 350, 93), 'en': (212, 68, 350, 93), 'jp': (212, 68, 350, 93), 'tw': (212, 68, 350, 93)},
    file={'cn': './assets/cn/dockscan/DETAIL_STAR_AREA.png', 'en': './assets/en/dockscan/DETAIL_STAR_AREA.png', 'jp': './assets/jp/dockscan/DETAIL_STAR_AREA.png', 'tw': './assets/tw/dockscan/DETAIL_STAR_AREA.png'},
)
