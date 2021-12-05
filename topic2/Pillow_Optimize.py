import PIL
from PIL import Image
from tkinter.filedialog import *
from timeit import default_timer as timer

file_path = askopenfilename()
Image = PIL.Image.open(file_path)
save_path = asksaveasfilename()
start = timer()
height, width = Image.size
Img = Image.resize((height,width), PIL.Image.ANTIALIAS)
Img.save(save_path+"Img.png", optimize = True, quality = 0)
end = timer()
print(end - start)