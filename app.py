from flask import Flask, render_template, request, session
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
from flask_session import Session
from time import time
import psycopg2
import os

# the app we use to manage the routes and run the app
app = Flask(__name__)
app.config['SECRET_KEY'] = "gotti"

# main homepage of the website
@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template("home.html")  
@app.route('/login')
def login():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor()
    session['u'] = request.args.get('u')
    try:
        cur.execute("""
        SELECT *  FROM users WHERE username = %s;        
        """, (session['u'],))
    except Exception:
        cur.execute("""
        CREATE TABLE users (
            username TEXT NOT NULL PRIMARY KEY,
            time INT[],
            accx INT[],
            accy INT[],
            accz INT[]
        );
        """)
        cur.execute("""
        SELECT *  FROM users WHERE username = %s;        
        """, (session['u'],))
    user = cur.fetchone()
    if user is None:
        cur.execute("""
        INSERT INTO users(username, time, accx, accy, accz)
        VALUES (%s, %s, %s, %s, %s)
        """, (session['u'], [], [], [], []))
    con.commit()
    con.close()
    return '<p>Hello, '+session['u']+'!</p>'

@app.route('/clear')
def clear():
    session.clear()
#get data
@app.route('/data')
def data():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor()
    u = request.args.get('u')
    try:
        cur.execute("""
        SELECT *  FROM users WHERE username = %s;        
        """, (u,))
    except Exception:
        cur.execute("""
        CREATE TABLE users (
            username TEXT NOT NULL PRIMARY KEY,
            time INT[],
            accx INT[],
            accy INT[],
            accz INT[]
        );
        """)
        cur.execute("""
        SELECT *  FROM users WHERE username = %s;        
        """, (u,))
    user = cur.fetchone()
    if not user is None:
        user[1].append(time.now())
        user[2].append(int(request.args.get('accx')))
        user[3].append(int(request.args.get('accy')))
        user[4].append(int(request.args.get('accz')))
        accx = np.array(user[2])
        accy = np.array(user[3])
        accz = np.array(user[4])
        tim= np.array(user[1])
        tim = tim - tim[0]
        cur.execute(""" UPDATE users
            SET time = %s
            WHERE username = %s""", (tim,), (u,))
        cur.execute(""" UPDATE users
            SET accx = %s
            WHERE username = %s""", (accx,), (u,))
        cur.execute(""" UPDATE users
            SET accy = %s
            WHERE username = %s""", (accy,), (u,))
        cur.execute(""" UPDATE users
            SET accz = %s
            WHERE username = %s""", (accz), (u,))
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
        return  '<img src="data:image/png;base64,' + plotData[0] + '" alt = "accelerometer data" style="width: 20%" >'
    con.commit()
    con.close()
    return "<p>user not found</p>"
# runs our app using Flask
if __name__ == "__main__":
    app.run(debug = True)
