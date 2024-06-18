import datetime
class Muestreo(object):
    def __init__(self,Objetos:list,APP_PLOT:object,it_rec,file_name) -> None:
        self.save_it=0;self.texto=''
        self.Objetos=Objetos
        self.APP_PLOT = APP_PLOT
        self.it_rec =it_rec
        self.file_name = file_name
    def ad_muestra(self):
        if self.APP_PLOT.grabar:
            self.save_it+=1
            muestra=[str(datetime.datetime.now())]
            for objeto in self.Objetos:
                datos=objeto.get_data()
                if type(datos)==list:
                    for dato in datos:muestra.append(dato)
            if 	self.APP_PLOT.w!= False:
                for channel in self.APP_PLOT.w.variables_dibujo:
                    self.APP_PLOT.w.update_data(channel,datetime.datetime.now(),muestra[channel])
            self.APP_PLOT.muestra = muestra   
            print(*muestra, sep='\t')
            self.texto+=str(muestra).replace('[','').replace(']','\n').replace("'",'')
            print(self.save_it,self.it_rec)
            if self.save_it==self.it_rec:
                print('saving')
                self.save_it=0
                self.texto= self.saving(self.file_name,self.texto) 
            
        if not self.APP_PLOT.grabar:
            if len(self.texto)>0:self.texto= self.saving(self.file_name,self.texto)
    def saving(self,file_name,texto):
        file= open(file_name,'a')
        file.write(texto)
        file.close()
        save_it=0
        texto=''
        return texto
        
