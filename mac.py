import re
import subprocess
import netifaces
import os

# Obtener una lista de interfaces de red disponibles
interfaces = subprocess.check_output(['ifconfig', '-a']).decode().split('\n\n')
interfaces = [interface.split()[0][:-1] for interface in interfaces if interface]

BANNER = """
 __  __    _    ____       ____ _
|  \/  |  / \  / ___|     / ___| |__   __ _ _ __   __ _  ___ _ __
| |\/| | / _ \| |   _____| |   | '_ \ / _` | '_ \ / _` |/ _ \ '__|
| |  | |/ ___ \ |__|_____| |___| | | | (_| | | | | (_| |  __/ |
|_|  |_/_/   \_\____|     \____|_| |_|\__,_|_| |_|\__, |\___|_|
                                                  |___/
By: Andreu Seguí Segura
"""
os.system('clear')
print(BANNER)

# Imprimir las interfaces disponibles y sus direcciones MAC
print('Interfaces de red disponibles:')
for interface in interfaces:
    mac_actual = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    print(f'{interface} ({mac_actual})')

# Solicitar la interfaz y verificar que esté en la lista de interfaces
while True:
    interface = input('\nQue interfaz que quieres cambiar: ')
    if interface in interfaces:
        break
    print(f'La interfaz "{interface}" no se encontró en la lista de interfaces disponibles.')
    print('\nInterfaces de red disponibles:')
    for interface in interfaces:
        mac_actual = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
        print(f'{interface} ({mac_actual})')

# Verificar que la dirección MAC ingresada esté en el formato correcto
while True:
    mac_nueva = input('Introduce la nueva dirección MAC en formato AA:BB:CC:DD:EE:FF: ')
    """
    Expresion regular para verificar la direccion mac:
    `^` y `$`: indican el principio y fin de la cadena.
    `([0-9A-Fa-f]{2}[:]){5}`: indica que debe haber exactamente 5 grupos de dos caracteres hexadecimales (0-9, A-F, a-f) seguidos de :. Esto asegura que la dirección MAC tenga un total de 6 grupos de 2 caracteres hexadecimales.
    `([0-9A-Fa-f]{2})`: indica que debe haber un último grupo de dos caracteres hexadecimales sin : al final. Esto asegura que la dirección MAC tenga un total de 6 grupos de 2 caracteres hexadecimales y que no termine con :
    """
    if re.match('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$', mac_nueva):
        break
    print('La dirección MAC ingresada no está en el formato correcto. Asegúrate de ingresarla en el formato AA:BB:CC:DD:EE:FF')

# Ejecutar el comando de consola para cambiar la dirección MAC
subprocess.call(['ifconfig', interface, 'down'])
subprocess.call(['ifconfig', interface, 'hw', 'ether', mac_nueva])
subprocess.call(['ifconfig', interface, 'up'])

# Imprimir un mensaje de éxito
print(f"La dirección MAC de la interfaz {interface} ha sido cambiada a {mac_nueva}.")
