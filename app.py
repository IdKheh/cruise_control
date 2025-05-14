from flask import Flask, render_template
import plotly.express as px
import pandas as pd
import serial
import os
import time
from CuriseControl import *

# ser = serial.Serial('/dev/ttyACM0',9600, timeout =1) #polaczenie ardiuno i raspberry
app = Flask(__name__)


@app.route('/')
def index():
    params = {
        'kp': 1.0,
        'Ti': 2,
        'kd': 0.6,
        'd_zadane': 0.2,
        'Tp': 5,
        't_sym': 5
    }
    # ser.write(str(0).encode('utf-8'))
    # ser.write(str(9).encode('utf-8'))
    
    return render_template('index.html', params=params)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/<FUNCTION>')
def execCommand(FUNCTION = None):
    
    exec(FUNCTION.replace("<br>", "\n"))
    return ""

def savePlot(number, time, PWM, D):    
    df = pd.DataFrame(dict(
        Time=time,
        Sygnal=PWM,
        Odleglosc=D
    ))
    
    fig = px.line(df, x="Time", y=["Sygnal", "Odleglosc"],
                title="Przebieg PWM oraz odleglosci w czasie",
                labels={"Time": "Czas [s]", "value": "Odległość [m]", "variable": "Legenda"})

    fig.write_image("static/plot"+str(number)+".png")
    
def start(number : int, kp : float, Ti: float, kd : float, d_zadane : float, Tp : int, t_sym : int):
    pid = PID(kp, Ti, kd, d_zadane, Tp, t_sym*60)
    
    for i in range(pid.getN()):
        distanceSensor = 5 #polaczyc z sensorem
        # ser.write(str(pid.control(distanceSensor)).encode('utf-8')) #wysterować pojazd
        pid.sleep()
        
    savePlot(number, pid.getTime(), pid.getPWM(), pid.getD())  #zapisać to jako wykres
    return ""


def deleteFile(number):
    for i in range(1,number+1):
        os.remove('static/plot'+str(i)+'.png')


def reset(number : int):
    deleteFile(number)
    print("reset")
    return ''


def poweroff(number : int):
    deleteFile(number)
    #os.system('shutdown -h now')
    print("poweroff")
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)