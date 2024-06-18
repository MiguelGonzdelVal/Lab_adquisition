'''
Programacion del Widget
copyright INTA
Miguel González del Val

'''


import sys
import numpy
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.widgets import CheckButtons
import threading
import time

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=30, height=40,nrows=1,ncols=1):
        fig,self.ax = plt.subplots(figsize=(width, height),nrows=nrows,ncols=ncols,)
        if nrows==1:
            self.ax = [self.ax]
        self.nrows=nrows
        self.cols=ncols
        
        super(MplCanvas, self).__init__(fig)
        # self.check = CheckButtons(self.axes, ('2 Hz', '4 Hz'), (True, True))

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, entradas=dict, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        numero_graficas = len(entradas.keys())
        self.canvas = MplCanvas(self, width=50, height=40, nrows=numero_graficas,ncols=1)
        self.setCentralWidget(self.canvas)

        
        self.variables_dibujo = {}
        for entra in entradas: self.variables_dibujo[entra]=[[],[]] 
        
        self.update_plot()
        
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
    def update_data(self,channel,x,y):
        self.variables_dibujo[channel][0].append(x)
        self.variables_dibujo[channel][1].append(y)
        
    
    def update_plot(self):
        # Drop off the first y element, append a new one.
        #self.canvas.ax.cla()
        for eje , datos in zip(self.canvas.ax,self.variables_dibujo.values()):
            eje.plot(datos[0], datos[1], 'r')
                    
        self.canvas.draw()


