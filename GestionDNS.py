#!/usr/bin/env python

from funciones import valid_ipv4
import sys

#En este apartado vamos a añadir un registro A a la zona externa.
if len(sys.argv)==5 and sys.argv[4].split(".")[0]=="172":
    if sys.argv[1]=="-a" and sys.argv[2]=="-dir":
        #Comprobamos si la IP tiene un formato correcto.
        if valid_ipv4(sys.argv[4])==False:
            print("Formato ip incorrecto")
            sys.exit()
        reg="%s\tIN\tA\t%s\n"%(sys.argv[3],sys.argv[4])
        #Comprobamos si existe el registro A que vamos a insertar.
        leer=open('/var/cache/bind/db.externa.ariasgonzalonazareno','r')
        for linea in leer.readlines():
            if linea==reg:
                print("Ya existen esos parametros")
                sys.exit()
        leer.close()
        #En este paso insertaremos el registro A.
        iesgn=open('/var/cache/bind/db.externa.ariasgonzalonazareno','a')
        iesgn.write(reg)
        iesgn.close()
        #Insertamos un registro PTR en la zona inversa.
        inv="%s.%s\tIN\tPTR\t%s.arias.gonzalonazareno.org.\n"%(sys.argv[4].split(".")[3], sys.argv[4].split(".")[2], sys.argv[3])
        externa=open('/var/cache/bind/db.22.172','a')
        externa.write(inv)
        externa.close()
    else:
        print ("Parametros incorrectos")

#En este apartado vamos a añadir un registro A a la zona interna.
elif len(sys.argv)==5 and sys.argv[4].split(".")[0]=="10":
    if sys.argv[1]=="-a" and sys.argv[2]=="-dir":
        #Comprobamos si la IP tiene un formato correcto.
        if valid_ipv4(sys.argv[4])==False:
            print("formato ip incorrecto")
            sys.exit()
        reg="%s\tIN\tA\t%s\n"%(sys.argv[3],sys.argv[4])
        #Comprobamos si existe el registro A que vamos a insertar.
        leer=open('/var/cache/bind/db.interna.ariasgonzalonazareno','r')
        for linea in leer.readlines():
            if linea==reg:
                print("Ya existen esos parametros")
                sys.exit()
        leer.close()
        #En este paso insertaremos el registro A.
        iesgn=open('/var/cache/bind/db.interna.ariasgonzalonazareno','a')
        iesgn.write(reg)
        iesgn.close()
        #Insertamos un registro PTR en la zona inversa.
        inv="%s\tIN\tPTR\t%s.arias.gonzalonazareno.org."%(sys.argv[4].split(".")[3], sys.argv[3])
        interna=open('/var/cache/bind/db.0.0.10','a')
        interna.write(inv)
        interna.close()
    else:
        print ("Parametros incorrectos")

#En este apartado vamos a insertar un alias en la zona externa o interna.
elif sys.argv[1]=="-a" and sys.argv[2]=="-alias":
    zona=input("Indica la zona donde añadir el alias, interna o externa (i/e): ")
    #Si elegimos la opcion "e" añadiremos el alias en la zona externa.
    if zona=="e" or zona=="E":
        reg="%s\tIN\tCNAME\t%s\n"%(sys.argv[3],sys.argv[4])
        iesgn=open('/var/cache/bind/db.externa.ariasgonzalonazareno','a')
        iesgn.write(reg)
        iesgn.close()
    #Si elegimos la opcion "i" añadiremos el alias en la zona interna.
    elif zona=="i" or zona=="I":
        reg="%s\tIN\tCNAME\t%s\n"%(sys.argv[3],sys.argv[4])
        iesgn=open('/var/cache/bind/db.interna.ariasgonzalonazareno','a')
        iesgn.write(reg)
        iesgn.close()
    else:
        print ("Parametros incorrectos")

#En este apartado borraremos un registro, indicando el nombre.
elif len(sys.argv)==3:
    if sys.argv[1]=="-b":
        #Tendremos que elegir de donde queremos borrar el registro.
        zona=input("De que zona desea eliminar el registro, interna o externa (i/e): ")
        if zona=="e" or zona=="E":
            f=open('/var/cache/bind/db.externa.ariasgonzalonazareno', 'r')
            lineas=f.readlines()
            f.close()
            f=open('/var/cache/bind/db.externa.ariasgonzalonazareno', 'w')
            name=[]
            #Borro el registro recorriendo la lista, y lo voy añadiendo al fichero menos la linea que sea igual al parametro que le hemos pasado
            for i in lineas:
                name.append(i.split("\t")[0])
                if i.split(" ")[0] !=sys.argv[2] and i.split("\t")[0] !=sys.argv[2]:
                    f.write(i)
            f.close()
            if sys.argv[2] not in name:
                print("Ningun registro borrado con el nombre", sys.argv[2])
            else:
                print("Registro borrado correctamente", sys.argv[2])
                #Una vez borrado en la zona directa, comprobamos si existe un registro en la zona inversa.
                f=open('/var/cache/bind/db.22.172', 'r')
                lineas=f.readlines()
                f.close()
                f=open('/var/cache/bind/db.22.172', 'w')
                cont=0
                #Recorro la lista y borro la linea que coincida.
                for i in lineas:
                    lista=i.split("\t")
                    if len(lista)==4 and lista[2]=="PTR" and lista[3].startswith(sys.argv[2]):
                        lineas.pop(cont)
                    else:
                        cont=cont+1
                for i in lineas:
                    f.write(i)
                f.close()

        elif zona=="i" or zona=="I":
            f=open('/var/cache/bind/db.interna.ariasgonzalonazareno', 'r')
            lineas=f.readlines()
            f.close()
            f=open('/var/cache/bind/db.interna.ariasgonzalonazareno', 'w')
            name=[]
            for i in lineas:
                name.append(i.split(" ")[0])
                name.append(i.split("\t")[0])
                if i.split(" ")[0] !=sys.argv[2] and i.split("\t")[0] !=sys.argv[2]:
                    f.write(i)
            f.close()
            if sys.argv[2] not in name:
                print("Ningun registro borrado con el nombre", sys.argv[2])
            else:
                print("Registro borrado correctamente", sys.argv[2])
                f=open('/var/cache/bind/db.0.0.10', 'r')
                lineas=f.readlines()
                f.close()
                f=open('/var/cache/bind/db.0.0.10', 'w')
                cont=0
                for i in lineas:
                    lista=i.split("\t")
                    if len(lista)==4 and lista[2]=="PTR" and lista[3].startswith(sys.argv[2]):
                        lineas.pop(cont)
                    else:
                        cont=cont+1
                for i in lineas:
                    f.write(i)
                f.close()

        else:
            print ("Parametros incorrectos")
    else:
        print ("Parametros incorrectos")

else:
    print("Indicar parametros correctos")
