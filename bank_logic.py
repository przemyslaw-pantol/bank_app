import random
from datetime import datetime
import sqlite3

class Klient:
    ID=1
    def __init__(self, imie, nazwisko):
        self.id = Klient.ID
        Klient.ID += 1
        self.imie = imie
        self.nazwisko = nazwisko
        self.stan_konta = 0.0
        self.nr_klienta = str(self.nr_klient())
        self.historia=[]
    def nr_klient(self):
        a = ""
        c = ""
        b = str(self.id)
        for _ in range((len(b)), 6):
            a = a + "0"
        for _ in range(0, 6):
            c = c + str(random.randint(0, 9))
        return f"{a}{self.id}{c}"
    
    def dodaj_historie(self, rodzaj, ilosc, file):
        now=datetime.now()
        czas=now.strftime("%H:%M:%S")
        dzien=now.date()
        self.historia.append(f"{self.nr_klienta},{rodzaj},{ilosc},{dzien},{czas}")
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (id_number, type, amount ,date, time)
            VALUES (?, ?, ? ,?,?)
            """, (self.nr_klienta, rodzaj, ilosc, dzien ,czas))
        conn.commit()
        conn.close()
        print("done")

    def inf(self,id,bank):
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        klient=cursor.execute("""
            SELECT FROM customers WHERE id_number = ? 
            """, (self.nr_klienta))
        conn.commit()
        conn.close()
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

