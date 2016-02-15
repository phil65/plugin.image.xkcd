# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import random
import xbmc
from Utils import *
import datetime

# TVRAGE_KEY = 'VBp9BuIr5iOiBeWCFRMG'


def get_xkcd_images():
    now = datetime.datetime.now()
    filename = "xkcd%ix%ix%i" % (now.month, now.day, now.year)
    path = xbmc.translatePath(ADDON_DATA_PATH + "/" + filename + ".txt")
    if xbmcvfs.exists(path):
        return read_from_file(path)
    items = []
    for i in range(0, 25):
        try:
            url = 'http://xkcd.com/%i/info.0.json' % random.randrange(1, 1640)
            results = get_JSON_response(url, 9999, folder="XKCD")
            item = {'thumb': results["img"],
                    'path': results["img"],
                    'poster': results["img"],
                    'title': results["title"],
                    'plot': results["alt"]}
            items.append(item)
        except:
            log("Error when setting XKCD info")
    save_to_file(content=items,
                 filename=filename,
                 path=ADDON_DATA_PATH)
    return items

