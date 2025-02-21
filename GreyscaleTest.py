from matplotlib.image import imread
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, filedialog

# Function to open a file dialog and get the image path
def get_image_path():
    # Hide the root Tkinter window
    root = Tk()
    root.withdraw()  # Hide the root window
    # Open file dialog and allow the user to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tif;*.tiff")]
    )
    return file_path

# Get the image path from the user using the file explorer
image_path = get_image_path()

# Check if the user canceled the file dialog
if not image_path:
    print("No file selected. Exiting program.")
    exit()

# Load the input image
try:
    input_image = imread(image_path)
except Exception as e:
    print(f"An error occurred while loading the image: {e}")
    exit()

# Extract the red, green, and blue channels
r, g, b = input_image[:, :, 0], input_image[:, :, 1], input_image[:, :, 2]

# Gamma correction value
gamma = 1.04

# Constants for grayscale conversion
r_const, g_const, b_const = 0.2126, 0.7152, 0.0722

# Apply gamma correction and compute grayscale
grayscale_image = r_const * r**gamma + g_const * g**gamma + b_const * b**gamma

# Normalize the grayscale image to the range [0, 1] for display
grayscale_image = grayscale_image / grayscale_image.max()

# Ask the user for a threshold value
try:
    threshold = float(input("Enter a threshold value between 0 and 1: "))
    if threshold < 0 or threshold > 1:
        raise ValueError("Threshold must be between 0 and 1.")
except ValueError as e:
    print(f"Invalid input: {e}. Using default threshold of 0.5.")
    threshold = 0.5

# Apply the threshold to create a binary image
binary_image = np.where(grayscale_image >= threshold, 1, 0)

# Create a figure with subplots
fig = plt.figure(1, figsize=(18, 12))

# Subplot 1: Original Image
img1 = fig.add_subplot(341)  # 3 rows, 4 columns, 1st subplot
img1.imshow(input_image)
img1.set_title("Original Image")

# Subplot 2: Grayscale Image
img2 = fig.add_subplot(342)  # 3 rows, 4 columns, 2nd subplot
img2.imshow(grayscale_image, cmap='gray')
img2.set_title("Grayscale Image")

# Subplot 3: Histogram of Grayscale Image
img3 = fig.add_subplot(343)  # 3 rows, 4 columns, 3rd subplot
img3.hist(grayscale_image.ravel(), bins=256, range=(0, 1), color='black', alpha=0.75)
img3.set_title("Histogram of Grayscale Image")
img3.set_xlabel("Pixel Intensity")
img3.set_ylabel("Frequency")

# Subplot 4: Binary Image
img4 = fig.add_subplot(344)  # 3 rows, 4 columns, 4th subplot
img4.imshow(binary_image, cmap='gray')
img4.set_title(f"Binary Image (Threshold = {threshold})")

# Subplot 5: Histogram of Red Channel
img5 = fig.add_subplot(345)  # 3 rows, 4 columns, 5th subplot
img5.hist(r.ravel(), bins=256, range=(0, 256), color='red', alpha=0.75)
img5.set_title("Histogram of Red Channel")
img5.set_xlabel("Pixel Intensity")
img5.set_ylabel("Frequency")

# Subplot 6: Histogram of Green Channel
img6 = fig.add_subplot(346)  # 3 rows, 4 columns, 6th subplot
img6.hist(g.ravel(), bins=256, range=(0, 256), color='green', alpha=0.75)
img6.set_title("Histogram of Green Channel")
img6.set_xlabel("Pixel Intensity")
img6.set_ylabel("Frequency")

# Subplot 7: Histogram of Blue Channel
img7 = fig.add_subplot(347)  # 3 rows, 4 columns, 7th subplot
img7.hist(b.ravel(), bins=256, range=(0, 256), color='blue', alpha=0.75)
img7.set_title("Histogram of Blue Channel")
img7.set_xlabel("Pixel Intensity")
img7.set_ylabel("Frequency")

# Subplot 8: Cumulative Histogram of Grayscale Image
img8 = fig.add_subplot(348)  # 3 rows, 4 columns, 8th subplot
img8.hist(grayscale_image.ravel(), bins=256, range=(0, 1), color='black', alpha=0.75, cumulative=True)
img8.set_title("Cumulative Histogram of Grayscale Image")
img8.set_xlabel("Pixel Intensity")
img8.set_ylabel("Cumulative Frequency")

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the figure
plt.show()