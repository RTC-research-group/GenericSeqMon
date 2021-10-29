import os
import socket

from pyNAVIS import MainSettings

from logFunctions import logFile, logCompressedFile

if __name__ == '__main__':
    # Define operation mode
    mode = "uncompressed"

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
                # TODO: Generate plots

            print("File " + str(file_count) + "/" + str(files_length) + " in dataset " +
                  str(dataset_count) + "/" + str(datasets_length) + " has been processed\n")

    # Close the UDP connection to jAER
    if mode != "compressed":
        udp_socket.close()
    else:
        udp_socket.close()
