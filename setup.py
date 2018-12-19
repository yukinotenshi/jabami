import os

from model import *
from background import execute


if not os.path.exists('data.db'):
    db.connect()
    db.create_tables([Video, Quality, VideoQuality, WaitingQueue, ProcessedVideo])
    db.close()

if not os.path.exists('encoded'):
    os.mkdir('encoded')

if not os.path.exists('upload'):
    os.mkdir('upload')

if not execute("ffmpeg -h"):
    print("FFMPEG not installed! Please install ffmpeg and add it to PATH")
else:
    print("All good! Now run app.py")
