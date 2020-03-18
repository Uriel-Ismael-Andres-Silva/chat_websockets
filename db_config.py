from configparser import ConfigParser #Nos ayuda a leer o escribir archivos ini

def get_configuration_data(filename="bd.ini",section="postgresql"):#tiene parametros estaticos
    parser=ConfigParser()#Creamos el analizador
    parser.read(filename)#Leemos el archivo bd.ini
    
    #Obtener la seccion postgresql del archivo bd.ini para la conexion a la base de dtos
    db={}
    
    if parser.has_section(section):#Comprobamos si la seccion postgresql existe
        params=parser.items(section)#Obtenemos los parametros de la seccion
        for param in params:#Recorremos los parametros 1 a 1
            db[param[0]]=param[1]
    else:
        raise Exception('La Seccion {0} no se encontro en el archivo {1}'.format(seccion, archivo))#En caso de que no se encuentre la secicon se lanza esta excepcion
    
    return db#retornamos los datos
