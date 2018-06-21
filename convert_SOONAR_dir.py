import os
import datetime as dt
import pickle
from astropy.io import fits

def convert_SOONAR_dir():
    #For every file (recusive) in SOONAR directory
    for subdir, dirs, files in os.walk('/Volumes/SOONAR FAST/SOONAR'):
        for file in files:
            target_folder = subdir + os.sep
            target_file = subdir + os.sep + file
            #If it is a .npy file
            if (target_file.endswith(".pkl")):
                print(target_file)
                #Extract data (as a list)
                open_file = open(target_file, 'rb')
                open_array = pickle.load(open_file)
                open_file.close()
                dt_array = open_array[0]
                hdr_array = open_array[1]
                id_array = open_array[2]
                #Sort data
                sorted_array = sorted (zip (dt_array, hdr_array, id_array), key=lambda x: x[0])
                #Write sorted data to a .fit file
                write_to_fits(target_folder+'/'+sorted_array[0][0].strftime('%H%M')+'-'+sorted_array[-1][0].strftime('%H%M')+'-'+file[0:9]+'.FIT', sorted_array)
                #Delete .pkl file
                os.remove(target_file)

def write_to_fits (target_loc, sorted_array):
    #Create HDUL(ist)
    new_hdul = fits.HDUList()
    #Add (sorted) images to the .fit file
    for i in range(0,len(sorted_array)):
        new_hdul.append(fits.ImageHDU(sorted_array[i][2], sorted_array[i][1]))
    new_hdul.writeto(target_loc, overwrite = True, output_verify = "fix")

convert_SOONAR_dir()
