import youtube_dl, os, glob

def songlow(url):


    ydl_opts = {
        'format': 'worstaudio/worst',
        'outtmpl': '%(title)s.mp3',
        'ignoreerrors': False,
        'nonplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    print('Video downloaded...\n')

def songhigh(url):


    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.mp3',
        'ignoreerrors': False,
        'nonplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    print('Video downloaded...\n')