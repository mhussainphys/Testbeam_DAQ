import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
import glob
from bisect import bisect_left
import matplotlib.pyplot as plt

def greatest_number_less_than_value(seq,value):
    if bisect_left(seq,value)>0:
        return seq[bisect_left(seq,value)-1]
    else: return seq[0]

def new_sync_labview_files(lab_sync_abs_path, timestamp_abs_path, labview_unsync_base_path):
    #ots file 
    bool = True
    ots_time_list = np.loadtxt(timestamp_abs_path, delimiter=' ', unpack=False).tolist()
    if len(ots_time_list) != 0:        
        otstime_lines = [line.rstrip('\n') for line in open(timestamp_abs_path)]
        ots_time_start = float(otstime_lines[0])
        ots_time_stop = float(otstime_lines[len(otstime_lines) - 1])

        #labview files for start and stop
        labview_file_list = sorted([float(x.split("lab_meas_unsync_")[-1].split(".txt")[0]) for x in glob.glob(labview_unsync_base_path + "/lab_meas_unsync_*")])
        exact_labview_file_start = greatest_number_less_than_value(labview_file_list, ots_time_start)
        exact_labview_file_stop = greatest_number_less_than_value(labview_file_list, ots_time_stop)
        index_labview_file_start = labview_file_list.index(exact_labview_file_start)
        index_labview_file_stop = labview_file_list.index(exact_labview_file_stop)

        #print exact_labview_file_start, exact_labview_file_stop
        #print labview_file_list
        #Result array from all labview files between start and stop
        all_labview_array = np.array([])
        for i in range(index_labview_file_start, index_labview_file_stop + 1):
            labview_file_name = labview_unsync_base_path + "/lab_meas_unsync_%.3f.txt" % labview_file_list[i]
            labview_array = np.array(np.loadtxt(labview_file_name, delimiter='\t', unpack=False))
            if i == index_labview_file_start:
                all_labview_array = labview_array            
            else: 
                all_labview_array = np.vstack((all_labview_array, labview_array))
            if len(all_labview_array.shape) == 1:
                all_labview_array_time_list = all_labview_array[0]
            else:
                all_labview_array_time_list = all_labview_array[:,0].tolist()
 
                
        #Synchronizing both the files
        synced_array = np.array([])
        for i in range(len(ots_time_list)):
            if (not isinstance(all_labview_array_time_list,list)):
                labview_time = all_labview_array_time_list
                delta_time = labview_time - ots_time_list[i]
                if abs(delta_time) > 100:
                    labview_warning = 1
                    print "The difference in timestamps is greater than 100s, probably the instruments were off. Could be possible that the kerberos password expired for the rsync session!!!"
                    bool = False
                    return bool
                    break
                else:
                    labview_warning = 0
                    if i==0:        
                        synced_array = np.append(all_labview_array, [labview_warning, delta_time])
                    else:
                        synced_array = np.vstack((synced_array,np.append(all_labview_array, [labview_warning, delta_time])))
            else:        
                labview_time = min(all_labview_array_time_list, key=lambda x:abs(x-float(ots_time_list[i])))
                delta_time = labview_time - ots_time_list[i]
                if abs(delta_time) > 100:
                    labview_warning = 1
                    print 'The difference in timestamps is greater than 100s, probably the instruments were off!!!!!'
                    bool = False
                    return bool
                    break
                else:
                    labview_warning = 0
                    index_labview_time = all_labview_array_time_list.index(float(labview_time))    
                    if i==0:
                        synced_array = np.append(all_labview_array[index_labview_time,:], [labview_warning, delta_time])  
                    else:
                        synced_array = np.vstack((synced_array,np.append(all_labview_array[index_labview_time,:], [labview_warning, delta_time])))
        np.savetxt(lab_sync_abs_path, synced_array, delimiter=' ')         
    else:
        print 'Timestamp file is empty'
        bool = False
    return bool



def plot_labview_data(run_number):
    timestamp_abs_path = "/data/TestBeam/2018_11_November_CMSTiming/VMETimestamp/timestamp%i.txt" % run_number
    labview_unsync_base_path = "/home/otsdaq/CMSTiming_Labview/LabviewUnsyncFiles/"
    ots_time_list = np.loadtxt(timestamp_abs_path, delimiter=' ', unpack=False).tolist()
    if len(ots_time_list) != 0:        
        otstime_lines = [line.rstrip('\n') for line in open(timestamp_abs_path)]
        ots_time_start = float(otstime_lines[0])
        ots_time_stop = float(otstime_lines[len(otstime_lines) - 1])

        labview_file_list = sorted([float(x.split("lab_meas_unsync_")[-1].split(".txt")[0]) for x in glob.glob(labview_unsync_base_path + "/lab_meas_unsync_*")])
        exact_labview_file_start = greatest_number_less_than_value(labview_file_list, ots_time_start)
        exact_labview_file_stop = greatest_number_less_than_value(labview_file_list, ots_time_stop)
        index_labview_file_start = labview_file_list.index(exact_labview_file_start)
        index_labview_file_stop = labview_file_list.index(exact_labview_file_stop)
        
        all_labview_array = np.array([])
        for i in range(index_labview_file_start, index_labview_file_stop + 1):
            labview_file_name = labview_unsync_base_path + "/lab_meas_unsync_%.3f.txt" % labview_file_list[i]
            labview_array = np.array(np.loadtxt(labview_file_name, delimiter='\t', unpack=False))
            if i == index_labview_file_start:
                all_labview_array = labview_array            
            else: 
                all_labview_array = np.vstack((all_labview_array, labview_array))
        plt.plot(all_labview_array[:,0], all_labview_array[:,8], '.') #0 time, 1 sm1v, 2 sm1i, 3 sm2v, 4 sm2i....and so on
        plt.show()
    else:
        print 'Timestamp file is empty'


def plot_labview_data_norun():
        labview_unsync_base_path = "/home/otsdaq/CMSTiming_Labview/LabviewUnsyncFiles/"
        labview_file_list = sorted([float(x.split("lab_meas_unsync_")[-1].split(".txt")[0]) for x in glob.glob(labview_unsync_base_path + "/lab_meas_unsync_595964*")])        
        all_labview_array = np.array([])
        for i in range(len(labview_file_list)):
            labview_file_name = labview_unsync_base_path + "/lab_meas_unsync_%.3f.txt" % labview_file_list[i]
            labview_array = np.array(np.loadtxt(labview_file_name, delimiter='\t', unpack=False))
            if i == 0:
                all_labview_array = labview_array            
            else: 
                all_labview_array = np.vstack((all_labview_array, labview_array))
        plt.plot(all_labview_array[:,0], all_labview_array[:,7], '.') #0 time, 1 sm1v, 2 sm1i, 3 sm2v, 4 sm2i....and so on
        plt.show()
