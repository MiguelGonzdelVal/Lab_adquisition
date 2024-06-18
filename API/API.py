'''
Archivo Python de un programa creado desde cero a partir del programa de Frank
INTA Miguel Gonzalez del Val
gonzalezvm@inta.es

'''

import subprocess
import threading
import tkinter as tk
from tkinter import ttk

import time
import datetime
import random
#from time import time
# from datetime import datetime
#  from scipy.integrate import simps, 
import serial

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import __main__
import matplotlib.animation as animation


class main_window(tk.Tk):

    def __init__(self,variables_medida,t_s,file_name):
        self.hilo = False
        self.temperatura = str(time.time())   
        self.parar=False
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Temperature control App")
        self.variables_medida = variables_medida
        self.fig,self.ax=plt.subplots(figsize=(4,4),nrows=1,sharex=True)
        self.ax=[self.ax]

        self.valor=[[]]
        self.time =[[]]
        self.recording = tk.BooleanVar()
        self.recording.set(False)
        self.file_name = file_name
        self.sampling_time = tk.StringVar()
        self.sampling_time.set(str(t_s))
        
        self.n_plots = tk.IntVar()
        self.n_plots.set(1)
        

        self.var_dibujo = {}
        for key in self.variables_medida:
            self.var_dibujo[key] = tk.IntVar()
        self.t_s = t_s
        self.check_box = ttk.Checkbutton(self,text='Recording',variable=self.recording).grid(row=0,column=0)
        tk.Label(text='sampling time').grid(row=0,column=1)
        self.entrada_tiempo = tk.Entry(self,textvariable=self.sampling_time).grid(row=0,column=2)
        self.boton_sampling = tk.Button(self,text='sampling fix',command=lambda:self.sampling_fix() ).grid(row=0,column=3)
        
        tk.Label(text='number plots').grid(row=0,column=4)
        self.entrada_n_plots = tk.Entry(self,textvariable=self.n_plots).grid(row=0,column=5)
         #create_thread graph
        self.boton_n_plots = tk.Button(self,text='update_graph',command=lambda:self.update_fig()).grid(row=0,column=6)
        
        

        self.file_name_var = tk.StringVar(self,value=self.file_name)
        tk.Label(text='file name').grid(row=1,column=4)
        self.entrada_file_name = tk.Entry(self,textvariable=self.file_name_var).grid(row=1,column=5)

        self.boton_file_name = tk.Button(self,text='change loc',command=lambda:self.update_filename() ).grid(row=1,column=6)
        self.variables_dibujadas=[]
        # self.hilo_graficar.join()
        self.subventana = subventana(self,width=500,height=500).grid(row=3,column=0)
        # self.ploteo = ploteo(self,width=500,height=500).grid(row=3,column=2)
        #self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        #self.canvas.get_tk_widget().grid(row=3,column=2)
        #self.ani = animation.FuncAnimation(self.fig, self.update_data, interval=1000, cache_frame_data=False)

        
    def update_data(self,j):
        for i in range(len(self.variables_dibujadas)):
            self.valor[i].append(self.variables_medida[self.variables_dibujadas[i]])
            self.time[i].append(self.variables_medida['datetime'])
            #print(self.valor,self.time)
            self.ax[i].clear()      
            self.ax[i].plot(self.time[i],self.valor[i])      

    def reset(self):
        print('cambiando')
        
        self.valor=[[] for _ in self.ax]
        self.time=[[] for _ in self.ax]
    def sampling_fix(self):
        try:
            self.t_s = float(self.sampling_time.get())
        except Exception as e:print(e)
    def update_fig(self):
        self.parar = True
        def asignar_valores():
            self.variables_dibujadas = [a.get() for a in self.combolist]
            print(self.variables_dibujadas )
        
        self.new_window = tk.Toplevel(self)
        elementos_lista_desplegable= list(self.variables_medida.keys())
        
        self.combo_opcions = [tk.StringVar() for _ in range(self.n_plots.get())]
        self.combolist = [ttk.Combobox(self.new_window,values= elementos_lista_desplegable,textvariable=self.combo_opcions[_]) for _ in range(self.n_plots.get())]
        for plot in range(self.n_plots.get()):
            self.combolist[plot].pack()
        boton = tk.Button(self.new_window,command=lambda:asignar_valores(),text='asignar').pack()
        self.fig,self.ax=plt.subplots(figsize=(4,4),nrows=self.n_plots.get(),sharex=True)

        if self.n_plots.get()==1:
            self.ax=[self.ax]


        self.valor=[[] for _ in self.ax]
        self.time=[[] for _ in self.ax]
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.new_window)
        self.canvas.get_tk_widget().pack()
        self.ani = animation.FuncAnimation(self.fig, self.update_data, interval=1000, cache_frame_data=False)
        
        self.new_window.mainloop()
        
        # self.hilo_graficar.append(threading.Thread(target=self.update_fig,daemon=True))
       

        
    
    def update_filename(self):
        self.file_name=self.file_name_var.get() 
        with open(self.file_name,'w') as f:
            for var in self.variables_medida:
                f.write(f'{var},')
            f.write('\n')   


class subventana(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent)
        row = 0   
        self.entradas =[] 
        self.variables_medida=parent.variables_medida
        for n_variable, valor in parent.variables_medida.items():
                    
                    
            
            
            # self.entradas.append(tk.Entry(self,textvariable=self.variables[-1]))
            self.entradas.append(tk.Label(self,text=f'{n_variable}\n{valor}'))
            self.entradas[-1].grid(row=row,column=1)
            row += 1
        self.update_time()

    def update_time(self):
        row = 0   
              
        for n_variable, valor in self.variables_medida.items():
                    
                    
            
            
            # self.entradas.append(tk.Entry(self,textvariable=self.variables[-1]))
            self.entradas[row].config(text=f'{n_variable}\n{valor}')
            self.entradas[row].grid(row=row,column=1)
            row += 1  
        self.after(1000,self.update_time)
            
class ploteo(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent)
        row = 0   
        self.entradas =[] 
        self.fig=plt.figure(figsize=(4,4))
        self.ax=[]
        
        self.variables_medida=parent.variables_medida
        self.variables_dibujadas=parent.variables_dibujadas
        self.valor = parent.valor
        self.time = parent.time
        self.update_time()

    def update_time(self):
        if len(self.variables_dibujadas)!=len(self.ax):
            self.fig,self.ax=plt.subplots(figsize=(4,4),nrows=len(self.variables_dibujadas),sharex=True)
            if len(self.variables_dibujadas)==1:self.ax=[self.ax]
        for i in range(len(self.ax)):
            self.valor[i].append(self.variables_medida[self.variables_dibujadas[i]])
            self.time[i].append(self.variables_medida[self.variables_dibujadas[0]])
            print(self.ax)
            self.ax[i].plot(self.time[i],self.valor[i])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=3,column=2)
        self.after(1000,self.update_time)   









