class Createdriverride:
    def __init__(self, usertype, from_where, to, date, time,sessionemail, status="Active",points=0):
        self.__pubid = ''
        self.__sessionemail = sessionemail
        self.__from_where = from_where
        self.__to = to
        self.__usertype = usertype
        self.__date = date
        self.__time = time
        self.__status=status
        self.__points=points


    def get_pubid(self):
        return self.__pubid
    def set_pubid(self, pubid):
        self.__pubid = pubid

    def get_points(self):
        return self.__points
    def set_points(self,points):
        self.__points=points

    def get_sessionemail(self):
        return self.__sessionemail
    def set_sessionemail(self, sessionemail):
        self.__sessionemail = sessionemail

    def get_from_where(self):
        return self.__from_where
    def set_from_where(self, from_where):
        self.__from_where = from_where

    def get_usertype(self):
        return self.__usertype
    def set_usertype(self, usertype):
        self.__usertype = usertype

    def get_to(self):
        return self.__to
    def set_to(self, to):
        self.__from_to = to

    def get_date(self):
        return self.__date
    def set_date(self, date):
        self.__date = date

    def get_time(self):
        return self.__time
    def set_time(self, time):
        self.__time = time

    def set_status(self, status):
        self.__status = status
    def get_status(self):
        return self.__status
