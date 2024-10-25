from utils import get_processes_and_total_duration
from models import Process

def pipeline(quantum, input_file):
    processes, total_duration = get_processes_and_total_duration(input_file)

    queue: list[Process] = []
    current_process_in_cpu = None

    output_to_be_written_on_file = f"Input file: {input_file}\nQuantum: {quantum}\n\n"

    for instant in range(total_duration):
        if instant < 10:
            output_to_be_written_on_file += f" {instant}   "
        else: 
            output_to_be_written_on_file += f"{instant}   "

    output_to_be_written_on_file += "\n"

    for instant in range(total_duration):
        if instant < 10:
            output_to_be_written_on_file += f"-----"
        else: 
            output_to_be_written_on_file += f"-----"

    output_to_be_written_on_file += "\n"

    for instant in range(total_duration):
        for process in processes:
            if process.arrival == instant:
                queue.append(process)
        
        if len(queue) > 0 and current_process_in_cpu is None:
            queue[0].last_entry = instant
            current_process_in_cpu = queue[0]
            queue.pop(0)
        elif current_process_in_cpu.current_duration == current_process_in_cpu.duration:
            queue[0].last_entry = instant
            current_process_in_cpu = queue[0]
            queue.pop(0)
        elif instant - current_process_in_cpu.last_entry == quantum:
            temp = current_process_in_cpu
            queue[0].last_entry = instant
            current_process_in_cpu = queue[0]
            queue.append(temp)
            queue.pop(0)
        else:    
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
    
        
        current_process_in_cpu.current_duration += 1

        for process in queue:
            for i in range(len(processes)):
                if process.name == processes[i].name:
                    processes[i].time_in_queue += 1

        output_to_be_written_on_file += f"{current_process_in_cpu.name} | " if current_process_in_cpu is not None else '  '

    output_to_be_written_on_file += "\n\nTempos de espera:\n"

    s = 0
    for process in processes:
        s += process.time_in_queue
        output_to_be_written_on_file += f"{process.name}: {process.time_in_queue}\n"

    output_to_be_written_on_file += f"\nTempo de espera médio: {s/len(processes)}"
    
    with open(f"{input_file.split('.txt')[0]}.output.txt", 'w') as f:
        f.write(output_to_be_written_on_file)

    print(f"Outputs em '{input_file.split('.txt')[0]}.output.txt'")
                