from dispositivo.Device_obj import Device
import serial
import time
import pickle
import socket
class Lakeshore_218(Device):
    def __init__(self,device_ID,baudrate,COM_port,canales_medicion,tipos_sensor):
        super().__init__(device_ID)
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate #9600
        self.ser.timeout = 15  # 15 sec.
        self.ser.parity = serial.PARITY_ODD
        self.ser.bytesize = 7
        self.ser.stopbits = 1
        self.ser.port = COM_port
        # self.ser.open()
        self.canales_medicion=canales_medicion
        self.encabezado= [f'LAKE_T_{ch}' for ch in self.canales_medicion]
        self.Port_number = 50001
        self.envio_datos=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        if len(canales_medicion)>len(tipos_sensor):
            print('Canales de medicion no asignados')     
            
        
    
    def lectura_canal(self,canal):
        self.ser.flushInput()
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
    
    def DAQ(self,q):
        self.ser.open()
        Medidas = {}
        for variable in self.encabezado: Medidas.update({variable:0})
        while True:
            # mensaje =b'hola'
            # self.envio_datos.sendto(mensaje,('localhost',50001))
            try:
                self.current_data=self.lectura_dato()
                for n_variable,dato in enumerate(self.current_data):
                    Medidas[self.encabezado[n_variable]]= dato
                q.put(Medidas)
            except Exception as e:
                print('Error Lakeshore 218',e)
            
            

        while True:
            
            self.current_data=self.lectura_dato()
            
            