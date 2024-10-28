import sys

class Process:
    name: str
    arrival: int
    duration: int
    io: list[int]
    current_duration: int
    last_entry: int | None
    time_in_queue: int

    def __init__(self, name, arrival, duration, io):
        self.name = name
        self.arrival = arrival
        self.duration = duration
        self.io = io
        self.current_duration = 0
        self.last_entry = None
        self.time_in_queue = 0

def read_args():
    quantum = None
    input_file = None

    for i, arg in enumerate(sys.argv):
        if arg == '--quantum':
            if len(sys.argv) >= i + 2:
                quantum = sys.argv[i + 1]
        
        if arg == '--input-file':
            if len(sys.argv) >= i + 2:
                input_file = sys.argv[i + 1]
    
    if quantum is None:
        raise Exception('Flag --quantum is required')

    if input_file is None:
        raise Exception('Flag --input-file is required')

    return int(quantum), input_file

def get_processes_and_total_duration(input_file: str):
    processes: list[Process] = []
    total_duration = 0

    with open(input_file, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            line_arr = line.strip().split(' ')
            processes.append(
                Process(
                    name=line_arr[0],
                    arrival=int(line_arr[1]), 
                    duration=int(line_arr[2]),
                    io=[int(element) for element in line_arr[3].split(',')] if len(line_arr) == 4 else []
                )
            )
            total_duration += int(line_arr[2])
    
    return processes, total_duration