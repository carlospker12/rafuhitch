from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def start():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/createridedriver')
def charts():
    return render_template('create_ride_driver.html' )

@app.route('/listofridesp')
def tables():
    return render_template('listofridesP.html' )

@app.route('/ridedetails')
def ridedetails():
    return render_template('ridedetails.html' )

@app.route('/register')
def register():
    return render_template('register.html' )

@app.route('/driverprofile')
def driver_profile():
    return render_template('Driver_Profile.html' )

if __name__ == "__main__":
    app.run(debug=True)
