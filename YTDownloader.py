import os
from pytube import YouTube
from pytube.cli import on_progress
from pytube.helpers import safe_filename
import ffmpeg 
# User guide
# 1. Install ffmpeg on the computer.
# 2. Run 'pip3 install pytube ffmpeg-python' in your terminal.
# 3. Assign FFMPEG_PATH and SAVE_PATH.
# 4. Change LINK for your youtube video url, this will download the highest quality contents.

FFMPEG_PATH = r"C:\Program Files\FFMPEG\bin\ffmpeg.exe"
SAVE_PATH = r"C:\Users\jamiechang917\Desktop"
LINK = "https://www.youtube.com/watch?v=TT6gTs2B1Uw"
SAVE_INTERMEDIATED_FILE = False
#---------------------------------------------------------
BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MEGENTA = "\u001b[35m"
CYAN =  "\u001b[36m"
WHITE = "\u001b[37m"
RESET = "\u001b[0m"
#---------------------------------------------------------
TEMP_AUDIO_PATH = ""
TEMP_VIDEO_PATH = ""

def merge(audio_path, video_path, output_path):
    audio_stream = ffmpeg.input(audio_path)
    video_stream = ffmpeg.input(video_path)
    print(f"{GREEN}Merging the video and the audio...{RESET}")
    ffmpeg.output(audio_stream, video_stream, output_path).run(cmd=FFMPEG_PATH)

def download_audio(streams: YouTube.streams):
    global TEMP_AUDIO_PATH
    while True:
        print(f"{CYAN}Choose one audio{RESET}")
        audio_streams = streams.filter(adaptive=True, type="audio").order_by("abr")
        itags = {str(i.itag) for i in audio_streams}
        for i,stream in enumerate(audio_streams[::-1]):
            audio_type = stream.mime_type.split("/")[-1]
            if i == 0:
                print(f"{YELLOW}itag: {stream.itag}, type: {audio_type}, average bitrate: {stream.abr}, codec: {stream.audio_codec}{RESET}")
            else:
                print(f"itag: {stream.itag}, type: {audio_type}, average bitrate: {stream.abr}, codec: {stream.audio_codec}")
        print("To quit press q")
        itag = input(f"{CYAN}itag: {RESET}")
        if itag == 'q':
            quit()
        if itag in itags:
            stream = audio_streams.get_by_itag(itag)
            stream_type = stream.mime_type.split("/")[-1]
            stream_filename = f"temp_audio.{stream_type}"
            TEMP_AUDIO_PATH = os.path.join(SAVE_PATH, stream_filename)
            print(f"{GREEN}Downloading the audio...{RESET}")
            stream.download(output_path=SAVE_PATH, filename=stream_filename)
            print("\n============================")
            break
        print(f"{RED}Invalid itag{RESET}")
        print("============================")
    return

def download_video(streams: YouTube.streams):
    global TEMP_VIDEO_PATH
    while True:
        print(f"{CYAN}Choose one video{RESET}")
        video_streams = streams.filter(adaptive=True, type="video").order_by("resolution")
        itags = {str(i.itag) for i in video_streams}
        for i,stream in enumerate(video_streams[::-1]):
            video_type = stream.mime_type.split("/")[-1]
            if i == 0:
                print(f"{YELLOW}itag: {stream.itag}, type: {video_type}, resolution: {stream.resolution}, fps: {stream.fps}, codec: {stream.video_codec}{RESET}")
            else:
                print(f"itag: {stream.itag}, type: {video_type}, resolution: {stream.resolution}, fps: {stream.fps}, codec: {stream.video_codec}")
        print("To quit press q")
        itag = input(f"{CYAN}itag: {RESET}")
        if itag == 'q':
            quit()
        if itag in itags:
            stream = video_streams.get_by_itag(itag)
            stream_type = stream.mime_type.split("/")[-1]
            stream_filename = f"temp_video.{stream_type}"
            TEMP_VIDEO_PATH = os.path.join(SAVE_PATH, stream_filename)
            print(f"{GREEN}Downloading the video...{RESET}")
            stream.download(output_path=SAVE_PATH, filename=stream_filename)
            print("\n============================")
            break
        print(f"{RED}Invalid itag{RESET}")
        print("============================")
    return

def main():
    os.system('color')
    yt = YouTube(LINK, on_progress_callback=on_progress)
    print(f"""
============================{GREEN}
     Youtube Downloader{RESET}
============================""")
    print(f"URL: {LINK}")
    print(f"Title: {RED}{yt.title}{RESET}")
    print(f"Channel: {yt.author}")
    print("============================")
    download_audio(yt.streams)
    download_video(yt.streams)
    output_file = os.path.join(SAVE_PATH,safe_filename(yt.title)+".mp4")
    merge(TEMP_AUDIO_PATH, TEMP_VIDEO_PATH, output_file)
    if SAVE_INTERMEDIATED_FILE == False:
        os.remove(TEMP_AUDIO_PATH)
        os.remove(TEMP_VIDEO_PATH)
    print(f"{GREEN}Done (output=\"{output_file}\"){RESET}")
    
if __name__ == '__main__':
    main()