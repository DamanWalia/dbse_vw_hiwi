import cv2
from timeit import default_timer as timer

start = timer()
#vidcap = cv2.VideoCapture(r'C:\Users\priya\OneDrive\Desktop\video_decompression\output_video.avi')
vidcap = cv2.VideoCapture(r'C:\Users\priya\OneDrive\Desktop\video_decompression\output_video.mp4')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(r"C:\Users\priya\OneDrive\Desktop\video_decompression\decompress_images\frame%d.png" % count, image)     # save frame as png file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1

end = timer()
print(end - start)
