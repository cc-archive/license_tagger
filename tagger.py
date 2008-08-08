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

#TODO : handle license
publisherlicenseText = "GNUGPL v2 or later"

if len(sys.argv) > 1:
    filepath = sys.argv[1]
    statusMessage = ""
else :
    statusMessage = "Open or drag-and-drop a file"


class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None, size=(500,250))
        self.programname = 'License Tagger'
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
        titleLine.Add(self.titleText,2,wx.EXPAND)
        licenseInfoBox.Add(titleLine,0,wx.EXPAND)

        authorLine = wx.BoxSizer(wx.HORIZONTAL)
        authorLine.Add(wx.StaticText(self, -1, "Author: "),1,wx.EXPAND)
        self.authorText = wx.TextCtrl(self, -1, self.author)
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
        self.fileNameText.SetLabel("Editing license metadata for " + self.filename)
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
        win = LicenseChooser(self)
        win.Show(True)

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
        liblicense.write(os.path.join(self.dirname, self.filename), 
                         "http://purl.org/dc/elements/1.1/title", 
                         self.title)
        liblicense.write(os.path.join(self.dirname, self.filename), liblicense.LL_LICENSE,
                         self.license)
    

#---------------------------------------------------------------------------
#TODO
#the best may be to use wx.Dialog and to get the result code with GetReturnCode (), check Dialog.py
class LicenseChooser(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Choose your license')

        self.licenseName = "license temp"
        self.licenseURI = "http://temp"

        self.SetSize((400, 200))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #Attribution
        byLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_by = wx.CheckBox(self, -1, "Require Attribution")
        byLine.Add(self.cb_by,1,wx.EXPAND)

        #Sharing
        ashLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_ash = wx.CheckBox(self, -1, "Allow Sharing")
        ashLine.Add(self.cb_ash,1,wx.EXPAND)

        #Remixing
        arLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_ar = wx.CheckBox(self, -1, "Allow Remixing")
        arLine.Add(self.cb_ar,1,wx.EXPAND)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnApply, self.cb_ar )

        #Prohibit Commercial Works
        pcwLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_pcw = wx.CheckBox(self, -1, "Prohibit Commercial Works")
        pcwLine.Add(self.cb_pcw,1,wx.EXPAND)

        #Share Alike
        saLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_sa = wx.CheckBox(self, -1, "Require Others to Share-Alike")
        saLine.Add(self.cb_sa,1,wx.EXPAND)

        #License name and URI
        licenseNameLine = wx.BoxSizer(wx.HORIZONTAL)
        licenseNameLine.Add(wx.StaticText(self, -1, "License:"),1,wx.EXPAND)
        licenseNameLine.Add(wx.TextCtrl(self, -1, self.licenseName),3,wx.EXPAND)

        licenseURILine = wx.BoxSizer(wx.HORIZONTAL)
        licenseURILine.Add(wx.StaticText(self, -1, "URI:"),1,wx.EXPAND)
        licenseURILine.Add(wx.TextCtrl(self, -1, self.licenseURI),3,wx.EXPAND)

        #Apply
        applybtn=wx.Button(self, wx.ID_APPLY)
        applybtn.Bind(wx.EVT_BUTTON, self.OnApply)

        sizer=wx.BoxSizer(wx.VERTICAL)  
        sizer.AddMany([ byLine, ashLine, arLine,
                            pcwLine, saLine, licenseNameLine, 
                            licenseURILine ])
        sizer.Add(applybtn)
        self.SetSizer(sizer)

        #We define the attributes URI        
        self.attributes = ["http://creativecommons.org/ns#Attribution",
              "http://creativecommons.org/ns#Distribution",
              "http://creativecommons.org/ns#DerivativeWorks",
              "http://creativecommons.org/ns#CommercialUse",
              "http://creativecommons.org/ns#ShareAlike"] 

    def OnApply(self, event):
        self.Destroy()

    def OnCloseWindow(self, event):
        self.Destroy()

    def update_checkboxes(self,license):
        if license:
            self.current_flags= list(self.license_flags(license))
        else:
            self.current_flags=[False,False,False,False,False]
        self.cb_by.SetValue(self.current_flags[0])
        self.cb_ash.SetValue(self.current_flags[1])
        self.cb_ar.SetValue(self.current_flags[2])
        self.cb_ar.Enable(True)
        self.cb_pcw.set_active(self.current_flags[3])
        self.cb_sa.set_active(self.current_flags[4])

    def license_flags(self,license):
        """
        Returns the CC flags of a given license. (compares attributes to permits/requires/prohibits)
        """
        permits = liblicense.get_permits(license)
        requires = liblicense.get_requires(license)
        prohibits = liblicense.get_prohibits(license)
        return (self.attributes[0] in requires,
                self.attributes[1] in permits,
                self.attributes[2] in permits,
                self.attributes[3] in prohibits,
                self.attributes[4] in requires)

    def ArToggled(self):
        """
        If "Allow Remixing" is false, then no "Share Alike" question.
        """
        if self.cb_ar.GetValue == False:
            self.cb_sa.Enable(False)
        else :
            self.cb_sa.Enable(True)

#---------------------------------------------------------------------------

app = wx.App()
frame = MainWindow()
frame.Show()
app.MainLoop()


