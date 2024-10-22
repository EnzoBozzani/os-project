from utils import read_args, get_processes_and_total_duration
from models import Process

def main():
    quantum, input_file = read_args()

    processes, total_duration = get_processes_and_total_duration(input_file)

    queue: list[Process] = []
    current_process_in_cpu = None

    for instant in range(total_duration):
        if instant < 10:
            print(f" {instant}", end='   ')
        else: 
            print(f"{instant}", end='   ')
    print()

    for instant in range(total_duration):
        if instant < 10:
            print(f"--", end='---')
        else: 
            print(f"-", end='----')
    print()

    for instant in range(total_duration):
        for process in processes:
            if process.arrival == instant:
                queue.append(process)
        
        if len(queue) > 0 and current_process_in_cpu is None:
            queue[0].last_entry = instant
            current_process_in_cpu = queue[0]
            queue.pop(0)

        if current_process_in_cpu.current_duration == current_process_in_cpu.duration:
            queue[0].last_entry = instant
            current_process_in_cpu = queue[0]
            queue.pop(0)
        
        for io_index, io_instant in enumerate(current_process_in_cpu.io):
            if current_process_in_cpu.current_duration == io_instant:
                temp = current_process_in_cpu
                temp.io.pop(io_index)

                if len(queue) > 0:
                    queue[0].last_entry = instant
                    current_process_in_cpu = queue[0]
                    queue.pop(0)
                else:
                    temp.last_entry = instant
                    current_process_in_cpu = temp

                queue.append(temp)
                break
        
        if instant - current_process_in_cpu.last_entry == quantum:
            temp = current_process_in_cpu
            queue[0].last_entry = instant
            current_process_in_cpu = queue[0]
            queue.append(temp)
            queue.pop(0)
        
        if current_process_in_cpu is not None:
            current_process_in_cpu.current_duration += 1
        print(f"{current_process_in_cpu.name}" if current_process_in_cpu is not None else '  ', end=' | ')
            
            

if __name__ == '__main__':
    main()