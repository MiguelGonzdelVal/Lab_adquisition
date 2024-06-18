import asyncio
import time
import pickle
import socket
import datetime

class data_adquisition():
    def __init__(self,Objetos,file_name,q,t_s) -> None:
        
        Datos={'datetime':datetime.datetime.now()}
        for Objeto in Objetos:
            for variable in Objeto.encabezado:
                Datos[variable]=0
        
        self.Datos =Datos
        self.file_name = file_name
        self.q = q
        self.t_s =t_s
        
    def guardar_texto(self,texto):
        file = open(self.root.file_name,'a')
        file.write(texto)
        file.close()
    def procesar_texto(self,Datos):
        texto= f'{datetime.datetime.now()}'
        for D in Datos.values():
            texto+=f',{D}'
        texto+='\n'
        return texto
        
    def tomar_dato(self):
        global Datos
        t_anterior = 0
        n=0
        texto=''
        while True:
            
            ultimo_dato=dict()
            self.Datos['datetime']=datetime.datetime.now()
            while not self.q.empty():
                ultimo_dato = self.q.get()
                
                for variable, dato in ultimo_dato.items():
                    self.Datos[variable]=dato
                #self.Datos['datetime']=datetime.datetime.now()
            if self.root.recording.get():
                if time.time()-t_anterior>self.root.t_s:
                    texto+=self.procesar_texto(self.Datos)
                    n+=1
                    t_anterior=time.time()
                if n==2:
                    self.guardar_texto(texto)
                    n=0
                    texto=''
            
       
