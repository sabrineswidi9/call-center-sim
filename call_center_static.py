import tkinter as tk
from tkinter import ttk
from threading import Thread, Semaphore
from queue import PriorityQueue
import time

# Paramètres
NOMBRE_AGENTS = 3

# File d'attente avec priorité
queue = PriorityQueue()
semaphore = Semaphore(1)
threads = []
agent_counts = [0] * NOMBRE_AGENTS
progress_bars = []

# Interface Tkinter
root = tk.Tk()
root.title("Centre d'appel - Simulation Multithread avec Priorité")
root.geometry("400x700")

# Éléments graphiques
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=10)

type_var = tk.StringVar(value="Normal")
type_menu = tk.OptionMenu(root, type_var, "Normal", "VIP", "Urgent")
type_menu.pack(pady=5)

listbox = tk.Listbox(root, font=("Arial", 10), width=40)
listbox.pack(pady=10)

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 10), fg="blue")
status_label.pack(pady=10)

# Barres de progression des agents
for i in range(NOMBRE_AGENTS):
    label = tk.Label(root, text=f"Agent-{i+1} appels : 0", font=("Arial", 10))
    label.pack()
    progress = ttk.Progressbar(root, length=200, mode='determinate', maximum=20)
    progress.pack(pady=2)
    progress_bars.append((label, progress))

def agent_worker(agent_id):
    while True:
        priority, client, client_type = queue.get()
        if client is None:
            break
        with semaphore:
            status_var.set(f"Agent-{agent_id} traite {client} ({client_type})...")
            if client_type == "VIP":
                time.sleep(1)
            elif client_type == "Urgent":
                time.sleep(0.5)
            else:
                time.sleep(2)
            status_var.set(f"Agent-{agent_id} a fini avec {client}")
            listbox.insert(tk.END, f"✓ Agent-{agent_id} a servi {client} ({client_type})")
            agent_counts[agent_id - 1] += 1
            label, bar = progress_bars[agent_id - 1]
            label.config(text=f"Agent-{agent_id} appels : {agent_counts[agent_id - 1]}")
            bar['value'] = agent_counts[agent_id - 1]
        queue.task_done()

def appeler_client():
    nom = entry.get().strip()
    client_type = type_var.get()
    if nom:
        priorities = {"Urgent": 1, "VIP": 2, "Normal": 3}
        priority = priorities.get(client_type, 3)
        listbox.insert(tk.END, f"Client {nom} ({client_type}) ajouté à la file")
        queue.put((priority, nom, client_type))
        entry.delete(0, tk.END)

def test_mass_appels():
    clients = [
        ("client1", "Normal"),
        ("client2", "VIP"),
        ("client3", "Urgent"),
        ("client4", "Normal"),
        ("client5", "Urgent")
    ]
    for nom, ctype in clients:
        priority = {"Urgent": 1, "VIP": 2, "Normal": 3}[ctype]
        listbox.insert(tk.END, f"Client {nom} ({ctype}) ajouté à la file")
        queue.put((priority, nom, ctype))

def quitter_application():
    for _ in range(NOMBRE_AGENTS):
        queue.put((99, None, None))  # signal d'arrêt pour les threads
    root.destroy()

# Bouton pour appeler
btn_appeler = tk.Button(root, text="📞 Appeler", command=appeler_client, font=("Arial", 12), bg="lightblue")
btn_appeler.pack(pady=10)

# Bouton pour test automatique
btn_test = tk.Button(root, text="⚙️ Test automatique", command=test_mass_appels, font=("Arial", 10), bg="lightgrey")
btn_test.pack(pady=5)

# Bouton pour quitter
btn_quitter = tk.Button(root, text="❌ Quitter", command=quitter_application, font=("Arial", 12), bg="salmon")
btn_quitter.pack(pady=10)

# Lancer les threads agents
for i in range(NOMBRE_AGENTS):
    t = Thread(target=agent_worker, args=(i+1,), daemon=True)
    t.start()
    threads.append(t)

# Boucle principale
root.mainloop()
