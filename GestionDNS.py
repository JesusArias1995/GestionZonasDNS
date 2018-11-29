#!/usr/bin/env python
# -*- coding: utf-8 -*-
from funciones import valid_ipv4
import sys

if len(sys.argv)==5 and sys.argv[4].split(".")[0]=="172":
    if sys.argv[1]=="-a" and sys.argv[2]=="-dir":
        if valid_ipv4(sys.argv[4])==False:
            print("Formato ip incorrecto")
            sys.exit()
        reg="%s\tIN\tA\t%s\n"%(sys.argv[3],sys.argv[4])
        leer=open('db.externa','r')
        for linea in leer.readlines():
            if linea==reg:
                print("Ya existen esos parametros")
                sys.exit()
        leer.close()
        iesgn=open('db.externa','a')
        iesgn.write(reg)
        iesgn.close()
        inv="%s.%s\tIN\tPTR\t%s.arias.gonzalonazareno.org.\n"%(sys.argv[4].split(".")[3], sys.argv[4].split(".")[2], sys.argv[3])
        externa=open('db.172.22','a')
        externa.write(inv)
        externa.close()
    else:
        print ("Parametros incorrectos")

elif len(sys.argv)==5 and sys.argv[4].split(".")[0]=="10":
    if sys.argv[1]=="-a" and sys.argv[2]=="-dir":
        print ("Añadir nombre", sys.argv[3], "con dirección", sys.argv[4])
        if valid_ipv4(sys.argv[4])==False:
            print("formato ip incorrecto")
            sys.exit()
        reg="%s\tIN\tA\t%s\n"%(sys.argv[3],sys.argv[4])
        leer=open('db.interna','r')
        for linea in leer.readlines():
            if linea==reg:
                print("Ya existen esos parametros")
                sys.exit()
        leer.close()
        iesgn=open('db.interna','a')
        iesgn.write(reg)
        iesgn.close()

        inv="%s\tIN\tPTR\t%s.arias.gonzalonazareno.org."%(sys.argv[4].split(".")[3], sys.argv[3])
        interna=open('db.10.0.0','a')
        interna.write(inv)
        interna.close()
    else:
        print ("Parametros incorrectos")


elif sys.argv[1]=="-a" and sys.argv[2]=="-alias":
    zona=input("Indica la zona donde añadir el alias, interna o externa (i/e): ")
    if zona=="e" or zona=="E":
        reg="%s\tIN\tCNAME\t%s\n"%(sys.argv[3],sys.argv[4])
        iesgn=open('db.externa','a')
        iesgn.write(reg)
        iesgn.close()
    elif zona=="i" or zona=="I":
        reg="%s\tIN\tCNAME\t%s\n"%(sys.argv[3],sys.argv[4])
        iesgn=open('db.interna','a')
        iesgn.write(reg)
        iesgn.close()
    else:
        print ("Parametros incorrectos")


elif len(sys.argv)==3:
    if sys.argv[1]=="-b":
        zona=input("De que zona desea eliminar el registro, interna o externa (i/e): ")
        if zona=="e" or zona=="E":
            f=open('db.externa', 'r')
            lineas=f.readlines()
            f.close()
            f=open('db.externa', 'w')
            name=[]
            for i in lineas:
                name.append(i.split("\t")[0])
                if i.split(" ")[0] !=sys.argv[2] and i.split("\t")[0] !=sys.argv[2]:
                    f.write(i)
            f.close()
            if sys.argv[2] not in name:
                print("Ningun registro borrado con el nombre", sys.argv[2])
            else:
                print("Registro borrado correctamente", sys.argv[2])
                f=open('db.172.22', 'r')
                lineas=f.readlines()
                f.close()
                f=open('db.172.22', 'w')
                cont=0
                for i in lineas:
                    lista=i.split("\t")
                    if len(lista)==4 and lista[2]=="PTR" and lista[3].startswith(sys.argv[2]):
                        name=" ".join(lista)
                        lineas.pop(cont)
                    else:
                        cont=cont+1
                for i in lineas:
                    f.write(i)
                f.close()

        elif zona=="i" or zona=="I":
            print ("Borrar registro", sys.argv[2])
            f=open('db.interna', 'r')
            lineas=f.readlines()
            f.close()
            f=open('db.interna', 'w')
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
                f=open('db.10.0.0', 'r')
                lineas=f.readlines()
                f.close()
                f=open('db.10.0.0', 'w')
                cont=0
                for i in lineas:
                    lista=i.split("\t")
                    if len(lista)==4 and lista[2]=="PTR" and lista[3].startswith(sys.argv[2]):
                        name=" ".join(lista)
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
