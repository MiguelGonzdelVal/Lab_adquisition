from dispositivo.Device_obj import Device
import socket
import time
import numpy as np
from pandas import read_excel
from io import StringIO
from multiprocessing import Process
import socket
import pickle

class MGCPlus(Device):
    
    def __init__(self,device_ID,address,server_port,active_channels,active_subchannels):
        """Class of the MGCPlus device. It returns the current data for the preselected channels and subchannels.

        Args:
            device_ID (int): ID of the Device
            address (str): IP address where is connected the MGCPLus
            server_port (int): Server port of the device. Normally 7
            active_channels (list): Channels that are active
            active_subchannels (list): subchannes that are active
        """        
        
        super().__init__(device_ID)
        print('ejecutando')
        self.sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address= (address,server_port)
        self.sock.connect(server_address)
        self.Port_number = 50000
        print('conexion realizada')
        #le comunico al MGCplus que los canales estan activos:
        message=self.configurar_mensaje_canal(active_channels)
        self.sock.sendall(message)
        data=self.sock.recv(16)
        print('channels received',data)
        
        message=self.configurar_mensaje_subcanal(active_subchannels)
        self.sock.sendall(message)
        data=self.sock.recv(16)
        print('subchannels received',data)
        tabla_sensores = read_excel(r".\configurations\Sensors MGCPlus\sensor configurations.xlsx",
                                    engine='openpyxl')
        print(tabla_sensores)
        self.encabezado = []
        for canal in active_channels:
            canal_estudiado = tabla_sensores[tabla_sensores.Channel == canal]
            for subcanal in active_subchannels:
                if subcanal in set(canal_estudiado['Subchannel'].values):
                    
                    self.encabezado.append(canal_estudiado[canal_estudiado.Subchannel==subcanal]['Name'].values[0])
        self.envio_datos=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        
        
    def configurar_mensaje_canal(self,active_channels):
        """Sends the message in order to activate the channels specified by the user

        Args:
            active_channels (list):  channels specified by the user

        Returns:
            str(bynary): the message that is sent to the MGCPlus in order to activate the channels
        """        
        mensaje = 'PCS'
        for ch in active_channels:mensaje+=str(ch)+','
        mensaje=mensaje[:-1]+'\n'
        return mensaje.encode('ascii')
    def configurar_mensaje_subcanal(self,active_subchannels):
        """Sends the message in order to activate the subchannels specified by the user

        Args:
            active_subchannels (list):  subchannels specified by the user

        Returns:
            str(bynary): the message that is sent to the MGCPlus in order to activate the subchannels
        """
        mensaje = 'SPS'
        for ch in active_subchannels:mensaje+=str(ch)+','
        mensaje=mensaje[:-1]+'\n'
        return mensaje.encode('ascii')
    def lectura_dato(self):
        """reads a sample of the MGCplus of the activated subchannels. It asks for a data and returns a list with all the data

        Returns:
            list: list with the data that was asked to the MGCplus
        """  
              
        message=b'TEX44\n'
        self.sock.sendall(message)
        data=self.sock.recv(16)
        message=b'MVF1250\n'
        self.sock.sendall(message)
        data=self.sock.recv(16)
        message=b'RMV?214\n'
        self.sock.sendall(message)
        data=self.sock.recv(1024)
        
        dato=np.loadtxt(StringIO(data.decode().replace(',','\t')))
        return [dato[i] for i in range(0,len(dato),3)]
        
        
    def DAQ(self,q):
        """
        Creates a loop that is always 
        asking for data to the MGCplus

        """        
        Medidas = {}
        for variable in self.encabezado: Medidas.update({variable:0})
        while True:
            
            self.current_data=self.lectura_dato()
            
            for n_variable,dato in enumerate(self.current_data):
                Medidas[self.encabezado[n_variable]]= dato
            q.put(Medidas)
                
                

            
            
            
