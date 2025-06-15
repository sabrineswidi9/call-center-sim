import time
import random
from datetime import datetime  # <-- Étape 3

NOMBRE_CLIENTS = 10

def traiter_appel(client_id):
    print(f"[Agent] Traitement de l’appel du client {client_id}...")
    temps_traitement = random.uniform(1, 3)
    time.sleep(temps_traitement)
    print(f"[Agent] Appel du client {client_id} terminé en {temps_traitement:.2f} secondes.\n")

def main():
    print("📞 Simulation séquentielle du Call Center")

    # --- Étape 3 : début du chronomètre
    start_time = time.time()
    print(f"🕒 Début : {datetime.now().strftime('%H:%M:%S')}")

    for i in range(1, NOMBRE_CLIENTS + 1):
        print(f"\n📲 Client {i} appelle...")
        traiter_appel(i)

    # --- Étape 3 : fin du chronomètre
    end_time = time.time()
    print(f"🕒 Fin   : {datetime.now().strftime('%H:%M:%S')}")

    duree = end_time - start_time
    print(f"\n⏱️ Temps total d’exécution : {duree:.2f} secondes")

if __name__ == "__main__":
    main()

