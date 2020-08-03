###
#       Author: Jason McDonald <JMcDon31@gmail.com>
#
#       Description: Find all jpg images in the current directory, white
#           balnce, and increase color using a similar method to GIMP. 
#
#       Comments: This program only works for jpg images currently.
#           numpy and pillow are required for this program to function.
#
#       Usage: python3 white_balance.py
#
###
from PIL import Image, ImageEnhance
import numpy as np
import os
import pathlib

# Get list of files in current directory
image_list = [f for f in os.listdir('.') if os.path.isfile(f)]

#Create directory for white balanced photos
pathlib.Path('WhiteBalanced').mkdir(parents=True, exist_ok=True)
image_list = np.sort(image_list)
for image  in image_list:
    if image.lower().endswith('.jpg'): #only balance jpg files
        print(image)
        img = Image.open(image)

        #enhance color 
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)

        exif_data = img.info['exif'] #save exif data 

        # convert image into np array so it can be manipulated
        original_img = np.asarray(img)
        final_img = np.copy(original_img)

        for i in range(3): #i stands for the channel index 
            hist, bins = np.histogram(original_img[..., i].ravel(), 256, (0, 256))
            bmin = np.min(np.where(hist>(hist.sum()*0.0005)))
            bmax = np.max(np.where(hist>(hist.sum()*0.0005)))
            final_img[...,i] = np.clip(original_img[...,i], bmin, bmax)
            final_img[...,i] = (final_img[...,i]-bmin) / (bmax - bmin) * 255

        #save image
        save_img = Image.fromarray(final_img)
        save_img.save("WhiteBalanced/"+image[:-4]+'_.jpg', exif=exif_data)
