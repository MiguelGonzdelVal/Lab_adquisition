from dispositivo.mgcplus_obj import *
from dispositivo.Si155_obj import *
#from dispositivo.Lakeshore_obj import *
import threading
import time
from tkinter import filedialog
import tkinter as tk
import ventanas_confi
import config
from guardado import escritura_encabezado
from Muestreo import Muestreo
from multiprocessing import Pool,Manager,Process,Queue
import datetime
import API.DAQ
import API.API


if __name__ == '__main__':
    main_window = tk.Tk()
    # main_window.attributes('-fullscreen',True)
    app = ventanas_confi.Application(main_window)
    app.mainloop()

    Objetos,t_s,it_rec=config.set_up(app)
    
    
    archivo=filedialog.asksaveasfile(parent=main_window)
    main_window.destroy()
    main_window.mainloop()

    file_name = archivo.name
    
   
    Heading = escritura_encabezado(Objetos,file_name)
    
    with Manager() as manager:
        q = Queue()
       
        
        daq = API.DAQ.data_adquisition(Objetos,file_name,q,t_s)       
        lista_procesos = []
        
        for Objeto in Objetos:
            lista_procesos.append(Process(target=Objeto.DAQ,args=(q,),daemon=True))
            lista_procesos[-1].start()
        print('procesos corriendo')
        
        root = API.API.main_window(daq.Datos,t_s,file_name)
        daq.root= root

        threading.Thread(target=daq.tomar_dato,daemon=True).start()
        print('iniciado el DA thread')
        # root.update_time()
        root.mainloop()
      
    
                
            
     


