import wx
import os.path
import sys
from wx.lib.wordwrap import wordwrap

#TODO : handle license
publisherlicenseText = "GNUGPL v2 or later"

if len(sys.argv) > 1:
    filepath = sys.argv[1]

class MainWindow(wx.Frame):

    def __init__(self):
        super(MainWindow, self).__init__(None, size=(400,200))
        self.programname = 'License Tagger'
        self.dirname = '.'
        self.filename = ''
        self.CreateInteriorWindowComponents()
        self.CreateExteriorWindowComponents()

    def CreateInteriorWindowComponents(self):
        self.sizer=wx.BoxSizer(wx.VERTICAL)                 
        self.license = ''
        self.author = ''
        self.title = ''
        self.CreateLicenseInfo()
        self.CreateSaveDoneButtons()
        self.SetSizer(self.sizer)
        
    def CreateSaveDoneButtons(self):
        self.buttonsbox = wx.BoxSizer(wx.HORIZONTAL)
        exit=wx.Button(self, 100, "&Exit")
        exit.Bind(wx.EVT_BUTTON, self.OnExit)
        self.buttonsbox.Add(exit,1,wx.EXPAND)
        save=wx.Button(self, 101, "&Save")
        save.Bind(wx.EVT_BUTTON, self.OnSave)
        self.buttonsbox.Add(save,1,wx.EXPAND)
        #TODO : remove====
        test=wx.Button(self, 100, "&Test")
        test.Bind(wx.EVT_BUTTON, self.OnTest)
        self.buttonsbox.Add(test,1,wx.EXPAND)
        #==================
        self.sizer.Add(self.buttonsbox,0,wx.EXPAND)

    def CreateLicenseInfo(self):
        self.licenseInfoBox = wx.BoxSizer(wx.VERTICAL)

        self.licenseInfoBox.Add(wx.StaticText(self, -1, self.filename),0,wx.EXPAND)

        self.licenseLine = wx.BoxSizer(wx.HORIZONTAL)
        self.licenseLine.Add(wx.StaticText(self, -1, "License: "),1,wx.EXPAND) #TODO: bold
        self.licenseText = wx.StaticText(self, -1, self.license)
        self.licenseLine.Add(self.licenseText,1,wx.EXPAND)
        self.licenseInfoBox.Add(self.licenseLine,0,wx.EXPAND)

        self.titleLine = wx.BoxSizer(wx.HORIZONTAL)
        self.titleLine.Add(wx.StaticText(self, -1, "Title: "),1,wx.EXPAND) #TODO: set bold
        self.titleText = wx.TextCtrl(self, -1, self.title)
        self.titleLine.Add(self.titleText,1,wx.EXPAND)
        self.licenseInfoBox.Add(self.titleLine,0,wx.EXPAND)

        self.authorLine = wx.BoxSizer(wx.HORIZONTAL)
        self.authorLine.Add(wx.StaticText(self, -1, "Author: "),1,wx.EXPAND) #TODO: set bold
        self.authorText = wx.TextCtrl(self, -1, self.author)
        self.authorLine.Add(self.authorText,1,wx.EXPAND)
        self.licenseInfoBox.Add(self.authorLine,0,wx.EXPAND)
        self.sizer.Add(self.licenseInfoBox,0,wx.EXPAND)

    def UpdateLicenseInfo(self):
        self.licenseName.SetLabel("License: "+self.license)

    def CreateExteriorWindowComponents(self):
        self.CreateMenu()
        self.CreateStatusBar()
        self.SetTitle()

    def CreateMenu(self):
        #File Menu
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_OPEN, '&Open', 'Open a new file', self.OnOpen),
             (wx.ID_SAVE, '&Save', 'Save the current file', self.OnSave),
             (wx.ID_SAVEAS, 'Save &As', 'Save the file under a different name',
                self.OnSaveAs),
             (None, None, None, None),
             (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        #Help Menu
        helpMenu = wx.Menu()
        about = helpMenu.Append(wx.ID_ABOUT,'&About','Information about this program')
        self.Bind(wx.EVT_MENU, self.OnAbout, about)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(helpMenu, '&Help')
        self.SetMenuBar(menuBar)

    def SetTitle(self):
        # MainWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        super(MainWindow, self).SetTitle(self.programname + ' ' + self.filename)


    # Helper methods:

    def defaultFileDialogOptions(self):
        ''' Return a dictionary with file dialog options that can be
            used in both the save file dialog as well as in the open
            file dialog. '''
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.*')

    def askUserForFilename(self, **dialogOptions):
        dialog = wx.FileDialog(self, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.SetTitle() # Update the window title with the new filename
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename


    # Event handlers:

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = self.programname
        info.Version = "0.1"
        info.Copyright = "(C) 2008 Creative Commons"
        info.Description = wordwrap(
            "A \"hello world\" program is a software program that prints out "
            "\"Hello world!\" on a display device. It is used in many introductory "
            "tutorials for teaching a programming language."
            
            "\n\nSuch a program is typically one of the simplest programs possible "
            "in a computer language. A \"hello world\" program can be a useful "
            "sanity test to make sure that a language's compiler, development "
            "environment, and run-time environment are correctly installed.",
            350, wx.ClientDC(self))
        info.WebSite = ("http://www.creativecommons.org", self.programname + " home page")
        info.Developers = [ "Steren Giannini" ]
        info.License = wordwrap(publisherlicenseText, 500, wx.ClientDC(self))
        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)

    def OnExit(self, event):
        self.Close()  # Close the main window.

    def OnSave(self, event):
        textfile = open(os.path.join(self.dirname, self.filename), 'w')
        textfile.write(self.license)
        textfile.close()

    #TODO remove============
    def OnTest(self, event):
        self.sizer.Clear()
        self.Update()
    #=======================

    def OnOpen(self, event):
        if self.askUserForFilename(style=wx.OPEN,
                                   **self.defaultFileDialogOptions()):
            textfile = open(os.path.join(self.dirname, self.filename), 'r')
            self.license = textfile.read()
            self.title = self.license
            self.author = self.license
            self.UpdateLicenseBox()
            textfile.close()

    def OnSaveAs(self, event):
        if self.askUserForFilename(defaultFile=self.filename, style=wx.SAVE,
                                   **self.defaultFileDialogOptions()):
            self.OnSave(event)

    def UpdateLicenseBox(self):
        self.licenseText.SetLabel(self.license)
        self.titleText.SetValue(self.title)
        self.authorText.SetValue(self.author)



app = wx.App()
frame = MainWindow()
frame.Show()
app.MainLoop()


