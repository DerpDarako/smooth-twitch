#!/usr/bin/python
# coding: utf-8

import sys
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import livestreamer
"""
from PyQt4 import QtGui, QtCore
import pycurl
import json
from StringIO import StringIO

def window():
    "wxapp"
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.twitch.tv/kraken/games/top?limit=10')
    c.setopt(c.HTTPHEADER,['Accept: application/vnd.twitchtv.v2+json'])
    "curl -H 'Accept: application/vnd.twitchtv.v2+json' -X GET https://api.twitch.tv/kraken/games/top"
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    data = json.loads(body)
    app = QtGui.QApplication(sys.argv)
    win = QtGui.QWidget()
    grid = QtGui.QGridLayout()
    view = QtGui.QTableWidget()
    channels = QtGui.QTableWidget()
    channels.setColumnCount(3)
    channels.setRowCount(10)

    view.setColumnCount(2)
    view.setRowCount(10)
    i = 0
    view.setHorizontalHeaderLabels(QtCore.QString("Name;Count;").split(";"))
    channels.setHorizontalHeaderLabels(QtCore.QString("Name;Title;Count;").split(";"))
    for key in data['top']:
        for cle, value in key.iteritems():
            if cle == "game":
                name = value['name']
            elif cle == "viewers":
                viewers = value
                print viewers
        view.setItem(i,0,QtGui.QTableWidgetItem(name))
        view.setItem(i,1,QtGui.QTableWidgetItem(str(viewers)))
        i +=1
    grid.addWidget(view,0,0,2,2)
    grid.addWidget(channels,0,2,2,2)
    grid.addWidget(QtGui.QPushButton("B"),1,5,1,1)
    view.verticalHeader().setVisible(False)
    win.setLayout(grid)
    win.setGeometry(2500,200,400,400)
    win.setFixedSize(450,250)
    win.setWindowTitle("PyQt")
    win.show()

    scroll = view.verticalScrollBar()
    scroll_max = scroll.maximum()
    scroll.valueChanged.connect(lambda value :scrollEvent(value, scroll_max))
    view.cellClicked.connect(lambda row, col:cellClick(row, col, view, channels))
    sys.exit(app.exec_())

def scrollEvent(value, scroll_max):
    if value == scroll_max:
        print "update"
def cellClick(row,col, view, channels):
    game= view.item(row,col).text().replace(' ','+')
    buffer = StringIO()
    c = pycurl.Curl()
    url = "https://api.twitch.tv/kraken/streams?game=%s&limit=10&broadcaster_language=fr" % (game)
    c.setopt(c.URL,url )
    c.setopt(c.HTTPHEADER,['Accept: application/vnd.twitchtv.v3+json'])
    "curl -H 'Accept: application/vnd.twitchtv.v2+json' -X GET https://api.twitch.tv/kraken/games/top"
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    data = json.loads(body)
    i = 0
    for data in data['streams']:
        for key, value in data.iteritems():
            if key == 'channel':
                name = value["name"]
                title = value["status"]
            elif key == "viewers":
                viewers = value
        channels.setItem(i,0,QtGui.QTableWidgetItem(name))
        channels.setItem(i,1,QtGui.QTableWidgetItem(title))
        channels.setItem(i,2,QtGui.QTableWidgetItem(str(viewers)))
        i += 1

if __name__ == '__main__':
    window()
