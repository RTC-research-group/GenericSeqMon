import sys

from playsound import playsound


def logFile(srcAudiofile, dstEventsfile, udpSocket):
    # Start logging
    command = "startlogging " + dstEventsfile
    udpSocket.send(command.encode())  # Send the command
    try:
        response = udpSocket.recv(1024)  # Buffer size is 1024 bytes
        print(response[:-3].decode())  # Print the response
    except ConnectionResetError:
        print("Cannot establish connection to jAER. Make sure you have it opened")
        sys.exit(1)

    # Play the sound
    # IMPORTANT: playsound v1.2.2
    playsound(srcAudiofile)

    # Stop logging
    command = "stoplogging"
    udpSocket.send(command.encode())  # Send the command
    try:
        response = udpSocket.recv(1024)  # Buffer size is 1024 bytes
        print(response[:-3].decode())  # Print the response
    except ConnectionResetError:
        print("Cannot establish connection to jAER. Make sure you have it opened")
        sys.exit(1)
