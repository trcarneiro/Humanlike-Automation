from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, MetaData, Table, func, and_
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import logging
from sqlalchemy import and_

Base = declarative_base()

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='squadron_scraper.log',
                    filemode='w')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger('').addHandler(console_handler)

class DynamicDataHandler:
    def __init__(self, database_uri):
        self.engine = create_engine(database_uri)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initializing DynamicDataHandler...")

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

    '''def insert_data(self, table_name, data_list):
        if not data_list:
            print("Data list is empty. No insertion will be made.")
            return

        DynamicModel = self.create_dynamic_model(table_name, data_list[0])

        session = self.Session()

        for data in data_list:
            query = session.query(DynamicModel)
            # Exclui chaves que não devem ser consideradas na verificação de duplicidade( TROCA ESSA LOGICA DEPOIS PARA A CAMADA DA API)
            check_data = {key: value for key, value in data.items() if key not in ['id', 'insert_datetime','members']}
            for key, value in check_data.items():
                query = query.filter(getattr(DynamicModel, key) == value)

            # Verifica se já existe um registro com os mesmos dados
            exists = query.first() is not None

            if not exists:
                record = DynamicModel(**data)
                session.add(record)
                self.logger.info(F"Data inserted: {data}")
            else:
                self.logger.info(F"Duplicate data found: {data}")

        session.commit()
        session.close()'''


    def insert_data(self, table_name, data_list):
        if not data_list:
            print("Data list is empty. No insertion will be made.")
            return

        DynamicModel = self.create_dynamic_model(table_name, data_list[0])
        session = self.Session()

        # Subquery to get latest id for each link
        subq = session.query(
            func.max(DynamicModel.id).label("last_id")
        ).group_by(DynamicModel.link).subquery("subq")

        # Query to fetch last records by joining with subquery
        last_records_query = session.query(DynamicModel).join(
            subq, DynamicModel.id == subq.c.last_id
        )

        existing_records = {record.link: record for record in last_records_query}

        for data in data_list:
            link = data['link']
            if link in existing_records:
                current_record = existing_records[link]
                # Compare relevant fields
                if not all([
                    current_record.ground_targets_destroyed == data['ground_targets_destroyed'],
                    current_record.flight_time == data['flight_time'],
                    current_record.air_targets_destroyed == data['air_targets_destroyed'],
                    current_record.deaths == data['deaths']
                ]):
                    record = DynamicModel(**data)
                    session.add(record)
                    print(f"Data inserted: {data}")
                    self.logger.info(f"Data inserted: {data}")
                else:
                    print(f"Duplicate data found: {data}")
                    self.logger.info(f"Duplicate data found: {data}")
            else:
                record = DynamicModel(**data)
                session.add(record)
                print(f"Data inserted for new clan: {data}")
                self.logger.info(f"Data inserted for new clan: {data}")

        session.commit()
        session.close()

