import tkinter as tk
from scapy.all import ARP, Ether, Raw, sniff, srp
import threading
import netifaces as ni

def get_interface_ip(interface):
    iface_addr = ni.ifaddresses(interface)
    ip_addr = iface_addr[ni.AF_INET][0]['addr'] if ni.AF_INET in iface_addr else None
    return ip_addr

def scan_network(interface):
    # 获取接口的 IP 地址和子网掩码
    ip_addr = get_interface_ip(interface)
    if not ip_addr:
        print(f"无法获取接口 {interface} 的 IP 地址")
        return []

    network = ip_addr.rsplit('.', 1)[0] + '.0/24'
    print(f"Scanning network: {network}")

    arp_request = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp_request

    result = srp(packet, timeout=2, iface=interface, verbose=0)[0]

    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    print("Found devices:")
    for client in clients:
        print(f"IP: {client['ip']}, MAC: {client['mac']}")

    return [client['ip'] for client in clients]

def packet_callback(packet, text_widget):
    try:
        # Display packet summary
        text_widget.insert(tk.END, f"{packet.summary()}\n")
        text_widget.see(tk.END)  # Auto-scroll

        # If the packet has a payload, display its content
        if packet.haslayer(Raw):
            payload = packet[Raw].load
            text_widget.insert(tk.END, f"Payload: {payload}\n\n")
            text_widget.see(tk.END)  # Auto-scroll
    except Exception as e:
        print(f"Error processing packet: {e}")

def capture_packets(interface, text_widget, ip):
    print(f"Starting to capture packets on {interface}...")
    sniff(iface=interface, prn=lambda pkt: packet_callback(pkt, text_widget), filter=f"ip and host {ip}", store=0)

def setup_gui(ips):
    root = tk.Tk()
    root.title("Wi-Fi Packet Sniffer")

    if len(ips) >= 1:
        # First device
        label1 = tk.Label(root, text=f"Device 1 (IP: {ips[0]}):")
        label1.pack()

        text1 = tk.Text(root, height=30, width=250)
        text1.pack()

        threading.Thread(target=capture_packets, args=("wlp0s20f3", text1, ips[0]), daemon=True).start()
    
    if len(ips) >= 2:
        # Second device
        label2 = tk.Label(root, text=f"Device 2 (IP: {ips[1]}):")
        label2.pack()

        text2 = tk.Text(root, height=30, width=250)
        text2.pack()

        threading.Thread(target=capture_packets, args=("wlp0s20f3", text2, ips[1]), daemon=True).start()
    
    root.mainloop()

if __name__ == "__main__":
    interface = 'wlp0s20f3'
    ips = scan_network(interface)
    setup_gui(ips)
