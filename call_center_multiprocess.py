import time
import random
from datetime import datetime
from multiprocessing import Process, Pipe

NOMBRE_CLIENTS = 10

def agent(client_id, conn):
    # Lire le message du client
    message = conn.recv()
    print(f"[Agent-{client_id}] Reçu : {message}")
    
    # Traitement
    temps_traitement = 2.0  # temps de traitement fixe en secondes
    time.sleep(temps_traitement)
    
    print(f"[Agent-{client_id}] Appel traité en {temps_traitement:.2f} secondes.\n")
    conn.close()

def main():
    print("📞 Simulation Multiprocessus du Call Center")
    start_time = time.time()
    print(f"🕒 Début : {datetime.now().strftime('%H:%M:%S')}")

    processus = []

    for i in range(1, NOMBRE_CLIENTS + 1):
        parent_conn, child_conn = Pipe()
        p = Process(target=agent, args=(i, child_conn))
        p.start()
        
        # Envoyer un appel simulé
        print(f"📲 Client {i} appelle...")
        parent_conn.send(f"Appel du client {i}")
        
        processus.append(p)

    # Attendre la fin de tous les processus enfants
    for p in processus:
        p.join()

    end_time = time.time()
    print(f"🕒 Fin   : {datetime.now().strftime('%H:%M:%S')}")
    print(f"\n⏱️ Temps total d’exécution : {end_time - start_time:.2f} secondes")

if __name__ == "__main__":
    main()
