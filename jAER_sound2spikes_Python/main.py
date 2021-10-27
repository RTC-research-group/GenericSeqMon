import os
import socket
import time

from pyNAVIS import MainSettings

from logFunctions import logFile, logCompressedFile

# TODO: Check all paths. Take notes

if __name__ == '__main__':
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

    # Get each folder (dataset) in source (audio) folder
    datasets = os.listdir(src_directory)

    # For each dataset get all files
    for i in datasets:
        # Get a list of all files in the dataset
        files = os.listdir(src_directory + "/" + i)

        # Read each file and convert audio information into events (through
        # jAER processing) saving it in the new events folder
        for j in files:
            if mode != "compressed":
                logFile(src_directory, dst_directory, i, j, udp_socket)
            else:
                logCompressedFile(src_directory, dst_directory, i, j, udp_socket, jAER_settings)
                # TODO: Generate plots

    # Close the UDP connection to jAER
    if mode != "compressed":
        udp_socket.close()
    else:
        udp_socket.close()
