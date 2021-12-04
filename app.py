from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
# the app we use to manage the routes and run the app
app = Flask(__name__)


# main homepage of the website
@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template("home.html")    
    else:
        #data = request.form['data'] 
        return render_template("data.html")
# runs our app using Flask
if __name__ == "__main__":
    app.run(debug = True)
