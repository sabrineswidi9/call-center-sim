import tkinter as tk
from threading import Thread, Semaphore
from queue import Queue
import time

# Paramètres
NOMBRE_AGENTS = 3

# File d'attente et sémaphores
queue = Queue()
semaphore = Semaphore(1)
threads = []

# Interface Tkinter
root = tk.Tk()
root.title("Centre d'appel - Simulation Multithread")
root.geometry("400x450")

# Éléments graphiques
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=10)

listbox = tk.Listbox(root, font=("Arial", 10), width=40)
listbox.pack(pady=10)

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 10), fg="blue")
status_label.pack(pady=10)

def agent_worker(agent_id):
    while True:
        client = queue.get()
        if client is None:
            break
        with semaphore:
            status_var.set(f"Agent-{agent_id} traite {client}...")
            time.sleep(2)  # Simule un appel
            status_var.set(f"Agent-{agent_id} a fini avec {client}")
            listbox.insert(tk.END, f"✓ Agent-{agent_id} a servi {client}")
        queue.task_done()

def appeler_client():
    nom = entry.get().strip()
    if nom:
        queue.put(nom)
        listbox.insert(tk.END, f"Client {nom} ajouté à la file")
        entry.delete(0, tk.END)

def quitter_application():
    for _ in range(NOMBRE_AGENTS):
        queue.put(None)  # Pour arrêter proprement les threads
    root.destroy()

# Bouton pour appeler
btn_appeler = tk.Button(root, text="📞 Appeler", command=appeler_client, font=("Arial", 12), bg="lightblue")
btn_appeler.pack(pady=10)

# Bouton pour quitter
btn_quitter = tk.Button(root, text="❌ Quitter", command=quitter_application, font=("Arial", 12), bg="salmon")
btn_quitter.pack(pady=10)

# Démarrer les threads agents
for i in range(NOMBRE_AGENTS):
    t = Thread(target=agent_worker, args=(i+1,), daemon=True)
    t.start()
    threads.append(t)

# Boucle principale de l'interface
root.mainloop()
