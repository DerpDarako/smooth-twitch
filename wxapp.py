#!/usr/bin/python
# coding: utf-8

import wx

import pycurl
import json
from StringIO import StringIO
import livestreamer

class ToChange(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
            style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.parent = parent
        self.initialize()


    def initialize(self):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://api.twitch.tv/kraken/games/top?limit=15')
        c.setopt(c.HTTPHEADER,['Accept: application/vnd.twitchtv.v2+json'])
        "curl -H 'Accept: application/vnd.twitchtv.v2+json' -X GET https://api.twitch.tv/kraken/games/top"
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        data = json.loads(body)



        sizer = wx.GridBagSizer(hgap=5, vgap=5)


        self.label = wx.StaticText(self,-1,label=u'Hello !')
        self.label.SetBackgroundColour(wx.BLUE)
        self.label.SetForegroundColour(wx.WHITE)

        self.combo = wx.ComboBox(self, -1)

        self.to_change = wx.Button(self,-1,label="Watch")
        self.to_change.Disable()


        self.list = wx.ListCtrl(self, -1,
                style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_SINGLE_SEL)
        self.list.InsertColumn(0,'Name', width=250)
        self.list.InsertColumn(1,'Viewers')
        for key in data['top']:
            for cle, value in key.iteritems():
                if cle == "game":
                    name = value['name']
                elif cle == "viewers":
                    viewers = value
            self.list.Append([name, viewers])
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.getChannels, self.list)
        self.list.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.printAnd)

        "creation de la seconde liste"
        self.channel = wx.ListCtrl(self, -1,
                style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_SINGLE_SEL)
        self.channel.InsertColumn(0,'Name', width=100)
        self.channel.InsertColumn(1,'Title', width=500)
        self.channel.InsertColumn(2,'Viewers')


        "placement des objets sur la grille"
        sizer.Add( self.label, (1,0),(1,2), wx.EXPAND )
        sizer.Add(self.list, (2,0), (5,2), wx.EXPAND)
        sizer.Add(self.channel, (2,3), (5,2), wx.EXPAND)
        sizer.Add(self.combo, (2,5), (1,1), wx.EXPAND)
        sizer.Add(self.to_change, (3,5), (1,1), wx.EXPAND)
        self.to_change.Bind(wx.EVT_BUTTON, self.watch)

        "Modifie la taille des colonnes de la grille quand la fenetre est redimmensione"
        sizer.AddGrowableCol(0)

        "Dunno"
        self.SetSizerAndFit(sizer)
        self.Show(True)
    def getChannels(self, event):
        game = (event.GetItem().GetText()).replace(' ','+')
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://api.twitch.tv/kraken/streams?game='+game+'&limit=100')
        c.setopt(c.HTTPHEADER,['Accept: application/vnd.twitchtv.v3+json'])
        "curl -H 'Accept: application/vnd.twitchtv.v2+json' -X GET https://api.twitch.tv/kraken/games/top"
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        data = json.loads(body)
        "print data['streams']"
        self.channel.DeleteAllItems()
        for data in data['streams']:
            for key, value in data.iteritems():
                if key == 'channel':
                    name = value["name"]
                    title = value["status"]
                elif key == "viewers":
                    viewers = value
            self.channel.Append([name, title, viewers])
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.getQualities, self.channel)

    def getQualities(self, event):
        stream = event.GetText()
        streams = livestreamer.streams('https://twitch.tv/'+stream)
        self.combo.Clear()
        for quality in streams:
            self.combo.Append(quality)
        self.combo.SetValue('best')
        self.to_change.Enable()

    def printSome(self, event):
        print "j'ai select : %s" % (event.getData())

    def printEnd(self, event):
        print "je suis à la fin:("
    def printAnd(self, event):
        print "je suis à la fin oh yeah"
        print "Orientation : %s" % event.GetOrientation()
        print "Position : %s" % event.GetPosition()
        print "Range : %s" % self.list.GetScrollRange(8)
        print "hm? %s " % self.list.GetScrollThumb(8)
    def watch(self, event):
        value = self.channel.GetItemText(self.channel.GetFirstSelected())
        """
        quality = self.combo.GetSelectself.combo.GetTextSelection()
        """
        quality = self.combo.GetStringSelection()
        if not quality:
            quality="best"
        print "livestreamer https://twitch.tv/%s %s" % (value, quality)

if __name__ == "__main__":

    app = wx.App()
    frame = ToChange(None,-1,'my application')
    app.MainLoop()
