import sys
import time
from threading import Thread

from AERzip import compressFunctions
from playsound import playsound

# TODO: Fix variable names

collector_thread = None
data = bytearray()
end_collector_thread = False


def logFile(src_directory, dst_directory, dataset_name, file_name, udp_socket):
    # Start logging
    command = "startlogging " + dst_directory + "/" + dataset_name + "/" + file_name
    udp_socket.send(command.encode())  # Send the command
    try:
        response = udp_socket.recv(1024)  # Buffer size is 1024 bytes
        print(response[:-3].decode())  # Print the response
    except ConnectionResetError:
        print("Cannot establish connection to jAER. Make sure you have it opened")
        # TODO: Exceptions
        sys.exit(1)

    # Play the sound
    # IMPORTANT: playsound v1.2.2
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


def logCompressedFile(src_directory, dst_directory, dataset_name, file_name, udp_socket, settings):
    global collector_thread, data, end_collector_thread

    # --- Wait while data collector thread is alive ---
    start_time = time.time()
    show_message = True

    while collector_thread is not None and collector_thread.is_alive():
        if time.time() - start_time > 5 and show_message:
            show_message = False
            print("\nSomething went wrong: Unable to receive data from UDP socket...")
        time.sleep(0.1)

    # --- Disable ending of the data collector thread ---
    end_collector_thread = False

    # --- Start data collector thread ---
    print("Collecting data for file " + dataset_name + "/" + file_name)
    data = bytearray()
    collector_thread = Thread(target=collectUdpData, args=[udp_socket, ])
    collector_thread.start()

    # Play the sound
    # IMPORTANT: playsound v1.2.2
    time.sleep(0.1)
    playsound(src_directory + "/" + dataset_name + "/" + file_name)
    time.sleep(0.1)

    # Enable ending of the data collector thread
    print("Stop collecting data")
    end_collector_thread = True

    # Compress and store data with AERZip
    compressed_data = compressFunctions.compressData(data, compressor="ZSTD")
    compressFunctions.storeCompressedFile(compressed_data, dst_directory, dataset_name, file_name)


def collectUdpData(udp_socket):
    global data

    # Receive data from socket
    while not end_collector_thread:
        buffer = udp_socket.recv(1024)
        if buffer:
            data.extend(buffer)
