
from flask import Flask, render_template, request
from helper import getPlots
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
# the app we use to manage the routes and run the app
app = Flask(__name__)


# main homepage of the website
@app.route('/')
def home():
    return render_template("home.html")
# runs our app using Flask
if __name__ == "__main__":
    app.run(debug = True)
