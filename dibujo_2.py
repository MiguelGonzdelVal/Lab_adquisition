#### script solo dedicado al dibujo 

import serial
import time
import numpy as np
import hyperion
from datetime import datetime
import socket
import matplotlib
matplotlib.use('tkagg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from io import StringIO
import sys


if __name__ == '__main__':
	
	#print(sys.argv[1])
	h1 = hyperion.Hyperion('10.0.0.55')
	#h2 = hyperion.Hyperion('192.168.1.35')

	fig,ax = plt.subplots(ncols=2)
	file_name_1=f'.//spectrum data//{datetime.now()}_1.txt'.replace(':','_')
	file_name_2=f'.//spectrum data//{datetime.now()}_2.txt'.replace(':','_')
	file_names=(file_name_1,file_name_2)
	for file_name in file_names:
					with open(file_name,'w') as f:
							spectra = h1.spectra
							
							wavelengths = spectra.wavelengths
							f.write(f'lambda:{wavelengths}\n')
							f.write('channel,time,spectrum\n')
							spectra = h1.spectra
							
							
	def animation_function(i):
		global canales,fig
		for j in range(2):
			ax[j].clear()
			ax[j].set_xlabel('Wavelength (nm)')
			ax[j].set_ylabel('Amplitude (dBm)')
		h1.active_full_spectrum_channel_numbers = range(1, h1.channel_count + 1)
		spectra = h1.spectra
		wavelengths = spectra.wavelengths
		colores=['b','r','g','k']

		texto_1=''
		ahora_1=datetime.now()
		for channel in h1.active_full_spectrum_channel_numbers:
			ax[0].plot(wavelengths, spectra[channel],colores[channel-1] ,label = str(channel))
			texto_1+=f'\n{channel},{ahora_1}'
			for Lambda in spectra[channel]:texto_1+=f',{Lambda}'
		ax[0].legend()

		texto_2=''
				

		ax[1].legend()
		for interrogador,texto in enumerate((texto_1,texto_2)):
			texto+='\n\n'
			with open(file_names[interrogador],'a') as f:f.write(texto)
	
                
        
	
	
	
	


  
animation = FuncAnimation(fig,func = animation_function,interval = 3000)
plt.show()



