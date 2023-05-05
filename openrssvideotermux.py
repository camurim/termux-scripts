#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
import argparse
import feedparser
import traceback
import json
import urllib.request
import urllib.parse as urlparse

logging.basicConfig(level=logging.DEBUG)


def get_video_id(value):
    query = urlparse.urlparse(value)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            p = urlparse.parse_qs(query.query)
            return p["v"][0]
        if query.path[:7] == "/embed/":
            return query.path.split("/")[2]
        if query.path[:3] == "/v/":
            return query.path.split("/")[2]
    return None


def main():
    if "YT_API_KEY" not in os.environ:
        logging.error("the enviroment variable YT_API_KEY has not been defined!")
        exit(1)

    YT_API_KEY = os.environ["YT_API_KEY"]

    parser = argparse.ArgumentParser(
        description="Usage", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-l",
        "--longvideo",
        action="store_true",
        help="Takes the first video that meets the time criteria",
    )
    parser.add_argument(
        "-H",
        "--hour",
        default=0,
        type=int,
        help="Minimum video size in hours (-l required)",
    )
    parser.add_argument(
        "-m",
        "--minute",
        default=0,
        type=int,
        help="Minimum video size in minutes (-l required)",
    )
    parser.add_argument(
        "-s", "--skiptime", default=0, type=int, help="Skip N seconds of video"
    )
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

            video_id = get_video_id(e.link)
            api_key = os.environ["YT_API_KEY"]
            searchUrl = (
                "https://www.googleapis.com/youtube/v3/videos?id="
                + video_id
                + "&key="
                + api_key
                + "&part=contentDetails"
            )
            response = urllib.request.urlopen(searchUrl).read()
            data = json.loads(response)
            all_data = data["items"]
            contentDetails = all_data[0]["contentDetails"]
            duration = contentDetails["duration"]

            exp = re.search("([1-9]?[0-9]?[0-9])+H", duration)
            if exp:
                video_hour = int(exp.group(1))
            else:
                video_hour = 0

            exp = re.search("([1-9]?[0-9]?[0-9])+M", duration)
            if exp:
                video_minute = int(exp.group(1))
            else:
                video_minute = 0

            logging.debug("Video hour: " + str(video_hour))
            logging.debug("Video minute: " + str(video_minute))
            logging.debug("----------------------------")

            if (videoHour > 0 and video_hour >= videoHour) or (
                videoMinute > 0 and video_minute >= videoMinute
            ):
                entry = e
                break
    else:
        entry = NewsFeed.entries[0]

    logging.debug("Ending reading YouTube feed")

    if "entry" in locals():
        logging.debug(
            "Opening the video " + entry.title + " published at " + entry.published
        )

        completeUrl = entry.link + "&t=" + str(skiptime)
        os.system(
            'am start --user 0 -a android.intent.action.VIEW -d "%s" > /dev/null 2>&1'
            % (completeUrl)
        )
    else:
        logging.debug("No video meets the criteria")


if __name__ == "__main__":
    main()
