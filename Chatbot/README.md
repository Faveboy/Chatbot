### README.md

```markdown
# Android App Navigation Chatbot

## Overview

This script uses a large language model (LLM) to navigate Android applications via ADB commands. The LLM generates commands based on natural language statements to perform specific actions within the app.

## Prerequisites

1. **Python**: Ensure you have Python installed on your machine.
2. **Dependencies**: Install the required Python libraries.
3. **ADB**: Android Debug Bridge must be installed and configured on your machine.
4. **RSA Keys**: Prepare ADB authentication keys for a secure connection.

## Setup Instructions

### Step 1: Install Dependencies

Run the following command to install necessary Python libraries:

```bash
pip install -r requirements.txt
```

### Step 2: Prepare ADB Authentication Keys

Generate RSA keys using the `adb keygen` command:

```bash
adb keygen adbkey
```

This will create `adbkey` (private key) and `adbkey.pub` (public key).

Copy the public key to the Android device:

```bash
adb push adbkey.pub /sdcard/adbkey.pub
adb shell "cat /sdcard/adbkey.pub >> /data/misc/adb/adb_keys"
adb shell "rm /sdcard/adbkey.pub"
```

Save the keys in the script directory:
- Save `adbkey` as `private_key.txt`.
- Save `adbkey.pub` as `public_key.txt`.

### Step 3: Enable ADB over TCP/IP

Connect your device via USB and enable ADB over TCP/IP:

```bash
adb tcpip 5555
```

### Step 4: Update IP Range in Script

Modify the `discover_devices` function in the script to match your network’s IP range:

```python
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
```

### Step 5: Run the Script

Save the provided script as `android_navigation_chatbot.py` and run it:

```bash
python android_navigation_chatbot.py
```

## Script Overview

1. **Device Discovery**: Scans the local network for Android devices connected via ADB over TCP/IP.
2. **ADB Connection**: Authenticates and connects to the discovered Android device.
3. **Screenshot Handling**: Takes screenshots of the device’s screen.
4. **Natural Language Processing**: Uses an LLM to generate ADB commands from natural language statements.
5. **Navigation Execution**: Executes the generated ADB commands on the Android device.

### Example Natural Language Statement

```python
nl_statement = "Navigate me to settings and change my name to Bob"
```

### Output

- Screenshots of the initial and final states of the device screen.
- A series of ADB commands executed to perform the navigation.

## Notes

- Ensure your Android device and the machine running the script are on the same network.
- Modify the script as needed to fit specific requirements or network configurations.

## Support

For any issues or questions, please contact Abdullah Murad at abdullahmurad.business@gmail.com.
```

### requirements.txt

```plaintext
transformers
adb-shell
Pillow
```
