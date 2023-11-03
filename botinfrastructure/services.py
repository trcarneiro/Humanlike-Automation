import time
from database_handler import get_pending_actions,Session, ProcessTrigger, ProcessLog


def monitor_database():
    while True:
        pending_actions = get_pending_actions()

        for action in pending_actions:
            # Aqui você coloca a lógica para acionar o bot correspondente
            pass

        time.sleep(10)



'''if __name__ == "__main__":
    monitor_database()
'''