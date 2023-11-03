
import json
import datetime
from .database_handler import Database_handler, HomeAction, ProcessTrigger, ProcessLog

def test_get_pending_actions():
    db = Database_handler()
    pending_actions = db.get_pending_actions()
    assert isinstance(pending_actions, list)

def test_initialize_process():
    db = Database_handler()
    bot_id = 1  # Replace with an actual bot ID from your database
    trigger_id = db.initialize_process(bot_id)
    assert isinstance(trigger_id, int)

def test_log_action():
    db = Database_handler()
    trigger_id = 1  # Replace with an actual trigger ID from your database
    action_id = 1  # Replace with an actual action ID from your database
    status = "Completed"
    message = "Action successfully completed."
    db.log_action(trigger_id, action_id, status, message)
    # Here, you might want to query the database to check if the log has been added
