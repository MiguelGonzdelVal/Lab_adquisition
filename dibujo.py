#### script solo dedicado al dibujo 

import serial
import time
import numpy as np

from datetime import datetime
import socket
import matplotlib
matplotlib.use('tkagg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
from io import StringIO
import pickle



s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 12345))
s.listen()
conn, addr = s.accept()
print(f"Connected by {addr}")    



fig,ax = plt.subplots(nrows=2,sharex=True)
datos=[]
def leer_archivos():
	global datos
	
	while True:
		data = conn.recv(1024)
		datos=pickle.loads(data)
		print(datos)
		
		
hilo=threading.Thread(target=leer_archivos).start()
DATA=[list()]
def animation_function(i):
    global datos,fig,DATA
    
    
    print(DATA)
    if len(datos)>1:
        DATA[0].append(datetime.now())
        if len(DATA[0])==1:
            for _ in datos:DATA.append([])
        for j in range(len(datos)):DATA[j+1].append(datos[j])
        ax[0].clear()
        
            
        ax[0].set_xlabel('datetime')
        ax[0].set_ylabel('T(ºC)')
        ax[0].plot(DATA[0],DATA[11])
        ax[0].plot(DATA[0],DATA[15])
        ax[1].clear()
        ax[1].set_xlabel('datetime')
        ax[1].set_ylabel('Pressure')
        ax[1].plot(DATA[0],DATA[2])
        


  
animation = FuncAnimation(fig,func = animation_function,interval = 1000)
plt.show()
