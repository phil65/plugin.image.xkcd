# -*- coding: utf8 -*-

# Copyright (C) 2016- Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcplugin
import xbmcgui
import random
import datetime
import routing
from resources.lib.Utils import *

plugin = routing.Plugin()

MAX_IMAGE = 1640
ITEM_PER_PAGE = 10


@plugin.route('/')
def root():
    items = [
        (plugin.url_for(todaysimages), xbmcgui.ListItem("Today´s images"), True),
        (plugin.url_for(browsebyoffset), xbmcgui.ListItem("Browse by offset"), True),
    ]
    xbmcplugin.addDirectoryItems(plugin.handle, items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/todaysimages')
def todaysimages():
    xbmcplugin.setContent(plugin.handle, 'images')
    items = get_xkcd_images(randomize=True)
    for item in items:
        add_image(item)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/browsebyoffset')
def browsebyoffset():
    xbmcplugin.setContent(plugin.handle, 'genres')
    items = []
    for i in range(0, MAX_IMAGE // ITEM_PER_PAGE):
        items.append((plugin.url_for(browsebyoffset_view, i*ITEM_PER_PAGE),
                      xbmcgui.ListItem("%s - %s" % (str(i * ITEM_PER_PAGE + 1), str((i + 1) * ITEM_PER_PAGE))),
                      True))
    xbmcplugin.addDirectoryItems(plugin.handle, items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/browsebyoffset/<offset>')
def browsebyoffset_view(offset):
    xbmcplugin.setContent(plugin.handle, 'images')
    items = get_xkcd_images(offset=int(offset))
    for item in items:
        add_image(item)
    xbmcplugin.endOfDirectory(plugin.handle)


def get_xkcd_images(limit=20, offset=0, randomize=False):
    now = datetime.datetime.now()
    filename = "xkcd%ix%ix%i" % (now.month, now.day, now.year)
    path = xbmc.translatePath("%s/%s.txt" % (ADDON_DATA_PATH, filename))
    if xbmcvfs.exists(path) and randomize:
        return read_from_file(path)
    items = []
    for i in range(0, limit):
        comic_id = random.randrange(1, MAX_IMAGE) if randomize else i + offset
        url = 'http://xkcd.com/%i/info.0.json' % comic_id
        results = get_JSON_response(url, 9999, folder="XKCD")
        if not results:
            continue
        item = {'thumb': results["img"],
                'path': results["img"],
                'label': results["title"],
                'plot': results["alt"]}
        items.append(item)
    save_to_file(content=items,
                 filename=filename,
                 path=ADDON_DATA_PATH)
    return items

if (__name__ == "__main__"):
    plugin.run()
xbmc.log('finished')
