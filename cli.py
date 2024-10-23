from utils import read_args
from pipeline import pipeline

def main():
    quantum, input_file = read_args()
    pipeline(quantum, input_file)

if __name__ == '__main__':
    main()