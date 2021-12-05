from flask import Flask, render_template, request, session
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
from flask_session import Session
import time
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
    if not 'accx' in session or not 'accy' in session or not 'accz' or not 'time' in session:
        session['accx'] = []
        session['accy'] = []
        session['accz'] = []
        session['time'] = []
    accx = session['accx']
    accy = session['accy']
    accz = session['accz']
    tim = session['time']
    accx.append(request.args.get('x'))
    accy.append(request.args.get('y'))
    accz.append(request.args.get('z'))
    tim.append(time.time())
    session['accx']=accx
    session['accy']=accy
    session['accz']=accz
    session['time']=tim
    tim = np.array(tim)
    tim=tim-tim[0]
    plt.plot(tim, accx,"-r", tim, accy, "-g", tim, accz, "-b")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s/s)")
    plt.legend(['x-axis', 'y-axis', 'z-axis'])
    plotData=[]
    fig = BytesIO()
    plt.savefig(fig, format='png')
    fig.seek(0)
    buffer = b''.join(fig)
    b2 = base64.b64encode(buffer)
    figDec =b2.decode('utf-8')
    plotData.append(figDec)
    return  '<img src="data:image/png;base64,' + plotData[0] + ' alt = "accelerometer data" >'
# runs our app using Flask
if __name__ == "__main__":
    app.run(debug = True)
