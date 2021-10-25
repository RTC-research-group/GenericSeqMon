import sys
import time

from playsound import playsound


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
