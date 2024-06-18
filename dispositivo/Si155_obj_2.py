from dispositivo.Device_obj import *
import hyperion
import socket
import struct
import threading
class LUNA_Si155(Device):
    
    #aplicacion para bajas frecuencias. Altas frecuencias hay que hacerlo ad hoc
    def __init__(self,device_ID,address,active_channels,spectrum_ad):
        super().__init__(device_ID)
        self.h1 = hyperion.Hyperion(address)
        self.active_channels=active_channels
        #self.set_reference_wavelengths()
        self.spectrum_ad=spectrum_ad
        #self.expected_peaks=expected_peaks
        #self.sensor_definition()
        self.canales=['A','B','C','D']
        self.conexion = socket.socket()
        self.conexion.connect((address,51972))
        self.peaks=self.toma_dato_peaks(self.conexion)
        self.peak_definition()
        self.sensor_definition()
        self.set_reference_wavelengths()
        hilo=threading.Thread(target=self.DAQ_peaks).start()
        
    
    def set_reference_wavelengths(self):
        self.peaks_0=self.toma_dato_peaks(self.conexion)
            
                

    def sensor_definition(self):
        self.sensor_db=pd.read_csv('sensores_Fibra.txt')
        self.sensor_db.index=self.sensor_db.Sensor_name
        
        
    def get_peak_values(self):
        designacion_canales=['A','B','C','D']
        self.picos=[]
        
        Values=[]
            
        for canal in self.active_channels:
            picos=self.peaks[canal-1]
            df_filt=self.Peaks_DB[self.Peaks_DB.CHANNEL==canal]
            for grating in df_filt.index:
                sup=self.Peaks_DB['Sup_limit'].loc[grating]
                inf=self.Peaks_DB['Inf_limit'].loc[grating]
                FBG_pos = np.where((sup >= picos) & (inf <=picos))
                
                if len(FBG_pos[0])>0:
                    Values.append(picos[FBG_pos[0][0]])
                    
                else:Values.append(np.nan)

                if len(FBG_pos[0])>1:self.Peaks_DB['Valor_actual_2'].loc[grating]=picos[FBG_pos[0][1]]
        
        self.Peaks_DB['Valor_actual']=Values
        
        
                
            
                
    def get_sensor_values(self):
        
        for sensor in self.Sensors_DB.index:
            FBG=self.Sensors_DB['FBG_associated'].loc[sensor]
            equ_type=self.Sensors_DB['equation_type'].loc[sensor]
            parameters=self.Sensors_DB[['A','B','C','D']].loc[sensor].values
            if self.Sensors_DB['Variation_reference'].loc[sensor]: 
                fbg_value=self.Peaks_DB['Valor_actual'].loc[FBG]-self.Peaks_DB['Valor_referencia'].loc[FBG]
            else:fbg_value=self.Peaks_DB['Valor_actual'].loc[FBG]
            
            self.sensor_values[sensor]=self.regression(equ_type,fbg_value,parameters)
            

    def peak_definition(self):
        '''
        esta funcion importa los picos de un archivo
        '''
        self.Peaks_DB=pd.read_csv('.//configurations//SI155//Current FBGS.txt')
        self.Peaks_DB.index=self.Peaks_DB.FBG_NAME.values
        self.Peaks_DB['Valor_actual']=[np.nan for _ in self.Peaks_DB.index]
        self.Peaks_DB['Valor_actual_2']=[np.nan for _ in self.Peaks_DB.index]
        self.get_peak_values()
        self.Peaks_DB['Valor_referencia']=self.Peaks_DB['Valor_actual']
        

    def sensor_definition(self):
        '''
        esta funcion importa los picos de un archivo
        '''
        self.Sensors_DB=pd.read_csv('.//configurations//SI155//Current sensors.txt')
        self.Sensors_DB.index=self.Sensors_DB.Sensor_name.values
        self.sensor_values={}
        for sensor in self.Sensors_DB.index:
            self.sensor_values.update({sensor:np.nan})
        
        
    def automatic_FBG_setting(self):
        texto='FBG_NAME,CHANNEL,Inf_limit,Sup_limit\n'
        for canal in self.active_channels:
            
            peaks=self.h1.peaks[canal]
            print(peaks)
            channel_name=self.canales[canal-1]
            if len(peaks)>0:
                texto+=f'FBG_{channel_name}1,{canal},1500,'
                
                    
                if len(peaks)>1:
                    for i in range(1,len(peaks)):
                        sup=(peaks[i-1]+peaks[i])/2
                        inf=sup+1e-4
                        texto+=f'{sup:.4f}\nFBG_{channel_name}{i+1},{canal},{inf:.4f},'
                texto+='1600\n'
        return texto

    def regression(self,equation,x,parameters):
        if equation=='linear':
            return self.lineal(x,parameters)
        if equation=='cubic':
            return self.cubic(x,parameters)
        
    def lineal(self,x,parameters):
        return parameters[0]*x+parameters[1]
    def cubic(self,x,parameters):
        return parameters[0]*x**3+parameters[1]*x**2+parameters[2]*x+parameters[3]


    
    def toma_dato_peaks(self,conexion):
        conexion.sendall(b'#GetPeaks\n')
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
            datos.append(list(struct.unpack(f'{canal}d',msg)))
            
        return datos[:4]
        
        
    def DAQ_peaks(self):
        while True:
            
            self.peaks=self.toma_dato_peaks(self.conexion)
            time.sleep(0.05)


    def DAQ(self):
        """Creates a loop that is always asking for data to the Si155

        """        
        
        while True:
            self.get_peak_values()
            self.get_sensor_values()
            
            try:
                self.current_data=[]
                for canal in range(1,5):
                    self.current_data+=self.peaks[canal-1]
                self.current_data+=[self.sensor_values[sensor] for sensor in self.sensor_values.keys()]
                    
                
                    
                #self.current_data=self.get_sensor_values()
            except Exception as e:print(e)
            time.sleep(.1)
