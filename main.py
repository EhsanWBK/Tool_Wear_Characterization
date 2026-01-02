
from threads.mainThread import *

if __name__ == '__main__':
    setupThreads() # Start therads
    htmlStop.wait()
    htmlThread.join() # Wait until HTML is closed
    shutdownThreads() # close other threads