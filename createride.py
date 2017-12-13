class Createdriverride:
    def __init__(self, type,from_where,to,date,time):
        self.__from_where = from_where
        self.__to = to
        self.__type = type
        self.__date = date
        self.__time = time

    def get_from_where(self):a
        return self.__from_where

    def set_from_where(self, from_where):
        self.__from_where = from_where

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

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
