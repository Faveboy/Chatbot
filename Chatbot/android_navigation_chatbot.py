
import os
import socket
import time
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.keygen import keygen
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from transformers import pipeline
from PIL import Image
from io import BytesIO

# Load keys
with open("private_key.txt") as f:
    priv = f.read()
with open("public_key.txt") as f:
    pub = f.read()

signer = PythonRSASigner(pub, priv)

def discover_devices(port=5555):
    devices = []
    for i in range(1, 255):
        ip = f"192.168.0.{i}"  # Adjust to your network’s IP range
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((ip, port))
                devices.append(ip)
        except (socket.timeout, ConnectionRefusedError):
            continue
    return devices

def connect_device(ip, port=5555):
    device = AdbDeviceTcp(ip, port, default_transport_timeout_s=9.)
    device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
    return device

def take_screenshot(device):
    result = device.shell("screencap -p")
    image = Image.open(BytesIO(result.replace(b'\r\n', b'\n')))
    image.save("screenshot.png")
    return image

def main():
    # Load the model
    model = pipeline("text2text-generation", model="google/flan-t5-small")
    
    # Discover and connect to device
    devices = discover_devices()
    if not devices:
        print("No devices found.")
        return
    
    device = connect_device(devices[0])
    
    # Take initial screenshot
    take_screenshot(device)
    
    # Define NL statement and generate ADB commands
    nl_statement = "Navigate me to settings and change my name to Bob"
    result = model(nl_statement)
    adb_commands = result[0]['generated_text'].split('\n')
    
    # Execute ADB commands
    for cmd in adb_commands:
        device.shell(cmd)
        time.sleep(1)
    
    # Take final screenshot
    take_screenshot(device)

if __name__ == "__main__":
    main()
