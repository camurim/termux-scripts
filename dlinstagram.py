#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit, argv, stderr
from os import chdir
from os.path import join, isfile, isdir, expanduser
import re
import instaloader
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
config_file = 'dlinstagram.cfg'

if not isfile(join(config_path,config_file)):
    print("Config file does not exists!",file=stderr)
    exit(1)

# Configurações
config = configparser.ConfigParser()
config.read(join(config_path,config_file))

pathConfig  = config['PATH']
downloadDir =  pathConfig['downloadDir'] # '/sdcard/instagram_dl'

loginConfig = config['LOGIN']
userName = loginConfig['userName']
password = loginConfig['password']

# Download files
chdir(downloadDir)

loader = instaloader.Instaloader(
	download_pictures=True,
	download_videos=True,
	download_video_thumbnails=False,
	download_geotags=False,
	download_comments=False,
	save_metadata=False,
	compress_json=False,
	filename_pattern=join(downloadDir,'{profile}_{mediaid}')
)

if userName and password:
	loader.login(userName, password)

expr = r'\/(?:reel|p)\/([^\/]*)/'
found = re.search(expr, url)

if found:
	print("Baixando ", found.group(1), "...")
	post = instaloader.Post.from_shortcode(loader.context, found.group(1))
	loader.download_post(post, ".")
