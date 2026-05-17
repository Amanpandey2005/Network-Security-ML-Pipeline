from scapy.all import sniff
import pandas as pd
import time
import threading

# Store packets
live_packets = []

# Lock for thread safety
packet_lock = threading.Lock()

def process_packet(packet):

    global live_packets

    try:

        packet_info = {}

        # Time
        packet_info["Time"] = time.strftime("%H:%M:%S")

        # Packet Length
        packet_info["Packet Length"] = len(packet)

        # Protocol
        if packet.haslayer("TCP"):

            packet_info["Protocol"] = "TCP"

        elif packet.haslayer("UDP"):

            packet_info["Protocol"] = "UDP"

        else:

            packet_info["Protocol"] = "OTHER"

        # IP Info
        if packet.haslayer("IP"):

            packet_info["Source IP"] = packet["IP"].src

            packet_info["Destination IP"] = packet["IP"].dst

        else:

            packet_info["Source IP"] = "Unknown"

            packet_info["Destination IP"] = "Unknown"

        # Prediction
        packet_info["Prediction"] = "BENIGN"

        # Thread safe append
        with packet_lock:

            live_packets.append(packet_info)

            # Keep only latest 5000 packets
            if len(live_packets) > 5000:

                live_packets = live_packets[-5000:]

    except Exception as e:

        print("Packet Error:", e)

def start_sniffing():

    sniff(
        prn=process_packet,
        store=False
    )

def get_live_data():

    global live_packets

    try:

        with packet_lock:

            data_copy = live_packets.copy()

        return pd.DataFrame(data_copy)

    except Exception as e:

        print("Live Data Error:", e)

        return pd.DataFrame()