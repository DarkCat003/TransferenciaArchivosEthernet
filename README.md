# TransferenciaArchivosEthernet
Transifere archivos cifrados y códificados mediantes un enlace ethernet sin necesidad de conexión a internet.

## Antes de programar: conexión Ethernet directa
Como no hay switch ni router, ambas PCs deben tener IPs estáticas.
### Ejemplo:
- PC 1
> IP: 192.168.10.1
> Máscara: 255.255.255.0

- PC 2
> IP: 192.168.10.2
> Máscara: 255.255.255.0

No necesitas puerta de enlace ni DNS.

📌 Usa un cable Ethernet cruzado (o uno normal si las tarjetas soportan auto-MDIX, que hoy es común).

# Lógica del cifrado
Convertimos la frase a un desplazamiento:
```pyhton
shift = sum(ord(c) for c in key) % 256
```

# ¿Dónde se guardan los archivos?
Se guardan en la variable SAVE_DIR 
```pyhton
SAVE_DIR = r"C:\ArchivosRecibidos"
```

# Prompt utilizado para generar la solución
Por error utilice el chat temporal, por lo que no puedo pasar el enlace compartido, así que aquí envio como genere esta solución:

> Hola chatgpt, necesito que me ayudes a generar un programa en python que me permita comunicarme con otra computadora PERO conectandome directamente con ella mediante ethernet, osea mi computadora conectada mediante el rj45 directamente a la otra computadora, sin switch y sin conexión a internet. Necesito que me ayudes generando ese programa, lo mas probable es que se requiera un cliente para el emisor, y otro para el receptor, así que necesito que el programa que me crees funcione tanto para enviar como para recibir. Aparte, necesito que tenga interfaz gráfica (super sencilla) y que los datos vayan cifrados en "Cifrado cesar" y códificados. Quien envia debe de indicar la llave para cifrar y quien recibe debe de poner esa frase. Se debe poder enviar "Texto" y "archivos"
