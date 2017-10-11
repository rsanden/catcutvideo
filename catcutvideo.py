#!/usr/bin/env python3

import sys, os
import re

FOOTAGE_DIR = './footage'
LISTFILE = './videolist.txt'
RESOLUTION = '1280x720'    # Use "SAME" to keep original

def canonicalize_time(t):
    assert t.count(':') <= 2
    if   t.count(':') == 2: h, m, s = t.split(':')
    elif t.count(':') == 1: h, m, s = [0] + t.split(':')
    elif t.count(':') == 0: h, m, s = [0, 0, t]

    if h == '': h = 0
    if m == '': m = 0
    if s == '': s = 0

    h = int(h)
    m = int(m)
    s = int(s)

    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)

def canonicalize_startend(timetup):
    start, end = timetup

    if start.strip().lower() in ('', 's', 'start'):
        start = '00:00:00'
    if end.strip().lower() in ('', 'e', 'end'):
        end = 'end'

    start = canonicalize_time(start)
    if end != 'end':
        end = canonicalize_time(end)

    return (start, end)

def vpath(videofile):
    return os.path.join(FOOTAGE_DIR, videofile)

def make_ffmpeg_cmd(videofile, timetup, N, rot):
    start, end = timetup

    end_txt = ' -to {}'.format(end)
    if end == 'end':
        end_txt = ''

    codec = 'copy'
    vf_array = []
    if RESOLUTION != 'SAME':
        vf_array = ['scale=' + RESOLUTION.replace('x', ':')]
        codec = 'libx264'

    meta_txt = ''
    if rot == 'rm0':
        meta_txt = '-metadata:s:v:0 rotate=0'
    if rot == 'rm90':
        meta_txt = '-metadata:s:v:0 rotate=90'
    if rot == 'rm180':
        meta_txt = '-metadata:s:v:0 rotate=180'
    if rot == 'rm270':
        meta_txt = '-metadata:s:v:0 rotate=-90'

    if rot == 'r90':
        vf_array += ['transpose=clock']
        meta_txt = '-metadata:s:v:0 rotate=0'
        codec = 'libx264'
    if rot == 'r180':
        vf_array += ['transpose=cclock', 'transpose=clock']
        meta_txt = '-metadata:s:v:0 rotate=0'
        codec = 'libx264'
    if rot == 'r270':
        vf_array += ['transpose=cclock_flip']
        meta_txt = '-metadata:s:v:0 rotate=0'
        codec = 'libx264'

    vf_txt = ''
    if vf_array:
        vf_txt = '-vf "{}"'.format(','.join(vf_array))

    cmd = """ ffmpeg -i {} -ss {} {} -c:a copy -c:v {} {} {} segment-{:03d}.mp4 """.format(vpath(videofile), start, end_txt, codec, vf_txt, meta_txt, N)
    return cmd

def generate_buildvideo_script(listfile):
    elements = []
    with open(listfile, 'r') as fp:
        for line in fp:
            element = None
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            pieces = line.split(maxsplit=1)
            if len(pieces) == 1:
                continue
            videofile = pieces[0]

            # Handle rotation
            rot = None
            if pieces[1].startswith('r'):
                rot, pieces[1] = re.split('[,\s]+', pieces[1], maxsplit=1)

            segments = [x.lower() for x in re.split('\s*,\s*', pieces[1])]

            if 'x' in segments:
                continue

            for segment in segments:
                if segment == 'a' or segment == 'all':
                    elements.append((videofile, '00:00:00', 'end', rot))
                    break
            else:
                for segment in segments:
                    start, end = canonicalize_startend(re.split('\s*-\s*', segment))
                    elements.append((videofile, start, end, rot))

    with open('segments.txt', 'w') as fp:
        for i, element in enumerate(elements):
            videofile, start, end, rot = element
            fp.write('file ' + 'segment-{:03d}.mp4'.format(i) + '\n')

    with open('buildvideo.bash', 'w') as fp:
        fp.write('#!/bin/bash' + '\n')
        for i, element in enumerate(elements):
            videofile, start, end, rot = element
            fp.write(make_ffmpeg_cmd(videofile, (start, end), i, rot) + '\n')
        concat_cmd = """ ffmpeg -f concat -i segments.txt -c:a copy -c:v libx264 -metadata:s:v:0 rotate=0 output.mp4 """
        fp.write(concat_cmd + '\n')

    os.chmod('buildvideo.bash', 0o755)

if __name__ == '__main__':
    generate_buildvideo_script(LISTFILE)
