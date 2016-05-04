#!/usr/bin/python
# coding: utf-8

import pycurl
from StringIO import StringIO
import json
import livestreamer


class TwitchApi():

    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset

    def twitch_request(self, url, header):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER,[header])
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        return json.loads(body)

    def get_games(self, offset = 0):
        url = "https://api.twitch.tv/kraken/games/" \
        "top?limit=%s&offset=%s" \
        % (self.limit, offset)
        header = 'Accept: application/vnd.twitchtv.v2+json'
        return self.twitch_request(url, header)

    def get_streamers(self, game, offset = 0):
        test = 0
        if test:
            url = "https://api.twitch.tv/kraken/" \
            "streams?game=%s&limit=%s&offset=%s" \
            % (game, self.limit, offset)
        else:
            url = "https://api.twitch.tv/kraken/" \
            "streams?game=%s&limit=%s&offset=%s&broadcaster_language=fr" \
            % (game, self.limit, offset)
        header = 'Accept: application/vnd.twitchtv.v3+json'
        return self.twitch_request(url, header)

    def get_qualities(self, streamer):
        url = "https://twitch.tv/%s" % (streamer)
        streams = livestreamer.streams(url)
        return streams
