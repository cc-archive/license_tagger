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
# Copyright 2008-2009, Creative Commons, www.creativecommons.org.
# Copyright 2008-2009, Steren Giannini
# Copyright 2007, Scott Shawcroft. (portion of this code is based on Scott's work)

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
        wx.Dialog.__init__(self,parent, -1, _('Choose your license'))

        self.license = license


        self.licenseURI = self.license.GetLicenseURIString()
        self.licenseName = self.license.GetLicenseNameString()

        self.SetSize((500, 235))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #Sharing
        ashLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_ash = wx.CheckBox(self, -1, _("Allow Sharing"))
        ashLine.Add(self.cb_ash,1,wx.EXPAND)
        self.cb_ash.Bind(wx.EVT_CHECKBOX, self.OnCheck_ash )

        #Attribution
        byLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_by = wx.CheckBox(self, -1, _("Require Attribution"))
        byLine.Add(self.cb_by,1,wx.EXPAND)
        self.cb_by.Bind(wx.EVT_CHECKBOX, self.OnCheck_by )

        #Remixing
        arLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_ar = wx.CheckBox(self, -1, _("Allow Remixing"))
        arLine.Add(self.cb_ar,1,wx.EXPAND)
        self.cb_ar.Bind(wx.EVT_CHECKBOX, self.OnCheck_ar )

        #Prohibit Commercial Works
        pcwLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_pcw = wx.CheckBox(self, -1, _("Prohibit Commercial Works"))
        pcwLine.Add(self.cb_pcw,1,wx.EXPAND)
        self.cb_pcw.Bind(wx.EVT_CHECKBOX, self.OnCheck_pcw )

        #Share Alike
        saLine = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_sa = wx.CheckBox(self, -1, _("Require Others to Share-Alike"))
        saLine.Add(self.cb_sa,1,wx.EXPAND)
        self.cb_sa.Bind(wx.EVT_CHECKBOX, self.OnCheck_sa )

        #License name and URI
        licenseNameLine = wx.BoxSizer(wx.HORIZONTAL)
        licenseNameLine.Add(wx.StaticText(self, -1, _("License:")),1,wx.EXPAND)
        self.licenseNameText = wx.StaticText(self, -1, self.licenseName)
        licenseNameLine.Add(self.licenseNameText,3,wx.EXPAND)
        
        licenseURILine = wx.BoxSizer(wx.HORIZONTAL)
        licenseURILine.Add(wx.StaticText(self, -1, _("URI:")),1,wx.EXPAND)
        self.licenseURIText = wx.TextCtrl(self, -1, self.licenseURI)
        self.licenseURIText.Bind(wx.EVT_TEXT, self.OnURIChanged)
        licenseURILine.Add(self.licenseURIText,3,wx.EXPAND)

        btnsizer = wx.StdDialogButtonSizer()
        cancelbtn = wx.Button(self, wx.ID_CANCEL)
        cancelbtn.SetToolTipString(_("Go back to the previous windows without saving your changes."))
        cancelbtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        applybtn = wx.Button(self, wx.ID_OK)
        applybtn.SetToolTipString(_("Select this Creative Commons license for the file."))
        applybtn.Bind(wx.EVT_BUTTON, self.OnApply)
        applybtn.SetDefault()
        btnsizer.AddButton(applybtn)
        btnsizer.AddButton(cancelbtn)
        btnsizer.Realize()

        #Sizer
        sizer=wx.BoxSizer(wx.VERTICAL)  
        sizer.AddMany([ ashLine, byLine, arLine,
                            pcwLine, saLine ])
        sizer.Add((20,20))
        sizer.Add(licenseNameLine,0,wx.EXPAND)    
        sizer.Add(licenseURILine,0,wx.EXPAND)
        sizer.Add((20,20))
        sizer.Add(btnsizer, 0, wx.EXPAND)   

        #Border
        border=wx.BoxSizer(wx.HORIZONTAL) 
        border.Add(sizer, 1, wx.ALL, 5)

        self.SetSizer(border)

        #We define the attributes URI        
        self.attributes = ["http://creativecommons.org/ns#Attribution",
              "http://creativecommons.org/ns#Distribution",
              "http://creativecommons.org/ns#DerivativeWorks",
              "http://creativecommons.org/ns#CommercialUse",
              "http://creativecommons.org/ns#ShareAlike"]
        #We create the license chooser object : it returns license URI when we provide it some attributes.
        self.ll_chooser = liblicense.LicenseChooser(None,self.attributes)

        #We check/uncheck the checkboxes considering the license
        self.UpdateCheckboxes(self.licenseURI)

    def OnApply(self, event):
        self.license.SetLicenseURI(self.licenseURIText.GetValue())
        self.Destroy()

    def OnCancel(self, event):
        self.Destroy()

    def OnCloseWindow(self, event):
        self.Destroy()

    def UpdateCheckboxes(self,license):
        if license:
            self.current_flags= list(self.license_flags(license))
        else:
            self.current_flags=[False,False,False,False,False]
        self.cb_by.SetValue(self.current_flags[0])
        self.cb_ash.SetValue(self.current_flags[1])
        self.cb_ar.SetValue(self.current_flags[2])
        self.cb_pcw.SetValue(self.current_flags[3])
        self.cb_sa.SetValue(self.current_flags[4])
        self.CheckForDisabledCheckboxes()


    def CheckForDisabledCheckboxes(self):
        #If "Allow Remixing" is false, then "Share Alike" is False and deactivated.
        if not self.current_flags[1]:
            self.cb_by.Enable(False)
            self.cb_by.SetValue(False)            
            self.cb_ar.Enable(False)
            self.cb_ar.SetValue(False)   
            self.cb_pcw.Enable(False)
            self.cb_pcw.SetValue(False)   
            self.cb_sa.Enable(False)
            self.cb_sa.SetValue(False)   
        else:
            self.cb_by.Enable(True)          
            self.cb_ar.Enable(True)
            self.cb_pcw.Enable(True)
            self.cb_sa.Enable(True)

        if self.current_flags[2]:
            self.cb_sa.Enable(True)
        else:
            self.cb_sa.Enable(False)


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

    def OnCheck_by(self,event):
        self.OnCheckBox(event, 0)

    def OnCheck_ash(self,event):
        self.OnCheckBox(event, 1)

    def OnCheck_ar(self,event):
        self.OnCheckBox(event, 2)

    def OnCheck_pcw(self,event):
        self.OnCheckBox(event, 3)

    def OnCheck_sa(self,event):
        self.OnCheckBox(event, 4)

    def OnCheckBox(self,event,checkbox):
        self.current_flags[checkbox] = event.IsChecked()
        self.CheckForDisabledCheckboxes()
        self.UpdateLicenseURI()
        self.UpdateLicenseName()


    def OnURIChanged(self,event):
        self.licenseURI = event.GetString()
        self.UpdateLicenseName()
        self.UpdateCheckboxes(self.licenseURI)

    def UpdateLicenseName(self):
        newname = liblicense.get_name(self.licenseURI)
        if newname:
            self.licenseName = newname
            self.licenseNameText.SetLabel(self.licenseName)
        else:
            self.licenseNameText.SetLabel('')

    def UpdateLicenseURI(self):
        #These are integers
        permits = 0
        requires = 0
        prohibits = 0

        if self.current_flags[0]:
          requires += self.ll_chooser.attribute_flag("http://creativecommons.org/ns#Attribution")
        if self.current_flags[1]:
          permits += self.ll_chooser.attribute_flag("http://creativecommons.org/ns#Distribution")
        if self.current_flags[2]:
          permits += self.ll_chooser.attribute_flag("http://creativecommons.org/ns#DerivativeWorks")
        if self.current_flags[3]:
          prohibits += self.ll_chooser.attribute_flag("http://creativecommons.org/ns#CommercialUse")
        if self.current_flags[4]:
          requires += self.ll_chooser.attribute_flag("http://creativecommons.org/ns#ShareAlike")

        #grab the license from the permits, requires and prohibits integers
        licenses = self.ll_chooser.get_licenses(permits=permits, requires=requires, prohibits=prohibits)

        if licenses:
            self.licenseURI = licenses[0]
            self.licenseURIText.SetValue(self.licenseURI)
        else :
            self.licenseURI = ''
            self.licenseURIText.SetValue('')


    def GetNewLicense(self):
        return self.license

