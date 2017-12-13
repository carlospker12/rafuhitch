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

    def get_password