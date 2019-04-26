# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @tantrumdev wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2019/4/16: Updated to use CFScrape - Still using single request
'''

import re
import traceback

from resources.lib.modules import cfscrape, client, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['hackimdb.com']
        self.base_link = 'https://hackimdb.com'
        # this still works too '/title/&%s'
        self.search_link = '/title/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('HackIMDB - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            r = client.request(url, headers=headers)
            try:
                match = re.compile('<iframe src="(.+?)"').findall(r)
                for url in match:
                    if 'youtube' in url:
                        continue
                    valid, hoster = source_utils.is_host_valid(url, hostDict)
                    if not valid:
                        continue
                    sources.append({
                        'source': hoster,
                        'quality': 'SD',
                        'language': 'en',
                        'url': url,
                        'direct': False,
                        'debridonly': False
                    })
            except Exception:
                return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('HackIMDB - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url