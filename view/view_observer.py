import matplotlib.pyplot as plt
import numpy as np
from utils.constants import DETECTOR, FILTER, ESTIMATOR


class ViewObserver:
    def __init__(self):
        self._id_to_func = {DETECTOR: ViewObserver.visualize_detector,
                            FILTER: ViewObserver.visualize_filter,
                            ESTIMATOR: ViewObserver.visualize_estimator}

        self._id_to_func_args = {}

    def notify(self, func_id, *argv):
        self._id_to_func_args[func_id] = argv

    def show(self):
        plt.figure()
        for func_id, args in self._id_to_func_args.items():
            self._id_to_func[func_id](args)

        plt.show()


    @staticmethod
    def visualize_detector(argv):
        plt.subplot(3, 1, 1)
        plt.ylabel("Candidates")

        plt.imshow(argv[4])
        plt.plot(argv[0], argv[1], 'r.', color='r', markersize=4)
        plt.plot(argv[2], argv[3], 'r.', color='g', markersize=4)

    @staticmethod
    def visualize_filter(argv):
        plt.subplot(3, 1, 2)
        plt.ylabel("Traffic_lights")

        plt.imshow(argv[2])
        red_x = [position[0] for position in argv[0]]
        red_y = [position[1] for position in argv[0]]
        green_x = [position[0] for position in argv[1]]
        green_y = [position[1] for position in argv[1]]
        plt.plot(red_x, red_y, 'r.', color='r', markersize=4)
        plt.plot(green_x, green_y, 'r.', color='g', markersize=4)

    @staticmethod
    def visualize_estimator(curr_container):
        curr_container = curr_container[0]
        plt.subplot(3, 1, 3)
        plt.ylabel("Distance")
        plt.imshow(curr_container.img)
        curr_p = np.array(curr_container.traffic_light)
        plt.plot(curr_p[:, 0], curr_p[:, 1], 'g.')
        for i in range(len(curr_p)):
            if curr_container.valid[i]:
                plt.text(curr_p[i, 0], curr_p[i, 1],
                         r'{0:.1f}'.format(curr_container.traffic_lights_3d_location[i, 2]), color='r')
        print("after filter", len(curr_p))