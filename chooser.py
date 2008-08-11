import wx
import os.path
import sys
from wx.lib.wordwrap import wordwrap

import liblicense

#TODO
#check wxSizer* wxDialog::CreateButtonSizer  	(  	long   	 flags  	 )   
# for standard button
class LicenseChooser(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,parent, -1, 'Choose your license')

        self.licenseURI = ''
        self.licenseName = 'licensename oleole'

        self.SetSize((400, 200))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #Attribution
        byLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_by = wx.CheckBox(self, -1, "Require Attribution")
        byLine.Add(self.cb_by,1,wx.EXPAND)
        self.cb_by.Bind(wx.EVT_CHECKBOX, self.OnCheckBox )

        #Sharing
        ashLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_ash = wx.CheckBox(self, -1, "Allow Sharing")
        ashLine.Add(self.cb_ash,1,wx.EXPAND)
        self.cb_ash.Bind(wx.EVT_CHECKBOX, self.OnCheckBox )

        #Remixing
        arLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_ar = wx.CheckBox(self, -1, "Allow Remixing")
        arLine.Add(self.cb_ar,1,wx.EXPAND)
        self.cb_ar.Bind(wx.EVT_CHECKBOX, self.OnCheckBox )

        #Prohibit Commercial Works
        pcwLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_pcw = wx.CheckBox(self, -1, "Prohibit Commercial Works")
        pcwLine.Add(self.cb_pcw,1,wx.EXPAND)
        self.cb_pcw.Bind(wx.EVT_CHECKBOX, self.OnCheckBox )

        #Share Alike
        saLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_sa = wx.CheckBox(self, -1, "Require Others to Share-Alike")
        saLine.Add(self.cb_sa,1,wx.EXPAND)
        self.cb_sa.Bind(wx.EVT_CHECKBOX, self.OnCheckBox )

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
        license = self.licenseURI
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

    def OnCheckBox(self,event):
        print 'checkbox'

    def GetNewLicense(self):
        return self.licenseURI

