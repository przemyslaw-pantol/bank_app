class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password

class Database:
    #tu przetzrymujemy urzytkowników
    def __init__(self):
        self.data = []
        #sprawdzamy czy uzytkownk widnieje w bazie 
    def check(self, login):
        for user in self.data:
            if user.login == login:
                return user
        return None
    #dodajemy kleinta do abzy 
    def add(self,obj):
        self.data.append(obj)

    #zapisujemy nwoego uzytkownika do pliku 
    def zapisz_do_pliku(self, klient, filename):
        with open(filename, 'a') as file:
            file.write(f"{klient.login},{klient.password}" +'\n')
    #wczytujemy klientów z pliku     
    def wczytaj_z_pliku(self, filename):
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    user = User(data[0], data[1])
                    self.data.append(user)
    
