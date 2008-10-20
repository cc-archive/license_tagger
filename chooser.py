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

#TODO
#check wxSizer* wxDialog::CreateButtonSizer  	(  	long   	 flags  	 )   
# for standard button
class LicenseChooser(wx.Dialog):

    def __init__(self, parent, license):
        wx.Dialog.__init__(self,parent, -1, 'Choose your license')

        self.license = license

        if self.license.GetLicense():
            self.licenseURI = self.license.GetLicense()
            self.licenseName = self.license.GetLicenseName()
        else:
            self.licenseURI = ''
            self.licenseName = ''

        self.SetSize((400, 200))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #Attribution
        byLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_by = wx.CheckBox(self, -1, "Require Attribution")
        byLine.Add(self.cb_by,1,wx.EXPAND)
        self.cb_by.Bind(wx.EVT_CHECKBOX, self.OnCheck_by )

        #Sharing
        ashLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_ash = wx.CheckBox(self, -1, "Allow Sharing")
        ashLine.Add(self.cb_ash,1,wx.EXPAND)
        self.cb_ash.Bind(wx.EVT_CHECKBOX, self.OnCheck_ash )

        #Remixing
        arLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_ar = wx.CheckBox(self, -1, "Allow Remixing")
        arLine.Add(self.cb_ar,1,wx.EXPAND)
        self.cb_ar.Bind(wx.EVT_CHECKBOX, self.OnCheck_ar )

        #Prohibit Commercial Works
        pcwLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_pcw = wx.CheckBox(self, -1, "Prohibit Commercial Works")
        pcwLine.Add(self.cb_pcw,1,wx.EXPAND)
        self.cb_pcw.Bind(wx.EVT_CHECKBOX, self.OnCheck_pcw )

        #Share Alike
        saLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_sa = wx.CheckBox(self, -1, "Require Others to Share-Alike")
        saLine.Add(self.cb_sa,1,wx.EXPAND)
        self.cb_sa.Bind(wx.EVT_CHECKBOX, self.OnCheck_sa )

        #License name and URI
        licenseNameLine = wx.BoxSizer(wx.HORIZONTAL)
        licenseNameLine.Add(wx.StaticText(self, -1, "License:"),1,wx.EXPAND)
        licenseNameText = wx.TextCtrl(self, -1, self.licenseName)
        licenseNameText.Enable(False)
        licenseNameLine.Add(licenseNameText,3,wx.EXPAND)
        
        licenseURILine = wx.BoxSizer(wx.HORIZONTAL)
        licenseURILine.Add(wx.StaticText(self, -1, "URI:"),1,wx.EXPAND)
        self.licenseURIText = wx.TextCtrl(self, -1, self.licenseURI)
        self.licenseURIText.Bind(wx.EVT_TEXT, self.OnURIChanged)
        licenseURILine.Add(self.licenseURIText,3,wx.EXPAND)

        #Apply
        applybtn=wx.Button(self, wx.ID_APPLY)
        applybtn.Bind(wx.EVT_BUTTON, self.OnApply)

        sizer=wx.BoxSizer(wx.VERTICAL)  
        sizer.AddMany([ byLine, ashLine, arLine,
                            pcwLine, saLine ])
        sizer.Add(licenseNameLine,0,wx.EXPAND)    
        sizer.Add(licenseURILine,0,wx.EXPAND)        
        sizer.Add(applybtn)
        self.SetSizer(sizer)

        #We define the attributes URI        
        self.attributes = ["http://creativecommons.org/ns#Attribution",
              "http://creativecommons.org/ns#Distribution",
              "http://creativecommons.org/ns#DerivativeWorks",
              "http://creativecommons.org/ns#CommercialUse",
              "http://creativecommons.org/ns#ShareAlike"] 

        #We check/uncheck the checkboxes considering the license
        self.update_checkboxes(self.licenseURI)

    def OnApply(self, event):
        self.license.SetLicense(self.licenseURIText.GetValue())
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
        #self.cb_ar.Enable(True)
        self.cb_pcw.SetValue(self.current_flags[3])
        self.cb_sa.SetValue(self.current_flags[4])

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

    #TODO : this is not necessary
    def ArToggled(self,event):
        """
        If "Allow Remixing" is false, then no "Share Alike" question.
        """
        print 'ARtoggled'
        if self.cb_ar.GetValue() == False:
            self.cb_sa.Enable(False)
        else :
            self.cb_sa.Enable(True)

    def OnCheck_by(self,event):
        self.OnCheckBox(event, '0')

    def OnCheck_ash(self,event):
        self.OnCheckBox(event, '1')

    def OnCheck_ar(self,event):
        self.OnCheckBox(event, '2')

    def OnCheck_pcw(self,event):
        self.OnCheckBox(event, '3')

    def OnCheck_sa(self,event):
        self.OnCheckBox(event, '4')

    def OnCheckBox(self,event,checkbox):
        print checkbox        
        print event.IsChecked()
        self.current_flags[checkbox] = event.IsChecked()
        self.UpdateLicenseURI()

    def OnURIChanged(self,event):
        print event.GetString()

    def UpdateLicenseURI(self):
        print 'update uri'   
    
    def GetNewLicense(self):
        return self.license
