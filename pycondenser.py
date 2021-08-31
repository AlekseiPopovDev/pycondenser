#!/usr/bin/env python3

"""
Tool to make condensed audio.
github.com/rin39
"""

import datetime
import os
import re
import ffmpeg
import shutil

VIDEO_EXT=('.mkv', '.mp4', '.avi', '.webm')
SUB_EXT=('.srt', '.ass')
DIRECTORY='condensed'
TEMP_DIRECTORY='condensed_temp'


def main():
    sub_files, vid_files = get_files()
    codec, audio_stream = get_audio_info(vid_files[0])
    os.mkdir(DIRECTORY)
    os.mkdir(TEMP_DIRECTORY)
    for i, subtitle in enumerate(sub_files):
        subtitles_from_file = parser(subtitle)
        extract_lines(subtitles_from_file, vid_files[i], i, codec, audio_stream)
        concat_extracted_lines(vid_files[i], i, codec)
        print(f'{vid_files[i]} is ready')
    shutil.rmtree(TEMP_DIRECTORY)


def get_audio_info(video_file):
    probe = ffmpeg.probe(video_file, select_streams='a')
    streams_n = len(probe['streams'])
    if streams_n == 1:
        codec = probe['streams'][0]['codec_name']
        audio_stream = "-map 0:1"
    else:
        for i in range(streams_n):
            print(f'{i+1}: {probe["streams"][i]["tags"]["language"]}')
        while True:
            stream = input("Select stream number: ")
            try:
                codec = probe['streams'][int(stream) - 1]['codec_name']
                audio_stream = f"-map 0:{int(stream) - 1}"
            except ValueError:
                continue
            except IndexError:
                continue
            else:
                break
    return codec, audio_stream


def concat_extracted_lines(video_file, ep, audiocodec):
    name, _ = os.path.splitext(video_file)
    voice_lines = os.listdir(f'{TEMP_DIRECTORY}/ep{ep+1}')
    voice_lines = natural_sort(voice_lines)
    concat_file = open('concat-file', 'w')
    for fragment in voice_lines:
        print(f'file {TEMP_DIRECTORY}/ep{ep+1}/{fragment}', file = concat_file)
    concat_file.close()
    os.system(f'ffmpeg -loglevel panic -f concat -i concat-file -c copy "{DIRECTORY}/{name}.{audiocodec}"')
    os.remove('concat-file')


def get_files():
    subtitle_files = []
    video_files = []
    files = [f for f in os.listdir() if os.path.isfile]
    for file in files:
        _, file_ext = os.path.splitext(file)
        is_video = any(_ == file_ext for _ in VIDEO_EXT)
        is_sub = any(_ == file_ext for _ in SUB_EXT)
        if is_video:
            video_files.append(file)
        if is_sub:
            subtitle_files.append(file)
    subtitle_files = natural_sort(subtitle_files)
    video_files = natural_sort(video_files)
    if len(subtitle_files) != len(video_files):
        raise Exception("Not equal n of subtitle and video files!")
    return subtitle_files, video_files


def natural_sort(l): #https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def parser(subtitle):
    if ".ass" in subtitle:
        DEFINER = 'Dialogue:'
        SPLITTER = ','
        START_INDEX = 1
        END_INDEX = 2
        SUBTITLE_EXT = 'ass'
    elif '.srt' in subtitle:
        DEFINER = ' --> '
        SPLITTER = ' --> '
        START_INDEX = 0
        END_INDEX = 1
        SUBTITLE_EXT = 'srt'
    else:
        raise NotImplementedError("Other subtitle formats are not supported.")
    timings = []
    with open(f'{subtitle}', 'r') as subtitle_file:
        lines = subtitle_file.readlines()
        for line in lines:
            if DEFINER in line:
                line_formatted = line.split(SPLITTER)
                if SUBTITLE_EXT == 'srt':
                    # Millisecond separator should be unified
                    sub_start = line_formatted[START_INDEX].strip().replace(',','.')
                    sub_end = line_formatted[END_INDEX].strip().replace(',','.')
                else: # ass
                    sub_start = line_formatted[START_INDEX].strip()
                    sub_end = line_formatted[END_INDEX].strip()
                timings.append([sub_start, sub_end])
        return timings


def extract_lines(subtitles, videofile_name, ep, audiocodec, audio_stream):
    os.mkdir(f'{TEMP_DIRECTORY}/ep{ep+1}')
    # In order to get quality condensed files, repeated lines and very short lines (less than 1 second) should be ignored
    prev_start = datetime.datetime.strptime('0:00:00.00', '%H:%M:%S.%f')
    prev_end = datetime.datetime.strptime('0:00:00.00', '%H:%M:%S.%f')
    MINIMAL_DURATION = datetime.datetime.strptime('0:00:01.00', '%H:%M:%S.%f')
    for i, subtitle in enumerate(subtitles):
        start = datetime.datetime.strptime(subtitle[0], '%H:%M:%S.%f')
        end = datetime.datetime.strptime(subtitle[1], '%H:%M:%S.%f')
        duration = str(end - start)
        # All timecodes should be unified
        if '.' not in duration:
            duration += '.000000'
        duration = datetime.datetime.strptime(duration, '%H:%M:%S.%f')
        if duration > MINIMAL_DURATION and prev_start != start and prev_end != end:
            os.system(f'ffmpeg -loglevel panic -i "{videofile_name}" {audio_stream} -vn -acodec copy -ss {subtitle[0]} -to {subtitle[1]} {TEMP_DIRECTORY}/ep{ep+1}/{i+1}.{audiocodec}')
        prev_start = start
        prev_end = end


main()

