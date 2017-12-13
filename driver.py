# from firebase import firebase
# firebase = firebase.FirebaseApplication('https://rafuhitch.firebaseio.com/')
# result = firebase.get('/listofridesp', none)

class driver:
    def __init__(self, name, nric, email, contactno, license, carmodel, password):
        self.__name = name
        self.__nric = nric
        self.__email = email
        self.__contactno = contactno
        self.__license = license
        self.__carmodel = carmodel
        self.__password = password

    def set_name(self, name):
        self.__name = name
    def set_nric(self,nric):
        self.__nric = nric
    def set_email(self,email):
        self.__email = email
    def set_contactno(self,contactno):
        self.__contactno = contactno
    def set_license(self,license):
        self.__license = license
    def set_carmodel(self,carmodel):
        self.__carmodel = carmodel
    def set_password(self, password):
        self.__password = password

    def get_name(self):
        return self.__name
    def get_nric(self):
        return self.__nric
    def get_email(self):
        return self.__email
    def get_contactno(self):
        return self.__contactno
    def get_license(self):
        return self.__license
    def get_carmodel(self):
        return self.__carmodel
    def get_password(self):
        return self.__password