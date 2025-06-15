import time
import random
from datetime import datetime
from threading import Thread
from queue import Queue

NOMBRE_CLIENTS = 10
NOMBRE_AGENTS = NOMBRE_CLIENTS  # test comparatif juste


file_appels = Queue()

def agent(agent_id):
    while True:
        client_id = file_appels.get()
        if client_id is None:
            break
        print(f"[Agent-{agent_id}] Traitement de l’appel du client {client_id}...")
        temps_traitement = 2.0
        time.sleep(temps_traitement)
        print(f"[Agent-{agent_id}] Appel du client {client_id} terminé en {temps_traitement:.2f} secondes.\n")
        file_appels.task_done()

def main():
    print("📞 Simulation multithread du Call Center")
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

    # Attendre que tous les appels soient traités
    file_appels.join()

    # Arrêter proprement les threads
    for _ in range(NOMBRE_AGENTS):
        file_appels.put(None)
    for t in threads:
        t.join()

    end_time = time.time()
    print(f"🕒 Fin   : {datetime.now().strftime('%H:%M:%S')}")
    print(f"\n⏱️ Temps total d’exécution : {end_time - start_time:.2f} secondes")

if __name__ == "__main__":
    main()

