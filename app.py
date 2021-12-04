from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
# the app we use to manage the routes and run the app
app = Flask(__name__)
accx = []
accy = []
accz = []

# main homepage of the website
@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template("home.html")    
#get data
@app.route('/data')
def data():
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')
    return "<p> " + x+"<br>"+y+"<br>" +z+ " </p>"
# runs our app using Flask
if __name__ == "__main__":
    app.run(debug = True)
