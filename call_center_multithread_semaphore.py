
import time
from datetime import datetime
from threading import Thread, Semaphore
from queue import Queue

NOMBRE_CLIENTS = 10
NOMBRE_AGENTS = NOMBRE_CLIENTS  # Pour test équitable

file_appels = Queue()
semaphore = Semaphore(1)  # Sémaphore binaire = comme un verrou
compteur_clients_servis = 0  # Ressource partagée

def agent(agent_id):
    global compteur_clients_servis
    while True:
        client_id = file_appels.get()
        if client_id is None:
            break

        print(f"[Agent-{agent_id}] Traitement de l’appel du client {client_id}...")
        time.sleep(2.0)  # traitement fixe

        # 🔒 Zone critique protégée
        semaphore.acquire()
        compteur_clients_servis += 1
        print(f"[Agent-{agent_id}] ➕ Client {client_id} servi. Total = {compteur_clients_servis}")
        semaphore.release()

        file_appels.task_done()

def main():
    print("📞 Simulation multithread avec sémaphore")
    start_time = time.time()
    print(f"🕒 Début : {datetime.now().strftime('%H:%M:%S')}")

    # Créer les threads agents
    threads = []
    for i in range(NOMBRE_AGENTS):
        t = Thread(target=agent, args=(i+1,))
        t.start()
        threads.append(t)

    # Ajouter les clients à la file
    for i in range(1, NOMBRE_CLIENTS + 1):
        print(f"📲 Client {i} appelle...")
        file_appels.put(i)

    # Attendre la fin
    file_appels.join()

    # Arrêter les threads
    for _ in range(NOMBRE_AGENTS):
        file_appels.put(None)
    for t in threads:
        t.join()

    end_time = time.time()
    print(f"🕒 Fin   : {datetime.now().strftime('%H:%M:%S')}")
    print(f"\n⏱️ Temps total d’exécution : {end_time - start_time:.2f} secondes")

if __name__ == "__main__":
    main()
