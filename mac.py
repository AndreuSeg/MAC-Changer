#!/usr/bin/env python3

import re
import subprocess
import netifaces
import argparse
import random
import os, sys

# Constantes
BANNER = """
__  __    _    ____       ____ _
|  \/  |  / \  / ___|     / ___| |__   __ _ _ __   __ _  ___ _ __
| |\/| | / _ \| |   _____| |   | '_ \ / _` | '_ \ / _` |/ _ \ '__|
| |  | |/ ___ \ |__|_____| |___| | | | (_| | | | | (_| |  __/ |
|_|  |_/_/   \_\____|     \____|_| |_|\__,_|_| |_|\__, |\___|_|
                                                |___/
By: Andreu Seguí Segura
"""


def flags():
    # Creamos el parseador
    parser = argparse.ArgumentParser()
    # Añadimos los argumentos
    parser.add_argument("-i", "--interface", type=str, help="Network interface to change")
    parser.add_argument("-r", "--random", action="store_true", help="Set a random mac")
    parser.add_argument("-p", "--permanent", action="store_true", help="Get the permanent mac")
    # Parseamos los arumentos al script
    args = parser.parse_args()
    # Devlovemos la variable del nombre del archivo
    return args


def get_interfaces():
    """
    Obtenemos las interfaces de red que hay en el sistema y las almacenamos en una lista.
    """
    interfaces = subprocess.check_output(['ifconfig', '-a']).decode().split('\n\n')
    interfaces = [interface.split()[0][:-1] for interface in interfaces if interface]
    return interfaces


def select_interface(interfaces):
    """
    Seleccionamos la interfaz que queremos cambiar y enseñamos la direccion mac actual.
    """
    # Solicitar la interfaz y verificar que esté en la lista de interfaces
    while True:
        interface = input('\nWhich interface you want to change: ')
        if interface in interfaces:
            break
        print(f'The interface "{interface}" was not found in the list of available interfaces.')
        print('\nInterfaces:')
        for interface in interfaces:
            mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            print(f'{interface} ({mac})')
    return interface


def verify_mac():
    """
    Verificamos si el usuario ha introducido una direccion mac valida.
    """
    # Verificar que la dirección MAC ingresada esté en el formato correcto
    while True:
        new_mac = input('Enter the new MAC address in the format AA:BB:CC:DD:EE:FF: ')
        """
        Expresion regular para verificar la direccion mac:
        `^` y `$`: indican el principio y fin de la cadena.
        `([0-9A-Fa-f]{2}[:]){5}`: indica que debe haber exactamente 5 grupos de dos caracteres hexadecimales (0-9, A-F, a-f) seguidos de :. Esto asegura que la dirección MAC tenga un total de 6 grupos de 2 caracteres hexadecimales.
        `([0-9A-Fa-f]{2})`: indica que debe haber un último grupo de dos caracteres hexadecimales sin : al final. Esto asegura que la dirección MAC tenga un total de 6 grupos de 2 caracteres hexadecimales y que no termine con :
        """
        if re.match('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$', new_mac):
            break
        print('The MAC address entered is not in the correct format. Be sure to enter it in the correct format. Ex:AA:BB:CC:DD:EE:FF')
    return new_mac


def generate_random_mac():
    """
    Genera una dirección MAC aleatoria y la devuelve como una cadena de texto en formato AA:BB:CC:DD:EE:FF.
    """
    # Genera seis bytes aleatorios en hexadecimal, cada uno representado por dos caracteres.
    random_bytes = [random.randint(0x00, 0xff) for _ in range(6)] # 0x indica que son numeros hecadeciamles.
    # Combina los bytes en una cadena de texto en formato AA:BB:CC:DD:EE:FF.
    mac_address = ':'.join(f'{byte:02x}' for byte in random_bytes)
    return mac_address


def change_mac(interface, new_mac):
    # Ejecutar el comando de consola para cambiar la dirección MAC
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])
    # Imprimir un mensaje de éxito
    print(f"The MAC address of the {interface} interface has been changed to {new_mac}.")


def get_perm_mac(interface):
    try:
        # Ejecutamos el comnado para obtener la mac permanente.
        result = subprocess.check_output('ip link show {} | grep permaddr'.format(interface), shell=True)
        # La pasamos a str y quitamos espacios en blanco con .strip()
        result = result.decode('utf-8').strip()
        # Almacenamos solo la mac
        permanent_mac = result.split("permaddr ")[1]
        return permanent_mac
    except subprocess.CalledProcessError:
        print('The mac address is the original. ')
        print('Aborting the script. ')
        sys.exit()


if __name__ == '__main__':
    os.system('clear')
    print(BANNER)
    args = flags()
    # Si no hay el argumento para especificar la mac que muestre todas las interfaces con sus respectiavas direcciones mac.
    if not args.interface:
        interfaces = get_interfaces()
        # Imprimir las interfaces disponibles y sus direcciones MAC
        print('Interfaces:')
        for interface in interfaces:
            mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            print(f'{interface} ({mac})')
        interface = select_interface(interfaces=interfaces)
        if args.random:
            new_mac = generate_random_mac()
            change_mac(interface=interface, new_mac=new_mac)
        elif args.permanent:
            permanent_mac = get_perm_mac(interface=interface)
            change_mac(interface=interface, new_mac=permanent_mac)
        else:
            new_mac = verify_mac()
            change_mac(interface=interface, new_mac=new_mac)
    elif args.interface:
        interface = args.interface
        mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
        print(f'{interface} ({mac})')
        if args.random:
            new_mac = generate_random_mac()
            change_mac(interface=interface, new_mac=new_mac)
        elif args.permanent:
            permanent_mac = get_perm_mac(interface=interface)
            change_mac(interface=interface, new_mac=permanent_mac)
        else:
            new_mac = verify_mac()
            change_mac(interface=interface, new_mac=new_mac)