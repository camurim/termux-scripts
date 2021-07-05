#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

import instaloader
from getpass import getpass
import os
import re
import sys

#verificar se a URL foi informada
try:
	url = sys.argv[1]
except IndexError:
	print("Forma de uso:\n\n", sys.argv[0], "URL\n\nInforme uma URL válida\n\n")
	sys.exit()

#diretório de download
downloadDir = '/sdcard/instagram_dl'
os.chdir(downloadDir)

loader = instaloader.Instaloader(
	download_pictures=True,
	download_videos=True,
	download_video_thumbnails=False,
	download_geotags=False,
	download_comments=False,
	save_metadata=False,
	compress_json=False,
	filename_pattern='{profile}_{mediaid}'
)

expr = r'\/p\/([^\/]*)/'
found = re.search(expr, url)

if found:
	print("Baixando ", found.group(1), "...")
	post = instaloader.Post.from_shortcode(loader.context, found.group(1))
	loader.download_post(post, ".")
