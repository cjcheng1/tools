#!/usr/bin/env python3

import subprocess
import re
import os

def get_configured_ssids():
    # 讀取 wpa_supplicant.conf 配置文件中的 SSID
    networks = {}
    try:
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as file:
            data = file.read()
            ssids_matches = re.findall(r'ssid="([^"]+)"', data)
            psk_matches = re.findall(r'psk="([^"]+)"', data)
            for ssid,psk in zip(ssids_matches,psk_matches):
                networks[ssid] = psk
    except FileNotFoundError:
        print("wpa_supplicant.conf 文件未找到")
    return networks


def has_existing_connection(ssid):
    connection_directory = "/etc/NetworkManager/system-connections"
    for filename in os.listdir(connection_directory):
        if filename.endswith(".nmconnection") and ssid in filename:
            return True
    return False



def get_available_networks():
    # 使用 nmcli 列出所有可用的 WiFi 網絡
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID,SIGNAL', 'device', 'wifi', 'list'], stdout=subprocess.PIPE)
    networks = result.stdout.decode('utf-8').strip().split('\n')
    available_networks = {}
    for network in networks:
        parts = network.split(':')
        if len(parts) == 2:
            ssid, signal = parts
            if ssid:  # 忽略空 SSID
                available_networks[ssid] = int(signal)
    return available_networks

def connect_to_ssid(ssid,psk,interface):

    if has_existing_connection(ssid):
        result = subprocess.run(['sudo','nmcli', 'connection','up', ssid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        result = subprocess.run(['sudo','nmcli', 'device', 'wifi', 'connect', ssid,'password', psk,'ifname',interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result.returncode == 0, result.stderr.decode('utf-8')

def connect_to_strongest_ssid(configured_ssids, available_networks,interface):
    sorted_networks = sorted(configured_ssids, key=lambda ssid: available_networks.get(ssid, -100), reverse=True)

    for ssid in sorted_networks:
        if ssid in available_networks:
            print(f"正在嘗試連接到 SSID: {ssid} 信號強度: {available_networks[ssid]}")
            success, error_message = connect_to_ssid(ssid,configured_ssids[ssid],interface)
            if success:
                print(f"成功連接到 {ssid}")
                return
            else:
                print(f"連接到 {ssid} 失敗: {error_message}")

    print("沒有找到可用的 SSID 或連接失敗")

if __name__ == "__main__":
    interface = 'wlan0'
    configured_networks = get_configured_ssids()
    if not configured_networks:
        print("沒有找到配置的 SSID")
    else:
        print("配置的 SSID:", configured_networks)
        available_networks = get_available_networks()
        print("可用的網絡:", available_networks)
        connect_to_strongest_ssid(configured_networks, available_networks,interface)
