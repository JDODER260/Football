import sys
import time

def loading_animation():
    while True:
        for i in range(4):
            sys.stdout.write("Loading" + "." * i + "   \r")
            sys.stdout.flush()
            time.sleep(0.5)
        for i in range(4, 0, -1):
            sys.stdout.write("Loading" + "." * i + "   \r")
            sys.stdout.flush()
            time.sleep(0.5)

loading_animation()
