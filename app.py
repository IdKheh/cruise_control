from flask import Flask, render_template, abort
import matplotlib.pyplot as plt
import pandas as pd
import serial
import os
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
    fun = str(FUNCTION).lstrip('/').split('(')[0]
    print(fun)
    if fun not in ('start', 'reset', 'poweroff'):
        abort(404)
    
    exec(FUNCTION.replace("<br>", "\n"))
    return ""

def savePlot(number, time, PWM, D):  
    
    print( len (time), len(PWM), len(D))
    df = pd.DataFrame(dict(
        Time=time,
        Sygnal=PWM,
        Odleglosc=D
    ))

    
    plt.figure(figsize=(10, 6))
    plt.plot(df["Time"], df["Sygnal"], label="Sygnal", color='blue')
    plt.plot(df["Time"], df["Odleglosc"], label="Odleglosc", color='orange')

    plt.title("Przebieg PWM oraz odleglosci w czasie")
    plt.xlabel("Czas [s]")
    plt.ylabel("Odległość [m]")
    plt.legend(title="Legenda")
    plt.grid(True)

    plt.savefig(f"static/plot{number}.png")
    plt.close()
    
def start(number : int, kp : float, Ti: float, kd : float, d_zadane : float, Tp : int, t_sym : int):
    pid = PID(kp, Ti, kd, d_zadane, Tp, t_sym*60)
    
    for i in range(pid.getN()):
        distanceSensor = 0.05  #polaczyc z sensorem
        # pid.control(distanceSensor);
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