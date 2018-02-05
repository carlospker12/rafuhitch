class Updatedriver:
    def __init__(self, name, password, nric, email, contactno, license, carmodel, summary, sessionemail):
        self.__pubid = ''
        self.__name = name
        self.__password = password
        self.__nric = nric
        self.__email = email
        self.__contactno = contactno
        self.__license = license
        self.__carmodel = carmodel
        self.__summary = summary

    def set_name(self, name):
        self.__name = name
    def set_password(self, password):
        self.__password = password
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
    def set_summary(self, summary):
        self.__summary = summary
    def set_sessionemail(self,sessionemail):
        self.__sessionemail = sessionemail

    def get_name(self):
        return self.__name
    def get_password(self):
        return self.__password
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
    def get_summary(self):
        return self.__summary
    def get_sessionemail(self):
        return self.__sessionemail

    def get_pubid(self):
        return self.__pubid
    def set_pubid(self, pubid):
        self.__pubid = pubid
