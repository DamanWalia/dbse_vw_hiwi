import os
import time

import numpy as np
import pims
from moviepy.editor import VideoFileClip,concatenate_videoclips
from skimage.io import imsave, imread
import cv2.cv2 as cv2

def get_chunk_sizes(n):
    chunk_sizes = []
    for i in range(2,n+1):
        if(n%i == 0):
            chunk_sizes.append(i)
    return chunk_sizes

def test_different_chunk_size(home):
    #home = '/home/harish/CLionProjects/ingest_tiledb/Input/'
    files = sorted(os.listdir(home))
    files = [home + s for s in files]
    #print(len(files))

    factors_chunk_size = get_chunk_sizes(len(files)) #[2,4,5,8,10,20]
    exec_time = []
    output_size = []

    for f in factors_chunk_size:
        if(os.path.exists('factor_{}'.format(f)) == False):
            os.mkdir('factor_{}'.format(f))

        start = time.time()
        for i in range(0,len(files),f):
            img_sequence = files[i:i+f]
            images = pims.ImageSequence(img_sequence)
            pims.export(images, 'factor_{}/{}.avi'.format(f,i/f))
        end = time.time()
        exec_time.append(end-start)
        output_size.append(os.path.getsize('factor_{}'.format(f)))

    print('Chunk_size \t Compression_time \t Compressed_size')
    for iter in range(0,len(factors_chunk_size)):
        print('{} \t {} \t {}'.format(factors_chunk_size[iter],exec_time[iter],output_size[iter]))

def compress_images(home,chunk_size):
    files = sorted(os.listdir(home))
    files = [home + s for s in files]

    if(os.path.exists('factor_{}'.format(chunk_size)) == False):
        os.mkdir('factor_{}'.format(chunk_size))

    start = time.time()
    for i in range(0,len(files),chunk_size):
        img_sequence = files[i:i+chunk_size]
        images = pims.ImageSequence(img_sequence)
        pims.export(images, 'factor_{}/{}.avi'.format(chunk_size,i/chunk_size))
    end = time.time()

    print('Compression_time: {}'.format((end-start)))

##def compress_videos():
    homedir = '/home/harish/PycharmProjects/compression/factor_360/'
    files = sorted(os.listdir(homedir))
    files = [homedir + s for s in files]

    start = time.time()
    videos = []
    for f in files:
        videos.append(VideoFileClip(f))

    compressed_video = concatenate_videoclips(videos)
    compressed_video.write_videofile('compressed_video.mp4') #the data is merged but not compressed
    end = time.time()
    print(round(end-start,2))

##def compress_videos_cv():
    homedir = '/home/harish/PycharmProjects/compression/factor_360/'
    files = sorted(os.listdir(homedir))
    files = [homedir + s for s in files]

    start = time.time()

    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # video = cv2.VideoWriter("compressed_video_mp4v.mp4", fourcc, 30, (1920, 1208))

    # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # video = cv2.VideoWriter("compressed_video_mjpg.mp4", fourcc, 30, (1920, 1208))

    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # video = cv2.VideoWriter("compressed_video_mp4v.mp4", fourcc, 30, (1920, 1208))
    #
    # fourcc = cv2.VideoWriter_fourcc(*"H264")
    # video = cv2.VideoWriter("compressed_video_h264.mp4", fourcc, 30, (1920, 1208))
    #
    # fourcc = cv2.VideoWriter_fourcc(*'PIM1')
    # video = cv2.VideoWriter("compressed_video_pim1.avi", fourcc, 30, (1920, 1208))
    #
    # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # video = cv2.VideoWriter("compressed_video_mjpg.avi", fourcc, 30, (1920, 1208))
    #
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter("compressed_video_xvid.avi", fourcc, 30, (1920, 1208))

    for f in files:
        curr_f = cv2.VideoCapture(f)
        while curr_f.isOpened():
            r, frame = curr_f.read()
            if not r:
                break
            video.write(frame)

    video.release()
    end = time.time()
    print(round(end-start,2))

def get_image(video_path,image_index):
    start = time.time()
    video = pims.Video(video_path)
    image = video.get_frame(image_index)
    imsave('frame_{}.png'.format(image_index),image)
    end = time.time()
    print('{} \t {}'.format(image_index,round(end-start,2)))
    # print('Time taken to retrieve frame {} is {} seconds'.format(image_index,(end-start)))

print('Frame_index \t Time_taken')
homedir = '/home/harish/PycharmProjects/compression/factor_360/'
files = sorted(os.listdir(homedir))
files = [homedir + s for s in files]
get_image(files[0],0)
# for i in range(359,-1,-1):
#     get_image(files[0],i)



# compress_videos()
# compress_videos_cv()
# compress_images('/home/harish/CLionProjects/ingest_tiledb/Input/',10)

