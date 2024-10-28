import tkinter as tk
from tkinter import filedialog

from pipeline import pipeline

def upload_file(text_area):
    file_path = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )

    if file_path:
        text_area.delete(0, tk.END) 
        text_area.insert(tk.END, file_path)

def run_pipeline(quantum, input_file, output, output_path):
    pipeline(quantum.get(), input_file.get())

    path: str = input_file.get()

    path_arr = path.split('.txt')

    path_arr.append('.grafico.txt')

    output_file = f"{path_arr[0]}{path_arr[2]}"

    with open(output_file, 'r') as f:
        output.delete(1.0, tk.END) 

        output_path.delete(0, tk.END)
        output_path.insert(tk.END, f"Outputs em '{path_arr[0]}.saida.txt' e '{path_arr[0]}.grafico.txt'")
        
        for line in f.readlines():
            output.insert(tk.END, line)

def main():
    w = tk.Tk()
    w.title("Escalonador de Processos")
    w.geometry("1500x700")

    label_input_file = tk.Label(w, text="Input file:")
    input_file = tk.Entry(w, width=30)
    label_quantum = tk.Label(w, text="Quantum:")
    quantum = tk.Entry(w, width=30)
    output = tk.Text(w, width=200, height=30)
    output_path = tk.Entry(w, width=100)
    file_btn = tk.Button(w, text="Selecionar arquivo", command=lambda: upload_file(input_file))
    run_btn = tk.Button(w, text="Processar", command=lambda: run_pipeline(quantum, input_file, output, output_path))

    file_btn.pack(pady=5)
    label_input_file.pack(pady=5)
    input_file.pack(pady=5)
    label_quantum.pack(pady=5)
    quantum.pack(pady=5)
    run_btn.pack(pady=20)
    output_path.pack(pady=1)
    output.pack(pady=1)

    w.mainloop()

if __name__ == '__main__':
    main()

