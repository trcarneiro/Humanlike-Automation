from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base, mapper
from datetime import datetime
import json

Base = declarative_base()

class DynamicDataHandler:
    def __init__(self, database_uri):
        self.engine = create_engine(database_uri)
        self.Session = sessionmaker(bind=self.engine)

    def create_dynamic_model(self, table_name, data_sample):
        metadata = MetaData()
        columns = [
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('insert_datetime', DateTime, default=datetime.utcnow),
        ]

        for key, value in data_sample.items():
            if isinstance(value, int):
                columns.append(Column(key, Integer))
            elif isinstance(value, float):
                columns.append(Column(key, Float))
            else:
                columns.append(Column(key, String(255)))

        table = Table(table_name.lower(), metadata, *columns)
        metadata.create_all(self.engine)

        class DynamicTable(Base):
            __table__ = table

        return DynamicTable

    def insert_data(self, table_name, data_list):
        if not data_list:
            print("A lista de dados está vazia. Nenhuma inserção será feita.")
            return

        DynamicModel = self.create_dynamic_model(table_name, data_list[0])

        session = self.Session()
        for data in data_list:
            record = DynamicModel(**data)
            session.add(record)
        session.commit()
        session.close()

'''if __name__ == "__main__":
    # Load database config from a json file
    with open('db_config.json', 'r') as f:
        config = json.load(f)
    
    DATABASE_URI = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"

    # Dados de exemplo para inserir na tabela
    data_list = [
        {'link': 'https://warthunder.com/pt/community/claninfo/NIKE%20x%20UzBeK', 'place': 1, 'name': '[WeBak] NIKE x UzBeK', 'duel_ratio': '46.5K', 'members': 127, 'air_targets_destroyed': '6.2K', 'ground_targets_destroyed': '10.1K', 'deaths': '8.5K', 'flight_time': '37.2 d'},
        # Adicione mais dicionários conforme necessário
    ]

    # Inicializando a classe de manipulação de dados e inserindo os dados
    handler = DynamicDataHandler(DATABASE_URI)
    handler.insert_data('SquadronLeaderboard', data_list)'''