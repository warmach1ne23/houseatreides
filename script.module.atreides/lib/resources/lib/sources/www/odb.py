# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import re
import traceback

from resources.lib.modules import client, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['odb.to']
        self.base_link = 'https://api.odb.to'
        self.movie_link = '/embed?imdb_id=%s'
        self.tv_link = '/embed?imdb_id=%s&s=%s&e=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.movie_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ODB - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ODB - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            imdb = url
            url = self.base_link + self.tv_link % (imdb, season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ODB - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            r = client.request(url, headers=headers)
            try:
                match = re.compile('iframe id="odbIframe" src="(.+?)"').findall(r)
                for url in match:
                    host = url.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].lower()
                    sources.append({
                        'source': host,
                        'quality': 'HD',
                        'language': 'en',
                        'url': url,
                        'direct': False,
                        'debridonly': False
                    })
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('ODB - Exception: \n' + str(failure))
                return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ODB - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
