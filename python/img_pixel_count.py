from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the image
image_path = 'images/cropped_images/deskewed_0001.jpg'
image = Image.open(image_path)

# Since the questions seem to be laid out in a grid, we'll try to detect the grid pattern.
# First, we'll convert the image to grayscale and then to a numpy array.
gray_image = image.convert('L')  # convert image to grayscale
image_np = np.array(gray_image)

# Let's use matplotlib to visualize the grayscale image to decide on the crop locations
plt.imshow(image_np, cmap='gray')
plt.title('Grayscale Image')
plt.axis('on')  # Show the axis to see the extent
plt.show()
