import youtube_dl, os, glob

def song(url):


    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.mp3',
        'ignoreerrors': False,
        'nonplaylist': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    print('Video downloaded...\n')