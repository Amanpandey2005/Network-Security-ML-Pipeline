from scapy.all import sniff
import pandas as pd
import time
import sys
import os
import socket

# Current directory
current_dir = os.path.dirname(__file__)

# Project root
project_root = os.path.abspath(
    os.path.join(current_dir, "..")
)

# Add src path
sys.path.append(current_dir)

from predict import predict

# Logs folder
logs_dir = os.path.join(
    project_root,
    "logs"
)

os.makedirs(
    logs_dir,
    exist_ok=True
)

# CSV path
log_file = os.path.join(
    logs_dir,
    "live_traffic.csv"
)

# Packet storage
packet_data = []

# Threat counters
total_packets = 0

malicious_packets = 0

benign_packets = 0

def get_protocol(packet):

    if packet.haslayer("TCP"):

        return 6

    elif packet.haslayer("UDP"):

        return 17

    elif packet.haslayer("ICMP"):

        return 1

    return 0

def get_ports(packet):

    src_port = 0

    dst_port = 0

    if packet.haslayer("TCP"):

        src_port = packet["TCP"].sport

        dst_port = packet["TCP"].dport

    elif packet.haslayer("UDP"):

        src_port = packet["UDP"].sport

        dst_port = packet["UDP"].dport

    return src_port, dst_port

def get_ips(packet):

    src_ip = "Unknown"

    dst_ip = "Unknown"

    if packet.haslayer("IP"):

        src_ip = packet["IP"].src

        dst_ip = packet["IP"].dst

    return src_ip, dst_ip

def process_packet(packet):

    global total_packets

    global malicious_packets

    global benign_packets

    try:

        total_packets += 1

        # IP extraction
        src_ip, dst_ip = get_ips(packet)

        # Port extraction
        src_port, dst_port = get_ports(packet)

        # Protocol
        protocol = get_protocol(packet)

        # Packet size
        packet_length = len(packet)

        # Create ML input
        data = {

            "Packet Length": packet_length,

            "Protocol": protocol,

            "Source Port": src_port,

            "Destination Port": dst_port
        }

        # Prediction
        prediction = predict(data)

        # Threat counting
        if prediction != "BENIGN":

            malicious_packets += 1

        else:

            benign_packets += 1

        # Console output
        print("\n================================")

        print("📦 Packet Captured")

        print(f"Source IP: {src_ip}")

        print(f"Destination IP: {dst_ip}")

        print(f"Protocol: {protocol}")

        print(f"Packet Length: {packet_length}")

        print(f"Prediction: {prediction}")

        print("================================")

        # Save packet log
        packet_data.append({

            "Time":
                time.strftime("%H:%M:%S"),

            "Source IP":
                src_ip,

            "Destination IP":
                dst_ip,

            "Source Port":
                src_port,

            "Destination Port":
                dst_port,

            "Protocol":
                protocol,

            "Packet Length":
                packet_length,

            "Prediction":
                prediction
        })

        # Convert to dataframe
        log_df = pd.DataFrame(packet_data)

        # Save logs continuously
        log_df.to_csv(
            log_file,
            index=False
        )

        # Threat alert
        if prediction != "BENIGN":

            print(
                f"\n⚠ ALERT: {prediction} detected!"
            )

    except Exception as e:

        print("Error:", e)

def start_capture():

    print("\n🚀 Starting Real-Time Packet Capture...")

    print(
        "\nMonitoring live network traffic...\n"
    )

    sniff(

        prn=process_packet,

        store=False
    )

if __name__ == "__main__":

    start_capture()