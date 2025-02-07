import gc
import math
import os
import socket
import sys
import time

import librosa as librosa
from AERzip import compressionFunctions
from pyNAVIS import MainSettings, ReportFunctions

from logFunctions import logFile, logCompressedFile

if __name__ == '__main__':
    # Start time
    start_time = time.time()

    # Define operation mode
    mode = "compressed"
    compressor = "ZSTD"  # TODO: Add to log functions

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
            dataset_name = os.path.relpath(directory, src_directory)

            # Increase the file number
            file_count += 1
            total_file_count += 1

            if not os.path.exists(dst_directory + dataset_name + "_aedats_" + compressor + "/" + file_name + ".aedat"):
                try:
                    if mode != "compressed":
                        logFile(src_directory, dst_directory, dataset_name, file_name, udp_socket)
                    else:
                        logCompressedFile(src_directory, dst_directory, dataset_name, file_name, udp_socket, jAER_settings)

                    print("File " + str(file_count) + "/" + str(len(files)) + " (folder " + str(dataset_count) +
                          "/" + str(folders_length) + ") has been processed. Total files: " + str(total_file_count) + "/" +
                          str(files_length))

                    # Cleaning memory
                    gc.collect()

                except Exception as e:
                    print("An exception occurred while trying to collect the data")
                    print(e)

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

    # Generate PDF reports (compressed or uncompressed files)
    for dir_path, dir_names, file_names in os.walk(dst_directory):
        for f in file_names:
            if f.endswith('.aedat'):
                dataset_rel_path = os.path.relpath(dir_path, dst_directory)
                dataset_report_path = os.path.abspath(dst_directory + "/../reports/" + dataset_rel_path + "/")

                if not os.path.exists(dataset_report_path + "/" + f + ".pdf"):
                    if not os.path.exists(dataset_report_path):
                        os.makedirs(dataset_report_path)

                    compressed_file = compressionFunctions.loadCompressedFile(os.path.abspath(os.path.join(dir_path, f)))
                    _, spikes_file, new_settings = compressionFunctions.compressedFileToSpikesFile(compressed_file, jAER_settings)

                    # TODO: What to do with invalid files?
                    try:
                        ReportFunctions.PDF_report(spikes_file, new_settings, dataset_report_path + "/" + f + ".pdf")
                    except Exception as e:
                        #os.remove(dataset_report_path + "/" + f + ".pdf")
                        print("PDF generation failed: " + dataset_rel_path + "/" + f + ".pdf")
                        print(e)

                    # Cleaning memory
                    gc.collect()

    # Time report
    end_time = time.time()
    diff = end_time - start_time
    seconds = diff % 60
    minutes = int((diff / 60) % 60)
    hours = int((diff / (60 * 60)) % 24)
    days = math.floor(diff / (60 * 60 * 24))
    print("All files have been processed in " + str(days) + " days, " + str(hours) + " hours, "
          + str(minutes) + " minutes and " + '{0:.3f}'.format(seconds) + " seconds")

    # Get total duration of audio files
    total_audio_duration = 0

    for dir_path, dir_names, file_names in os.walk(src_directory):
        for f in file_names:
            total_audio_duration += librosa.get_duration(filename=os.path.abspath(os.path.join(dir_path, f)))

    print("Total audio duration: " + '{0:.3f}'.format(total_audio_duration) + " seconds")

    # Shutdown
    sys.stdout.close()
    #os.system('shutdown -s')
