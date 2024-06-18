from dispositivo.Device_obj import *
import hyperion
import socket
import struct
import threading
import asyncio
from dispositivo.Sensores.Sensor_database import *
class LUNA_Si155(Device):
    
    #aplicacion para bajas frecuencias. Altas frecuencias hay que hacerlo ad hoc
    def __init__(self,device_ID,address,active_channels,spectrum_ad,adq_FBG,streaming):
        super().__init__(device_ID)
        self.h1 = hyperion.Hyperion(address)
        self.active_channels=active_channels
        #self.set_reference_wavelengths()
        self.spectrum_ad=spectrum_ad
        #self.expected_peaks=expected_peaks
        #self.sensor_definition()
        self.canales=['A','B','C','D']
        self.conexion = socket.socket()
        self.adq_FBG = adq_FBG
        self.streaming = streaming
        self.encabezado = [f'CH_{i+1}' for i in range(4)]
        
        

    def DAQ(self,q):
        """Creates a loop that is always asking for data to the Si155

        """        
        n=10
        texto=''
        Medidas = {}
        for variable in self.encabezado: Medidas.update({variable:0})
        
        while True:
                
            self.current_data=[]
            self.peak =self.h1.peaks()
            
            linea = conversion(self.peaks)
            if self.streaming:
                texto += str(self.peaks)[1:-1]+'\n'
                n-=1
                if not n:
                    with open(self.file_name_streaming,'a') as f:f.write(texto)
                    n=10
                    texto = ''
            for sensor_name in self.sensores:
                
                objeto = self.sensores[sensor_name]
                objeto.FBG=linea
                self.current_data+=[objeto.epsilon]
            if self.adq_FBG:
                for sensor_object in self.sensores.values():
                    self.current_data+=[objeto.FBG]
            
            for n_variable,dato in enumerate(self.current_data):
                Medidas[self.encabezado[n_variable]]= dato
            q.put(Medidas)

    def define_sensors(self):
        df = pd. read_excel('tabla sensores.ods')
        Tabla_sensores = pd.read_excel('tabla sensores.ods',sheet_name='Sensores_deformacion',engine="odf")
        self.sensores={}
        
        for indice in Tabla_sensores.index:
            nombre= Tabla_sensores['Nombre Sensor'].loc[indice]
            l_inf= Tabla_sensores['lambda INF'].loc[indice]
            l_sup = Tabla_sensores['Lambda_sup'].loc[indice]
            thermal = bool(Tabla_sensores['Referencia temperatura(sensor termico)'].loc[indice])
            canal = Tabla_sensores['Canal'].loc[indice]
            if not thermal:
                pass
            
            self.sensores[nombre]= sensor_deformacion(canal,l_inf,l_sup,thermal,conversion(self.peaks))
            print(self.sensores)
