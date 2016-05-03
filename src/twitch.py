#!/usr/bin/python
# coding: utf-8

import pycurl
from StringIO import StringIO
import json
import livestreamer

class TwitchApi():
        def twitch_request(self, url, header):
            buffer = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.HTTPHEADER,[header])
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = buffer.getvalue()
            return json.loads(body)

        def get_games(self):
            url = 'https://api.twitch.tv/kraken/games/top?limit=10'
            header = 'Accept: application/vnd.twitchtv.v2+json'
            return self.twitch_request(url, header)

        def get_streamers(self, game):
            url = "https://api.twitch.tv/kraken/streams?game=%s&limit=10&broadcaster_language=fr" % (game)
            header = 'Accept: application/vnd.twitchtv.v3+json'
            return self.twitch_request(url, header)

        def get_qualities(self, streamer):
            url = "https://twitch.tv/%s" % (streamer)
            streams = livestreamer.streams(url)
            return streams

