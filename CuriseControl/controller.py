import time

class PID:
    def __init__(self, kp, Ti, kd, d_zadane, Tp, t_sym):
        self.__kp = kp    # nastawa P
        self.__Ti = Ti    # nastawa I
        self.__kd = kd    # nastawa D

        self.__Tp = Tp # okres probkowania [s]
        self.__t_sym = t_sym # czas symulacji [s]
        self.__t = [0] #czas symulacji
        self.__n=int(round(self.__t_sym/self.__Tp,0))
        
        self.__d_0 = 0 # odleglosc poczatkowa [m]
        self.__d = [self.__d_0] # odleglosc [m/s]
        self.__d_zadane = d_zadane # h zadane [m]
        self.__d_min = 0 # [m/s]
        self.__d_max = 5 # [m/s]
        
        self.__e=[0] #uchyb [m]
        self.__upi= []
        self.__pwm_min = 0
        self.__pwm_max = 255
        self.__pwm = [0] #wartość prądu z regulatora [V]
        
        
    def control(self, distanceSensor):
        self.__t.append(self.__t[-1]+self.__Tp)
        self.__d.append(distanceSensor)
        self.__e.append(self.__d_zadane-distanceSensor)
        self.__upi.append(self.__kp*(self.__e[-1]+(1/self.__Ti)*sum(self.__e) + self.__kd*(self.__e[-1]-self.__e[-2])))
        
        self.__pwm.append(max(min((self.__pwm_max - self.__pwm_min) * self.__upi[-1], self.__pwm_max), self.__pwm_min))
        
        #self.__pwm.append(max(min(self.__upi[-1], self.__pwm_max), self.__pwm_min))
        
        print(self.__e[-1],self.__upi[-1], self.__pwm[-1] )

        return self.__pwm[-1]
    
    def sleep(self):
        time.sleep(self.__Tp)
        
    def getTime(self):
        return self.__t
    
    def getPWM(self):
        return self.__pwm
    
    def getD(self):
        return self.__d
    
    def getN(self):
        return self.__n
    
    
    