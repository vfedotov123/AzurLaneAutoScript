import csv
import os
import re
from datetime import datetime

import cv2
import numpy as np

from module.base.utils import crop
from module.dockscan.assets import DETAIL_SHIP_NAME, DETAIL_SHIP_LEVEL, DETAIL_STAR_AREA
from module.logger import logger
from module.ocr.ocr import Ocr
from module.retire.assets import SHIP_DETAIL_CHECK
from module.retire.dock import Dock
from module.ui.page import page_dock


class ShipNameOcr(Ocr):
    def __init__(self, buttons, name='SHIP_NAME_OCR'):
        # Use 'cnocr' model which supports full character set including
        # lowercase letters, spaces, and punctuation needed for EN ship names.
        # The 'azur_lane' model only supports 0-9, A-Z, :, /, - which is insufficient.
        # Ship name is white text on the ship portrait background.
        super().__init__(buttons, lang='cnocr', letter=(255, 255, 255), threshold=128, name=name)

    def after_process(self, result):
        result = super().after_process(result)
        result = result.strip()
        return result


class DetailLevelOcr(Ocr):
    """Read level number from 'Level:125' text on the detail page Stats section."""

    def __init__(self, buttons, name='DETAIL_LEVEL'):
        # White text on dark Stats panel background
        super().__init__(buttons, lang='cnocr', letter=(255, 255, 255), threshold=128, name=name)

    def after_process(self, result):
        result = super().after_process(result)
        # Extract the first number from text like "Level:125" or "Level: 70"
        match = re.search(r'\d+', result)
        if match:
            return int(match.group())
        return 0


class DockScan(Dock):
    scan_results = []

    def run(self):
        logger.hr('Dock Scan', level=1)
        self.scan_results = []

        # Navigate to dock
        self.ui_ensure(page_dock)

        # Set dock filter: show all ships sorted by level descending
        self.dock_filter_set(
            sort='level', index='all', faction='all',
            rarity='all', extra='no_limit',
        )
        self.dock_sort_method_dsc_set(enable=True)
        self.handle_dock_cards_loading()

        # Enter first ship
        entered = self.dock_enter_first(non_npc=True)
        if not entered:
            logger.warning('Dock is empty, nothing to scan')
            return

        # Main scan loop
        self.scan_all_ships()

        # Export results
        self.export_csv()

        # Return to dock
        self.ui_back(page_dock)

        logger.hr('Dock Scan Complete', level=1)
        logger.info(f'Total ships scanned: {len(self.scan_results)}')

    def scan_all_ships(self):
        """
        Scan all ships by swiping through ship detail pages.
        Starts from the currently displayed ship detail page.
        """
        count = 0
        max_retry = 3

        while True:
            self.device.screenshot()

            # Save first screenshot for debugging coordinate calibration
            if count == 0:
                self.device.image_save('./screenshots/dock_scan_debug.png')
                logger.info('Debug screenshot saved to ./screenshots/dock_scan_debug.png')

            # Read ship data from current detail page
            ship_data = self.read_ship_detail()
            count += 1
            ship_data['index'] = count

            self.scan_results.append(ship_data)
            logger.info(
                f'Ship #{count}: {ship_data["name"]} '
                f'Lv.{ship_data["level"]} '
                f'Stars:{ship_data["stars"]}'
            )

            # Save intermediate results every 100 ships
            if count % 100 == 0:
                logger.info(f'Intermediate save at {count} ships')
                self.export_csv()

            # Swipe to next ship
            # Using SHIP_DETAIL_CHECK as check_button instead of default EQUIPMENT_OPEN
            # because we are on the ship detail page, not the equipment page
            result = self.ship_view_next(check_button=SHIP_DETAIL_CHECK)
            if result:
                continue
            else:
                # ship_view_next returned False - might be last ship or swipe failed
                # Retry a few times to be sure
                retried = False
                for retry in range(max_retry):
                    logger.info(f'Swipe failed, retry {retry + 1}/{max_retry}')
                    result = self.ship_view_next(check_button=SHIP_DETAIL_CHECK)
                    if result:
                        retried = True
                        break

                if retried:
                    continue
                else:
                    logger.info('Reached last ship in dock')
                    break

    def read_ship_detail(self):
        """
        Read ship name, level, and limit break stars from the current detail page screenshot.

        Returns:
            dict: {'name': str, 'level': int, 'stars': int}
        """
        image = self.device.image

        # Read ship name
        try:
            name_ocr = ShipNameOcr(DETAIL_SHIP_NAME, name='DETAIL_NAME')
            name = name_ocr.ocr(image)
            if not name:
                name = 'UNKNOWN'
        except Exception as e:
            logger.warning(f'Ship name OCR failed: {e}')
            name = 'UNKNOWN'

        # Read ship level from "Level:125" text in Stats section
        try:
            level_ocr = DetailLevelOcr(DETAIL_SHIP_LEVEL, name='DETAIL_LEVEL')
            level = level_ocr.ocr(image)
            if not isinstance(level, int) or level < 0:
                level = 0
        except Exception as e:
            logger.warning(f'Ship level OCR failed: {e}')
            level = 0

        # Detect limit break stars
        try:
            stars = self.detect_stars(image)
        except Exception as e:
            logger.warning(f'Star detection failed: {e}')
            stars = -1

        return {'name': name, 'level': level, 'stars': stars}

    def detect_stars(self, image):
        """
        Detect the number of limit break stars by counting yellow star icons
        in the star area of the ship detail page.

        Stars are bright yellow/gold. Empty star slots are dark/grey.
        We convert to HSV and count clusters of yellow pixels.

        Args:
            image: Full screenshot (numpy array, RGB)

        Returns:
            int: Number of filled stars (0-6), or -1 on failure
        """
        star_area = crop(image, DETAIL_STAR_AREA.area)

        # Convert RGB to HSV for color detection
        # Note: OpenCV expects BGR, but ALAS images are RGB
        star_bgr = cv2.cvtColor(star_area, cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(star_bgr, cv2.COLOR_BGR2HSV)

        # Yellow/gold star color range in HSV
        # Hue: 18-45 (yellow range), Sat: 100-255 (saturated), Val: 180-255 (bright)
        lower_yellow = np.array([18, 100, 180])
        upper_yellow = np.array([45, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Count yellow pixels per column to find star positions
        col_sums = mask.sum(axis=0).astype(float)

        # Threshold: a column is "star" if enough yellow pixels
        height = mask.shape[0]
        threshold = height * 128 * 0.3  # At least 30% of column height is yellow

        # Find contiguous star regions (peaks in column sums)
        stars = 0
        in_star = False
        for val in col_sums:
            if val > threshold and not in_star:
                stars += 1
                in_star = True
            elif val <= threshold:
                in_star = False

        return min(stars, 6)

    def export_csv(self):
        """
        Export scan results to CSV file.
        Uses utf-8-sig encoding for proper Excel compatibility.
        """
        output_path = self.config.DockScan_OutputFile
        if not output_path:
            output_path = './dock_scan_result.csv'

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Name', 'Level', 'Stars', 'ScanTimestamp'])
            for ship in self.scan_results:
                writer.writerow([
                    ship['index'],
                    ship['name'],
                    ship['level'],
                    ship['stars'],
                    timestamp,
                ])

        logger.info(f'Dock scan results exported to {output_path}')


if __name__ == '__main__':
    DockScan('alas', task='DockScan').run()
