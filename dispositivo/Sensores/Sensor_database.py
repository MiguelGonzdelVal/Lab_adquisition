import json
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
def conversion(linea):
    out = {}
    
    out['time']=linea[0]
    canales = np.array(linea[1:5],dtype=int)
    campo=5
    for n_canal,peaks_canal in enumerate(canales,1):
        out[n_canal]=np.array(linea[campo:campo+peaks_canal],dtype=float)
        campo+=peaks_canal
    return out

class sensor(object):
    def __init__(self,channel,wavelength_inf,wavelength_sup):
        self.channel =channel
        self.wavelength_inf = wavelength_inf
        self.wavelength_sup = wavelength_sup
        self._FBG =np.nan
        self._FBG_0 = np.nan
    @property
    def FBG(self):
        return self._FBG
    @FBG.setter
    def FBG(self,line):
        
        
        peaks = line[self.channel]
        picos = peaks[np.where((peaks>self.wavelength_inf )&(peaks<self.wavelength_sup))]
        if picos.size:
            self._FBG = picos[0]
        else:self._FBG = np.nan

    
    @property
    def FBG_0(self):
        return self._FBG_0
    @FBG_0.setter
    def FBG_0(self,lambda_B):
        self._FBG_0 = lambda_B
      
       
    


class sensor_temperature(sensor):
    def __init__(self, channel:int,wavelength_inf:float, wavelength_sup:float,ctes_calibracion:tuple):
        super().__init__(channel,wavelength_inf, wavelength_sup)
        self._T=np.nan
        self.A,self.B,self.C,self.D = ctes_calibracion

    @property
    def T(self):
      
        self._T = self.A*self.FBG**3 + self.B*self.FBG**2 + self.C*self.FBG + self.D
        return self._T

class sensor_deformacion(sensor):
    def __init__(self, channel:int,wavelength_inf:float, wavelength_sup:float,sensor_temp:sensor_temperature,linea:dict):
        """_summary_

        Args:
            channel (int): _description_
            wavelength_inf (float): _description_
            wavelength_sup (float): _description_
            sensor_temp (sensor_temperature): _description_
            linea (list): _description_
        """        
        super().__init__(channel,wavelength_inf, wavelength_sup)
        self._T=np.nan
        
        self.FBG = linea
        self.FBG_0 = self.FBG
        self._epsilon=0
        self.F_g=0.78
        

    @property
    def epsilon(self):
        self._epsilon =1/0.78*(self.FBG-self.FBG_0)/self.FBG_0*1e6
        return self._epsilon


    
    
        
sensores={}


if __name__=='__main__':
    with open('datos_ej.txt','r') as f:
        lineas= f.readlines()
    df = pd.read_csv(r'CTO4_RT.txt',header=None)
    df.plot(x=0,y=1)
    plt.show()
    linea =conversion(lineas[0])
    
    # A1 = sensor_temperature(1,1539,1544,(0,0,2,0))
    # A1.FBG=linea
    A1 = False
    Tabla_sensores = pd.read_excel('tabla sensores.ods',sheet_name='Sensores_deformacion',engine="odf")

    print(Tabla_sensores.columns)
    for indice in Tabla_sensores.index:
        nombre= Tabla_sensores['Nombre Sensor'].loc[indice]
        l_inf= Tabla_sensores['lambda INF'].loc[indice]
        l_sup = Tabla_sensores['Lambda_sup'].loc[indice]
        thermal = bool(Tabla_sensores['Referencia temperatura(sensor termico)'].loc[indice])
        canal = Tabla_sensores['Canal'].loc[indice]
        if not thermal:
            pass
        
        sensores[nombre]= sensor_deformacion(canal,l_inf,l_sup,thermal,linea)

    
    plt.figure()
    DATA={}
    for sensor in sensores: 
        DATA.update({sensor:[]})

    for linea in lineas:
        linea = conversion(linea)
        data = []
        for sensor_name in sensores:
            sensores[sensor_name].FBG=linea
            data.append(sensores[sensor_name].epsilon)
            DATA[sensor_name].append(data)
    for sensor_data in DATA.values():
        plt.plot(sensor_data)

    plt.show()
    
    
    


# def sensor_def(channel,lambda_inf,lambda_sup):

