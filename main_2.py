from dispositivo.mgcplus_obj import *
import threading
import pandas as pd
Address_ID=1
   
MGC=pd.read_csv('.\\configurations\\MGC_plus.txt',sep=';')
server_address=MGC.Valor.values[0]
server_port=int(MGC.Valor.values[1])
active_channels=[int(ch) for ch in MGC.Valor.values[2].split(',')]
active_subchannels=[int(ch) for ch in MGC.Valor.values[3].split(',')]
print(server_address,server_port,active_channels,active_subchannels,MGC.Valor.values[3].split(','))
objeto=MGCPlus(Address_ID,server_address,server_port,active_channels,active_subchannels)
