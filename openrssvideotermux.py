#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import argparse
import feedparser
import pafy
import traceback
import argparse

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":

   parser = argparse.ArgumentParser(description="Usage",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

   parser.add_argument("-l", "--longvideo", action="store_true", help="Takes the first video that meets the time criteria")
   parser.add_argument("-H", "--hour", default = 0, type = int, help="Minimum video size in hours (-l required)")
   parser.add_argument("-m", "--minute", default = 0, type = int, help="Minimum video size in minutes (-l required)")
   parser.add_argument("-s", "--skiptime", default = 0, type = int, help="Skip N seconds of video")
   parser.add_argument("rss", help="YouTube Chanell RSS Feed URL")
   args = vars(parser.parse_args())

   longVideo = args["longvideo"]
   videoHour = args["hour"]
   videoMinute = args["minute"]
   rssFeedUrl = args["rss"]
   skiptime = args["skiptime"]

   logging.debug("Starting reading YouTube feed...")
   NewsFeed = feedparser.parse(rssFeedUrl)
   if longVideo:
      for e in NewsFeed.entries:
         logging.debug("Video title: " + e.title)
         try:
            video = pafy.new(e.link)
         except Exception as e:
            logging.error(traceback.format_exc())
            continue

         video_hour = int(video.duration[0:2])
         video_minute = int(video.duration[3:5])

         logging.debug("Video hour: " + str(video_hour))
         logging.debug("Video minute: " + str(video_minute))
         logging.debug("----------------------------")

         if ((videoHour > 0 and video_hour >= videoHour) or (videoMinute > 0 and video_minute >= videoMinute)):
            entry = e
            break
   else:
      entry = NewsFeed.entries[0]

   logging.debug("Ending reading YouTube feed")

   if 'entry' in locals():
      logging.debug("Opening the video " + entry.title + " published at " + entry.published)

      os.system("termux-open-url \"" + entry.link + "&t=" + str(skiptime) + "\"")
   else:
      logging.debug("No video meets the criteria")
