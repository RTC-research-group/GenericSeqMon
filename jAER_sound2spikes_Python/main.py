import math
import os
import socket
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
    src_directory = current_path + "/../datasets/audio"
    if mode != "compressed":
        dst_directory = current_path + "/../datasets/events"
    else:
        dst_directory = current_path + "/../datasets/compressedEvents"

    # Get a list of all datasets in source (audio) folder
    datasets = os.listdir(src_directory)
    datasets_length = len(datasets)

    # Dataset count variable
    dataset_count = 0

    # For each dataset get all files
    for i in datasets:
        # Increase the dataset count and clear the file count
        dataset_count += 1
        file_count = 0

        # Get a list of all files in the dataset and his length
        files = os.listdir(src_directory + "/" + i)
        files_length = len(files)

        # Read each file and convert audio information into events (through
        # jAER processing) saving it in the new events folder
        for j in files:
            # Increase the file number
            file_count += 1

            if mode != "compressed":
                logFile(src_directory, dst_directory, i, j, udp_socket)
            else:
                logCompressedFile(src_directory, dst_directory, i, j, udp_socket, jAER_settings)

            print("File " + str(file_count) + "/" + str(files_length) + " in dataset " +
                  str(dataset_count) + "/" + str(datasets_length) + " has been processed\n")

    # Close the UDP connection to jAER
    if mode != "compressed":
        udp_socket.close()
    else:
        udp_socket.close()

    end_time = time.time()

    # Generate PDF reports
    for dir_path, dir_names, file_names in os.walk(dst_directory):
        for f in file_names:
            spikes_file = compressionFunctions.loadCompressedFile(os.path.abspath(os.path.join(dir_path, f)))
            _, spikes_file, new_settings = compressionFunctions.compressedFileToSpikesFile(spikes_file, jAER_settings)

            dataset_report_path = os.path.abspath(dst_directory + "/../reports/" + os.path.basename(dir_path) + "/")

            if not os.path.exists(dataset_report_path):
                os.makedirs(dataset_report_path)

            ReportFunctions.PDF_report(spikes_file, new_settings, dataset_report_path + "/" + f + ".pdf")

    diff = end_time - start_time
    seconds = int(diff % 60)
    minutes = int(diff % (60 * 60))
    hours = int(diff % (60 * 60 * 24))
    days = int(math.floor(diff / (60 * 60 * 24)))
    print("All files have been processed in " + str(days) + " days, " + str(hours) + " hours, "
          + str(minutes) + " minutes and " + str(diff) + " seconds")
