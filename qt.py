#!/usr/bin/python
# coding: utf-8

import sys
import twitch
from PyQt4 import QtGui, QtCore


class Main():

    def __init__(self, argv):
        self.app = QtGui.QApplication(argv)
        self.twitch = twitch.TwitchApi()
        self.game_row = 10
        self.stream_row = 10
        self.quality = "best"
        x = 2500
        y = 200
        width = 900
        heigth = 300
        self.initialize(x, y, width, heigth)

    def initialize(self, x, y , width, heigth):
        self.win = QtGui.QWidget()
        self.grid = QtGui.QGridLayout()
        self.win.setLayout(self.grid)

        "table games"
        self.table_games = QtGui.QTableWidget()
        self.table_games.setColumnCount(2)
        self.table_games.setRowCount(self.game_row)
        self.table_games.setColumnWidth(0,250)
        self.table_games.verticalHeader().setVisible(False)
        self.table_games.horizontalScrollBar().setDisabled(True)
        self.table_games.horizontalScrollBar().setVisible(False)
        self.table_games.setHorizontalHeaderLabels(QtCore.QString("Name;Count;").split(";"))
        self.table_games.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        "table streams"
        self.table_streams = QtGui.QTableWidget()
        self.table_streams.setColumnCount(3)
        self.table_streams.setHorizontalHeaderLabels(QtCore.QString("Name;Title;Count;").split(";"))
        self.table_streams.setRowCount(0)
        self.table_streams.setColumnWidth(1,250)
        self.table_streams.horizontalScrollBar().setVisible(False)
        self.table_streams.verticalHeader().setVisible(False)
        self.table_streams.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        "combobox"
        self.combo_quality = QtGui.QComboBox()


        "more games"
        self.button_games = QtGui.QPushButton("Get more games")
        self.button_games.setDisabled(True)

        "more streams"
        self.button_streams = QtGui.QPushButton("Get more streams")
        self.button_streams.setDisabled(True)

        "watch"
        self.button_watch = QtGui.QPushButton("Watch")
        self.button_watch.setDisabled(True)

        "grid"
        self.grid.addWidget(self.table_games, 0, 0, 3, 2)
        self.grid.addWidget(self.table_streams, 0, 2, 3, 3)
        self.grid.addWidget(self.button_games, 3, 0, 1, 1)
        self.grid.addWidget(self.button_streams, 3, 2, 1, 1)
        self.grid.addWidget(self.combo_quality, 0, 5, 1, 1)
        self.grid.addWidget(self.button_watch, 1, 5, 1, 1)

        "events"
        self.table_games.verticalScrollBar().valueChanged.connect(self.scroll_games_event)
        self.table_games.cellClicked.connect(self.load_streamers)
        self.table_streams.cellClicked.connect(self.load_qualities)
        self.table_streams.verticalScrollBar().valueChanged.connect(self.scroll_streams_event)
        self.button_watch.clicked.connect(self.watch_stream)

        "load games"
        self.win.setGeometry(x,y, width, heigth)
        self.win.setFixedSize(width, heigth)
        self.win.setWindowTitle("PyQt")
        self.win.show()
        self.load_games()
        sys.exit(self.app.exec_())

    def scroll_games_event(self, value):
        if self.table_games.verticalScrollBar().maximum() == value:
            self.button_games.setDisabled(False)
    def scroll_streams_event(self, value):
        if self.table_streams.verticalScrollBar().maximum() == value:
            if self.table_streams.rowCount() == self.stream_row:
                self.button_streams.setDisabled(False)

    def load_games(self):
        data = self.twitch.get_games()
        i = 0
        for key in data['top']:
            name = key["game"]['name']
            viewers = key["viewers"]
            self.table_games.setItem(i, 0, QtGui.QTableWidgetItem(name))
            self.table_games.setItem(i, 1, QtGui.QTableWidgetItem(str(viewers)))
            i += 1

    def load_streamers(self, row, col):
        game = self.table_games.item(row, 0).text().replace(' ','+')
        datas = self.twitch.get_streamers(game)
        self.table_streams.setDisabled(False)
        self.stream_row = len(datas['streams'])
        self.table_streams.setRowCount(self.stream_row)
        self.table_streams.verticalScrollBar().setValue(0)
        i = 0
        for data in datas['streams']:
            name = data['channel']['name']
            title = data['channel']['status']
            viewers = data['viewers']
            self.table_streams.setItem(i, 0, QtGui.QTableWidgetItem(name))
            self.table_streams.setItem(i, 1, QtGui.QTableWidgetItem(title))
            self.table_streams.setItem(i, 2, QtGui.QTableWidgetItem(str(viewers)))
            i += 1
    def load_qualities(self, row, col):
        streamer = self.table_streams.item(row, 0).text()
        self.combo_quality.clear()
        index = 0
        for quality in self.twitch.get_qualities(streamer):
            self.combo_quality.addItem(QtCore.QString(quality))
            if quality ==  self.quality:
                self.combo_quality.setCurrentIndex(index)
            index += 1
        self.button_watch.setDisabled(False)
    def watch_stream(self, boolean):
        print self.combo_quality.currentText()

if __name__ == "__main__":
    s = Main(sys.argv)
