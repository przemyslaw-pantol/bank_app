import wx

class Patterns():
    def __init__(self):
        pass

    def lab_text_patern(self, panel, sizer, labels,style=0):
        text_ctrls = []
        #tworzymy na podastawie napisów text razem z polem do wpisyania i dodajemy pole do wpisyania do listy potrzebne do pobierzania z nich danych 

        for label in labels:
            text_ctrl = wx.TextCtrl(panel,style=style)
            sizer.Add(wx.StaticText(panel, label=label, style=wx.ALIGN_CENTER), 0, wx.EXPAND | wx.ALL, 5)
            sizer.Add(text_ctrl, 0, wx.EXPAND | wx.ALL, 2)
            text_ctrls.append(text_ctrl)

        return text_ctrls
        #podobnie jka eczessniej tylko traz na podastawie funkcji i nazwy tworzymi i dodajemy przycisk 
    
    def button_pattern(self, panel, sizer, label, function):
            button = wx.Button(panel, label=label)
            sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            button.Bind(wx.EVT_BUTTON, function)

    
         