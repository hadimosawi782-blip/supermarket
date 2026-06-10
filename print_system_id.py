import hashlib, socket
system_id = hashlib.md5(f"supermarket_{socket.gethostname()}".encode()).hexdigest()[:12].upper()
print(system_id)
