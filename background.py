import os
import shutil
import subprocess
from time import sleep
from threading import Thread

from constants import COMMANDS, MANIFEST_ENTRIES
from model import db, WaitingQueue, ProcessedVideo

BASE_PATH = "encoded"


def cast_encoder():
    thread = Thread(target=encode_background_task)
    thread.start()


def encode_background_task():
    db.connect()
    while True:
        video_queue = get_from_queue()

        if video_queue is None:
            sleep(5)
            continue

        video = video_queue.video
        filename, qualities = video.filename, video.video_qualities()
        foldername = os.path.join(BASE_PATH, filename.split('.')[0])
        create_dir(foldername)
        command = prepare_command(filename, qualities)
        succeed = execute(command)
        if not succeed:
            continue

        manifest = create_master_manifest(qualities, foldername)
        processed = ProcessedVideo(video=video, manifest=manifest)
        video_queue.delete_instance()
        processed.save()


def create_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

    os.mkdir(dir_name)


def get_from_queue():
    video_in_queue = WaitingQueue.get_or_none(WaitingQueue.id > 0)

    return video_in_queue


def prepare_command(filename, qualities):
    base_command = "ffmpeg -hide_banner -y -i {}".format(os.path.join(".\\upload", filename))
    foldername = os.path.join(BASE_PATH, filename.split('.')[0])

    encode_commands = [COMMANDS[q].format(foldername=foldername) for q in qualities]
    return "{} {}".format(base_command, ' '.join(encode_commands))


def execute(cmd):
    command = cmd.split()
    try:
        process = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(str(process.stdout))
        print(str(process.stderr))
    except AttributeError:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, _ = process.communicate()
        
    return process.returncode == 0


def create_master_manifest(qualities, foldername):
    manifest = '#EXTM3U\n#EXT-X-VERSION:3\n'
    manifest += '\n'.join([MANIFEST_ENTRIES[q] for q in qualities])

    path = os.path.join(foldername, 'master.m3u8')
    with open(path, 'w') as f:
        f.write(manifest)

    return path
