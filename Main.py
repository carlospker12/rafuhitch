from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField, form
from createride import Createdriverride as Createdriverride
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('./cred/rafuhitch-firebase-adminsdk-ip26u-288aa3dbc4.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rafuhitch.firebaseio.com/ '
})

root = db.reference()



app = Flask(__name__)


class createdriverrideform(Form):
    from_where = StringField('From')
    to_where = StringField('To')
    date = StringField('Date')
    time = StringField('Time')
    type = RadioField('Type Of Publication', choices=[('driver')], default='type')


@app.route('/', methods =["GET","POST"])
def login():
    if  request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "google@google.com":
            if password == "password":
                return render_template("listofridesP.html")
    return render_template('login.html')

@app.route('/',methods=["GET","POST"])
def new():
    form = createdriverrideform(request.form)
    if request.method == 'POST' and form.validate():
        if  form.type.data == 'driver':
            from_where= form.from_where.data
            to_where = form.to_where.data
            date = form.date.data
            time = form.time.data

            cdr = Createdriverride(from_where,to_where,date,time)

            cdr_db = root.child('listofrides')
            cdr_db.push({
                    'type': cdr.get_type(),
                    'from': cdr.get_from_where(),
                    'to': cdr.get_to(),
                    'date': cdr.get_date(),
                    'time': cdr.get_time(),

            })

            flash('Magazine Inserted Sucessfully.', 'success')



        return redirect(url_for('listofridesp'))


    return render_template('create_ride_driver.html', form= form)



@app.route('/')
def tables():
    listofridesp = root.child('listofridesp').get()
    list = []
    for id in listofridesp:

        eachupdate = listofridesp[id]

        if eachupdate['type'] == 'driver':
            createride = Createdriverride( eachupdate['from'], eachupdate['to'],
                                eachupdate['date'], eachupdate['time'])
            createride.set_type(type)
            print(createride.get_type())
            list.append(createride)
    return render_template('listofridesP.html' )

@app.route('/')
def ridedetails():
    return render_template('ridedetails.html' )

@app.route('/')
def register():
    return render_template('register.html' )

@app.route('/')
def driver_profile():
    return render_template('Driver_Profile.html' )

@app.route('/')
def register_driver():
    return render_template('register_driver.html' )

if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
