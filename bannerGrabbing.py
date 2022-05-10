from portScanner import Scanner
from socket import error as SocketError
import socket
import os
import errno

class Grabber:
    def __init__(self, host):
        self.host = host
        self.listePort = []
        self.mesDonnees = ""

    #-------------------------------------------------------------------------------
    # Fonction permettant d'ouvrir et de lire mon fichier créer avec le portScanner
    # afin de récuperer les ports qui on été identifié comme ouvert
    #-------------------------------------------------------------------------------
    def ouvrirEtLectureFichier(self):
        fichier = open("/tmp/output.txt")
        #Mise du curseur au début
        fichier.seek(0,0)
        line = fichier.readline().rstrip()
        while line:
            self.listePort.append(int(line))
            print(self.listePort)
            #lire la ligne suivante
            line = fichier.readline().rstrip()

    #-------------------------------------------------------------------------------
    # Fonction permettant de creer le dossier avec l'adresse ip de l'hote, si le
    # fichier n'existe pas.
    #-------------------------------------------------------------------------------
    def creerLeDossier(self):
        if not os.path.exists(f'/tmp/{self.host}'):
            os.makedirs(f'/tmp/{self.host}')
        print("self.listePort")

    #-------------------------------------------------------------------------------
    # Fonction permettant d'écrire pour chaque port identifié comme ouvert
    # un fichier avec les information du service qui tourne sur celui ci
    #-------------------------------------------------------------------------------
    def writePortInfoFile(self, filepath):
        fichier=open(filepath, "w+")
        fichier.write(self.mesDonnees)
        print("writePortFile")

    #-------------------------------------------------------------------------------
    # Fonction permettant d'avoir les informations des ports qui sont ouverts
    # et appel la fonction permettant d'écrire un fichier
    #-------------------------------------------------------------------------------
    def infoPortService(self):
        #Pour tout les port qui sont dans ma liste listePort
        for i in range(len(self.listePort)):
            try:
                #création de la connection a mon hote
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.5)
                resultat = mySocket.connect_ex((self.host, self.listePort[i]))
                #envoie un retour chariot a mon hote (utile pour le port 80 notamment)
                mySocket.send("\n".encode())
                #reçoit le message sous forme de chaine de type bytes ("b'")
                data = mySocket.recv(1024)
                #on décode le message
                 .mesDonnees = data.decode()
                #on affiche le message dans la console
                print(data.decode())
                #on appel la fonction qui va nous permettre d'écrire notre message dans un fichier dont le nom est le port
                Grabber.writePortInfoFile(self,"/tmp/" + self.host  +"/"+str(self.listePort[i])+".txt")
            #si le serveur nous renvoie un packet RST et ferme la connection alors on passe
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    raise
                pass


def main():
    ip = 'scanme.nmap.org'
    monScan = Scanner(ip)
    monScan.scan(10,82)
    monScan.write("/tmp/output.txt")

    monGrab = Grabber(ip)
    monGrab.ouvrirEtLectureFichier()
    monGrab.creerLeDossier()
    monGrab.infoPortService()


if __name__ == '__main__':
    main()
