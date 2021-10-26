import os
import socket

from pyNAVIS import MainSettings

from logFunctions import logFile, logCompressedFile

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
    jAER_settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=4, ts_tick=1,
                                 bin_size=10000)

    # Get the current project directory
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Define datasets source and destination folders
    folder_name = current_path + "/../datasets/audio/"
    if mode != "compressed":
        dest_folder_name = current_path + "/../datasets/events/"
    else:
        dest_folder_name = current_path + "/../datasets/compressedEvents/"

    # Get each folder (dataset) in source (audio) folder
    classes_folders = os.listdir(folder_name)

    # For each dataset get all files
    for i in classes_folders:
        # For each dataset create the associated events or compressedEvents folder
        save_folder_name = dest_folder_name + i + "_aedats/"
        if not os.path.exists(save_folder_name):
            os.makedirs(save_folder_name)

        # Get a list of all files in the dataset
        files_in_class = os.listdir(folder_name + i)

        # Read each file and convert audio information into events (through
        # jAER processing) saving it in the new events folder
        for j in files_in_class:
            if mode != "compressed":
                logFile(folder_name + i + "/" + j,
                        save_folder_name + j + ".aedat",
                        udp_socket)
            else:
                logCompressedFile(folder_name + i + "/" + j,
                                  save_folder_name + j + ".aedat",
                                  udp_socket, jAER_settings)
                # TODO: Generate plots

    # Close the UDP connection to jAER
    if mode != "compressed":
        udp_socket.close()
    else:
        udp_socket.close()
