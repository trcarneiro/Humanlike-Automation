import datetime
from database_handler import *

def execute_action(action):
    # Simula a execução de uma ação.
    print(f"Executando ação {action.type_action} com xpath {action.xpath} e valor {action.value}")

def main():
    session = Session()

    # Consulta para encontrar triggers pendentes
    pending_triggers = session.query(ProcessTrigger).filter_by(status='pending').all()

    for trigger in pending_triggers:
        print(f"Processando trigger {trigger.id}")

        # Consulta para encontrar ações correspondentes
        actions = session.query(HomeAction).filter_by(procedure_id=trigger.bot_id).all()

        for action in actions:
            execute_action(action)

            # Registrar o resultado na tabela process_log
            log = ProcessLog(trigger_id=trigger.id, action_id=action.id, status='success', message='Ação executada com sucesso')
            session.add(log)

        # Atualizar o status do trigger
        trigger.status = 'completed'
        trigger.updated_at = datetime.datetime.utcnow()

    session.commit()
    session.close()

if __name__ == "__main__":
    main()
