from loadingtest import main, stop
import threading
import time
thread = threading.Thread(target=main)
thread.start()
time.sleep(.03)
stop()


