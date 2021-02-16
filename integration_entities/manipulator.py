class Manipulator:
    def __init__(self, view_observer):
        self._view_observer = view_observer

    def handle(self, *argv):

        self.prepare_data(*argv)
        res = self.execute()
        return res
