#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import feedparser

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    NewsFeed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCuiukp_wROL9PdZKm1hxSfA")

    entry = NewsFeed.entries[0]

    logging.debug(entry.published)
    logging.debug("******")
    logging.debug(entry.summary)
    logging.debug("------News Link--------")
    logging.debug(entry.link)

    os.system("termux-open-url \"" + entry.link + "\"")
