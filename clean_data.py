import os
import shutil
from astropy.io import fits

#Iterate through every .FIT files on the SSD
for subdir, dirs, files in os.walk('/Volumes/SOONAR FAST'):
    for file in files:
        target_file = subdir + os.sep + file
        broken_loc = '/Users/jeparker/Desktop/Broken Files/' + file
        if (target_file.endswith(".FIT")):
            FITS_file = target_file
            #Try to open its image and header data
            try:
                image_data = fits.getdata(FITS_file, ext=0)
                hdr = fits.open(FITS_file)[0].header
            #If this fails move the file to a separate folder
            except (OSError, TypeError):
                print(FITS_file)
                shutil.move(FITS_file, broken_loc)
                #os.remove(FITS_file)


