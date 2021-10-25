import sys
import time
from threading import Thread

from playsound import playsound

# TODO: Fix variable names

# TODO: Install pypi package
from ...AERzip.AERzip import compressFunctions

collectorThread = None
data = bytearray()
endCollectorThread = False


def logFile(src_audiofile, dst_spikesfile, udp_socket):
    # Start logging
    command = "startlogging " + dst_spikesfile
    udp_socket.send(command.encode())  # Send the command
    try:
        response = udp_socket.recv(1024)  # Buffer size is 1024 bytes
        print(response[:-3].decode())  # Print the response
    except ConnectionResetError:
        print("Cannot establish connection to jAER. Make sure you have it opened")
        sys.exit(1)

    # Play the sound
    # IMPORTANT: playsound v1.2.2
    time.sleep(0.1)
    playsound(src_audiofile)
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


def logCompressedFile(src_audiofile, dst_spikesfile, udp_socket, settings):
    global collectorThread, data, endCollectorThread

    # --- Wait while data collector thread is alive ---
    timeIni = time.time()
    showMessage = True

    while collectorThread is not None and collectorThread.is_alive():
        if time.time() - timeIni > 5 and showMessage:
            showMessage = False
            print("\nSomething went wrong: Unable to receive data from UDP socket...")
        time.sleep(0.1)

    # --- Disable ending of the data collector thread ---
    endCollectorThread = False

    # --- Start data collector thread ---
    print("Collecting data for file " + dst_spikesfile)
    data = bytearray()
    collectorThread = Thread(target=collectUdpData, args=[udp_socket, ])
    collectorThread.start()

    # Play the sound
    # IMPORTANT: playsound v1.2.2
    time.sleep(0.1)
    playsound(src_audiofile)
    time.sleep(0.1)

    # Enable ending of the data collector thread
    print("Stop collecting data")
    endCollectorThread = True

    # Compress data with AERZip
    # TODO: compressData function definition without loading
    compressFunctions.compressAedat(events_dir, spikes_file_path, settings, returnData=False)


def collectUdpData(udp_socket):
    global data

    # Receive data from socket
    while not endCollectorThread:
        buffer = udp_socket.recv(1024)
        if buffer:
            data.extend(buffer)
