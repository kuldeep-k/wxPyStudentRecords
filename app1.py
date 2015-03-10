import wx
import sqlite3
import wx.grid as  gridlib

conn = sqlite3.connect('mydb.db')

########################################################################
class App1(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "List Control", size=(600,520))
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0
        
        fgs = wx.FlexGridSizer(4, 2, 9, 25)

        student_id = wx.StaticText(panel, label="Student ID")
        first_name = wx.StaticText(panel, label="First Name")
        last_name = wx.StaticText(panel, label="Last Name")
        blankLbl = wx.StaticText(panel, label="")

        self.tc1 = wx.TextCtrl(panel)
        self.tc2 = wx.TextCtrl(panel)
        self.tc3 = wx.TextCtrl(panel)
        
        searchbtn = wx.Button(panel, label="Search")
        searchbtn.Bind(wx.EVT_BUTTON, self.search_record)
    
        fgs.AddMany([(student_id), (self.tc1, 1, wx.EXPAND), (first_name), 
            (self.tc2, 1, wx.EXPAND), (last_name, 1, wx.EXPAND), (self.tc3, 1, wx.EXPAND), (blankLbl, 1, wx.EXPAND), (searchbtn, 1, wx.EXPAND)])
        #fgs.Add(addbtn)
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)
 
        self.list_ctrl = wx.ListCtrl(panel, size=(500,300),
                         style=wx.LC_REPORT
                         |wx.BORDER_SUNKEN
                         )
        self.list_ctrl.InsertColumn(0, 'Student ID')
        self.list_ctrl.SetColumnWidth(0, 100)
        self.list_ctrl.InsertColumn(1, 'First Name')
        self.list_ctrl.SetColumnWidth(1, 100)
        self.list_ctrl.InsertColumn(2, 'Last Name')
        self.list_ctrl.SetColumnWidth(2, 100)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnRowClick, self.list_ctrl)
        
        '''self.list_ctrl = wx.grid.Grid(self, size=(500,500))
        self.list_ctrl.CreateGrid(50, 5)
        
        #self.list_ctrl.SetRowSize(0, 60)
        #self.list_ctrl.SetColSize(0, 120)'''
        
        btn = wx.Button(panel, label="Add New Record")
        btn.Bind(wx.EVT_BUTTON, self.add_new_record)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        
        panel.SetSizer(sizer)
        self.initFromDB()
        
    def search_record(self, event):
        dbq = conn.cursor()
            
        tc1 = self.tc1.GetValue()
        tc2 = self.tc2.GetValue()
        tc3 = self.tc3.GetValue()
        
        rs = dbq.execute("SELECT * FROM student WHERE id = ?", (selectedStudentId,))    
        dataSet = rs.fetchone()
        
            
        
    def OnRowClick(self, event):
        selectedStudentId = str(self.idSet[event.GetIndex()])
        dbq = conn.cursor()
        rs = dbq.execute("SELECT * FROM student WHERE id = ?", (selectedStudentId,))    
        dataSet = rs.fetchone()
        appForm = AppForm(self, dataSet)
        print dataSet
        
    def initFromDB(self):
        dbq = conn.cursor()
        rs = dbq.execute("SELECT * FROM student")    
        dataSet = rs.fetchall()
        self.index = 0
        self.idSet = []
        for row in dataSet:
            self.list_ctrl.InsertStringItem(self.index, str(row[0]))
            self.list_ctrl.SetStringItem(self.index, 1, row[1])
            self.list_ctrl.SetStringItem(self.index, 2, row[2])  
            '''self.list_ctrl.SetCellValue(self.index, 0, str(row[0]))
            self.list_ctrl.SetCellValue(self.index, 1, row[1])
            self.list_ctrl.SetCellValue(self.index, 2, row[2])'''
            self.idSet.append(row[0])
            self.index += 1
 
    def add_new_record(self, event):
        appForm = AppForm(self) 
        
    #----------------------------------------------------------------------
    def add_line(self, event):
        line = "Line %s" % self.index
        self.list_ctrl.InsertStringItem(self.index, line)
        self.list_ctrl.SetStringItem(self.index, 1, "01/19/2010")
        self.list_ctrl.SetStringItem(self.index, 2, "USA")
        self.index += 1


class AppForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self, parent, editData = False):
        wx.Frame.__init__(self, None, wx.ID_ANY, size=(500,200))
        panel=wx.Panel(self, -1)
        self.parent = parent
        
        self.editMode = False
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        fgs = wx.FlexGridSizer(4, 2, 9, 25)

        student_id = wx.StaticText(panel, label="Student ID")
        first_name = wx.StaticText(panel, label="First Name")
        last_name = wx.StaticText(panel, label="Last Name")
        blankLbl = wx.StaticText(panel, label="")

        self.tc1 = wx.TextCtrl(panel)
        self.tc2 = wx.TextCtrl(panel)
        self.tc3 = wx.TextCtrl(panel)
        
        if editData != False:
            self.tc1.SetValue(str(editData[0]))
            self.tc2.SetValue(editData[1])
            self.tc3.SetValue(editData[2])
            self.editMode = True
            managebtn = wx.Button(panel, label="Update")
            managebtn.Bind(wx.EVT_BUTTON, self.edit_record)
        else:
            managebtn = wx.Button(panel, label="Add")
            managebtn.Bind(wx.EVT_BUTTON, self.add_record)
        
        fgs.AddMany([(student_id), (self.tc1, 1, wx.EXPAND), (first_name), 
            (self.tc2, 1, wx.EXPAND), (last_name, 1, wx.EXPAND), (self.tc3, 1, wx.EXPAND), (blankLbl, 1, wx.EXPAND), (managebtn, 1, wx.EXPAND)])
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

    def edit_record(self, event):
        try:
            dbq = conn.cursor()
            
            tc1 = self.tc1.GetValue()
            tc2 = self.tc2.GetValue()
            tc3 = self.tc3.GetValue()
            
            st = True
            
            if st == True:
                qry = dbq.execute("UPDATE student SET first_name = ?, last_name = ? WHERE id = ? ", (self.tc2.GetValue(), self.tc3.GetValue(), self.tc1.GetValue()))    
                conn.commit()
                
                self.parent.list_ctrl.DeleteAllItems()
                self.parent.initFromDB()
                self.Close(True)
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
            if val is not None:
                raise ValueError('Student ID is already exists ')
            return True    
        except ValueError as e:
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
