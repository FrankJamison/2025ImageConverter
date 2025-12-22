import sys
import os
from PIL import Image

#Grab arguments
image_folder = sys.argv[1]
output_folder = sys.argv[2]

#Check if new/ folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#Loop through Pokedex and convert images
for filename in os.listdir(image_folder):
    img = Image.open(os.path.join(image_folder, filename))
    clean_name = os.path.splitext(filename)[0]
    img.save(f'{output_folder}/{clean_name}.png', 'png')
