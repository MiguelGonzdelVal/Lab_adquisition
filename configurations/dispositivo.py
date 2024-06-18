#Defino una instancia padre que se llame Dispositivo
import numpy as np
from io import StringIO
import time
import serial
import hyperion
import pandas as pd
import socket
class Device(object):
    def __init__(self, device_ID):
        """Generate a parent class for all devices

        Args:
            device_ID (int): ID of the device so it can be cathegorized
        """        
        self.device_ID=device_ID
        self.current_data=None
    def get_data(self):
        """A function that returns the current data.

        Returns:
            list: list of all the data asked by the user
        """        
        return self.current_data


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
        self.sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address= (address,server_port)
        self.sock.connect(server_address)
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
        
        
    def DAQ(self):
        """Creates a loop that is always asking for data to the MGCplus
        """        
        
        while True:
            try:
                self.current_data=self.lectura_dato()
            except Exception as e:print(e)
            
            time.sleep(.1)

    
        
class Lakeshore_218(Device):
    def __init__(self,device_ID,baudrate,COM_port,canales_medicion,tipos_sensor):
        super().__init__(device_ID)
        ser = serial.Serial()
        ser.baudrate = baudrate #9600
        ser.timeout = 15  # 15 sec.
        ser.parity = serial.PARITY_ODD
        ser.bytesize = 7
        ser.stopbits = 1
        ser.port = COM_port
        self.ser=ser
        self.ser.open()
        self.canales_medicion=canales_medicion
        
        if len(canales_medicion)>len(tipos_sensor):
            print('Canales de medicion no asignados')     
            
        
    
    def lectura_canal(self,canal):
        self.ser.flushInput()
        respuesta=False
        mensaje =f'KRDG?{canal}\r\n'
        mensaje=mensaje.encode(encoding='UTF-8')
        while True:
            self.ser.write(mensaje)
            d = self.ser.read(7).decode(encoding='UTF-8')
            print
            if d[0]=='+':
                try:
                    d=float(d)
                    break
                except Exception as e:
                    print(e)
                    pass
                
            else:time.sleep(0.1)
        return d

    def lectura_dato(self):
        out=[]

        for canal in self.canales_medicion:
            
            out+= [self.lectura_canal(canal) ]
            time.sleep(0.5)
        return out
    
    def DAQ(self):
        
        while True:
            try:
                self.current_data=self.lectura_dato()
            except Exception as e:
                print('Error Lakeshore 218',e)
            
            time.sleep(.1)

class LUNA_Si155(Device):
    
    #aplicacion para bajas frecuencias. Altas frecuencias hay que hacerlo ad hoc
    def __init__(self,device_ID,address,active_channels,spectrum_ad):
        super().__init__(device_ID)
        self.h1 = hyperion.Hyperion(address)
        self.active_channels=active_channels
        #self.set_reference_wavelengths()
        self.spectrum_ad=spectrum_ad
        self.expected_peaks=expected_peaks
        #self.sensor_definition()
        self.canales=['A','B','C','D']
        self.peak_definition()
        self.sensor_definition()
        
        
    
    def set_reference_wavelengths(self):
        self.lambda_0= {}
        canales=['A','B','C','D']
        for canal in self.active_channels:
            picos=self.h1.peaks[canal]
            expected_peaks=self.expected_peaks[canal-1]
            for i in range(expected_peaks):
                if i<len(picos):
                    fbg=picos[i]
                    
                else:fbg=np.nan
                self.lambda_0.update({f'FBG_{canales[canal-1]}{i+1}_0':fbg})
                exec(f'self.FBG_{canales[canal-1]}{i+1}_0=fbg')
            
                

    def sensor_definition(self):
        self.sensor_db=pd.read_csv('sensores_Fibra.txt')
        self.sensor_db.index=self.sensor_db.Sensor_name
        
        
    def get_peak_values(self):
        designacion_canales=['A','B','C','D']
        self.picos=[]
        for canal in self.active_channels:
            picos=self.h1.peaks[canal]
            for grating in self.Peaks_DB.index:
                sup=self.Peaks_DB['Sup_limit'].loc[grating]
                inf=self.Peaks_DB['Inf_limit'].loc[grating]
                FBG_pos = np.where((sup >= picos) & (inf <=picos))
                
                if len(FBG_pos[0])>0:
                    self.Peaks_DB['Valor_actual'].loc[grating]=picos[FBG_pos[0][0]]
                else:self.Peaks_DB['Valor_actual'].loc[grating]=np.nan

                if len(FBG_pos[0])>1:self.Peaks_DB['Valor_actual_2'].loc[grating]=picos[FBG_pos[0][1]]
                
            
                
    def get_sensor_values(self):
        
        for sensor in self.Sensors_DB.index:
            FBG=self.Sensors_DB['FBG_associated'].loc[sensor]
            equ_type=self.Sensors_DB['equation_type'].loc[sensor]
            parameters=self.Sensors_DB[['A','B','C','D']].loc[sensor].values
            if self.Sensors_DB['Variation_reference'].loc[sensor]: 
                fbg_value=self.Peaks_DB['Valor_actual'].loc[FBG]-self.Peaks_DB['Valor_referencia'].loc[FBG]
            else:fbg_value=self.Peaks_DB['Valor_actual'].loc[FBG]
            
            self.sensor_values[sensor]=self.regression(equ_type,fbg_value,parameters)
            

    def peak_definition(self):
        '''
        esta funcion importa los picos de un archivo
        '''
        self.Peaks_DB=pd.read_csv('.//configurations//SI155//Current FBGS.txt')
        self.Peaks_DB.index=self.Peaks_DB.FBG_NAME.values
        self.Peaks_DB['Valor_actual']=[np.nan for _ in self.Peaks_DB.index]
        self.Peaks_DB['Valor_actual_2']=[np.nan for _ in self.Peaks_DB.index]
        self.get_peak_values()
        self.Peaks_DB['Valor_referencia']=self.Peaks_DB['Valor_actual']
        

    def sensor_definition(self):
        '''
        esta funcion importa los picos de un archivo
        '''
        self.Sensors_DB=pd.read_csv('.//configurations//SI155//Current sensors.txt')
        self.Sensors_DB.index=self.Sensors_DB.Sensor_name.values
        self.sensor_values={}
        for sensor in self.Sensors_DB.index:
            self.sensor_values.update({sensor:np.nan})
        
        
    def automatic_FBG_setting(self):
        texto='FBG_NAME,CHANNEL,Inf_limit,Sup_limit\n'
        for canal in self.active_channels:
            
            peaks=self.h1.peaks[canal]
            print(peaks)
            channel_name=self.canales[canal-1]
            if len(peaks)>0:
                texto+=f'FBG_{channel_name}1,{canal},1500,'
                
                    
                if len(peaks)>1:
                    for i in range(1,len(peaks)):
                        sup=(peaks[i-1]+peaks[i])/2
                        inf=sup+1e-4
                        texto+=f'{sup:.4f}\nFBG_{channel_name}{i+1},{canal},{inf:.4f},'
                texto+='1600\n'
        print(texto)

    def regression(self,equation,x,parameters):
        if equation=='linear':
            return self.lineal(x,parameters)
        if equation=='cubic':
            return self.cubic(x,parameters)
        
    def lineal(self,x,parameters):
        return parameters[0]*x+parameters[1]
    def cubic(self,x,parameters):
        return parameters[0]*x**3+parameters[1]*x**2+parameters[2]*x+parameters[3]
        
class Pressure(Device):
    def __init__(self,device_ID,baudrate,COM_port,tipos_sensor):
        super().__init__(device_ID)
        self.serial_port = serial.Serial(COM_port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        self.serial_port.timeout=5
        
        self.data_bytes=self._message()
                
    def _message(self):
        ascii_codes = [49, 50, 50, 48, 48]+ [55, 52, 48]+ [48, 50, 61, 63]
        data_bytes = bytes(ascii_codes)+self.checksum(ascii_codes)+bytes([13])
        return data_bytes
        
    def lectura_dato(self):
        self.serial_port.flushInput()
        print(self.data_bytes)
        self.serial_port.write(self.data_bytes)
        palabra=''
        presion=0
        contador=0
        while True:
            caracter=self.serial_port.read()
            contador+=1
            if caracter!=b'\xff':
                try:
                    caracter=caracter.decode(encoding='ascii')
                except:
                    palabra=''
                    break
                    print('waiting',palabra)
                    pass
            else:
                continue
                print(caracter)
         
            if caracter=='\r':
                try:
                    presion = self.procesado_palabra(palabra)
                except Exception as e:print(e)
                break
            else:
                if isinstance(caracter,str):palabra+=caracter
            if contador ==50:
                presion=0
                break
                
        #print(palabra)
            
        return presion
    def checksum(self,data):
        dato=str(sum(data)%256)
        while len(dato)<3:
            dato='0'+dato
        return dato.encode(encoding='ascii')
    def convesion_float(self,dato):
        
        presion_numeros = int(dato[0:4])/1000
        exponente=int(dato[4:])-20
        return presion_numeros*10**exponente   
    
             
    def procesado_palabra(self,palabra):
        presion = 'nan'
        #print(palabra[-9:-3])
        if int(palabra[-11:-9])==6:
            presion = self.convesion_float(palabra[-9:-3])
        if presion!='nan':
            return presion
        else:return 0
        
    def DAQ(self):
        
        while True:
            try:
                self.current_data=[self.lectura_dato()]
            except Exception as e:
                print('Error VACUMM Sensor',e)
            
            time.sleep(.1)
    
        
        

    
