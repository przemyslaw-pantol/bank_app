#importujemy biblioteki 
import wx
import wx.adv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import sys
#dodajemy moduł z plików
from bank_login import User,Database
from wx_patern import *
from sql_bank import * 

data= Database()


BAZA_LOGOWANIE = "loginy.csv"
DB = "banking.db"
#tworzymy okna dialogowe konretnych funkcji bankowych 

class Find_Client_Dialog(wx.Dialog):
    def __init__(self, parent,name,surname):
        super(Find_Client_Dialog, self).__init__(parent, title="Dodaj Klienta", size=(300, 200))

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text=wx.StaticText(self,label=client_info(name,surname,DB))
        sizer.Add(self.text, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        self.Centre()

class Add_Client_Dialog(wx.Dialog):
    def __init__(self, parent):
        super(Add_Client_Dialog, self).__init__(parent, title="Dodaj Klienta", size=(300, 200))

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = lab_text_patern(self,sizer, ['Imię', 'Nazwisko'])

        button_pattern(self,sizer, 'Dodaj Klienta', self.add_client)

        self.SetSizer(sizer)
        self.Centre()

    def add_client(self, event):
        imie = self.text_ctrl[0].GetValue()
        nazwisko = self.text_ctrl[1].GetValue()
        try:
                if len(imie) == 0 or len(nazwisko) == 0:
                    raise ValueError('uzupełnij imię lub nazwisko')
                if not imie.isalpha() or not nazwisko.isalpha():
                    raise  ValueError('nazwisko i imie musi składać się z samych liter')
                klient=add_client(imie,nazwisko,DB)

                wx.MessageBox(f"Konto Pani/Pana {imie} {nazwisko} o nr {klient} zostało utworzone.", "Powiadomienie",wx.OK | wx.ICON_INFORMATION)
                self.Destroy()
        except ValueError as e:
                wx.MessageBox(f"Błąd podczas tworzenia konta: {e}", "Błąd", wx.OK | wx.ICON_ERROR)

class Info_Klient_Dialog(wx.Dialog):
    def __init__(self, parent):
        super(Info_Klient_Dialog, self).__init__(parent, title="Info", size=(200, 200))

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = lab_text_patern(self, sizer, ['Imie:','Nazwisko'])
        button_pattern(self, sizer, 'Info', self.info)

        self.SetSizer(sizer)
        self.Centre()

    def info(self,event):
        imie=self.text_ctrl[0].GetValue()
        nazwisko=self.text_ctrl[1].GetValue()
        try:
            klient = client_info(imie,nazwisko,DB)

            if not klient:
                raise ValueError('Nie znaleziono klienta')
            client_data = f"name: {klient[1]}, surname: {klient[2]},balance: {klient[3]}, id_number:{klient[4]}"
            wx.MessageBox(client_data, "Info", wx.OK | wx.ICON_INFORMATION)
        except ValueError as e:
            wx.MessageBox(f"Błąd podczas wykonywania akcji: {e}", "Błąd", wx.OK | wx.ICON_ERROR)

class Wpłata_Dialog(wx.Dialog):
    def __init__(self, parent):
        super(Wpłata_Dialog, self).__init__(parent, title="Wpłata", size=(300, 200))

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.text_ctrl = lab_text_patern(self, sizer, ['Nr klienta', 'Kwota'])
        button_pattern(self, sizer, 'Wpłać', self.dodaj_srodki)

        self.SetSizer(sizer)
        self.Centre()
        
    def dodaj_srodki(self, event):
        try:
            id = self.text_ctrl[0].GetValue()
            amount = self.text_ctrl[1].GetValue()
            update_balance(id,amount,DB,'+')
            wx.MessageBox("Akcja wykonana pomyślnie","informacja",wx.OK)
            self.Destroy()
        except ValueError as e:
            wx.MessageBox(f"Błąd podczas wykonywania akcji: {e}", "Błąd", wx.OK | wx.ICON_ERROR)
        
class Wypłata_Dialog(wx.Dialog):
    def __init__(self, parent):
        super(Wypłata_Dialog, self).__init__(parent, title="Wypłata", size=(300, 200))
    
        sizer = wx.BoxSizer(wx.VERTICAL)
     
        self.text_ctrl=lab_text_patern(self, sizer, ['Nr Klienta:','Kwota:'])
        button_pattern(self, sizer, "Wypłata", self.wypłać)

        self.SetSizer(sizer)
        self.Centre()
    
    def wypłać(self, event):
        id = self.text_ctrl[0].GetValue()
        wplata = self.text_ctrl[1].GetValue()
        try:
            update_balance(id,wplata,DB,"-")
            wx.MessageBox("Akcja wykonana pomyślnie","informacja",wx.OK)
            self.Destroy()
        except ValueError as e:
            wx.MessageBox(f"Błąd podczas wykonywania akcji: {e}", "Błąd", wx.OK | wx.ICON_ERROR)

class Przelew_Dialog(wx.Dialog):
    def __init__(self, parent):
        super(Przelew_Dialog, self).__init__(parent, title="Przelew", size=(300, 400))
   
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl=lab_text_patern(self, sizer, ['Nr klienta nadawcy','Nr klienta odbiorcy','Kwota'])
        button_pattern(self, sizer, 'Przelew', self.przelew)

        self.SetSizer(sizer)
        self.Centre()
   
    def przelew(self, event):
        try:
            a = self.text_ctrl[0].GetValue()
            b = self.text_ctrl[1].GetValue()
            c = self.text_ctrl[2].GetValue()
            update_balance(a,c,DB,"-")
            update_balance(b,c,DB,"+")
            wx.MessageBox("Akcja wykonana pomyślnie","informacja",wx.OK)
            self.Destroy()
        except ValueError as e:
            wx.MessageBox(f"Błąd podczas wykonywania akcji: {e}", "Błąd", wx.OK | wx.ICON_ERROR)

class Historia_Dialog(wx.Dialog):
    def __init__(self, parent):
        super(Historia_Dialog, self).__init__(parent, title="Pokaż historie", size=(400, 400))

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = lab_text_patern(self, sizer, ['Nr klienta'])
        button_pattern(self, sizer, 'Pokaż historie', self.show_history_dialog)

        self.history_text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL, size=(380, 280))
        sizer.Add(self.history_text_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)
        self.Centre()

    def show_history_dialog(self, event):
        try:
            klient_nr = self.text_ctrl[0].GetValue()
            client_data = find_log(klient_nr,DB)
            self.history_text_ctrl.Clear()

            if client_data:
                for element in client_data:
                    self.history_text_ctrl.AppendText(f"{element}\n")
            else:
                self.history_text_ctrl.AppendText("Brak historii dla tego klienta.")

        except ValueError as e:
            wx.MessageBox(f"Błąd podczas wykonywania akcji: {e}", "Błąd", wx.OK | wx.ICON_ERROR)

#głwone okno aplikacji 
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(600, 540),style=wx.DEFAULT_FRAME_STYLE & ~(wx.MAXIMIZE_BOX | wx.RESIZE_BORDER))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer_find= wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_date_stat = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_text_stat = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_text_stat_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer_find)
        self.sizer.Add(self.sizer_date_stat)
        self.sizer.Add(self.sizer_text_stat)
        self.sizer.Add(self.sizer_text_stat_2)
        
        self.create_menu_bar()

        self.find_data = lab_text_patern(self,self.sizer_find,["Name:","Surname:"])
        self.find_button = button_pattern(self,self.sizer_find,"Find client",self.show_find_dialog)

        self.data_stats=wx.adv.DatePickerCtrl(self)
        self.data_stats_2=wx.adv.DatePickerCtrl(self)
        self.sizer_date_stat.Add(self.data_stats)
        self.sizer_date_stat.Add(self.data_stats_2)
        self.stats=button_pattern(self,self.sizer_date_stat,"stats",self.on_stats)

        self.label_stats = wx.StaticText(self,label="stats")
        self.sizer_text_stat_2.Add(self.label_stats)

        self.data_stats_3=wx.adv.DatePickerCtrl(self)
        self.sizer_text_stat.Add(self.data_stats_3)
        self.text_stats_button = button_pattern(self,self.sizer_text_stat,"stats",self.agg_stats)
                                                         

        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_CLOSE, self.on_exit)

    def on_stats(self,event):
        return date_stats(self.data_stats.GetValue(),self.data_stats_2.GetValue(),DB)
    
    def agg_stats(self,event):
        data = stats_agg(self.data_stats_3.GetValue(),DB)
        self.label_stats.SetLabel(data)

    def show_find_dialog(self,event):
        dodaj_klienta_dialog = Find_Client_Dialog(self,self.find_data[0].GetValue(),self.find_data[1].GetValue())
        dodaj_klienta_dialog.ShowModal()
        dodaj_klienta_dialog.Destroy()
        
        
    def on_data_choice(self, event):
        selected_data = self.data_choice.GetValue()
        self.plot_day(selected_data, self.sizer)
        
    def create_menu_bar(self):
        menubar = wx.MenuBar()
    
        action_menu = wx.Menu()
        add_client_item = action_menu.Append(wx.ID_ANY, "Dodaj Klienta", "Dodaj nowego klienta")
        self.Bind(wx.EVT_MENU, self.show_add_client_dialog, add_client_item)
    
        add_wpłata_item = action_menu.Append(wx.ID_ANY, "Wpłata", "Wpłata")
        self.Bind(wx.EVT_MENU, self.show_add_wpłata_dialog, add_wpłata_item)
    
        add_wypłata_item = action_menu.Append(wx.ID_ANY, "Wypłata", "Wypłata")
        self.Bind(wx.EVT_MENU, self.show_add_wypłata_dialog, add_wypłata_item)
    
        add_przelew_item = action_menu.Append(wx.ID_ANY, "Przelew", "Przelew")
        self.Bind(wx.EVT_MENU, self.show_add_przelew_dialog, add_przelew_item)

        add_historia_item = action_menu.Append(wx.ID_ANY, "Historia klienta", "Historia klienta")
        self.Bind(wx.EVT_MENU, self.show_add_historia_dialog, add_historia_item)

        add_info_item = action_menu.Append(wx.ID_ANY, "Informacje o kliencie", "Informacje o kliencie")
        self.Bind(wx.EVT_MENU, self.show_add_info_dialog, add_info_item)

        menubar.Append(action_menu, "&Akcje")
        
        self.SetMenuBar(menubar)
    
    def on_exit(self, event):
        sys.exit()
    #funkcje uruchamiające okna dilogowe po wybraniu konkretnych opcji
    def show_add_client_dialog(self, event):
        dodaj_klienta_dialog = Add_Client_Dialog(self)
        dodaj_klienta_dialog.ShowModal()
        dodaj_klienta_dialog.Destroy()
    
    def show_add_wpłata_dialog(self,event):
        wpłata_dialog = Wpłata_Dialog(self)
        wpłata_dialog.ShowModal()
        wpłata_dialog.Destroy()
    
    def show_add_wypłata_dialog(self,event):
        wypłata_dialog = Wypłata_Dialog(self) 
        wypłata_dialog.ShowModal()
        wypłata_dialog.Destroy()
    
    def show_add_przelew_dialog(self,event):
        przelew_dialog = Przelew_Dialog(self)
        przelew_dialog.ShowModal()
        przelew_dialog.Destroy()
    
    def show_add_historia_dialog(self,event):
        historia_dialog=Historia_Dialog(self)
        historia_dialog.ShowModal()
        historia_dialog.Destroy()
    
    def show_add_info_dialog(self,event):
        info_dialog=Info_Klient_Dialog(self)
        info_dialog.ShowModal()
        info_dialog.Destroy()

    def plot_day(self, data,sizer):
        pass

#okno logowania 
class LoginFrame(wx.Frame):
    def __init__(self, parent=None):
            super(LoginFrame, self).__init__(parent, title="Logowanie", size=(300, 200))
            self.panel = wx.Panel(self)
            self.login_panel = LoginPanel(self.panel)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.login_panel, 1, wx.EXPAND)

            self.panel.SetSizer(sizer)
            self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Destroy()

class LoginPanel(wx.Panel):
    def __init__(self, parent):
        super(LoginPanel, self).__init__(parent)

        sizer1 = wx.BoxSizer(wx.VERTICAL)

        label_login = wx.StaticText(self, label="Login:")
        sizer1.Add(label_login, 0, wx.EXPAND | wx.ALL, 5)

        self.text_ctrl_login = wx.TextCtrl(self)
        sizer1.Add(self.text_ctrl_login, 0, wx.EXPAND | wx.ALL, 5)

        label_password = wx.StaticText(self, label="Password:")
        sizer1.Add(label_password, 0, wx.EXPAND | wx.ALL, 5)

        self.text_ctrl_password = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        sizer1.Add(self.text_ctrl_password, 0, wx.EXPAND | wx.ALL, 5)

        button_login = wx.Button(self, label="Login", id=wx.ID_OK)
        sizer1.Add(button_login, 0, wx.EXPAND | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_login, button_login)

        self.SetSizer(sizer1)
    
    def on_login(self, event):
            login = self.text_ctrl_login.GetValue()
            password = self.text_ctrl_password.GetValue()
            try:
                if login is None or password is None:
                    raise ValueError('Wprowadz login i hasło')
                
                user = data.check(login)

                if user is None or login != user.login or password != user.password:
                    raise ValueError('Błedny login albo hasło')
                wx.MessageBox("Zalogowano pomyślnie!", "Sukces", wx.OK | wx.ICON_INFORMATION)

                if user.login=='admin':  
                    admin_panel = AdminPanel(self, "Panel Administratora")
                    admin_panel.Show()

                else:
                    frame = MainFrame(self.GetTopLevelParent(), "Bank")
                    frame.Show()
                    self.GetTopLevelParent().Hide()

            except ValueError as e:
                wx.MessageBox(f"Błąd podczas wykonywania akcji: {e}", "Błąd", wx.OK | wx.ICON_ERROR)

    def on_close(self, event):
        self.Destroy()

#okno aministratora uruchamia sie po wpisaniu admin admin w polu loogwania 
class AdminPanel(wx.Frame):
    def __init__(self, parent, title):
        super(AdminPanel, self).__init__(parent, title=title, size=(300, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = lab_text_patern(self, sizer, ['Login'])
        self.text_ctrl2 = lab_text_patern(self, sizer, ['Password','Repeat password'], wx.TE_PASSWORD)
        button_pattern(self, sizer, "Sign in", self.sign_in)

        self.SetSizer(sizer)
        self.Centre()

    def sign_in(self, event):
        login = self.text_ctrl[0].GetValue()
        pass1 = self.text_ctrl2[0].GetValue()
        pass2 = self.text_ctrl2[1].GetValue()

        try:
            if not pass1 or not pass2:
                raise ValueError('Wprowadź hasło i powtórz je')
            if pass1 != pass2:
                raise ValueError('Podane hasła nie są identyczne')
            login_check = data.check(login)
            if login_check != None:
                raise ValueError('Użytkownik o podanym loginie już istnieje')
            
            c = User(login, pass1)
            data.add(c)
            data.zapisz_do_pliku(c,BAZA_LOGOWANIE)
            self.Destroy()

        except ValueError as e:
            wx.MessageBox(f"Błąd podczas wykonywania akcji: {e}", "Błąd", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    data.wczytaj_z_pliku(BAZA_LOGOWANIE)

    app = wx.App(True)
    login = LoginFrame(None)
    login.Show()
    app.MainLoop()