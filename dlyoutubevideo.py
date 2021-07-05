#!/data/data/com.termux/files/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import youtube_dl

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Especifique a URL do vídeo")
        exit(1)

    url = sys.argv[1]

    ydl_opts = {
                'nocheckcertificate': True,
                'outtmpl': '/sdcard/youtube_dl/%(title)s.%(ext)s'
                }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    exit(0)
