import threading
from program import start as program_start
from server import start as server_start

if __name__ == '__main__':
    program = threading.Thread(target=program_start)
    program.start()
    
    server_start()