class User:
    def __init__(self,name,email,password,username):
        self.__name=name
        self.__username=username
        self.__email=email
        self.__password=password

    def set_name(self,name):
        self._name=name
    def set_username(self,username):
        self._username=username
    def set_email(self,email):
        self.__email=email
    def set_password(self,password):
        self.__password=password

    def get_name(self):
        return self.__name
    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password