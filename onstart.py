from lcd import LCD
import socket

lcd = LCD()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        l = s.getsockname()
        print(l)
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
        print('s')
    finally:
        s.close()
    return IP

ip = socket.gethostbyname(socket.gethostname())
lcd.text(get_ip(), 0)
lcd.text('', 1)
