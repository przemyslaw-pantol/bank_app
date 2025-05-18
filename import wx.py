import wx

class CustomMonthYearPicker(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300, 200))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Label
        label = wx.StaticText(panel, label="Select Year and Month:")
        vbox.Add(label, flag=wx.LEFT | wx.TOP, border=10)

        # Month Dropdown
        months = [f"{i:02d}" for i in range(1, 13)]  # 01 to 12
        self.month_combo = wx.ComboBox(panel, choices=months, style=wx.CB_READONLY)
        self.month_combo.SetValue("01")  # Default to January
        vbox.Add(self.month_combo, flag=wx.LEFT | wx.TOP, border=10)

        # Year Dropdown
        current_year = wx.DateTime.Now().GetYear()
        years = [str(y) for y in range(current_year - 50, current_year + 51)]  # Past 50 and next 50 years
        self.year_combo = wx.ComboBox(panel, choices=years, style=wx.CB_READONLY)
        self.year_combo.SetValue(str(current_year))  # Default to current year
        vbox.Add(self.year_combo, flag=wx.LEFT | wx.TOP, border=10)

        # OK Button
        button = wx.Button(panel, label="Get Selected Year & Month")
        button.Bind(wx.EVT_BUTTON, self.on_get_date)
        vbox.Add(button, flag=wx.LEFT | wx.TOP, border=10)

        panel.SetSizer(vbox)

        self.Centre()
        self.Show()

    def on_get_date(self, event):
        month = self.month_combo.GetValue()
        year = self.year_combo.GetValue()
        wx.MessageBox(f"Selected Year: {year}\nSelected Month: {month}", "Info")


if __name__ == "__main__":
    app = wx.App()
    CustomMonthYearPicker(None, title="Year and Month Picker")
    app.MainLoop()
