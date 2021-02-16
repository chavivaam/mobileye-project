from integration_entities.manipulator import Manipulator
from techs_codes.run_attention import find_tfl_lights
import numpy as np
from utils.constants import IMAGE, DETECTOR


class CandidatesDetector(Manipulator):
    def __init__(self, view_observer):
        super().__init__(view_observer)
        self._image = None

    def prepare_data(self, *argv):
        self._image = argv[IMAGE].astype(np.float32) / 255

    def execute(self):
        red_x, red_y, green_x, green_y = find_tfl_lights(self._image, some_threshold=42)
        self._view_observer.notify(DETECTOR, red_x, red_y, green_x, green_y, self._image)
        return red_x, red_y, green_x, green_y
