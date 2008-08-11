#! /usr/bin/env python
# Creative Commons has made the contents of this file
# available under a CC-GNU-LGPL license:
#
# http://creativecommons.org/licenses/LGPL/2.1/
#
# A copy of the full license can be found as part of this
# distribution in the file COPYING.
# 
# You may use the liblicense software in accordance with the
# terms of that license. You agree that you are solely 
# responsible for your use of the liblicense software and you
# represent and warrant to Creative Commons that your use
# of the liblicense software will comply with the CC-GNU-LGPL.
#
# Copyright 2008, Creative Commons, www.creativecommons.org.
# Copyright 2008, Steren Giannini
# Copyright 2007, Scott Shawcroft. (portion of this code is based on Scott work)

import wx
import os.path
import sys
from wx.lib.wordwrap import wordwrap

import liblicense

import chooser

#TODO : handle license
publisherlicenseText = "GNUGPL v2 or later"

if len(sys.argv) > 1:
    filepath = sys.argv[1]
    statusMessage = ""
else :
    filepath = False
    statusMessage = "Open or drag-and-drop a file"

class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None, size=(500,250))
        self.programname = 'License Tagger'
        
        #for parameter, we split the filepath into dirname and filename
        if filepath :
            pathsplit = os.path.split(filepath)
            self.dirname = pathsplit[0]
            self.filename = pathsplit[1]
            self.license = liblicense.read(filepath)
            #TODO remove the 2 folowing lines when ReadInfo is totally OK                   
            self.author = ''
            self.title = ''
        else :
            self.dirname = '.'
            self.filename = ''
            self.license = None
            self.author = ''
            self.title = ''

        self.CreateExteriorWindowComponents()
        self.CreateInteriorWindowComponents()
        #TODO
        #for drag and drop http://docs.wxwidgets.org/trunk/overview_dnd.html and DragAndDrop.py
        #self.SetDropTarget(dt)


    def CreateInteriorWindowComponents(self):
        self.sizer=wx.BoxSizer(wx.VERTICAL)                 
        self.SetStatusText(statusMessage)
        self.CreateLicenseInfo()
        self.sizer.Add((60, 20), -1, wx.EXPAND)
        self.CreateSaveDoneButtons()
        self.SetSizer(self.sizer)
        
    def CreateSaveDoneButtons(self):
        buttonsbox = wx.BoxSizer(wx.HORIZONTAL)
        exit=wx.Button(self, wx.ID_EXIT)
        exit.Bind(wx.EVT_BUTTON, self.OnExit)
        buttonsbox.Add(exit,2,wx.EXPAND)
        buttonsbox.Add((60, 20), 1, wx.EXPAND)
        save=wx.Button(self, wx.ID_SAVE)
        save.Bind(wx.EVT_BUTTON, self.OnSave)
        buttonsbox.Add(save,2,wx.EXPAND)
        #TODO : remove====
        #test=wx.Button(self, 100, "&Test")
        #test.Bind(wx.EVT_BUTTON, self.OnTest)
        #self.buttonsbox.Add(test,1,wx.EXPAND)
        #==================
        self.sizer.Add(buttonsbox,-1,wx.EXPAND)

    def CreateLicenseInfo(self):
        licenseInfoBox = wx.BoxSizer(wx.VERTICAL)

        self.fileNameText = wx.StaticText(self, -1, self.filename)
        licenseInfoBox.Add(self.fileNameText,-1,wx.EXPAND)

        licenseCell = wx.BoxSizer(wx.HORIZONTAL)
        self.licenseText = wx.StaticText(self, -1, self.GetLicenseName())
        licenseCell.Add(self.licenseText,3,wx.EXPAND)
        self.editLicense=wx.Button(self, wx.ID_EDIT)
        self.editLicense.Bind(wx.EVT_BUTTON, self.OnEdit)
        licenseCell.Add(self.editLicense,1,wx.EXPAND)

        licenseLine = wx.BoxSizer(wx.HORIZONTAL)
        licenseLine.Add(wx.StaticText(self, -1, "License: "),1,wx.EXPAND)
        licenseLine.Add(licenseCell,2,wx.EXPAND)        

        licenseInfoBox.Add(licenseLine,-1,wx.EXPAND)

        titleLine = wx.BoxSizer(wx.HORIZONTAL)
        titleLine.Add(wx.StaticText(self, -1, "Title: "),1,wx.EXPAND)
        self.titleText = wx.TextCtrl(self, -1, self.title)
        #TODO: remove this line when title metadata works:
        self.titleText.Enable(False)
        #
        titleLine.Add(self.titleText,2,wx.EXPAND)
        licenseInfoBox.Add(titleLine,0,wx.EXPAND)

        authorLine = wx.BoxSizer(wx.HORIZONTAL)
        authorLine.Add(wx.StaticText(self, -1, "Author: "),1,wx.EXPAND)
        self.authorText = wx.TextCtrl(self, -1, self.author)
        #TODO: remove this line when title metadata works:
        self.authorText.Enable(False)
        #        
        authorLine.Add(self.authorText,2,wx.EXPAND)
        licenseInfoBox.Add(authorLine,0,wx.EXPAND)
        self.sizer.Add(licenseInfoBox,0,wx.EXPAND)



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
        title = self.programname
        if self.filename != '':
            title += ' ' + self.filename
        super(MainWindow, self).SetTitle(title)

    def UpdateLicenseBox(self):
        self.fileNameText.SetLabel(self.filename)
        self.licenseText.SetLabel(self.GetLicenseName())
        #self.titleText.SetValue(self.title)
        #self.authorText.SetValue(self.author)

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
        self.WriteLicenseData()
        self.UpdateLicenseBox()

    def OnSaveAs(self, event):
        if self.askUserForFilename(defaultFile=self.filename, style=wx.SAVE,
                                   **self.defaultFileDialogOptions()):
            self.OnSave(event)

    def OnEdit(self, event):
        win = chooser.LicenseChooser(self)
        win.CenterOnScreen()
        win.Show()
        #if (win.ShowModal() == wx.ID_OK):
        win.ShowModal()        
        newLicense = win.GetNewLicense()
        print newLicense

    #TODO remove============
    #def OnTest(self, event):
    #=======================

    def OnOpen(self, event):
        if self.askUserForFilename(style=wx.OPEN,
                                   **self.defaultFileDialogOptions()):
            self.ReadInfo()
            #self.title = self.license
            #self.author = self.license
            self.UpdateLicenseBox()
            self.SetStatusText("")

    def ReadInfo(self):
        self.license = liblicense.read(os.path.join(self.dirname, self.filename))
        print "readinfo:" + self.license

    def GetLicenseName(self):
        """
        This method returns:
        - the license name if possible
        - the license url if the name can't be found
        - (unlicensed) if no license info
        - '' if no file
        """
        if self.filename == '':
            return ''
        else :
            if self.license == None:
                return '(unlicensed)'
            elif liblicense.get_name(self.license) != None:
                return liblicense.get_name(self.license)
            else :
                return self.license

    def WriteLicenseData(self):
        #TODO: when liblicense actually works for creator and title : do it        
        #liblicense.write(os.path.join(self.dirname, self.filename), 
        #                 "http://purl.org/dc/elements/1.1/title", 
        #                 self.title)
        liblicense.write(os.path.join(self.dirname, self.filename), liblicense.LL_LICENSE,
                         self.license)

app = wx.App()
frame = MainWindow()
frame.Show()
app.MainLoop()


