class Points:
    def __init__(self, points):
        self.__points = points
        self.__pubid = ''

    def set_points(self, points):
        self.__points = points

    def get_points(self):
        return self.__points

    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid
