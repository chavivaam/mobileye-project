import pickle
import numpy as np
from PIL import Image
from integration_entities.tfl_manager import TflManager
from utils.tfl_metadata import TflMetadata
from utils.constants import PLAYLIST_PATH, EXTENSION_FILE, FRAME_ID


class Controller:
    def __init__(self):
        with open(PLAYLIST_PATH) as file:
            self._paths = file.read().split("\n")

        metadata = self._extract_metadata()
        self._tfl_manager = TflManager(metadata)

    def _extract_metadata(self):
        EM_matrices = list()
        focal = None
        pp = None
        pkl_path = self._paths[0]

        with open(pkl_path, 'rb') as pklfile:
            data = pickle.load(pklfile, encoding='latin1')
        focal = data['flx']
        pp = data['principle_point']

        EM = np.eye(4)
        first_frame_id = Controller.extract_frame_id(self._paths[1])
        for i in range(first_frame_id, len(self._paths) - 2 + first_frame_id):
            EM = np.dot(data['egomotion_' + str(i) + '-' + str(i + 1)], EM)
            EM_matrices.append(EM[...])

        return TflMetadata(EM_matrices, focal, pp)

    @staticmethod
    def extract_frame_id(frame_path):
        frame_path_without_extension = frame_path.split(EXTENSION_FILE)[0]
        id_as_str = frame_path_without_extension.split("_")[FRAME_ID]
        id_ = int(id_as_str)
        return id_

    def run(self):
        for frame_i in range(1, len(self._paths)):
            try:
                image = np.array(Image.open(self._paths[frame_i]))
                self._tfl_manager.handle_frame(image)

            except Exception as a:
                pass


if __name__ == "__main__":
    c = Controller()
    c.run()
