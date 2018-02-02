from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, form
from createride import Createdriverride as Createdriverride
from createrideP import createridep
from driver  import Driver
import firebase_admin
from firebase_admin import credentials, db
from signup import User
from points import Points
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

UPLOAD = ('UPLOAD/')
app = Flask(__name__)

cred = credentials.Certificate('./cred/rafuhitch-firebase-adminsdk-ip26u-288aa3dbc4.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rafuhitch.firebaseio.com/'
})

root = db.reference()


drivervalidation = 'driver'
app = Flask(__name__)

class registereddriverform(Form):
    name = StringField('Name',[validators.DataRequired()])
    password = StringField('Password',[validators.DataRequired()])
    nric = StringField('NRIC',[validators.DataRequired()])
    email = StringField('Email',[validators.DataRequired()])
    contactno = StringField('Contact Number',[validators.DataRequired()])
    license = StringField('Car License Plate Number',[validators.DataRequired()])
    carmodel = StringField('Car Brand & Model',[validators.DataRequired()])

class createdriverrideform(Form):
    from_where = StringField('Starting Position',render_kw={"placeholder": "Start"})
    to_where = StringField('Destination', render_kw={"placeholder": "End"})
    date = StringField('Date',render_kw={"placeholder": "DD/MM/YYYY"})
    time = StringField('Time',render_kw={"placeholder": "Time"})
    userid = StringField('Verification',render_kw={"placeholder": "Enter 'driver' "} )
    sessionemail = StringField('Verification',render_kw={"placeholder": "Enter 'driver' "} )


class createpassengerrideform(Form):
    from_where = StringField('Starting Position',render_kw={"placeholder": "Start"})
    to_where = StringField('Destination', render_kw={"placeholder": "End"})
    date = StringField('Date',render_kw={"placeholder": "DD/MM/YYYY"})
    time = StringField('Time',render_kw={"placeholder": "Time"})
    userid = StringField('Verification',render_kw={"placeholder": "Enter 'passenger' "} )

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route('/createridepassenger',methods=["GET","POST"])
def createridepassenger():
    form = createpassengerrideform(request.form)
    if request.method == 'POST' and form.validate():
        if  form.userid.data.lower() == '':
            from_where= form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data
            userid = form.userid.data

            crd = createridep(userid,from_where,to_where,date,time)

            crd_db = root.child('listofridepassenger')
            crd_db.push({
                'Starting position': crd.get_from_where(),
                'Destination': crd.get_to(),
                'date': crd.get_date(),
                'time': crd.get_time(),
                'usertype':crd.get_usertype()

            })
            return redirect(url_for('listofridesdriver'))
    return render_template('create_ride_passenger.html', form= form)

@app.route('/createridedriver/',methods=["GET","POST"])
def createridedriver():
    form = createdriverrideform(request.form)
    if request.method == 'POST' and form.validate():
        if  form.userid.data.lower() == '':
            from_where= form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data
            userid = form.userid.data
            sessionemail = form.sessionemail.data

            cdr = Createdriverride(userid,from_where,to_where,date,time,sessionemail)

            cdr_db = root.child('listofridesp')
            cdr_db.push({
                'sessionemail': session['Email'],
                'Starting position': cdr.get_from_where(),
                'Destination': cdr.get_to(),
                'date': cdr.get_date(),
                'time': cdr.get_time(),
                'usertype':cdr.get_usertype()

            })

            dprofile = root.child('Driverprofile').get()

            for pubid in dprofile:
                pt = dprofile[pubid]
                dprofile = Points(pt['Points'])
                dprofile.set_pubid(pubid)
                totalpoints = pt['Points']
                newp = int(totalpoints) + 10
                # print(newp)
                firstchild = root.child('Driverprofile')
                firstchild.child(pubid).update({'Points' : newp})

            return redirect(url_for('listofridesD'))
    return render_template('create_ride_driver.html', form= form)
@app.route('/myrides/')
def myrides():
    listmyrides = root.child('listofridesp').get()
    list= []
    for pubid in listmyrides:
        eachobj = listmyrides[pubid]
        myride = Createdriverride(eachobj['Starting position'],eachobj['Destination'],eachobj['date'],eachobj['time'],eachobj['usertype'],eachobj['sessionemail'])
        myride.set_pubid(pubid)
        print(myride.get_pubid())
        list.append(myride)

    return render_template('myride.html', listmyrides = list)
# def listofridesD():
#     listofridesd = root.child('listofridesp').get()
#     list = []
#     for pubid in listofridesd:
#         eachupdate = listofridesd[pubid]
#         ride = Createdriverride( eachupdate['Starting position'], eachupdate['Destination'],eachupdate['date'], eachupdate['time'],eachupdate['usertype'])
#         ride.set_pubid(pubid)
#         print(ride.get_pubid())
#         list.append(ride)
#
#     return render_template('listofridesdriver.html',  listofridesd = list )

@app.route('/listofridesdriver')
def listofridesD():
    listofridesd = root.child('listofridesp').get()
    list = []
    for pubid in listofridesd:
        eachupdate = listofridesd[pubid]
        ride = Createdriverride( eachupdate['Starting position'], eachupdate['Destination'],eachupdate['date'], eachupdate['time'],eachupdate['usertype'],eachupdate['sessionemail'])
        ride.set_pubid(pubid)
        print(ride.get_pubid())
        list.append(ride)

    return render_template('listofridesdriver.html',  listofridesd = list )

@app.route('/listofridespassenger')
def listofridesP():
    listofridesp = root.child('listofridepassenger').get()
    list = []
    for pubid in listofridesp:
        eachupdate = listofridesp[pubid]
        ride = Createdriverride( eachupdate['Starting position'], eachupdate['Destination'],eachupdate['date'], eachupdate['time'],eachupdate['usertype'])
        ride.set_pubid(pubid)
        print(ride.get_pubid())
        list.append(ride)

    return render_template('listofridespassenger.html',  listofridesp = list )

@app.route('/ridedetail')
@app.route('/ridedetail/<string:id>/', methods=['GET', 'POST'])
def ridedetail(id):
    form = createpassengerrideform(request.form)
    if request.method == 'POST' and form.validate():
        if form.userid.data.lower() == '':
            from_where = form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data
            userid = form.userid.data
    url = 'listofridepassenger/' + id
    eachpub = root.child(url).get()

    ride = Createdriverride( eachpub['Starting position'], eachpub['Destination'],
                             eachpub['date'], eachpub['time'],eachpub['usertype'])

    return render_template('ridedetails.html', ride=ride, form=form, start=ride.get_usertype(),
                           status=ride.get_status(), ending=ride.get_from_where(), timing=ride.get_time(),
                           dating=ride.get_date)


@app.route('/ridedetails')
@app.route('/ridedetails/<string:id>/', methods=['GET', 'POST'])
def ridedetails(id):
    form = createdriverrideform(request.form)
    if request.method == 'POST' and form.validate():
        if form.userid.data.lower() == '':
            from_where = form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data
            userid = form.userid.data
    url = 'listofridesp/' + id
    eachpub = root.child(url).get()

    ride = Createdriverride( eachpub['Starting position'], eachpub['Destination'],
                             eachpub['date'], eachpub['time'],eachpub['usertype'])



    return render_template('ridedetails.html', ride=ride, form=form, start=ride.get_usertype(),status=ride.get_status() , ending=ride.get_from_where(), timing=ride.get_time(),dating=ride.get_date )

@app.route('/register', methods=["GET","POST"])
def register():
    form = registereddriverform(request.form)
    if request.method == "POST":
        name=form.name.data
        email=form.email.data
        password=form.password.data

        userinfo=User(name,email,password)

        userinfo_db=root.child("userstuff")
        userinfo_db.push({
            "Name":userinfo.get_name(),
            "Email":userinfo.get_email(),
            "Password":userinfo.get_password(),
            "Points":0
        })
        return redirect(url_for("login"))

    return render_template('register.html', form= form)

class Log_InForm(Form):
    email = StringField('Email: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ',[validators.DataRequired()])

@app.route('/login', methods =["GET","POST"])
def login():
    form = Log_InForm(request.form)
    if  request.method == "POST" and form.validate():
        email = form.email.data
        password = form.password.data

        ifUserExists = root.child('userstuff').order_by_child('Email').equal_to(email).get()
        if len(ifUserExists) <= 0:
            ifUserExists = root.child("Driverprofile").order_by_child('Email').equal_to(email).get()
            if len(ifUserExists)<=0:
                flash("Invalid Login")
                return redirect(url_for('login'))
            else:
                for k, v in ifUserExists.items():
                    print(k, v)
                    # print(sha256_crypt.encrypt(password))
                    print(v['Email'])
                    print(v['Password'])

                    if email == v['Email'] and password == v['Password']:
                        session['logged_in'] = True
                        session['Email'] = email
                        return redirect(url_for('createridedriver'))
        else:
            for k, v in ifUserExists.items():
                print(k, v)
                # print(sha256_crypt.encrypt(password))
                print(v['Email'])
                print(v['Password'])

                if email == v['Email'] and password == v['Password']:
                    session['logged_in'] = True
                    session['Email'] = email
                    return redirect(url_for('createridepassenger'))
                else:

                    flash("Invalid Login")
                    return render_template('login.html', form=form)

    return render_template('login.html')

@app.route('/driverprofile')
def driverprofile():
    driver = root.child('Driverprofile').get()
    list = []
    for pubid in driver:
        print('2', driver[pubid])
        eachdriver = driver[pubid]
        driver = Driver(eachdriver['Name'], eachdriver['Password'], eachdriver['NRIC'], eachdriver['Email'], eachdriver['Contactno'], eachdriver['License'], eachdriver['Car Model'], eachdriver['Points'], )
        driver.set_pubid(pubid)
        list.append(driver)

    return render_template('Driver_Profile.html', driverprofile = list)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('UPLOAD/', filename))
            return redirect(url_for('uploaded_file', filename = filename))
    return render_template('Driver_Profile.html')

@app.route('/show/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:50000/upload/' + filename
    return render_template('Driver_Profile.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD, filename)

@app.route('/registerdriver',methods=['GET','POST'])
def registerdriver():
    if request.method == 'POST' :
        name = request.form["name"]
        password = request.form["password"]
        nric = request.form["nric"]
        email = request.form["email"]
        contactno = request.form["contactno"]
        license = request.form["license"]
        carmodel = request.form["carmodel"]
        points= 0

        rd = Driver(name, password, nric, email, contactno, license, carmodel,points)

        rd_db = root.child('Driverprofile')
        rd_db.push({
            'Name': rd.get_name(),
            'Password': rd.get_password(),
            'NRIC': rd.get_nric(),
            'Email': rd.get_email(),
            'Contactno':rd.get_contactno(),
            'License': rd.get_license(),
            'Car Model':rd.get_carmodel(),
            'Points':0
        })

        return redirect(url_for('login'))


    return render_template('register_driver.html', form= form)


@app.route("/rewards")
def rewards():
    driver = root.child('Driverprofile').get()
    list = []
    for pubid in driver:
        eachdriver = driver[pubid]
        driver = Driver(eachdriver['Name'], eachdriver['Password'], eachdriver['NRIC'], eachdriver['Email'],
                        eachdriver['Contactno'], eachdriver['License'], eachdriver['Car Model'], eachdriver['Points'], )
        driver.set_pubid(pubid)
        list.append(driver)
    return render_template('rewards.html', driverprofile = list)


@app.route("/redeem")
def redeem():
    dprofile = root.child('Driverprofile').get()

    for pubid in dprofile:
        pt = dprofile[pubid]
        dprofile = Points(pt['Points'])
        dprofile.set_pubid(pubid)
        totalpoints = pt['Points']
        newp = int(totalpoints) - 100
        firstchild = root.child('Driverprofile')
        firstchild.child(pubid).update({'Points': newp})

    driver = root.child('Driverprofile').get()
    list = []
    for pubid in driver:
        eachdriver = driver[pubid]
        driver = Driver(eachdriver['Name'], eachdriver['Password'], eachdriver['NRIC'], eachdriver['Email'],
                        eachdriver['Contactno'], eachdriver['License'], eachdriver['Car Model'], eachdriver['Points'], )
        driver.set_pubid(pubid)
        list.append(driver)

    import random

    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    passlen = 4
    p = "".join(random.sample(s, passlen))

    return render_template('redeem.html', driverprofile = list, code = p )




if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(port=50000, debug=True)
