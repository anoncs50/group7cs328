from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
# the app we use to manage the routes and run the app
app = Flask(__name__)
app.config['SECRET_KEY'] = "gotti"

# main homepage of the website
@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template("home.html")    
#get data
@app.route('/data')
def data():
    if not 'accx' in session or not 'accy' in session or not 'accz' in session:
        session['accx'] = []
        session['accy'] = []
        session['accz'] = []
    session['accx'].append(request.args.get('x'))
    session['accy'].append(request.args.get('y'))
    session['accy'].append(request.args.get('z'))
    return "<p> x accel:" + str(accx)+"<br>y accel:"+str(accy)+"<br>z accel:" +str(accz)+ " </p>"
# runs our app using Flask
if __name__ == "__main__":
    app.run(debug = True)
