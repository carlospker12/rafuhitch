from flask import Flask, render_template
app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/charts')
def charts():
    return render_template('charts.html' )

@app.route('/listofridep')
def tables():
    return render_template('listofridesP.html' )

@app.route('/ridedetails')
def ridedetails():
    return render_template('ridedetails.html' )

@app.route('/register')
def register():
    return render_template('register.html' )

@app.route('/driver_profile')
def driver_profile():
    return render_template('Driver_Profile.html' )

if __name__ == "__main__":
    app.run(debug=True)
