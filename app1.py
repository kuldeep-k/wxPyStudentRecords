import wx
import sqlite3

conn = sqlite3.connect('mydb.db')

########################################################################
class App1(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "List Control", size=(600,600))
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0
 
        self.list_ctrl = wx.ListCtrl(panel, size=(500,500),
                         style=wx.LC_REPORT
                         |wx.BORDER_SUNKEN
                         )
        self.list_ctrl.InsertColumn(0, 'Student ID')
        self.list_ctrl.SetColumnWidth(0, 100)
        self.list_ctrl.InsertColumn(1, 'First Name')
        self.list_ctrl.SetColumnWidth(1, 100)
        self.list_ctrl.InsertColumn(2, 'Last Name')
        self.list_ctrl.SetColumnWidth(2, 100)        
        btn = wx.Button(panel, label="Add New Record")
        btn.Bind(wx.EVT_BUTTON, self.add_new_record)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        
        panel.SetSizer(sizer)
        self.initFromDB()
        
    def initFromDB(self):
        dbq = conn.cursor()
        rs = dbq.execute("SELECT * FROM student")    
        res = rs.fetchall()
        #print res
        self.index = 0
        for row in res:
            #line = "%s" % row[0]
            self.list_ctrl.InsertStringItem(self.index, str(row[0]))
            #self.list_ctrl.SetStringItem(self.index, 0, row[0])
            self.list_ctrl.SetStringItem(self.index, 1, row[1])
            self.list_ctrl.SetStringItem(self.index, 2, row[2])  
            self.index += 1
 
    def add_new_record(self, event):
        appForm = AppForm(self) 
        #appForm.show()
    #----------------------------------------------------------------------
    def add_line(self, event):
        line = "Line %s" % self.index
        self.list_ctrl.InsertStringItem(self.index, line)
        self.list_ctrl.SetStringItem(self.index, 1, "01/19/2010")
        self.list_ctrl.SetStringItem(self.index, 2, "USA")
        self.index += 1


class AppForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Frame.__init__(self, None, wx.ID_ANY, size=(500,500))
        panel=wx.Panel(self, -1)
        self.parent = parent
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        fgs = wx.FlexGridSizer(3, 2, 9, 25)

        student_id = wx.StaticText(panel, label="Student ID")
        first_name = wx.StaticText(panel, label="First Name")
        last_name = wx.StaticText(panel, label="Last Name")
        blankLbl = wx.StaticText(panel, label="")

        self.tc1 = wx.TextCtrl(panel)
        self.tc2 = wx.TextCtrl(panel)
        self.tc3 = wx.TextCtrl(panel)
        addbtn = wx.Button(panel, label="Add")
        addbtn.Bind(wx.EVT_BUTTON, self.add_record)
        #tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        fgs.AddMany([(student_id), (self.tc1, 1, wx.EXPAND), (first_name), 
            (self.tc2, 1, wx.EXPAND), (last_name, 1, wx.EXPAND), (self.tc3, 1, wx.EXPAND), (blankLbl, 1, wx.EXPAND), (addbtn, 1, wx.EXPAND)])
        #fgs.Add(addbtn)
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)
        self.SetBackgroundColour(wx.Colour(100,100,100))
        self.Centre()
        self.Show()
    def add_record(self, event):
        try:
            dbq = conn.cursor()
            
            tc1 = self.tc1.GetValue()
            tc2 = self.tc2.GetValue()
            tc3 = self.tc3.GetValue()
            
            st = self.checkValidations({'tc1' : tc1, "tc2" : tc2, "tc3" : tc3})
            
            if st == True:
                qry = dbq.execute("INSERT INTO student VALUES (?, ?, ?) ", (self.tc1.GetValue(), self.tc2.GetValue(), self.tc3.GetValue()))    
                conn.commit()
                
                self.parent.list_ctrl.DeleteAllItems()
                '''self.parent.list_ctrl.InsertColumn(0, 'Student ID')
                self.parent.list_ctrl.SetColumnWidth(0, 100)
                self.parent.list_ctrl.InsertColumn(1, 'First Name')
                self.parent.list_ctrl.SetColumnWidth(1, 100)
                self.parent.list_ctrl.InsertColumn(2, 'Last Name')
                self.parent.list_ctrl.SetColumnWidth(2, 100)'''
                self.parent.initFromDB()
                self.Close(True)
            #res = qry.fetchall()
        except ValueError as e:
            self.Warn(self.parent, "Something issue")        

    def checkValidations(self, data):
        #print data.keys()
        #print type(data['tc1'])
        #print isinstance(data['tc1'], int)
        #print data['tc1'].isdigit()
        #print isinstance(tc1, int)
        #print isinstance(tc1, basestring)
                
        try:
            if data['tc1'].isdigit() == False:
                raise ValueError("Student ID must be number.")
            dbq = conn.cursor()
            rs = dbq.execute("SELECT * FROM student WHERE id = ?", (data['tc1'],))    
            val = rs.fetchone()    
            print val
            if val is not None:
                raise ValueError('Student ID is already exists ')
            return True    
        except ValueError as e:
            #print e
            self.Warn(self, str(e))       
            return False
            
                
    def Warn(self, parent, message, caption = 'Warning!'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()    
            
         
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = App1()
    frame.Show()
    app.MainLoop()
