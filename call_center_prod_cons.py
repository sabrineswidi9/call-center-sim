import time
from threading import Thread, Semaphore
from queue import Queue

NOMBRE_CLIENTS = 10
NOMBRE_AGENTS = 3
BUFFER_TAILLE = 5

# Sémaphores
mutex = Semaphore(1)
plein = Semaphore(0)
vide = Semaphore(BUFFER_TAILLE)

# File d’attente limitée
file_appels = Queue(BUFFER_TAILLE)

def producteur(client_id):
    time.sleep(0.2)  # petit délai simulé
    vide.acquire()        # attendre qu’il y ait de la place
    mutex.acquire()
    file_appels.put(client_id)
    print(f"📲 Client {client_id} a placé son appel.")
    mutex.release()
    plein.release()       # signaler qu’il y a un appel à traiter

def consommateur(agent_id):
    while True:
        plein.acquire()     # attendre qu’il y ait un appel
        mutex.acquire()
        if file_appels.empty():
            mutex.release()
            continue
        client_id = file_appels.get()
        mutex.release()
        vide.release()      # signaler qu’il y a une place libre

        print(f"[Agent-{agent_id}] Traitement de l’appel du client {client_id}...")
        time.sleep(2.0)
        print(f"[Agent-{agent_id}] Client {client_id} servi.\n")

def main():
    print("📞 Simulation Producteurs / Consommateurs")

    # Lancer les threads consommateurs (agents)
    agents = []
    for i in range(NOMBRE_AGENTS):
        t = Thread(target=consommateur, args=(i+1,), daemon=True)
        t.start()
        agents.append(t)

    # Lancer les threads producteurs (clients)
    clients = []
    for i in range(1, NOMBRE_CLIENTS + 1):
        t = Thread(target=producteur, args=(i,))
        t.start()
        clients.append(t)

    for t in clients:
        t.join()

    # Pause pour laisser les consommateurs finir
    time.sleep(5)

    print("✅ Tous les clients ont été servis.")

if __name__ == "__main__":
    main()
