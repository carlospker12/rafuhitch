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
from schedule import schedule
from werkzeug.utils import secure_filename
from updatedriver import Updatedriver

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


class registereddriverform(Form):
    name = StringField('Name',[validators.DataRequired()])
    password = StringField('Password',[validators.DataRequired()])
    nric = StringField('NRIC',[validators.DataRequired()])
    email = StringField('Email',[validators.DataRequired()])
    contactno = StringField('Contact Number',[validators.DataRequired()])
    license = StringField('Car License Plate Number',[validators.DataRequired()])
    carmodel = StringField('Car Brand & Model',[validators.DataRequired()])
    summary = StringField('Summary', [validators.DataRequired()])

class updateddriverform(Form):
    name = StringField('Name', [validators.DataRequired()])
    password = StringField('Password', [validators.DataRequired()])
    nric = StringField('NRIC', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    contactno = StringField('Contact Number', [validators.DataRequired()])
    license = StringField('Car License Plate Number', [validators.DataRequired()])
    carmodel = StringField('Car Brand & Model', [validators.DataRequired()])
    summary = StringField('Summary', [validators.DataRequired()])
    sessionemail = StringField('Verification', render_kw={"placeholder": "Enter 'driver' "})
    points = StringField('Points', [validators.DataRequired()])

class createdriverrideform(Form):
    from_where = StringField('Starting Position',[validators.DataRequired()],render_kw={"placeholder": "Start"})
    to_where = StringField('Destination',[validators.DataRequired()], render_kw={"placeholder": "End"})
    date = StringField('Date',[validators.DataRequired()],render_kw={"placeholder": "DD/MM/YYYY"})
    time = StringField('Time',[validators.DataRequired()],render_kw={"placeholder": "Time"})
    userid = StringField('Verification',render_kw={"placeholder": "Enter 'driver' "} )
    sessionemail = StringField('Verification',render_kw={"placeholder": "Enter 'driver' "} )
    schedule = StringField('Verification',render_kw={"placeholder": "Enter 'driver' "} )


class schedule(Form):
    Monday = StringField('0',render_kw={"placeholder": "Start"})
    Tuesday = StringField('1', render_kw={"placeholder": "End"})
    Wednesday = StringField('2',render_kw={"placeholder": "DD/MM/YYYY"})
    Thursday = StringField('3',render_kw={"placeholder": "Time"})
    Friday = StringField('4',render_kw={"placeholder": "Enter 'driver' "} )
    Saturday = StringField('5',render_kw={"placeholder": "Enter 'driver' "} )
    Sunday = StringField('6',render_kw={"placeholder": "Enter 'driver' "} )


class createpassengerrideform(Form):
    from_where = StringField('Starting Position',render_kw={"placeholder": "Start"})
    to_where = StringField('Destination', render_kw={"placeholder": "End"})
    date = StringField('Date',render_kw={"placeholder": "DD/MM/YYYY"})
    time = StringField('Time',render_kw={"placeholder": "Time"})
    userid = StringField('Verification',render_kw={"placeholder": "Enter 'passenger' "} )
    sessionemail = StringField('Verification',render_kw={"placeholder": "Enter 'driver' "} )

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route('/createridepassenger',methods=["GET","POST"])
def createridepassenger():
    form = createdriverrideform(request.form)
    if request.method == 'POST' and form.validate():
        if  form.userid.data.lower() == '':
            from_where= form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data
            userid = form.userid.data
            sessionemail = form.sessionemail.data
            schedule = form.schedule.data

            crd = createridep(userid,from_where,to_where,date,time,sessionemail)

            crd_db = root.child('listofridepassenger')
            crd_db.push({
                'Starting position': crd.get_from_where(),
                'Destination': crd.get_to(),
                'date': crd.get_date(),
                'time': crd.get_time(),
                'usertype':crd.get_usertype(),
                'sessionemail': session['Email'],
                'status' :"Active",
                'schedule':request.form.getlist('days'),

            })


            pprofile = root.child('userstuff').get()
            for pubid in pprofile:
                pt = pprofile[pubid]
                if pt['Email'] == session['Email']:
                    totalpoints = pt['Points']
                    newp = int(totalpoints) + 10
                    # print(newp)
                    firstchild = root.child('userstuff')
                    firstchild.child(pubid).update({'Points': newp})

        return redirect(url_for('listofridesD'))

    return render_template('create_ride_passenger.html', form= form)

@app.route('/createridedriver/',methods=["GET","POST"])
def createridedriver():
    form = createdriverrideform(request.form)
    list = []
    if request.method == 'POST' and form.validate():
        if  form.userid.data.lower() == '':
            from_where= form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data
            userid = form.userid.data
            sessionemail = form.sessionemail.data
            schedule = form.schedule.data
            status="Active"

            cdr = Createdriverride(userid,from_where,to_where,date,time,sessionemail,schedule,status)

            cdr_db = root.child('listofridesp')
            cdr_db.push({
                'sessionemail': session['Email'],
                'Starting position': cdr.get_from_where(),
                'Destination': cdr.get_to(),
                'date': cdr.get_date(),
                'time': cdr.get_time(),
                'usertype':cdr.get_usertype(),
                'schedule':request.form.getlist('days'),
                'status':"Active"



            })

            dprofile = root.child('Driverprofile').get()
            for pubid in dprofile:
                pt = dprofile[pubid]
                if pt['Email'] == session['Email']:
                    totalpoints = pt['Points']
                    newp = int(totalpoints) + 10
                    # print(newp)
                    firstchild = root.child('Driverprofile')
                    firstchild.child(pubid).update({'Points' : newp})
            print(request.form.getlist('days'))
            schedule = [request.form.getlist('days')]

            return redirect(url_for('listofridesP'))
    return render_template('create_ride_driver.html', form= form)
@app.route('/myrides/')
def myrides():
    listmyrides = root.child('listofridesp').get()
    list= []
    if request.method=="POST":
        id=session.get("sessionemail","")
        status="Taken"
        data={"status":status}
        root.child("myrides/"+id).update(data)



    for pubid in listmyrides:
        eachobj = listmyrides[pubid]
        myride = Createdriverride(eachobj['Starting position'],eachobj['Destination'],eachobj['date'],eachobj['time'],eachobj['usertype'],eachobj['sessionemail'],eachobj['status'])
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
    # schedulelist = root.child('listofridesp').order_by_child('schedule').get()
    # list1 =[]
    list = []
    # for sid in schedulelist:
    #     eachid = schedulelist[sid]
    #     scheduleid = schedule(eachid['0'],eachid['1'],eachid['2'],eachid['3'],eachid['4'],eachid['5'],eachid['6'])
    #     scheduleid.set_sid(sid)
    #     print(scheduleid.get_sid)
    #     list1.append(scheduleid)
    for pubid in listofridesd:
        eachupdate = listofridesd[pubid]
        ride = Createdriverride(eachupdate['Starting position'], eachupdate['Destination'],eachupdate['date'], eachupdate['time'],eachupdate['usertype'],eachupdate['sessionemail'],eachupdate['schedule'],eachupdate["status"])
        ride.set_pubid(pubid)
        # print(ride.get_pubid())
        list.append(ride)

    return render_template('listofridesdriver.html',  listofridesd = list,schedulelist = list )

@app.route('/listofridespassenger')
def listofridesP():
    listofridesp = root.child('listofridepassenger').get()
    list = []
    for pubid in listofridesp:
        eachupdate = listofridesp[pubid]
        ride = Createdriverride( eachupdate['Starting position'], eachupdate['Destination'],eachupdate['date'], eachupdate['time'],eachupdate['usertype'],eachupdate['sessionemail'],eachupdate["status"])
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
                             eachpub['date'], eachpub['time'],eachpub['usertype'],eachpub['sessionemail'], eachpub['status'])


    if request.method == "POST":
        if request.form["taken"] == "Interested?":
            status ="Taken"
            ride = root.child("listofridepassenger/" + id)
            ride.set({
                "Starting position": from_where,
                "Destination": to_where,
                "date":date,
                "sessionemail":session["Email"],
                "time":time,
                "usertype":userid,
                #"schedule":schedule,
                "status": "Taken"})

            return redirect(url_for("myrides"))

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
                schedule = form.schedule.data

    url = 'listofridesp/' + id
    eachpub = root.child(url).get()

    ride = Createdriverride( eachpub['Starting position'], eachpub['Destination'],
                             eachpub['date'], eachpub['time'],eachpub['usertype'],eachpub['sessionemail'],eachpub['schedule'],eachpub["status"])

    if request.method == "POST":
        if request.form["taken"] == "Interested?":
            status ="Taken"
            ride = root.child("listofridesp/" + id)
            ride.set({
                "Starting position": from_where,
                "Destination": to_where,
                "date":date,
                "sessionemail":session["Email"],
                "time":time,
                "usertype":userid,
                "schedule":schedule,
                "status": "Taken"})

            return redirect(url_for("myrides"))


    return render_template('ridedetails.html', ride=ride, form=form, start=ride.get_usertype(),status=ride.get_status() , ending=ride.get_from_where(), timing=ride.get_time(),dating=ride.get_date)

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
            "Points":0,
            'sessionemail': userinfo.get_email()
        })
        flash("Account successfully created")
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

    dprofile = root.child('Driverprofile').get()
    list = []
    for pubid in dprofile:
        pt = dprofile[pubid]
        if pt['Email'] == session['Email']:
            totalpoints = pt['Name'], pt['Email'],  pt['Contactno'],  pt['License'],  pt['Car Model'],  pt['Points'], pt['Summary']
            list.append(totalpoints)
    return render_template('Driver_Profile.html', driverprofile = list, pubid = pubid)

# @app.route('/update')
@app.route('/update_dprofile/<string:id>/', methods=['GET', 'POST'])
def edit(id):
    points = Points.get_points()
    form = updateddriverform(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        password = form.password.data
        nric = form.nric.data
        email = form.email.data
        contactno = form.contactno.data
        license = form.license.data
        carmodel = form.carmodel.data
        summary = form.summary.data
        points = points.get_points()

        url = 'Driverprofile/' + id
        eachpub = root.child(url).get()

        edits = Updatedriver(eachpub['Name'], eachpub['Password'], eachpub['NRIC'], eachpub['Email'],
                eachpub['Contactno'], eachpub['License'], eachpub['Car Model'], eachpub['Summary'])
        edits2 = Points(eachpub['Points'])
        udc = Updatedriver(name, password, nric, email, contactno, license, carmodel, summary)
        points = Points(points)
        ud_db = root.child('Driverprofile/' + id)
        ud_db.set({
            'sessionemail' :session['Email'],
            'Name': udc.get_name(),
            'Password': udc.get_password(),
            'NRIC': udc.get_nric(),
            'Email': udc.get_email(),
            'Contactno': udc.get_contactno(),
            'License': udc.get_license(),
            'Car Model': udc.get_carmodel(),
            'Points': points.get_points(),
            'Summary': udc.get_summary(),})
        flash('Changes sucessfully updated','success')

        return redirect(url_for('driverprofile'))

    else:
        url = 'Driverprofile/' + id
        eachpub = root.child(url).get()

        edits = Updatedriver(eachpub['Name'], eachpub['Password'], eachpub['NRIC'], eachpub['Email'],
                             eachpub['Contactno'], eachpub['License'], eachpub['Car Model'], eachpub['Summary'])
        points = Points(eachpub['Points'])
        form.points.data = points.get_points()
        form.name.data = edits.get_name()
        form.password.data = edits.get_password()
        form.nric.data = edits.get_nric()
        form.email.data = edits.get_email()
        form.contactno.data = edits.get_contactno()
        form.license.data = edits.get_license()
        form.carmodel.data = edits.get_carmodel()
        form.summary.data = edits.get_summary()

    return render_template('update_dprofile.html', form=form)

@app.route('/passengerprofile')
def passengerprofile():


    pprofile = root.child('userstuff').get()
    list = []
    for pubid in pprofile:
        pt = pprofile[pubid]
        if pt['Email'] == session['Email']:
            totalpoints = pt['Name'], pt['Email'], pt['Points']
            list.append(totalpoints)
    return render_template('Passenger_Profile.html', passenger = list)

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
        summary = request.form['summary']
        points= 0

        rd = Driver(name, password, nric, email, contactno, license, carmodel, points, summary)

        rd_db = root.child('Driverprofile')
        rd_db.push({
            'Name': rd.get_name(),
            'Password': rd.get_password(),
            'NRIC': rd.get_nric(),
            'Email': rd.get_email(),
            'Contactno':rd.get_contactno(),
            'License': rd.get_license(),
            'Car Model':rd.get_carmodel(),
            'Points':0,
            'Summary': rd.get_summary(),
            'sessionemail':rd.get_email()
        })
        flash("Account successfully created")
        return redirect(url_for('login'))


    return render_template('register_driver.html', form= form)


@app.route("/rewards")
def rewards():

    dprofile = root.child('Driverprofile').get()
    for pubid in dprofile:
        pt = dprofile[pubid]
        if pt['Email'] == session['Email']:
            totalpoints = pt['Points']


    pprofile = root.child('userstuff').get()
    for pubid in pprofile:
        point = pprofile[pubid]
        if point['Email'] == session['Email']:
            totalpoints = point['Points']

    return render_template('rewards.html', points = totalpoints)


@app.route("/redeem")
def redeem():
    dprofile = root.child('Driverprofile').get()
    for pubid in dprofile:
        pt = dprofile[pubid]
        if pt['Email'] == session['Email']:
            totalpoints = pt['Points']
            if totalpoints >= 100:
                newp = int(totalpoints) - 100
                # print(newp)
                firstchild = root.child('Driverprofile')
                firstchild.child(pubid).update({'Points': newp})
                pt = dprofile[pubid]
                if pt['Email'] == session['Email']:
                    totalpoints = pt['Points']
            else:
                return render_template('redeemfail.html')

    pprofile = root.child('userstuff').get()
    for pubid in pprofile:
        point = pprofile[pubid]
        if point['Email'] == session['Email']:
            totalpoints = point['Points']
            if totalpoints >= 100:
                newp = int(totalpoints) - 100
                # print(newp)
                firstchild = root.child('userstuff')
                firstchild.child(pubid).update({'Points': newp})
                point = pprofile[pubid]
                if point['Email'] == session['Email']:
                    totalpoints = point['Points']
            else:
                return render_template('redeemfail.html')
    import random

    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    passlen = 4
    p = "".join(random.sample(s, passlen))

    f = open("promocodes.txt", "a+")
    f.write('RAFU%s'%(p) +'\n')
    f.close()
    return render_template('redeem.html', points = totalpoints, code = p )




if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(port=50000, debug=True)
