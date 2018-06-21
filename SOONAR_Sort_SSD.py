import os
from os import path
import datetime as dt
import numpy as np
import pickle
from astropy.io import fits

def write_to_fits (target_loc, sorted_array):
    #Create HDUL(ist)
    new_hdul = fits.HDUList()
    #Add (sorted) images to the .fit file
    for i in range(0,len(sorted_array)):
        new_hdul.append(fits.ImageHDU(sorted_array[i][2], sorted_array[i][1]))
    new_hdul.writeto(target_loc, overwrite = True, output_verify = "fix")

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
                #Delete .npy file
                os.remove(target_file)

def create_temp_files(folder):
    file_count = 0
    directory = os.fsencode(folder)
    #If directory SOONAR is not created
    if not os.path.exists('/Volumes/SOONAR FAST/SOONAR'):
        #create SOONAR direcotry
        os.makedirs('/Volumes/SOONAR FAST/SOONAR')
    #Iterate through .fit files in initial folder
    for file in os.listdir(directory):
        target_folder = '/Volumes/SOONAR FAST/SOONAR'
        filename = os.fsdecode(file)
        if filename.endswith(".FIT"):
            #Extract image, header, date, and time data
            FITS_file = folder+'/'+filename
            image_data = fits.getdata(FITS_file, ext=0)
            hdr = fits.open(FITS_file)[0].header
            date_str = hdr['DATE-OBS']
            time_str = hdr['TIME-OBS']
            date_time = dt.datetime.strptime(date_str+' '+time_str, '%Y-%m-%d %H:%M:%S')
            #If year folder is not created
            if not os.path.exists(target_folder+'/'+date_str[0:4]):
                #create year folder
                os.makedirs(target_folder+'/'+date_str[0:4])
            #If month folder is not created
            if not os.path.exists(target_folder+'/'+date_str[0:4]+'/'+date_str[5:7]+date_time.strftime('%b').upper()):
                #create month folder
                os.makedirs(target_folder+'/'+date_str[0:4]+'/'+date_str[5:7]+date_time.strftime('%b').upper())
            #If day folder is not created
            if not os.path.exists(target_folder+'/'+date_str[0:4]+'/'+date_str[5:7]+date_time.strftime('%b').upper()+'/'+date_str[8:10]):
                #create day folder
                os.makedirs(target_folder+'/'+date_str[0:4]+'/'+date_str[5:7]+date_time.strftime('%b').upper()+'/'+date_str[8:10])
            #Set target_folder to created directory
            target_folder = target_folder+'/'+date_str[0:4]+'/'+date_str[5:7]+date_time.strftime('%b').upper()+'/'+date_str[8:10]
            #If new solar region-observatory combination
            temp_name = hdr['OBJECT']+'-'+hdr['ORIGIN'][0:4]
            target_file = target_folder+'/'+temp_name+'.pkl'
            if not os.path.exists(target_file):
                #Create temporary .pkl file holding (unsorted) date_time, header, and image_data for that solar region-observatory combination
                save_file = open(target_file, 'wb')
                pickle.dump([[date_time], [hdr], [image_data]], save_file)
                save_file.close()
            else:
                #Add and save date_time, header, and image_data to existing temporary .pkl file for given solar region-observatory combination
                open_file = open(target_file, 'rb')
                open_array = pickle.load(open_file)
                open_file.close()
                dt_array = open_array[0]
                hdr_array = open_array[1]
                id_array = open_array[2]
                dt_array.append(date_time)
                hdr_array.append(hdr)
                id_array.append(image_data)
                save_file = open(target_file, 'wb')
                pickle.dump([dt_array, hdr_array, id_array], save_file)
                save_file.close()
            #Troubleshooting Output
            file_count += 1
            print(str(file_count)+') ' +filename)
            #print(date_time)
            #print(temp_name)

#Iterate through every directory on the SSD
for direc in os.listdir('/Volumes/SOONAR FAST'):
    #If it is a current SOONAR directory (ends with '_SOON_All')
    if (direc.endswith('_SOON_All')):
        print('/Volumes/SOONAR FAST'+'/'+direc)
        #Create temporary pickle files
        create_temp_files('/Volumes/SOONAR FAST'+'/'+direc)
print('convert .pkl to .FIT')
#Sort pickle files and write them to .FIT
convert_SOONAR_dir()
