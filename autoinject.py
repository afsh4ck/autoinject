import nmap
import os
import socket

# Definir variables de color
AMARILLO = "\033[93m"
BLANCO = "\033[97m"
CYAN = "\033[96m"
VERDE = "\033[92m"
ROJO = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def cabecera():
    print(ROJO + title + RESET)
    print(divider)

title = """
                 __          _           _              __ 
  ____ _ __  __ / /_ ____   (_)____     (_)___   _____ / /_
 / __ `// / / // __// __ \ / // __ \   / // _ \ / ___// __/
/ /_/ // /_/ // /_ / /_/ // // / / /  / //  __// /__ / /_  
\__,_/ \__,_/ \__/ \____//_//_/ /_/__/ / \___/ \___/ \__/  
                                  /___/                    
                                                                                                                                   
Nmap & SQL injection automation tool             < afsh4ck >"""

divider = """------------------------------------------------------------
"""

# Mostrar cabecera
cabecera()

def escanear_puertos(ip):
    nm = nmap.PortScanner()
    print(VERDE + "[*] Escaneando puertos en " + ip + RESET)
    try:
        nm.scan(ip)
    except KeyboardInterrupt:
        print(ROJO + "\n[!] Escaneo de puertos interrumpido por el usuario." + RESET)
        return
    except:
        print(ROJO + "[!] Error al escanear puertos." + RESET)
        return
    for host in nm.all_hosts():
        print(VERDE+ "[*] Host : %s (%s)" % (host, nm[host].hostname()) + RESET)
        print(VERDE + "[*] Estado : %s" % nm[host].state() + RESET)
        for proto in nm[host].all_protocols():
            print(VERDE + "[*] Protocolo : %s" % proto + RESET)
            lport = nm[host][proto].keys()
            for port in sorted(lport):
                if nm[host][proto][port]['state'] == 'open':
                    print(VERDE + "[*] Puerto : %s Estado : %s" % (port, nm[host][proto][port]['state']) + RESET)
                else:
                    print(ROJO + "[*] Puerto : %s Estado : %s" % (port, nm[host][proto][port]['state']) + RESET)

def escanear_servicios(ip):
    print(VERDE + "[*] Escaneando servicios en " + ip + RESET)
    try:
        for port in range(1, 65536):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                print(VERDE + "[*] Puerto : %s Servicio : %s" % (port, service) + RESET)
            sock.close()
    except KeyboardInterrupt:
        print(ROJO + "\n[!] Escaneo de servicios interrumpido por el usuario." + RESET)
        return
    except:
        print(ROJO + "[!] Error al escanear servicios." + RESET)
        return

def inyeccion_sql(url):
    print(VERDE + "[*] Escaneando vulnerabilidades de inyección SQL en " + url + RESET)
    try:
        os.system("sqlmap -u " + url)
    except KeyboardInterrupt:
        print(ROJO + "\n[!] Escaneo de inyección SQL interrumpido por el usuario." + RESET)
        return
    except:
        print(ROJO + "[!] Error al escanear vulnerabilidades de inyección SQL." + RESET)
        return

def main():
    while True:
        print(CYAN + "[+] ¿Que quieres auditar hoy?" + RESET)
        print("1. Escaneo de puertos")
        print("2. Escaneo de servicios")
        print("3. Pruebas de inyección SQL")
        print("4. Salir del programa")
        opcion = input(VERDE + "> " + RESET)
        if opcion == "1":
            ip = input(CYAN + "[*] Ingrese la IP o dominio a escanear: " + RESET)
            escanear_puertos(ip)
            input("\nPresione Enter para continuar...")
            os.system("clear")
            cabecera()
        elif opcion == "2":
            ip = input(CYAN + "[*] Ingrese la IP o dominio a escanear: " + RESET)
            escanear_servicios(ip)
            input("\nPresione Enter para continuar...")
            os.system("clear")
            cabecera()
        elif opcion == "3":
            url = input(CYAN + "[*] Ingrese la URL para realizar pruebas de inyección SQL: " + RESET)
            inyeccion_sql(url)
            input("\nPresione Enter para continuar...")
            os.system("clear")
            cabecera()
        elif opcion == "4":
            print(ROJO + "[*] Saliendo del programa..." + RESET)
            print(VERDE + "[+] Happy hacking ;)" + RESET)
            exit()
        else:
            print(ROJO + "[!] Opción inválida." + RESET)

if __name__ == "__main__":
    main()
