from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, form
from createride import Createdriverride as Createdriverride
from driver  import Driver
import firebase_admin
from firebase_admin import credentials, db
from signup import User

cred = credentials.Certificate('./cred/rafuhitch-firebase-adminsdk-ip26u-288aa3dbc4.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rafuhitch.firebaseio.com/'
})

root = db.reference()



app = Flask(__name__)

class registereddriverform(Form):
    name = StringField('Name')
    username = StringField('username')
    password = StringField('Password')
    nric = StringField('NRIC')
    email = StringField('Email')
    contactno = StringField('Contact Number')
    license = StringField('Car License Plate Number')
    carmodel = StringField('Car Brand & Model')

class createdriverrideform(Form):
    from_where = StringField('Starting Position',render_kw={"placeholder": "Start"})
    to_where = StringField('Destination', render_kw={"placeholder": "End"})
    date = StringField('Date',render_kw={"placeholder": "DD/MM/YYYY"})
    time = StringField('Time',render_kw={"placeholder": "Time"})
    userid = StringField('Verification',[validators.Length(min=6, max=6)],render_kw={"placeholder": "Enter 'driver' "} )

class createpassengerrideform(Form):
    from_where = StringField('Starting Position',render_kw={"placeholder": "Start"})
    to_where = StringField('Destination', render_kw={"placeholder": "End"})
    date = StringField('Date',render_kw={"placeholder": "DD/MM/YYYY"})
    time = StringField('Time',render_kw={"placeholder": "Time"})
    userid = StringField('Verification',[validators.Length(min=9, max=9)],render_kw={"placeholder": "Enter 'passenger' "} )


@app.route('/createridedriver',methods=["GET","POST"])
def createridedriver():
    form = createdriverrideform(request.form)
    if request.method == 'POST' and form.validate():
        if  form.userid.data.lower() == 'driver':
            from_where= form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data
            userid = form.userid.data

            cdr = Createdriverride(userid,from_where,to_where,date,time)

            cdr_db = root.child('listofridesp')
            cdr_db.push({
                    'Starting position': cdr.get_from_where(),
                    'Destination': cdr.get_to(),
                    'date': cdr.get_date(),
                    'time': cdr.get_time(),
                    'usertype':cdr.get_usertype()

            })
            return redirect(url_for('listofridesP'))
    return render_template('create_ride_driver.html', form= form)

@app.route('/listofridesp')
def listofridesP():
    listofridesp = root.child('listofridesp').get()
    list = []
    for pubid in listofridesp:

        eachupdate = listofridesp[pubid]

        if eachupdate['usertype'] == 'driver':
            if eachupdate["status"] == "Active":
                ride = Createdriverride( eachupdate['Starting position'], eachupdate['Destination'],eachupdate['date'], eachupdate['time'],eachupdate['usertype'])

            ride.set_pubid(pubid)
            print(ride.get_pubid())
            list.append(ride)

    return render_template('listofridesP.html',  listofridesp = list )


@app.route('/ridedetails')
@app.route('/ridedetails/<string:id>/', methods=['GET', 'POST'])
def ridedetails(id):

    listofridesp = root.child('listofridesp').get()

    url = 'listofridesp/' + id
    eachpub = root.child(url).get()


    ride = Createdriverride( eachpub['Starting position'], eachpub['Destination'],
                             eachpub['date'], eachpub['time'],eachpub['usertype'])


    return render_template('ridedetails.html', ride=ride )

@app.route('/register', methods=["GET","POST"])
def register():
    form = registereddriverform(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        name=form.name.data
        email=form.email.data
        password=form.password.data

        userinfo=User(name,email,password,username)

        userinfo_db=root.child("userstuff")
        userinfo_db.push({
            "Username":userinfo.get_username(),
            "Name":userinfo.get_name(),
            "Email":userinfo.get_email(),
            "Password":userinfo.get_password()
        })
        return redirect(url_for("login"))

    return render_template('register.html', form= form)

class Log_InForm(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ',[validators.DataRequired()])

@app.route('/', methods =["GET","POST"])
def login():
    form = Log_InForm(request.form)
    if  request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        ifUserExists = root.child('userstuff').order_by_child('Username').equal_to(username).get()
        if len(ifUserExists) <= 0:

            error = 'Invalid login'
            flash(error, 'danger')
            return render_template('register.html', form=form)
        else:
            for k, v in ifUserExists.items():
                print(k, v)
                # print(sha256_crypt.encrypt(password))
                print(v['Username'])
                print(v['Password'])

                if username == v['Username'] and password == v['Password']:
                    session['logged_in'] = True
                    session['Username'] = username
                    return redirect(url_for('createridedriver'))
                else:
                    error = 'Invalid login'
                    flash(error, 'danger')
                    return render_template('register.html', form=form)

    return render_template('login.html')

@app.route('/driverprofile')
def driverprofile():
    driver = root.child('Driverprofile').get()
    list = []
    for pubid in driver:
        print('2', driver[pubid])
        eachdriver = driver[pubid]
        driver = Driver(eachdriver['Name'], eachdriver['Password'], eachdriver['NRIC'], eachdriver['Email'], eachdriver['Contactno'], eachdriver['License'], eachdriver['Car Model'])
        driver.set_pubid(pubid)
        list.append(driver)

    return render_template('Driver_Profile.html', driverprofile = list)


@app.route('/registerdriver',methods=['GET','POST'])
def registerdriver():
    form = registereddriverform(request.form)
    if request.method == 'POST' :
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        nric = request.form["nric"]
        email = request.form["email"]
        contactno = request.form["contactno"]
        license = request.form["license"]
        carmodel = request.form["carmodel"]


        rd = registereddriverform(username,name, password, nric, email, contactno, license, carmodel)

        rd_db = root.child('Driverprofile')
        rd_db.push({
                'username': rd.get_username(),
                'Name': rd.get_name(),
                'Password': rd.get_password(),
                'NRIC': rd.get_nric(),
                'Email': rd.get_email(),
                'Contactno':rd.get_contactno(),
                'License': rd.get_license(),
                'Car Model':rd.get_carmodel()
        })

        return redirect(url_for('login'))


    return render_template('register_driver.html', form= form)


@app.route('/createridepassenger',methods=["GET","POST"])
def createridepassenger():
    form = createpassengerrideform(request.form)
    if request.method == 'POST' and form.validate():
        if  form.userid.data.lower() == 'Passenger':
            from_where= form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data
            userid = form.userid.data

            cdr = Createdriverride(userid,from_where,to_where,date,time)

            cdr_db = root.child('listofridepassenger')
            cdr_db.push({
                    'Starting position': cdr.get_from_where(),
                    'Destination': cdr.get_to(),
                    'date': cdr.get_date(),
                    'time': cdr.get_time(),
                    'usertype':cdr.get_usertype()

            })
            return redirect(url_for('listofridesP'))
    return render_template('create_ride_passenger.html', form= form)



if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
    app.run(port="80")
