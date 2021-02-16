class TflMetadata:
    def __init__(self, EM_matrices, focal_length, pp):
        self._EM_matrices = EM_matrices
        self._focal_length = focal_length
        self._pp = pp

    def get_frame_metadata(self):
        for EM_matrix in self._EM_matrices:
            yield EM_matrix
