# GestionZonasDNS

## Crear el registro -> smtp A 192.168.4.1

```sh
gestionDNS.py -a -dir smtp 192.168.4.1
```

## Crear el registro -> correo CNAME smtp

```sh
gestionDNS.py -a -alias correo smtp
```

## Borrar el último registro

```sh
gestionDNS.py -b correo
```
