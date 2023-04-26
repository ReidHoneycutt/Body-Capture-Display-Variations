import socket
import cv2
import time
import math
from cvzone.PoseModule import PoseDetector
import cv2


# initialize the video capture, detector, and socket objects
def init_cap():
    cap = cv2.VideoCapture(0)
    return cap


def init_detector():
    detector = PoseDetector()
    return detector


def init_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))  # the 5000 is the server ip that client is going to connect to.
    s.listen(5)  # the queue
    return s


# functions to establish the client, and to send to the client
def getClient(s):
    while True:
        clientsocket, Address = s.accept()
        print(f'IP Address [{Address}] has connect to the server')
        if clientsocket:
            return clientsocket


def send(clientsocket, packet):
    clientsocket.send(packet)


# constructs the packet of hand data to send to the client
# the delimiter "@" seperates the coordinates, and the delimiter ":" seperates the two components of each coordinate
def msg_construction(data, max_w, max_h):
    num_hands = 0
    num_landmarks = 0
    packet = ""
    # if any hands  are recognized, create a packet containing the byte representation of the total data length, number of hands, and number of landmarks
    # the structure of a packet is "total data length + number of hands + number of landmarks + data of the hand coordinates"
    if len(data) > 0:
        num_hands = 1
        num_landmarks += len(data)
        for i in range(len(data)):
            if i < len(data) - 1:
                packet += str(round(data[i][1] / max_w, 2)) + ":" + str(round(data[i][2] / max_h, 2)) + "@"
            else:
                packet += str(round(data[i][1] / max_w, 2)) + ":" + str(round(data[i][2] / max_h, 2))


    data_len = len(packet).to_bytes(4, "big", signed=False)
    num_hands = num_hands.to_bytes(1, "big", signed=False)
    num_landmarks = num_landmarks.to_bytes(1, "big", signed=False)
    data = packet.encode("utf-8")
    packet = data_len + num_hands + num_landmarks + data
    return packet


# the function which runs continually throughout, searching for hands
def search_for_hands(clientsocket, cap, detector):
    max_w = 1
    max_h = 1
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        data, _ = detector.findPosition(img)
        if len(data) > 0:
            if max(data[:][1]) > max_w:
                max_w = max(data[:][1])

            if max(data[:][2]) > max_h:
                max_h = max(data[:][2])

        msg = msg_construction(data, 1000, 1000)
        send(clientsocket, msg)
        cv2.waitKey(0)

def main():
    s = init_server()
    c = getClient(s)
    cap = init_cap()
    detector = init_detector()
    search_for_hands(c, cap, detector)


if __name__ == '__main__':
    main()
