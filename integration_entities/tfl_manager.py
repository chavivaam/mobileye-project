from integration_entities.candidates_detector import CandidatesDetector
from integration_entities.candidates_filter import CandidatesFilter
from integration_entities.distance_estimator import DistanceEstimator
from view.view_observer import ViewObserver


class TflManager:
    def __init__(self, tfl_metadata):
        self._tfl_metadata = tfl_metadata
        self._view_manager = ViewObserver()
        self._candidate_detector = CandidatesDetector(self._view_manager)
        self._candidate_filter = CandidatesFilter(self._view_manager)
        self._distance_estimator = DistanceEstimator(self._tfl_metadata._focal_length, self._tfl_metadata._pp, self._view_manager)

    def handle_frame(self, img):
        frame_metadata = next(self._tfl_metadata.get_frame_metadata())


        # Chain
        self._distance_estimator.handle(img,

            self._candidate_filter.handle(img,

                self._candidate_detector.handle(img)

            ), frame_metadata)

        self._view_manager.show()

