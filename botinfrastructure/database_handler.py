import json
import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class HomeAction(Base):
    __tablename__ = 'home_action'
    id = Column(Integer, primary_key=True)
    type_action = Column(String(255))  # Defina um tamanho adequado aqui
    xpath = Column(String(255))  # Defina um tamanho adequado aqui
    value = Column(String(255))  # Defina um tamanho adequado aqui
    procedure_id = Column(Integer, ForeignKey('home_procedure.id'))

class ProcessTrigger(Base):
    __tablename__ = 'process_trigger'
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('home_bot.id'))
    status = Column(String(255))  # Adicionado tamanho
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProcessLog(Base):
    __tablename__ = 'process_log'
    id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey('process_trigger.id'))
    action_id = Column(Integer, ForeignKey('home_action.id'))
    status = Column(String(255))  # Adicionado tamanho
    message = Column(String(255))  # Adicionado tamanho
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class HomeBot(Base):
    __tablename__ = 'home_bot'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # Adicionado tamanho
    description = Column(Text)


class Database_handler:
    def __init__(self):
        # Configuração do banco de dados

        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(dir_path, 'db_config.json')
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"O arquivo de configuração {config_path} não foi encontrado.")

        with open(config_path, 'r') as f:
            config = json.load(f)
        
        DATABASE_URI = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
        self.engine = create_engine(DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        # Criação das tabelas no banco de dados
        Base.metadata.create_all(self.engine)

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
        
    def get_all_bots(engine):
        Session = sessionmaker(bind=engine)
        session = Session()
        bots = session.query(HomeBot).all()
        session.close()
        return bots
    
    def get_active_processes(self):
        session = self.Session()
        active_processes = session.query(ProcessTrigger).filter(ProcessTrigger.status == 'Started').all()
        session.close()
        return active_processes

    # Novo método para atualizar o status do processo
    def update_process_status(self, process_id, status):
        session = self.Session()
        process = session.query(ProcessTrigger).get(process_id)
        if process:
            process.status = status
            session.commit()
        session.close()

