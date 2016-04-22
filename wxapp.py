#!/usr/bin/python
# coding: utf-8

import wx

import pycurl
import json
from StringIO import StringIO

class ToChange(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=wx.Size(200,200),
            style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.parent = parent
        self.initialize()


    def initialize(self):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://api.twitch.tv/kraken/games/top?limit=20')
        c.setopt(c.HTTPHEADER,['Accept: application/vnd.twitchtv.v2+json'])
        "curl -H 'Accept: application/vnd.twitchtv.v2+json' -X GET https://api.twitch.tv/kraken/games/top"
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        print body
        data = json.loads(body)



        sizer = wx.GridBagSizer()

        self.entry = wx.TextCtrl(self,-1,value=u"Enter text here.")
        sizer.Add(self.entry,(0,0),(1,1),wx.EXPAND)

        button = wx.Button(self,-1,label="Click me !")
        sizer.Add(button, (0,1))

        self.label = wx.StaticText(self,-1,label=u'Hello !')
        self.label.SetBackgroundColour(wx.BLUE)
        self.label.SetForegroundColour(wx.WHITE)
        sizer.Add( self.label, (1,0),(1,2), wx.EXPAND )


        self.list = wx.ListCtrl(self, -1,
                style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_SINGLE_SEL)
        #self.list.AppendColumn("name")
        self.list.InsertColumn(0,'name')
        self.list.InsertColumn(1,'count')
        for key in data['top']:
            for cle, value in key.iteritems():
                if cle == "game":
                    name = value['name']
                elif cle == "viewers":
                    viewers = value
            self.list.Append([name, viewers])
            """
            self.list.Append([value['_id'], value['name']])
            """
        sizer.Add(self.list, (2,0), (1,2), wx.EXPAND)

        sizer.AddGrowableCol(0)
        self.SetSizerAndFit(sizer)
        self.Show(True)

if __name__ == "__main__":

    app = wx.App()
    frame = ToChange(None,-1,'my application')
    app.MainLoop()
