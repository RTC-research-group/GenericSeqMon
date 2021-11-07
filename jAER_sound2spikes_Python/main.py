import math
import os
import socket
import sys
import time

from AERzip import compressionFunctions
from pyNAVIS import MainSettings, ReportFunctions

from logFunctions import logFile, logCompressedFile

if __name__ == '__main__':
    start_time = time.time()

    # Define operation mode
    mode = "compressed"

    # Open connection to jAER
    udp_socket = None

    if mode != "compressed":
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.connect(('127.0.0.1', 8997))
    else:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(('127.0.0.1', 8991))

    # Define source settings (for compressed files)
    jAER_settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=4, timestamp_size=4,
                                 ts_tick=1, bin_size=10000)

    # Get the current project directory
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Define datasets source and destination folders
    src_directory = current_path + "/../datasets/audio/"
    if mode != "compressed":
        dst_directory = current_path + "/../datasets/events/"
    else:
        dst_directory = current_path + "/../datasets/compressedEvents/"

    # Open a file to write the comments
    sys.stdout = open(dst_directory + "/console.log", 'w')

    # Files and folders count
    files_length = 0
    folders_length = 0

    for _, dirnames, files in os.walk(src_directory):
        files_length += len(files)
        folders_length += len(dirnames)

    # More count variables
    dataset_count = 1
    file_count = 0
    total_file_count = 0

    for directory, _, files in os.walk(src_directory):
        for file_name in files:
            # Increase the file number
            file_count += 1
            total_file_count += 1

            dataset_name = os.path.relpath(directory, src_directory)

            if mode != "compressed":
                logFile(src_directory, dst_directory, dataset_name, file_name, udp_socket)
            else:
                logCompressedFile(src_directory, dst_directory, dataset_name, file_name, udp_socket, jAER_settings)

            print("File " + str(file_count) + "/" + str(len(files)) + " (folder " + str(dataset_count) +
                  "/" + str(folders_length) + ") has been processed. Total files: " + str(total_file_count) + "/" +
                  str(files_length))

            # Count update
            if file_count == len(files):
                dataset_count += 1
                file_count = 0

    # Close the UDP connection to jAER
    if mode != "compressed":
        udp_socket.close()
    else:
        udp_socket.close()

    end_time = time.time()

    '''# Generate PDF reports (compressed or uncompressed files)
    for dir_path, dir_names, file_names in os.walk(dst_directory):
        for f in file_names:
            spikes_file = compressionFunctions.loadCompressedFile(os.path.abspath(os.path.join(dir_path, f)))
            _, spikes_file, new_settings = compressionFunctions.compressedFileToSpikesFile(spikes_file, jAER_settings)

            dataset_report_path = os.path.abspath(dst_directory + "/../reports/" + os.path.basename(dir_path) + "/")

            if not os.path.exists(dataset_report_path):
                os.makedirs(dataset_report_path)

            ReportFunctions.PDF_report(spikes_file, new_settings, dataset_report_path + "/" + f + ".pdf")'''

    # Time report
    end_time = time.time()
    diff = end_time - start_time
    seconds = diff % 60
    minutes = int((diff / 60) % 60)
    hours = int((diff / (60 * 60)) % 24)
    days = math.floor(diff / (60 * 60 * 24))
    print("All files have been processed in " + str(days) + " days, " + str(hours) + " hours, "
          + str(minutes) + " minutes and " + '{0:.3f}'.format(seconds) + " seconds")

    # Shutdown
    sys.stdout.close()
    #os.system('shutdown -s')
