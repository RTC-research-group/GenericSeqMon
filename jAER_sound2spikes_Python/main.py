import os
import socket

from logFile import logFile

if __name__ == '__main__':
    # Open connection to jAER
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.connect(('127.0.0.1', 8997))

    # Get the current project directory
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Define datasets source and destination folders
    folder_name = current_path + "/../datasets/audio/"
    dest_folder_name = current_path + "/../datasets/events/"

    # Get each folder (dataset) in source (audio) folder
    classes_folders = os.listdir(folder_name)

    # For each dataset get all files
    for i in classes_folders:
        # For each dataset create the associated events folder
        save_folder_name = dest_folder_name + i + "_aedats/"
        if not os.path.exists(save_folder_name):
            os.mkdir(save_folder_name)

        # Get a list of all files in the dataset
        files_in_class = os.listdir(folder_name + i)

        # Read each file and convert audio information into events (through
        # jAER processing) saving it in the new events folder
        for j in files_in_class:
            logFile(folder_name + i + "/" + j,
                    save_folder_name + j,
                    udpSocket)

    # Close the UDP connection to jAER
    udpSocket.close()
