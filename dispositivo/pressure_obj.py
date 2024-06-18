from dispositivo.Device_obj import Device
import time
import serial
import numpy as np
class Pressure(Device):
    def __init__(self,device_ID,baudrate,COM_port,tipos_sensor):
        super().__init__(device_ID)
        self.serial_port = serial.Serial(COM_port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        self.serial_port.timeout=5
        self.encabezado = ['pressure(hPa)']
        
        self.data_bytes=self._message()
                
    def _message(self):
        ascii_codes = [49, 50, 50, 48, 48]+ [55, 52, 48]+ [48, 50, 61, 63]
        data_bytes = bytes(ascii_codes)+self.checksum(ascii_codes)+bytes([13])
        return data_bytes
        
    def lectura_dato(self):
        self.serial_port.flushInput()
        
        self.serial_port.write(self.data_bytes)
        palabra=''
        presion=np.nan
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
                presion=np.nan
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
