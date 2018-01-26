class createridep:
    def __init__(self, usertype, from_where, to, date, time):
        self.__pubid = ''
        self.__from_where = from_where
        self.__to = to
        self.__usertype = usertype
        self.__date = date
        self.__time = time


    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid

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
