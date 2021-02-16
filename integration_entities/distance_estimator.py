from integration_entities.manipulator import Manipulator
from utils.constants import IMAGE, INPUT, METADATA, ESTIMATOR
import techs_codes.SFM as SFM


class FrameContainer(object):
    def __init__(self, img):
        self.img = img
        self.traffic_light = []
        self.traffic_lights_3d_location = []
        self.EM = []
        self.corresponding_ind = []
        self.valid = []


class DistanceEstimator(Manipulator):

    def __init__(self, focal_length, pp, view_observer):
        super().__init__(view_observer)
        self._prev_container = None
        self._curr_container = None
        self._focal_length = focal_length
        self._pp = pp
        self._image = None
        self._is_first_frame = True

    def prepare_data(self, *argv):
        self._image = argv[IMAGE]
        tfl_positions = argv[INPUT]
        frame_EM = argv[METADATA]
        self._curr_container = FrameContainer(self._image)
        self._curr_container.traffic_light = tfl_positions[0] + tfl_positions[1]
        self._curr_container.EM = frame_EM

    def execute(self):
        if self._prev_container is not None:
            self._curr_container = SFM.calc_TFL_dist(self._prev_container, self._curr_container, self._focal_length, self._pp)
            self._view_observer.notify(ESTIMATOR, self._curr_container)
        self._prev_container = self._curr_container
        return None



