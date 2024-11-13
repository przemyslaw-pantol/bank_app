import random
from datetime import datetime

class Klient:
    ID = 1

    def __init__(self, imie, nazwisko):
        self.id = Klient.ID
        Klient.ID += 1
        self.imie = imie
        self.nazwisko = nazwisko
        self.stan_konta = 0.0
        self.nr_klienta = str(self.nr_klient())
        self.historia=[]
    #generowanie nr klienta
    def nr_klient(self):
        a = ""
        c = ""
        b = str(self.id)
        #dopełnianie zerami ID
        for _ in range((len(b)), 6):
            a = a + "0"
            #6 losowych liczb
        for _ in range(0, 6):
            c = c + str(random.randint(0, 9))
        return f"{a}{self.id}{c}"
    
    def dodaj_historie(self, rodzaj, ilosc, file):
        now=datetime.now()
        czas=now.strftime("%H:%M:%S")
        dzien=now.date()
        #dodoanie histori do klienta
        self.historia.append(f"{self.nr_klienta},{rodzaj},{ilosc},{dzien},{czas}")
        #dopisanie rekordu do pliku z tranzakcjami
        with open(file,"a") as file:
            file.write(self.historia[-1]+"\n")

    def inf(self,id,bank):
        #jesli znajdziemy klienta zwracamy jego dane 
        klient=bank.znajdz_klienta(id)
        if klient:
            return f"Imie {klient.imie} Nazwisko: {klient.nazwisko} Numer: {klient.nr_klienta} saldo= {klient.stan_konta}"

class Bank:
    def __init__(self):
        self.baza_klientów = []

    def usun(self):
        #usuwanie klenta 
        id=input("wprowadz id klienta: ")
        klient=self.znajdz_klienta(id)
        if klient:
            self.baza_klientów.remove(klient)
            print("Klient został usunięty")
        else:
            print("Brak klienta o podanym ID.")

    #informacja o klientcie na pdstawie imienia i nazwiska 
    def inf(self,imie, nazwisko):
        for klient in self.baza_klientów:
            if klient.imie.lower() == imie.lower() and klient.nazwisko.lower() == nazwisko.lower():
                return f"Imie {klient.imie} Nazwisko: {klient.nazwisko} Numer: {klient.nr_klienta} saldo= {klient.stan_konta}"
        return None
    #dodawanie klienta
    def dodaj_klienta(self, klient,file=0):
        self.baza_klientów.append(klient)
        #jesli dodamy siezke do pliku jak oargument dodajemy klienta i jego dane  do pliku 
        if file !=0:
            with open(file,"a") as file:
                file.write(f"{klient.id},{klient.imie},{klient.nazwisko},{klient.stan_konta},{klient.nr_klienta}"+"\n")

    #porównujemy klienta po id z bazy 
    def znajdz_klienta(self, nr_klienta):
        for klient in self.baza_klientów:
            if str(klient.nr_klienta) == str(nr_klienta):
                return klient
        return None
    #wczytaujemy dane o klientach z pliku i dodaojemy je jako obiekty i zapsiujemy w banku 
    def wczytaj_z_pliku(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) >= 5:
                        klient = Klient(data[1], data[2])
                        klient.id = int(data[0])
                        klient.stan_konta = float(data[3])
                        klient.nr_klienta = data[4]
                        self.dodaj_klienta(klient)
                    else:
                        print(f"Skipping line: {line.strip()}")
            print("Dane wczytane pomyślnie.")
        except FileNotFoundError:
            print("Plik nie istnieje.")
    #zapisujemy do poliku 
    def zapisz_do_pliku(self, filename):
        with open(filename, 'w') as file:
            for klient in self.baza_klientów:
                file.write(f"{klient.id},{klient.imie},{klient.nazwisko},{klient.stan_konta},{klient.nr_klienta}\n")
        print("Dane zapisane pomyślnie.")

    def wczytaj_historie(self, file):
        with open(file, "r") as file:
            for line in file:
                #robimy liste po przecinkach z historii
                data = line.strip().split(',')
                klient = self.znajdz_klienta(data[0])
                #jesli zanjdziemy klienta z tym nr dodoajemy historie 
                if klient:
                    klient.historia.append(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]}")

