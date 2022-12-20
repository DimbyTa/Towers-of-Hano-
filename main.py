import sys
from hanoi import Hanoi

def start(argv):
    hanoi = Hanoi(int(argv[1]))
    hanoi.play()
    
if __name__ == "__main__":
    start(sys.argv)
