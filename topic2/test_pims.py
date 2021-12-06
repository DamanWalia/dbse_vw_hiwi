import os
import time
import pims                                                     # conda install -c conda-forge pims
from moviepy.editor import VideoFileClip,concatenate_videoclips # conda install -c conda-forge moviepy
from skimage.io import imsave                                   # conda install scikit-image
import cv2.cv2 as cv2                                           # conda install -c conda-forge opencv

def get_chunk_sizes(n):
    """
    :param n: Number of images in a directory
    :return: Returns the factors for number of files
    """
    chunk_sizes = []
    for i in range(2,n+1):
        if(n%i == 0):
            chunk_sizes.append(i)
    return chunk_sizes

def test_different_chunk_size(home):
    """
    Measures the execution time to convert images to video for different frame sizes
    :param home: directory path containing image files
    :return: None
    """
    files = sorted(os.listdir(home))
    files = [home + s for s in files]

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
    """
    Compresses and converts 'chunk_size' images to a video in .avi format using MoviePy/PIMS
    :param home: directory path containing image files
    :param chunk_size: defines number of images/frames in a video
    :return: None,
    """
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

def compress_images_opencv(home,out_file, fourcc, fps):
    """
    Compresses and saves images as video based on different codec values using OpenCV
    :param home: directory path containing images
    :param out_file: video filename to save
    :param fourcc: codec values
    :param fps: frames per second
    :return: None
    """
    img_array = []
    size = (0,0)
    for filename in sorted(os.listdir(home)):
        img = cv2.imread(os.path.join(home,filename))
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(out_file, fourcc, fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def compress_videos(homedir,out_file):
    """
    Concatenate videos using PIMS/MoviePy
    :param homedir: directory path containing videos
    :param out_file: concatenated video file path
    :return: None
    """
    files = sorted(os.listdir(homedir))
    files = [homedir + s for s in files]

    start = time.time()
    videos = []
    for f in files:
        videos.append(VideoFileClip(f))

    compressed_video = concatenate_videoclips(videos)
    compressed_video.write_videofile(out_file) #the data is merged but not compressed
    end = time.time()
    print(round(end-start,2))

def compress_videos_cv(homedir, fourcc, out_file, fps, dim_x, dim_y):
    """
    Concatenate videos using OpenCV
    :param homedir: directory path of video files
    :param fourcc: codec value
    :param out_file: file path of concatenated video
    :param fps: frame per second
    :param dim_x: width of image
    :param dim_y: height of image
    :return:
    """
    files = sorted(os.listdir(homedir))
    files = [homedir + s for s in files]

    start = time.time()

    video = cv2.VideoWriter(out_file, fourcc, fps, (dim_x, dim_y))

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

def get_image(video_path,image_index, frame_file):
    """
    Decompresses a frame from video
    :param video_path: path of video input
    :param image_index: frame index
    :param frame_file: path of image file to save
    :return:
    """
    start = time.time()
    video = pims.Video(video_path)
    image = video.get_frame(image_index)
    imsave(frame_file,image)
    end = time.time()
    print('Time taken to retrieve frame {} is {} seconds'.format(image_index,round((end-start),2)))



