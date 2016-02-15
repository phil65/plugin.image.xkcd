# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import sys
import xbmc
import xbmcplugin
import xbmcgui
from resources.lib.Utils import *
from resources.lib import MiscScraper


class Main:

    def __init__(self):
        xbmc.log("version %s started" % ADDON_VERSION)
        self._parse_argv()
        if self.infos:
            for info in self.infos:
                listitems = start_info_actions(info, self.params)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE)
                if info.endswith("images"):
                    xbmcplugin.setContent(self.handle, 'images')
                else:
                    xbmcplugin.setContent(self.handle, '')
                pass_list_to_skin(name=info,
                                  data=listitems,
                                  prefix=self.params.get("prefix", ""),
                                  handle=self.handle,
                                  limit=self.params.get("limit", 20))
        else:
            items = {"todaysimages": "Today´s images",
                     "search": "Browse by offset"}
            for key, value in items.iteritems():
                li = xbmcgui.ListItem(value, iconImage='DefaultFolder.png')
                url = 'plugin://plugin.image.xkcd?info=%s' % key
                xbmcplugin.addDirectoryItem(handle=self.handle, url=url,
                                            listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(self.handle)

    def _parse_argv(self):
        args = sys.argv[2][1:]
        self.handle = int(sys.argv[1])
        self.control = "plugin"
        self.infos = []
        self.params = {"handle": self.handle,
                       "control": self.control}
        if args.startswith("---"):
            delimiter = "&"
            args = args[3:]
        else:
            delimiter = "&&"
        for arg in args.split(delimiter):
            param = arg.replace('"', '').replace("'", " ")
            if param.startswith('info='):
                self.infos.append(param[5:])
            else:
                try:
                    self.params[param.split("=")[0].lower()] = "=".join(param.split("=")[1:]).strip()
                except:
                    pass


def start_info_actions(info, params):
    log(info)
    prettyprint(params)
    if "prefix" in params and not params["prefix"].endswith('.'):
        params["prefix"] = params["prefix"] + '.'
    if info == 'todaysimages':
        return MiscScraper.get_xkcd_images()


if (__name__ == "__main__"):
    Main()
xbmc.log('finished')
