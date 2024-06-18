
import tkinter as tk
from tkinter import ttk
import pandas as pd
from dispositivo.Si155_obj import *
import widgets_plot
import threading
import time


class Application(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("SETUP")
        self.main_window = main_window
        self.MGC_value = tk.BooleanVar(self)
        self.MGCplus = ttk.Checkbutton(self, text="MGCPlus",variable=self.MGC_value)
        self.MGCplus.grid(row=0,column=0)

        self.Lakeshore_value = tk.BooleanVar(self)
        self.Lakeshore = ttk.Checkbutton(self, text="Lakeshore",variable=self.Lakeshore_value)
        self.Lakeshore.grid(row=1,column=0)

        self.Si155_value = tk.BooleanVar(self)
        self.Si155 = ttk.Checkbutton(self, text="LUNA SI155",variable=self.Si155_value)
        self.Si155.grid(row=2,column=0)

        self.Si155_FBG_value = tk.BooleanVar(self)
        self.Si155_FBG = ttk.Checkbutton(self, text="Include FBGS",variable=self.Si155_FBG_value)
        self.Si155_FBG.grid(row=2,column=2)
    

        self.Vaccum_value = tk.BooleanVar(self)
        self.Vaccum = ttk.Checkbutton(self, text="Vaccum sensor",variable=self.Vaccum_value)
        self.Vaccum.grid(row=3,column=0)

        self.MGCplus_conf=ttk.Button(self, text ="Config", command = lambda:self.emergente_guardar('.\\configurations\\MGC_plus.txt')).grid(row=0,column=4)
        self.Lakeshore218_conf=ttk.Button(self, text ="Config", command =lambda:self.emergente_guardar('.\\configurations\\Lakehore218.txt')).grid(row=1,column=4)
        self.Vaccum_conf=ttk.Button(self, text ="Config", command =lambda:self.emergente_guardar('.\\configurations\\pressure.txt')).grid(row=3,column=4)
        self.Si155_conf=ttk.Button(self, text ="Config", command =lambda:self.emergente_guardar_SI155()).grid(row=2,column=4) 


        self.Si155_streaming_value = tk.BooleanVar(self)
        self.Si155_streaming = ttk.Checkbutton(self, text="FBGS streaming",variable=self.Si155_streaming_value)
        self.Si155_streaming.grid(row=4)
        ttk.Label(self,text='Sampling_time').grid(row=5,column=0)
        self.tiempo_muestreo_value = tk.StringVar(self,'1')
        self.tiempo_muestreo_entry = tk.Entry(self,textvariable=self.tiempo_muestreo_value)
        self.tiempo_muestreo_entry.grid(row=5,column=4)      
        

        ttk.Label(self,text='rec_time').grid(row=7,column=0)
        self.tiempo_rec_value = tk.StringVar(self,'5')
        self.tiempo_rec_entry = tk.Entry(self,textvariable=self.tiempo_rec_value)
        self.tiempo_rec_entry.grid(row=7,column=4)      
        
        self.boton_salir=ttk.Button(self, text ="exit", 
                                    command =lambda:self.exit())
        self.boton_salir.grid(row=8)
        
        self.place(width=600, height=600)

        
        
        
    def emergente_guardar(self,a):

        #primero se leen las caracteristicas del MGCplus:
        MGC=pd.read_csv(a,sep=';')
        def guardar():
            for i in MGC.index:
                MGC['Valor'].loc[i]= entradas[i].get()
            print(MGC)
            MGC.to_csv(a,sep=';',index=False)

        ventana=tk.Tk()
        nombres=[]
        entradas=[]
        valores=[]
        valor=tk.StringVar()
        for i in MGC.index:
           nombres.append(ttk.Label(ventana, text=MGC.Variable.loc[i]).grid(row=i,column=0))
           valor.set(str(MGC.Valor.loc[i]))
           actual=str(MGC['Valor'].loc[i])
           valores.append(tk.StringVar())
           #
           entradas.append(ttk.Entry(ventana,textvariable=valores[-1]))
           entradas[-1].grid(row=i,column=1)
           entradas[-1].insert(0,actual)
           
        ttk.Button(ventana,command=guardar,text='Save').grid(column=3)
        ventana.mainloop()


    def emergente_guardar_SI155(self):

        si155=pd.read_csv(r".\configurations\Si155.txt",sep=';')
        def guardar():
            for i in si155.index:
                si155['Valor'].loc[i]= entradas[i].get()
            print(si155)
            si155.to_csv(r".\configurations\Si155.txt",sep=';',index=False)
        def peak_conf(comando):
            import os
            osCommandString = 'notepad.exe '+comando
            os.system(osCommandString)
        ventana=tk.Tk()
        nombres=[]
        entradas=[]
        valores=[]
        valor=tk.StringVar()
        for i in si155.index:
           nombres.append(ttk.Label(ventana, text=si155.Variable.loc[i]).grid(row=i,column=0))
           valor.set(str(si155.Valor.loc[i]))
           actual=str(si155['Valor'].loc[i])
           valores.append(tk.StringVar())
           #
           entradas.append(ttk.Entry(ventana,textvariable=valores[-1]))
           entradas[-1].grid(row=i,column=1)
           entradas[-1].insert(0,actual)
           
        ttk.Button(ventana,command=guardar,text='Save').grid(column=3)
        ttk.Button(ventana,command=lambda:peak_conf('"./configurations/SI155/Current FBGS.txt"'),text='Peak_config').grid(row=i+1)
        ttk.Button(ventana,command=lambda:self.auto_conf(),text='Autopeak config').grid(row=i+2)
        
        ventana.mainloop()
        
    def auto_conf(self):
        
        objeto=LUNA_Si155(3,'10.0.0.55',[1,2,3,4],False)
        texto=objeto.automatic_FBG_setting()
        file=open(r".\configurations\SI155\Current FBGS.txt",'w')
        file.write(texto);file.close()
    def exit(self):
        self.destroy()
        self.quit()
        
        
        


    
    
        
class Ventana_parada(object):
    def __init__(self,ventana):
        import tkinter as tk
        print('pulsar rec para comenzar')
        self.grabar=False
        
    def ejecutar(self):
        
        ventana=tk.Tk()
        boton_parada=ttk.Button(ventana, text ="STOP", command = lambda:self.stop()).grid(row=0,column=0)
        boton_rec=ttk.Button(ventana, text ="REC", command = lambda:self.rec()).grid(row=0,column=1)
        
        ventana.mainloop()
    def rec(self):
        self.grabar=True
    def stop(self):
        self.grabar=False


        
    
class Ventana_ploteo(object):
    def __init__(self,variables):
        import tkinter as tk
        print('pulsar rec para comenzar')
        self.grabar=False
        self.variables=variables
        self.w = False
        self.campos_dibujo={}
        self.Exit=False
        self.muestra=[]
        
        print('pulsar rec para comenzar')
        self.grabar=False
    def rec(self):
        self.grabar=True
    def stop(self):
        self.grabar=False
        
    def plotear(self):
        
        if len(self.campos_dibujo.keys()):
            self.app = widgets_plot.QtWidgets.QApplication(widgets_plot.sys.argv)
            self.w = widgets_plot.MainWindow(self.campos_dibujo)
            
            self.app.exec_()
            
            
        

    def añadir(self):
        self.campos_dibujo[self.lista_desplegable.current()+1]  =  self.lista_desplegable.get()
        self.lst.insert(tk.END, self.campos_dibujo[self.lista_desplegable.current()+1] )
        print(self.campos_dibujo)
    def quit(self):
        import __main__
        self.ventana.quit()
        self.Exit=True


    def ejecutar(self):
        
        self.ventana=tk.Tk()
        self.ventana.attributes('-fullscreen',True)
        boton_parada=ttk.Button(self.ventana, text ="STOP", command = lambda:self.stop()).grid(row=0,column=0)
        boton_rec=ttk.Button(self.ventana, text ="REC", command = lambda:self.rec()).grid(row=0,column=1)
        lista= tk.StringVar(value= list(self.campos_dibujo.values()))
        self.lista_desplegable=ttk.Combobox(self.ventana)
        self.lista_desplegable['values']=self.variables
        self.lista_desplegable.grid(row=3,column=0)
        self.boton_add=ttk.Button(self.ventana, text ="ADD", command = lambda:self.añadir()).grid(row=1,column=0)
        self.boton_plot=ttk.Button(self.ventana, text ="PLOT", command = lambda:self.plotear()).grid(row=2,column=0)
        self.lst = tk.Listbox(self.ventana,listvariable=lista)
        self.lst.grid(row=4,column=0)
        self.boton_quit=ttk.Button(self.ventana, text ="Quit", command = lambda:self.quit()).grid(row=5,column=0)
        def data_table():
            for fila,v in enumerate(self.variables):
                tk.Label(text=str(v)).grid(row=fila, column=3)
                if len(self.muestra):
                    tk.Label(text=str(self.muestra[fila])).grid(row=fila, column=4)
                    tk.Label.after(1000,data_table)
        data_table()
        self.ventana.mainloop()
        
            
   

if __name__=='__main__':
    # threading.Thread(target=MainWindow).start()
    
    APP_PLOT=Ventana_ploteo(['disp'])
    threading.Thread(target=APP_PLOT.ejecutar).start()
    x= 1
    y=2
    while True:
        x+= 1
        y+=2
        if APP_PLOT.w!= False:
            APP_PLOT.w.update_data(1,x,y)
        time.sleep(1)


    

        
