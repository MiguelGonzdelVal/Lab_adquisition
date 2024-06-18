from dispositivo.mgcplus_obj import *
from dispositivo.Si155_obj import *
from dispositivo.Lakeshore_obj import *
from dispositivo.pressure_obj import *
def set_up(app):
    DEVICES=[]
    [app.MGC_value.get(),app.Lakeshore_value.get(),app.Si155_value.get(),app.Vaccum_value.get()]
    Address_ID=1
    if app.MGC_value.get():
        MGC=pd.read_csv('.\\configurations\\MGC_plus.txt',sep=';')
        server_address=MGC.Valor.values[0]
        server_port=int(MGC.Valor.values[1])
        active_channels=[int(ch) for ch in MGC.Valor.values[2].split(',')]
        active_subchannels=[int(ch) for ch in MGC.Valor.values[3].split(',')]
        print(server_address,server_port,active_channels,active_subchannels,MGC.Valor.values[3].split(','))
        DEVICES.append(MGCPlus(Address_ID,server_address,server_port,active_channels,active_subchannels))
        Address_ID+=1

    if app.Vaccum_value.get():
        P=pd.read_csv('.\\configurations\\pressure.txt',sep=';')
        Baud_rate=int(P.Valor.values[0])
        port=str(P.Valor.values[1])
        DEVICES.append(Pressure(Address_ID,Baud_rate,port,'pressure'))
        Address_ID+=1

    if app.Si155_value.get():
        si=pd.read_csv('.\\configurations\\Si155.txt',sep=';')
        address=str(si.Valor.values[0])
        act_channels=[int(ch) for ch in si.Valor.values[1].split(',')]
        spectrum_ad=bool(si.Valor.values[2])
        adq_FBG = bool(app.Si155_FBG_value.get())
        streaming = bool(app.Si155_streaming_value.get())
        DEVICES.append(LUNA_Si155(Address_ID,address,act_channels,spectrum_ad,adq_FBG,streaming))
        Address_ID+=1
        

    if app.Lakeshore_value.get():
        L218=pd.read_csv('.\\configurations\\Lakehore218.txt',sep=';')
        Baud_rate=int(L218.Valor.values[0])
        COM_port=str(L218.Valor.values[1])
        act_channels=[int(ch) for ch in L218.Valor.values[2].split(',')]
        chann_type=L218.Valor.values[3].split(',')
        DEVICES.append(Lakeshore_218(2,Baud_rate,COM_port,act_channels,chann_type))
        Address_ID+=1
    #sampling time
    t_s=float(app.tiempo_muestreo_value.get())
    #recording time
    t_rec=float(app.tiempo_rec_value.get())
    it_rec =int(t_rec//t_s)
    return DEVICES,t_s,it_rec
