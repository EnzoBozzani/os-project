import tkinter as tk
from tkinter import messagebox

from pipeline import pipeline

janela = tk.Tk()
janela.title("Escalonador de Processos")
janela.geometry("500x500") 

label_processos = tk.Label(janela, text="Processos:")
label_processos.pack(pady=5)
entry_processos = tk.Entry(janela, width=30)
entry_processos.pack(pady=5)

label_quantum = tk.Label(janela, text="Quantum:")
label_quantum.pack(pady=5)
entry_quantum = tk.Entry(janela, width=30)
entry_quantum.pack(pady=5)

botao_processar = tk.Button(janela, text="Processar", command=pipeline)
botao_processar.pack(pady=20)

janela.mainloop()