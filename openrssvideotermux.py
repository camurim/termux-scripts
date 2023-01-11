#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import argparse
import feedparser
import pafy
import argparse

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":

   parser = argparse.ArgumentParser(description="Usage",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

   parser.add_argument("-l", "--longvideo", action="store_true", help="Get the first long video (>1h)")
   parser.add_argument("-s", "--skiptime", default = 0, type = int, help="Skip N seconds of video")
   parser.add_argument("rss", help="YouTube Chanell RSS Feed URL")
   args = vars(parser.parse_args())

   longVideo = args["longvideo"]
   rssFeedUrl = args["rss"]
   skiptime = args["skiptime"]

   NewsFeed = feedparser.parse(rssFeedUrl)
   if longVideo:
      for e in NewsFeed.entries:
         try:
            video = pafy.new(e.link)
         except:
            continue
         video_hour = int(video.duration[0:2])
         if (video_hour >= 1):
            entry = e
            break
   else:
      entry = NewsFeed.entries[0]

   if 'entry' in locals():
       logging.debug(entry.published)
       logging.debug("******")
       logging.debug(entry.summary)
       logging.debug("------News Link--------")
       logging.debug(entry.link)

       os.system("termux-open-url \"" + entry.link + "&t=" + str(skiptime) + "\"")
