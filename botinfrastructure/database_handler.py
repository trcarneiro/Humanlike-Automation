from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime  # Adicionado

Base = declarative_base()

class HomeAction(Base):
    __tablename__ = 'home_action'
    id = Column(Integer, primary_key=True)
    type_action = Column(String)
    xpath = Column(String)
    value = Column(String)
    procedure_id = Column(Integer, ForeignKey('home_procedure.id'))

# Adicionado
class ProcessTrigger(Base):
    __tablename__ = 'process_trigger'
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('home_bot.id'))
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

# Adicionado
class ProcessLog(Base):
    __tablename__ = 'process_log'
    id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey('process_trigger.id'))
    action_id = Column(Integer, ForeignKey('home_action.id'))
    status = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('mysql+pymysql://username:password@host/db_name')
Session = sessionmaker(bind=engine)

def get_pending_actions():
    session = Session()
    pending_actions = session.query(HomeAction).filter(/* sua condição */).all()
    session.close()
    return pending_actions
