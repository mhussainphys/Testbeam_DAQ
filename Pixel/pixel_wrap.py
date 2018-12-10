import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
import glob
import optparse
import argparse

def check(list_to_check):
    bool = True
    list_bad_elements = []
    for element in list_to_check:
        if not element.isdigit():
             list_bad_elements.append(element)
             print 'Removing %s element in the list' % element
             list_to_check.remove(element)
             bool = False
    return bool, list_to_check, list_bad_elements

#Parsing arguments                                                                                                                                                                                                
parser = argparse.ArgumentParser(description='Information for running the pixel reconstruction program')
parser.add_argument('--run_number', metavar='run_number', type=int, help='Enter the run number if you only want to combine data for a single run', required=False)
parser.add_argument('--filename_reco', metavar='filename_reco', type=str, default = 'DataVMETiming_Run', help='Full filename before the run number, This code assumes that there is nothing after the run number except .root', required=False)
parser.add_argument('--filename_pixel', metavar='filename_pixel', type=str, default = 'Pixel_Run_', help='Full filename before the run number, This code assumes that there is nothing after the run number except .txt', required=False)
parser.add_argument('--pixel_base_path', metavar='pixel_base_path', type=str, default= "/home/otsdaq/CMSTiming_Pixel/PixelFiles/network/", help = 'Pixel base path for text files (include / at the end)',required=False)
parser.add_argument('--reco_base_path', metavar='reco_base_path', type=str, default= "/data/TestBeam/2018_11_November_CMSTiming/RECO/v5_labview/", help = 'Base path for reconstructed run files (include / at theend)',required=False)
parser.add_argument('--pixel_reco_base_path', metavar='pixel_reco_base_path', type=str, default= "/data/TestBeam/2018_11_November_CMSTiming/RECO/v5_pixel_and_labview/", help = 'Base path for final reconstructedfiles having both pixel and labview data (include / at the end)',required=False)

args = parser.parse_args()
run_number = args.run_number
filename_reco = args.filename_reco
filename_pixel = args.filename_pixel
pixel_base_path = args.pixel_base_path
reco_base_path = args.reco_base_path
pixel_reco_base_path = args.pixel_reco_base_path

while(1):
    if run_number == None:
                #list of all the run numbers                                                                                                                                                                      
                list_reco_to_check = [(x.split(filename_reco)[1].split(".root")[0].split("_")[0]) for x in glob.glob('%s%s*' % (pixel_reco_base_path, filename_reco))]
                list_pixel_to_check = [(x.split(filename_pixel)[1].split(".txt")[0].split("_")[0]) for x in glob.glob('%s%s*' % (pixel_base_path, filename_pixel))]

                #Check if the list is fine                                                                                                                                                                        
                bool, list_reco, list_reco_bad_elements = check(list_reco_to_check)
                if(bool):
                    print 'The reco filenames in the list are fine.'
                else:
                    print 'The reco filenames in the list are screwed up, not processing bad file names!!!!!!!!!!!!!!'
 
                #Check if the list is fine                                                                                                                                                                        
                bool, list_pixel, list_pixel_bad_elements = check(list_pixel_to_check)
                if(bool):
                    print 'The pixel filenames in the list are fine.'
                else:
                    print 'The pixel filenames in the list are screwed up, not processing bad file names!!!!!!!!!!!!!!'
                time.sleep(5)

                #sets containing run numbers from labview reco folder and reco folder                                                                                                                             
                set_reco = set([int(x) for x in list_reco])
                set_pixel = set([int(x) for x in list_pixel])
                #set_pixel_bad_elements = set([int(x) for x in list_pixel_bad_elements])
                set_toprocess = set_pixel - set_reco
                if len(set_toprocess) == 0:
                        print 'No runs to process.'

                for x in set_toprocess:
                        #Absolute file paths                                                                                                                                                                      
                        pixel_reco_abs_path = "%s%s%d.root" % (pixel_reco_base_path,filename_reco,x)
                        reco_abs_path = "%s%s%d.root" % (reco_base_path,filename_reco,x)
                        pixel_abs_path = "%s%s%d.txt" % (pixel_base_path,filename_pixel,x)

                        #Create reco backup files for vme                                                                                                                                                         
                        os.system('cp %s %s' % (reco_abs_path, pixel_reco_abs_path))
                        
                        #call combine script for labview                                                                                                                                                          
                        os.system(''' root -l -q 'pixel_combine.C("%s","%s")' ''' % (pixel_abs_path, pixel_reco_abs_path))
                        print 'Combined pixel data with the reco file for run ', x
                print 'Going to sleep for 60 seconds...................'
                time.sleep(60)

    else:
                pixel_abs_path = "%s%s%d.txt" % (pixel_base_path,filename_pixel,run_number)
                pixel_reco_abs_path = "%s%s%d.root" % (pixel_reco_base_path,filename_reco,run_number)
                reco_abs_path = "%s%s%d.root" % (reco_base_path,filename_reco,run_number)
                #Create reco backup files for vme                                                                                                                                                         
                os.system('cp %s %s' % (reco_abs_path, pixel_reco_abs_path))
                print 'Combining the data for only a single run: ', run_number       
                os.system(''' root -l -q 'pixel_combine.C("%s","%s")' ''' % (pixel_abs_path, pixel_reco_abs_path))
                print 'Combined the data for the run: ', run_number
                break
