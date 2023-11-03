import json
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class HomeAction(Base):
    __tablename__ = 'home_action'
    id = Column(Integer, primary_key=True)
    type_action = Column(String)
    xpath = Column(String)
    value = Column(String)
    procedure_id = Column(Integer, ForeignKey('home_procedure.id'))

class ProcessTrigger(Base):
    __tablename__ = 'process_trigger'
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('home_bot.id'))
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProcessLog(Base):
    __tablename__ = 'process_log'
    id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey('process_trigger.id'))
    action_id = Column(Integer, ForeignKey('home_action.id'))
    status = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Database_handler:
    def __init__(self):
        with open('db_config.json', 'r') as f:
            config = json.load(f)
        
        DATABASE_URI = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
        self.engine = create_engine(DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def get_pending_actions(self):
        session = self.Session()
        pending_actions = session.query(HomeAction).filter(HomeAction.status == 'Pending').all()
        session.close()
        return pending_actions

    def initialize_process(self, bot_id):
        session = self.Session()
        new_trigger = ProcessTrigger(bot_id=bot_id, status='Started')
        session.add(new_trigger)
        session.commit()
        session.close()
        return new_trigger.id

    def log_action(self, trigger_id, action_id, status, message):
        session = self.Session()
        new_log = ProcessLog(trigger_id=trigger_id, action_id=action_id, status=status, message=message)
        session.add(new_log)
        session.commit()
        session.close()
