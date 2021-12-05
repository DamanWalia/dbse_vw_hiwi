import pyguetzli
from timeit import default_timer as timer
from PIL import Image

start = timer()
# PIL image
image = Image.open("c:/Users/daman/OneDrive/Desktop/sample.png")
optimized_jpeg = pyguetzli.process_pil_image(image)
# Saving the image
output = open("c:/Users/daman/OneDrive/Desktop/optimized.jpg", "wb")
output.write(optimized_jpeg)
end = timer()
print(end - start)