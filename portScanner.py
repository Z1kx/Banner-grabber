import socket

class Scanner:
    def __init__(self, host):
        self.host = host
        self.listePort = []

    #-------------------------------------------------------------------------------
    # Fonction permettant d'ajouter les port dans la liste pour le fichier txt
    #-------------------------------------------------------------------------------
    def add_port(self,port):
        self.listePort.append(port)

    #-------------------------------------------------------------------------------
    # Fonction permettant d'identifier si le port et ouvert et appele
    # la fonction d'ajout dans la liste si le port est ouvert
    #-------------------------------------------------------------------------------
    def scan(self, lowerport, upperport):
        for port in range(lowerport, upperport + 1):
            if (self.is_open(port) == 0):
                self.add_port(port)

    #-------------------------------------------------------------------------------
    # Fonction permettant d'identifier si le port est ouvert ou non
    #-------------------------------------------------------------------------------
    def is_open(self,port):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.3)
        resultat = mySocket.connect_ex((self.host, port))
        #print(format(resultat))
        mySocket.close()
        return resultat

    #-------------------------------------------------------------------------------
    # Fonction permettant d'écrire les ports dans un fichier txt
    #-------------------------------------------------------------------------------
    def write(self,filepath):
        fichier=open(filepath, "w+")
        for i in range (len(self.listePort)):
            fichier.write(str(self.listePort[i]) + "\n")



def main():
    ip = 'scanme.nmap.org'
    monScan = Scanner(ip)
    monScan.scan(10,82)
    monScan.write("/tmp/output.txt")

if __name__ == '__main__':
    main()
