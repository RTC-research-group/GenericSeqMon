import sys
import time
from threading import Thread

from AERzip import compressFunctions
from AERzip.CompressedFileHeader import CompressedFileHeader
from AERzip.compressFunctions import bytesToSpikesFile
from playsound import playsound

collector_thread = None
data = bytearray()
end_collector_thread = False


def logFile(src_directory, dst_directory, dataset_name, file_name, udp_socket):
    # Start logging
    command = "startlogging " + dst_directory + "/" + dataset_name + "_aedats" + "/" + file_name + ".aedat"
    udp_socket.send(command.encode())  # Send the command
    try:
        response = udp_socket.recv(1024)  # Buffer size is 1024 bytes
        print(response[:-3].decode())  # Print the response
    except ConnectionResetError:
        print("Cannot establish connection to jAER. Make sure you have it opened")
        # TODO: Exceptions
        sys.exit(1)

    # Play the sound
    time.sleep(0.1)
    playsound(src_directory + "/" + dataset_name + "/" + file_name)
    time.sleep(0.1)

    # Stop logging
    command = "stoplogging"
    udp_socket.send(command.encode())  # Send the command
    try:
        response = udp_socket.recv(1024)  # Buffer size is 1024 bytes
        print(response[:-3].decode())  # Print the response
    except ConnectionResetError:
        print("Cannot establish connection to jAER. Make sure you have it opened")
        sys.exit(1)


def logCompressedFile(src_directory, dst_directory, dataset_name, file_name, udp_socket, settings, compressor="ZSTD"):
    global collector_thread, data, end_collector_thread
    # --- Start data collector thread ---
    print("Collecting data for file " + "/" + dataset_name + "_aedats" + "/" + file_name + ".aedat")
    collector_thread = Thread(target=collectUdpData, args=[udp_socket, ])
    collector_thread.start()

    # Play the sound
    # TODO: v1.3.0 fails. Take note in the requirements of the package
    time.sleep(0.1)
    playsound(src_directory + "/" + dataset_name + "/" + file_name)
    time.sleep(0.1)

    # Enable ending of the data collector thread
    print("Stop collecting data")
    end_collector_thread = True

    # --- Wait while data collector thread is alive ---
    start_time = time.time()
    show_message = True

    while collector_thread is not None and collector_thread.is_alive():
        if time.time() - start_time > 5 and show_message:
            show_message = False
            print("\ncollector_thread is still running...")
            print("It is probably waiting to receive data from jAER UDP socket (unable to connect)")
        time.sleep(0.1)

    # --- Disable ending of the data collector thread ---
    end_collector_thread = False

    # Compress and store data with AERZip
    start_time = time.time()
    print("Compressing and storing data for file " + "/" + dataset_name + "_aedats" + "/" + file_name + ".aedat")

    address_size, timestamp_size = compressFunctions.getBytesToDiscard(settings)
    header = CompressedFileHeader(compressor, settings.address_size, settings.timestamp_size)
    # bytesToSpikesFile function needs to know data's address_size and timestamp_size
    # TODO: ----------- Compression time reduction!!! -------------
    raw_data = bytesToSpikesFile(data, dataset_name, file_name, header)
    file_data = compressFunctions.rawFileToCompressedFile(raw_data, address_size, timestamp_size, compressor)
    compressFunctions.storeCompressedFile(file_data, dst_directory, dataset_name + "_aedats", file_name + ".aedat")

    end_time = time.time()
    print("\nDone! Compressed and stored in " + '{0:.3f}'.format(end_time - start_time) + " seconds (total time)\n")


def collectUdpData(udp_socket):
    global data

    # Receive data from socket
    tmp_data = bytearray()
    while not end_collector_thread:
        buffer = udp_socket.recv(1024)
        if buffer:
            tmp_data.extend(buffer)

    # Store data
    data = tmp_data
