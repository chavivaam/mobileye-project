from integration_entities.manipulator import Manipulator
from utils.constants import IMAGE, INPUT, FILTER
from techs_codes.tfl_selection import run_neural_net


class CandidatesFilter(Manipulator):
    def __init__(self, view_observer):
        super().__init__(view_observer)
        self._image = None
        self._green_candidates = []
        self._red_candidates = []

    def prepare_data(self, *argv):
        self._image = argv[IMAGE]
        candidates = argv[INPUT]
        self._green_candidates = []
        self._red_candidates = []
        for red_index in range(len(candidates[0])):
            self._red_candidates.append((candidates[0][red_index], candidates[1][red_index]))

        for green_index in range(len(candidates[2])):
            self._green_candidates.append((candidates[2][green_index], candidates[3][green_index]))

    def execute(self):
        red_tfls, green_tfls = run_neural_net(self._red_candidates, self._green_candidates, self._image)
        self._view_observer.notify(FILTER, red_tfls, green_tfls, self._image)
        return red_tfls, green_tfls



