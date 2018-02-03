class Points:
    def __init__(self, points, sessionemail):
        self.__points = points
        self.__pubid = ''
        self.__sessionemail = sessionemail

    def set_points(self, points):
        self.__points = points

    def get_points(self):
        return self.__points

    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid

    def get_sessionemail(self):
        return self.__sessionemail

    def set_sessionemail(self, sessionemail):
        self.__sessionemail = sessionemail
