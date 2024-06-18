import dispositivo
import time
objeto=dispositivo.LUNA_Si155(3,'10.0.0.55',[1,2],1,False)

print(objeto.Peaks_DB)
for i in range(10):
    t_0=time.time()
    objeto.get_peak_values()
    objeto.get_sensor_values()
    print(time.time()-t_0)
    time.sleep(1)
    
print(objeto.sensor_values)


