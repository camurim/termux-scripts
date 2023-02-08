#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit, argv, stderr
from os import chdir
from os.path import join, isfile, isdir, expanduser
import re
import instaloader
import youtube_dl
import configparser

# Verificar se a URL foi informada
try:
	url = argv[1]
except IndexError:
	print("Forma de uso:\n\n", argv[0], "URL\n\nInforme uma URL válida\n\n")
	exit()

# Arquivo de configuração
home_folder = expanduser('~')
config_path = join(home_folder, '.config')
config_file = 'dlmedia.cfg'

if not isfile(join(config_path,config_file)):
    print("Config file does not exists!",file=stderr)
    exit(1)

# Configurações
config = configparser.ConfigParser()
config.read(join(config_path,config_file))

pathConfig  = config['PATH']
downloadDirInstagram =  pathConfig['downloadDirInstagram']
downloadDirYouTube =  pathConfig['downloadDirYouTube']

loginConfig = config['LOGIN_INSTAGRAM']
userName = loginConfig['userName']
password = loginConfig['password']

# Download Média
exprInstagram = r'\/(?:reel|p)\/([^\/]*)/'
exprYouTube = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'

foundInstagram = re.search(exprInstagram, url)
foundYouTube = re.search(exprYouTube, url)

# Instagram or YouTube
if foundInstagram:
    loader = instaloader.Instaloader(
        download_pictures=True,
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        filename_pattern=join(downloadDirInstagram,'{profile}_{mediaid}')
    )

    if userName and password:
        loader.login(userName, password)

    post = instaloader.Post.from_shortcode(loader.context, foundInstagram.group(1))
    loader.download_post(post, ".")
elif foundYouTube:
    ydl_opts = {
                'nocheckcertificate': True,
                'outtmpl': join(downloadDirYouTube,'%(title)s.%(ext)s')
                }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
