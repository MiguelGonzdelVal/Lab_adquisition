import socket
import struct
conexion = socket.socket()
conexion.connect(('10.0.0.55',51972))

def toma_dato(conexion):
        msg=conexion.recvfrom(32)[0]
        #print(struct.unpack('HH4xQLLLL',msg))
        canales=[]
        for channel in range(1,9):
            msg =conexion.recvfrom(2)[0]
            canales.append(int(struct.unpack('H',msg[:2])[0]))
            #print(f'channel {channel} {canales[-1]}')
        msg =conexion.recvfrom(16)[0]
        datos=[]
        for canal in canales:
            
            msg =conexion.recvfrom(8*canal)[0]
            datos.append(struct.unpack(f'{canal}d',msg))
        
        return datos[:4]
        
        '''
        t_actual=float(struct.unpack('I',msg[16:20])[0])+1e-9*float(struct.unpack('I',msg[20:24])[0])
        
        canales=list(struct.unpack('HHHHHHHHHHHHHHHH',msg[24:56]))
        print(t_actual,canales)
        ultimo_dato=56
        picos=[]
        for canal in canales:
            if canal>0:
                picos.append(struct.unpack(f'{canal}d',msg[ultimo_dato:ultimo_dato+canal*8]))
                print(picos[-1])
                ultimo_dato=ultimo_dato+canal*8

        '''
def DAQ_peaks():
    while True:
        toma_dato(conexion)
        time.sleep(0.05)
for i in range(10):print(toma_dato(conexion))

conexion.close()
