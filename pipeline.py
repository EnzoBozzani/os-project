from utils import get_processes_and_total_duration, Process

def pipeline(quantum, input_file):
    processes, total_duration = get_processes_and_total_duration(input_file)

    queue: list[Process] = []
    current_process_in_cpu = None

    chart_output = f"Input file: {input_file}\nQuantum: {quantum}\n\n"
    output = f"***********************************\n***** ESCALONADOR ROUND ROBIN *****\n----------------------------------\n------- INICIANDO SIMULACAO -------\n----------------------------------\n"

    for instant in range(total_duration):
        if instant < 10:
            chart_output += f" {instant}   "
        else: 
            chart_output += f"{instant}   "

    chart_output += "\n"

    for instant in range(total_duration):
        if instant < 10:
            chart_output += f"-----"
        else: 
            chart_output += f"-----"

    chart_output += "\n"

    for instant in range(total_duration):

        output += f"********** TEMPO {instant} **************\n"
        
        if current_process_in_cpu is None:
            for process in processes:
                if process.arrival == instant:
                    output += f"#[evento] CHEGADA <{process.name}>\n"
                    queue.append(process)

            queue[0].last_entry = instant
            current_process_in_cpu = queue[0]
            queue.pop(0)
        elif current_process_in_cpu.current_duration == current_process_in_cpu.duration:
            for process in processes:
                if process.arrival == instant:
                    output += f"#[evento] CHEGADA <{process.name}>\n"
                    queue.append(process)

            output += f"#[evento] ENCERRANDO <{current_process_in_cpu.name}>\n"
            queue[0].last_entry = instant
            current_process_in_cpu = queue[0]
            queue.pop(0)
        elif instant - current_process_in_cpu.last_entry == quantum:
            for process in processes:
                if process.arrival == instant:
                    output += f"#[evento] CHEGADA <{process.name}>\n"
                    queue.append(process)

            output += f"#[evento] FIM QUANTUM <{current_process_in_cpu.name}>\n"
            temp = current_process_in_cpu
            if len(queue) > 0:
                queue[0].last_entry = instant
                current_process_in_cpu = queue[0]
                queue.append(temp)
                queue.pop(0)
            else:
                temp.last_entry = instant
                current_process_in_cpu = temp
        else:    
            for io_index, io_instant in enumerate(current_process_in_cpu.io):
                if current_process_in_cpu.current_duration == io_instant:
                    temp = current_process_in_cpu
                    temp.io.pop(io_index)

                    output += f"#[evento] OPERACAO I/O <{current_process_in_cpu.name}>\n"
                    if len(queue) > 0:
                        queue[0].last_entry = instant
                        current_process_in_cpu = queue[0]
                        queue.pop(0)
                        queue.append(temp)
                    else:
                        temp.last_entry = instant
                        current_process_in_cpu = temp

                    break
            
            for process in processes:
                if process.arrival == instant:
                    output += f"#[evento] CHEGADA <{process.name}>\n"
                    queue.append(process)
    
        
        current_process_in_cpu.current_duration += 1

        for process in queue:
            for i in range(len(processes)):
                if process.name == processes[i].name:
                    processes[i].time_in_queue += 1

        output += "FILA: "
        
        if len(queue) > 0:
            for p in queue:
                output += f"{p.name}({p.duration - p.current_duration}) "
        else: 
            output += "Nao ha processos na fila"
        
        output += f"\nCPU: {current_process_in_cpu.name}({current_process_in_cpu.duration - current_process_in_cpu.current_duration + 1})\n"

        chart_output += f"{current_process_in_cpu.name} | " if current_process_in_cpu is not None else '  '

    chart_output += "\n\nTempos de espera:\n"

    output += f"********** TEMPO {total_duration} *************\n#[evento] ENCERRANDO <{current_process_in_cpu.name}>\nFILA: Nao ha processos na fila\nACABARAM OS PROCESSOS!!!\n----------------------------------\n------ Encerrando simulacao ------\n----------------------------------"

    s = 0
    for process in processes:
        s += process.time_in_queue
        chart_output += f"{process.name}: {process.time_in_queue}\n"

    chart_output += f"\nTempo de espera médio: {s/len(processes)}"
    
    with open(f"{input_file.split('.txt')[0]}.grafico.txt", 'w') as f:
        f.write(chart_output)
    
    with open(f"{input_file.split('.txt')[0]}.saida.txt", 'w') as f:
        f.write(output)

    print(f"Outputs em '{input_file.split('.txt')[0]}.grafico.txt' e '{input_file.split('.txt')[0]}.saida.txt'")
                