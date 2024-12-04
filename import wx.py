import wx
import wx.lib.agw.gradientbutton as GB

class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, title="Modern wxPython UI", size=(400, 300))

        panel = wx.Panel(frame)
        panel.SetBackgroundColour(wx.Colour(240, 240, 240))

        sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(panel, label="Welcome to Modern wxPython!")
        title_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        button = GB.GradientButton(panel, label="Click Me")
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        panel.SetSizer(sizer)
        frame.Show()
        return True

app = MyApp()
app.MainLoop()
