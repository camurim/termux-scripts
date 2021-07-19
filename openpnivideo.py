#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import feedparser
import pafy

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    NewsFeed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCzjtGnD7qqeaHW3nvDVrjQA")

    for e in NewsFeed.entries:
        video = pafy.new(e.link)
        video_hour = int(video.duration[0:2])
        if (video_hour >= 1):
            entry = e
            break 

    logging.debug(entry.published)
    logging.debug("******")
    logging.debug(entry.summary)
    logging.debug("------News Link--------")
    logging.debug(entry.link)

    os.system("termux-open-url \"" + entry.link + "\"")
