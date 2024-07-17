# -*- coding: utf-8 -*-
# @File    : receive_syslog
# @Project : 4U
# @Time    : 2024/7/17 15:00
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import socket
import logging

# Set up logging
logging.basicConfig(filename='syslog.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Define the UDP IP and port
UDP_IP = "192.168.203.51"  # Listen on all interfaces
UDP_PORT = 514

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for syslog messages on UDP port {UDP_PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        message = data.decode('utf-8')
        print(f"Received message from {addr}: {message}")
        logging.info(f"Received message from {addr}: {message}")
except KeyboardInterrupt:
    print("\nServer stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    sock.close()
