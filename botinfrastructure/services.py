import time
from database_handler import get_pending_actions,Session, ProcessTrigger, ProcessLog



def monitor_database():
    while True:
        pending_actions = get_pending_actions()

        for action in pending_actions:
            # Aqui você coloca a lógica para acionar o bot correspondente
            pass

        time.sleep(10)

from database_handler import Session, ProcessTrigger, ProcessLog

def initialize_process(bot_id):
    session = Session()
    new_trigger = ProcessTrigger(bot_id=bot_id, status='Started')
    session.add(new_trigger)
    session.commit()
    session.close()
    return new_trigger.id

def log_action(trigger_id, action_id, status, message):
    session = Session()
    new_log = ProcessLog(trigger_id=trigger_id, action_id=action_id, status=status, message=message)
    session.add(new_log)
    session.commit()
    session.close()

'''if __name__ == "__main__":
    monitor_database()
'''