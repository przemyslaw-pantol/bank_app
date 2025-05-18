import wx

def lab_text_patern(self, sizer, labels, style=0):
        """Tworzy etykiety i pola tekstowe w podanym sizerze"""
        text_ctrls = []
        
        for label in labels:
            # Etykieta
            static_text = wx.StaticText(self, label=label)
            sizer.Add(static_text, 0, wx.EXPAND | wx.ALL, 5)
            
            # Pole tekstowe
            text_ctrl = wx.TextCtrl(self, style=style)
            sizer.Add(text_ctrl, 0, wx.EXPAND | wx.ALL, 2)
            text_ctrls.append(text_ctrl)

        return text_ctrls
    
def button_pattern(self, sizer, label, function):
        """Tworzy przycisk w podanym sizerze i wiąże z funkcją"""
        button = wx.Button(self, label=label)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        button.Bind(wx.EVT_BUTTON, function)
        return button