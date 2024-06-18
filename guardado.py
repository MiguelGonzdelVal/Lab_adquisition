def saving(file_name,texto):
    file= open(file_name,'a')
    file.write(texto)
    file.close()
    save_it=0
    texto=''
    return texto

def escritura_encabezado(Objetos,file_name):
    Heading=[]
    no_sensor=[]
    with open(file_name,'w') as file:
        file.write('datetime')
        
        for objeto in Objetos:
            Heading+=objeto.encabezado
            file.write(','+','.join(objeto.encabezado))
        file.write('\n')
    return Heading
