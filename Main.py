from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, form
from createride import Createdriverride as Createdriverride
import firebase_admin
from firebase_admin import credentials, db
from signup import User

cred = credentials.Certificate('./cred/rafuhitch-firebase-adminsdk-ip26u-288aa3dbc4.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rafuhitch.firebaseio.com/ '
})

root = db.reference()



app = Flask(__name__)


class createdriverrideform(Form):
    from_where = StringField('Starting Position')
    to_where = StringField('Destination')
    date = StringField('Date')
    time = StringField('Time')
    userid = StringField('driver')


@app.route('/', methods =["GET","POST"])
def login():
    if  request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "google@google.com":
            if password == "password":
                return render_template("listofridesP.html")
    return render_template('login.html')

@app.route('/createridedriver',methods=["GET","POST"])
def new():
    form = createdriverrideform(request.form)
    if request.method == 'POST' and form.validate():
        if  form.userid.data == 'driver':
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

            flash('Magazine Inserted Sucessfully.', 'success')



            return redirect(url_for('login'))


    return render_template('create_ride_driver.html', form= form)



@app.route('/listofridesp')
def tables():
    listofridesp = root.child('listofridesp').get()
    list = []
    # for userid in listofridesp:
    #
    #     eachupdate = listofridesp[id]
    #
    #     if eachupdate['userid'] == 'driver':
    #         createride = Createdriverride( eachupdate['from'], eachupdate['to'],
    #                             eachupdate['date'], eachupdate['time'],eachupdate['userid'])
    #         createride.set_userid(userid)
    #         print(createride.get_userid())
    #         list.append(createride)
    # return render_template('listofridesP.html' )
    for pubid in listofridesp:

        eachupdate = listofridesp[pubid]

        if eachupdate['usertype'] == 'driver':
            ride = Createdriverride( eachupdate['Starting position'], eachupdate['Destination'],
                     eachupdate['date'], eachupdate['time'],eachupdate['usertype'])

            ride.set_pubid(pubid)
            print(ride.get_pubid())
            list.append(ride)

    return render_template('listofridesP.html',  listofridesp = list )


















@app.route('/ridedetails')
def ridedetails():
    return render_template('ridedetails.html' )

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]

        userinfo=User(name,email,password)

        userinfo_db=root.child("userstuff")
        userinfo_db.push({
            "Name":userinfo.get_name(),
            "Email":userinfo.get_email(),
            "Password":userinfo.get_password()
        })
        return redirect(url_for("listofridesP"))

    return render_template('register.html', form= form)

@app.route('/driverprofile')
def driver_profile():
    return render_template('Driver_Profile.html' )

@app.route('/registerdriver')
def register_driver():
    return render_template('register_driver.html' )

if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
